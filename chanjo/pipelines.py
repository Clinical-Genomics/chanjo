# -*- coding: utf-8 -*-
"""
chanjo.pipelines
~~~~~~~~~~~~~~~~~
The collections of central pipelines in Chanjo. Commonly invoked from
the 'chanjo' command line utility.
"""
import errno
import json
import warnings

from path import path
from sqlalchemy import exc as sa_exc

from .pyxshell import common
from .utils import convert_old_interval_id
from . import stages, producers
from .sql.models import Interval
from .sql.core import ChanjoDB
from .bam import BamFile


def annotate(bed_stream, sample_id, group_id, cutoff, bam_path, extension,
             prepend, bp_threshold, end_point):
  """Pipeline for annotating all intervals from a BED file stream.
  Writes both metadata (header) and tabular data for each interval with
  calculated coverage and completeness to the end point.

  Args:
    bed_stream (file): BED-file handle to read from
    sample_id (str): Unique Id for a given sample
    group_id (str): Id for a given group of samples (e.g. family/trio)
    cutoff (int): Threshold to use for completeness calculation
    bam_path (str): Path to BAM-file
    extension (int): Number of bases to extend each interval with (+/-)
    prepend (str): Renames each contig by prepending this string
    bp_threshold (int): Optimization threshold for reading BAM-file
      in chunks
    end_point (file or list): Write/append enabled object
  """
  # SETUP: Connect to CoverageAdapter
  bam = BamFile(bam_path)

  # STEP 1: Write metadata header
  # Write metadata to output header
  header = {
    'sample_id': sample_id,
    'group_id': group_id,
    'cutoff': cutoff,
    'coverage_source': path(bam_path).abspath(),
    'extension': extension
  }
  line = '#{}\n'.format(json.dumps(header))

  common.echo(line) > end_point

  # STEP 2: The Pipeline
  producers.more(bed_stream) \
    | stages.rstrip() \
    | common.cut(delimiter='\t') \
    | stages.prepare_bed_interval() \
    | stages.extend_interval(extension) \
    | stages.group_intervals(bp_threshold) \
    | stages.process_interval_group(bam) \
    | stages.calculate_metrics(cutoff) \
    | stages.stringify() \
    | common.append('\n') \
    > end_point


def build(bed_stream, sql_uri, sql_dialect, overwrite, end_point):
  # Connect to the database
  db = ChanjoDB(sql_uri, sql_dialect)

  # Check if the database already exists (simply expect 'mysql' to exist)
  # 'dialect' is in the form of '<db_type>+<connector>'
  if sql_dialect.startswith('mysql') or path(sql_uri).exists():
    if overwrite:
      # Wipe the database clean with a warning
      db.tare_down()
    elif sql_dialect == 'sqlite':
      # Prevent from wiping existing database to easily
      raise OSError(errno.EEXIST, sql_uri)

  # Set up new tables
  db.setup()

  producers.more(bed_stream) \
    | stages.rstrip() \
    | common.cut(delimiter='\t') \
    | stages.prepare_bed_interval() \
    | stages.build_interval(db) \
    | stages.aggregate() \
    | stages.build_block(db) \
    | stages.aggregate() \
    | stages.build_superblock(db) \
    | stages.commit_per_contig(db) \
    > end_point


def extend_annotations(db, sample_id, group_id):
  """Extend interval annotations to blocks and superblocks by
  calculating the mean of related elements.

  Args:
    db (ChanjoDB): Instance of class:`chanjo.sql.core.ChanjoDB`
    sample_id (str): Id of sample to extend
    group_id (str): Group Id of sample to extend

  Returns:
    bool: ``True`` if successful, ``False`` otherwise.
  """
  # Extend interval annotations to blocks
  # We commit so the SQL query in the next step works
  db.add([db.create(
    'block_data',
    parent_id=raw_block[0],
    sample_id=sample_id,
    group_id=group_id,
    coverage=raw_block[1],
    completeness=raw_block[2]
  ) for raw_block in db.block_stats(sample_id)]).commit()

  # Extend annotations to genes
  db.add([db.create(
    'superblock_data',
    parent_id=raw_superblock[0],
    sample_id=sample_id,
    group_id=group_id,
    coverage=raw_superblock[1],
    completeness=raw_superblock[2]
  ) for raw_superblock in db.superblock_stats(sample_id)]).commit()


def export(sql_uri, sql_dialect, end_point):
  # Connect to the database
  db = ChanjoDB(sql_uri, sql_dialect)

  # Fetch interval tuples from the database (producer)
  i = Interval  # alias
  columns = (i.contig_id, i.start, i.end, i.id, i.strand)

  producers.fetch_records(db, columns) \
    | stages.stringify() \
    | common.append('\n') \
    > end_point


def import_data(bed_stream, sql_uri, sql_dialect):
  """Import output from 'annotate' sub-command.

  Args:
    bed_stream (file): File handle (file or stdin)
    sql_uri (str): Path to the database or MySQL connection string
    sql_dialect (str): SQL database type (sqlite or mysql+<connector>)

  Returns:
    bool: True if successful
  """
  # Connect to the database
  db = ChanjoDB(sql_uri, sql_dialect)

  # Step 1:
  # Load the header information as JSON (removing the '#' character)
  metadata = json.loads(bed_stream.readline()[1:])

  # Extract info used later on
  sample_id = metadata['sample_id']
  group_id = metadata['group_id']

  # Add a Sample entry with metadata
  db.add(db.create('sample', **metadata))

  # Suppress silly Decimal/float conversion warnings
  # Ref: http://stackoverflow.com/questions/5225780
  with warnings.catch_warnings():
    warnings.simplefilter('ignore', category=sa_exc.SAWarning)
    # Step 2:
    # Run the rest of the pipeline
    _ = []
    producers.more(bed_stream) \
      | stages.rstrip() \
      | common.cut(delimiter='\t') \
      | stages.build_interval_data(db, sample_id, group_id) \
      > _

    # Commit updates after loading all intervals
    db.commit()

    # Extend annotations to blocks and superblocks
    extend_annotations(db, sample_id, group_id)


def import_json(input_stream, sql_uri, sql_dialect):
  """Legacy importer for the old JSON output format of the 'annotate' command.
  Deprecated.
  """
  db = ChanjoDB(sql_uri, dialect=sql_dialect)

  dump = json.load(input_stream)

  annotations = dump['annotations']
  sample_id = dump['sample_id']
  group_id = dump['group_id']

  if dump['splice']:
    extension = 2
  else:
    extension = 0

  # Add a Sample entry with metadata
  sample = db.create(
    'sample',
    sample_id=sample_id,
    group_id=str(group_id),
    cutoff=dump['cutoff'],
    extension=extension,
    coverage_source=dump['source'],
    element_source=None
  )

  db.add(sample).commit()

  # For each of the annotations (intervals)
  db.add([db.create(
    'interval_data',
    parent_id=convert_old_interval_id(annotation[2]),
    coverage=annotation[0],
    completeness=annotation[1],
    group_id=group_id,
    sample_id=sample_id
  ) for annotation in annotations])

  # Commit intervals before proceeding
  # We do this in part to leverage subsequent SQL queries.
  db.commit()

  # Extend annotations to blocks and superblocks
  extend_annotations(db, sample_id, group_id)
