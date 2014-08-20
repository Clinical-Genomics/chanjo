# -*- coding: utf-8 -*-
import json
import warnings

from sqlalchemy import exc as sa_exc
from toolz import pipe
from toolz.curried import map

from .._compat import text_type
from ..utils import split
from .consumers import build_interval_data
from .utils import convert_old_interval_id


def import_bed_stream(chanjo_db, bed_stream):
  """Import the "annotate" output into an existing Chanjo database.

  Args:
    chanjo_db (Store): ``chanjo.store.Store`` instance
    bed_stream (handle): BED-file handle
  """
  # step 1: load header information as JSON (removing the "#" character)
  metadata = json.loads(next(bed_stream)[1:])

  # extract info used later on
  sample_id = metadata['sample_id']
  group_id = metadata['group_id']

  # add a new Sample record using the metadata (don't commit yet)
  chanjo_db.add(chanjo_db.create('sample', **metadata))

  # suppress Decimal/float conversion warnings
  # ref: http://stackoverflow.com/questions/5225780
  with warnings.catch_warnings():
    warnings.simplefilter('ignore', category=sa_exc.SAWarning)
    # step 2: prepare the rest of the input data for consumption
    sequence = pipe(
      bed_stream,
      map(text_type.rstrip),
      map(split(sep='\t'))
    )

    # step 3: consume the interval data from the sequence
    for interval_data in sequence:
      build_interval_data(chanjo_db, sample_id, group_id, interval_data)

    # step 4: commit updates after loading all intervals
    chanjo_db.save()

    # step 5: extend annotations to blocks and superblocks
    return extend_annotations(chanjo_db, sample_id, group_id)


def extend_annotations(chanjo_db, sample_id, group_id):
  """Extend interval annotations to blocks and superblocks.

  Calculates the mean of metrics of related elements.

  Args:
    chanjo_db (Store): instance of class:`chanjo.store.Store`
    sample_id (str): id of sample to extend
    group_id (str): group id of sample to extend

  Returns:
    bool: ``True`` if successful, ``False`` otherwise.
  """
  # extend interval annotations to blocks
  # we commit so the SQL query in the next step works
  chanjo_db.add([chanjo_db.create(
    'block_data',
    parent_id=raw_block[0],
    sample_id=sample_id,
    group_id=group_id,
    coverage=raw_block[1],
    completeness=raw_block[2]
  ) for raw_block in chanjo_db.block_stats(sample_id)]).save()

  # extend annotations to genes
  chanjo_db.add([chanjo_db.create(
    'superblock_data',
    parent_id=raw_superblock[0],
    sample_id=sample_id,
    group_id=group_id,
    coverage=raw_superblock[1],
    completeness=raw_superblock[2]
  ) for raw_superblock in chanjo_db.superblock_stats(sample_id)]).save()


def import_json(chanjo_db, json_stream):
  """Legacy importer for the old JSON output format of the 'annotate' command.
  Deprecated.
  """
  dump = json.load(json_stream)

  annotations = dump['annotations']
  sample_id = dump['sample_id']
  group_id = dump['group_id']

  if dump['splice']:
    extension = 2
  else:
    extension = 0

  # add a Sample entry with metadata
  sample = chanjo_db.create(
    'sample',
    sample_id=sample_id,
    group_id=str(group_id),
    cutoff=dump['cutoff'],
    extension=extension,
    coverage_source=dump['source'],
    element_source=None
  )

  chanjo_db.add(sample)

  # for each of the annotations (intervals)
  chanjo_db.add([chanjo_db.create(
    'interval_data',
    parent_id=convert_old_interval_id(annotation[2]),
    coverage=annotation[0],
    completeness=annotation[1],
    group_id=group_id,
    sample_id=sample_id
  ) for annotation in annotations])

  # commit intervals before proceeding
  # we do this in part to leverage subsequent SQL queries
  chanjo_db.save()

  # extend annotations to blocks and superblocks
  return extend_annotations(chanjo_db, sample_id, group_id)
