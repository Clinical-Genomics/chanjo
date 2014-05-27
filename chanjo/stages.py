# -*- coding: utf-8 -*-
"""
chanjo.stages
~~~~~~~~~~~~~~
Itermediary pipes in some pipelines, also known as 'filters'. Mostly
highlty customized subsections for various Chanjo pipelines.
"""
from .pyxshell.pipeline import pipe
from .utils import completeness, merge_intervals, assign_relative_positions


@pipe
def stringify(stdin, delimiter='\t'):
  """Converts each sequence (list, tuple) item in a in a stream to their
  "tabluar" string representation.

  Args:
    stdin (list): Stream of yielded sequences, e.g. lists
    delimiter (str, optional): Delimiter to use for separating "columns"

  Yields:
    str: Stringified item joined by the delimiter
  """
  for sequence in stdin:
    yield delimiter.join(map(str, sequence))


@pipe
def rstrip(stdin):
  """Strips invisible characters like ``\\t`` and ``\\n`` from the end
  of strings.

  Args:
    stdin (list): Stream of strings

  Yields:
    str: String without trailing special characters
  """
  for string in stdin:
    yield string.rstrip()


@pipe
def prepare_bed_interval(stdin, block_column=5):
  """Preprocess BED intervals. Converts positions to 1:1 based and
  splits optional block and superblock Ids into lists.

  Args:
    stdin (list): Stream of BED interval lists
    block_column (int, optional): Column with block Ids

  Yields:
    list: Converted interval list
  """
  for interval in stdin:
    # Convert start/end to integers and 1:1-based positions
    interval[1] = int(interval[1]) + 1
    interval[2] = int(interval[2])

    # Split block and superblock Ids
    # The columns are not always mandatory
    block_column = 5
    for i, column in enumerate(interval[block_column:]):
      interval[block_column + i] = interval[block_column + i].split(',')

    yield interval


@pipe
def build_interval(stdin, db):
  """Extract interval data for a single interval (exon) at a time.
  """
  for interval in stdin:
    # Create a brand new interval
    new_interval = db.create(
      'interval',
      interval_id=interval[3],
      contig_id=interval[0],
      start=interval[1],
      end=interval[2],
      strand=interval[4]
    )

    # Yield the new interval for each of the related blocks
    for block_id, superblock_id in zip(interval[5], interval[6]):
      yield block_id, new_interval, superblock_id


@pipe
def aggregate(stdin):
  # Store created groups
  groups = {}
  # To optimize loading
  last_contig = None

  for payload in stdin:
    element = payload[1]

    # Yield a batch (per chromosome)
    if last_contig != element.contig_id:
      for group in groups.values():
        yield group

      # Reset
      groups = {}
      last_contig = element.contig_id

    if payload[0] not in groups:
      groups[payload[0]] = [payload]

    else:
      groups[payload[0]].append(payload)

  # Yield also the groups for the last contig
  for group in groups.values():
    yield group


@pipe
def build_block(stdin, db):
  for intervals in stdin:
    block_id, some_interval, superblock_id = intervals[0]

    # Create a brand new block
    new_block = db.create(
      'block',
      block_id=block_id,
      contig_id=some_interval.contig_id,
      start=min(map(lambda x: x[1].start, intervals)),
      end=max(map(lambda x: x[1].end, intervals)),
      strand=some_interval.strand,
      superblock_id=superblock_id
    )

    # Relate the intervals to the block
    new_block.intervals = [interval for _, interval, _ in intervals]

    yield superblock_id, new_block


@pipe
def build_superblock(stdin, db):
  for blocks in stdin:
    superblock_id, some_block = blocks[0]

    # Create a brand new superblock
    new_superblock = db.create(
      'superblock',
      superblock_id=superblock_id,
      contig_id=some_block.contig_id,
      start=min(map(lambda x: x[1].start, blocks)),
      end=max(map(lambda x: x[1].end, blocks)),
      strand=some_block.strand
    )

    db.add(new_superblock)

    # Relate the blocks to the superblock
    new_superblock.blocks = [block for _, block in blocks]

    yield new_superblock


@pipe
def commit_per_contig(stdin, db):
  # To optimize loading
  last_contig = None

  for superblock in stdin:

    # Commit once for every finished contig
    if last_contig != superblock.contig_id:
      db.commit()
      # Update latest contig Id
      last_contig = superblock.contig_id

  # Commit also the last contig
  db.commit()

  yield 0


@pipe
def build_interval_data(stdin, db, sample_id, group_id):
  for interval_data in stdin:
    # Create a new intervals data entry
    db.add(db.create(
      'interval_data',
      parent_id=interval_data[0],
      sample_id=sample_id,
      group_id=group_id,
      coverage=float(interval_data[5]),
      completeness=float(interval_data[6])
    ))

  yield 0


@pipe
def extend_interval(stdin, extension):
  """Extends interval symetrically.
  """
  for interval in stdin:
    # Convert start/end to integers and 1:1-based positions
    interval[1] -= extension
    interval[2] += extension

    yield interval


@pipe
def group_intervals(stdin, threshold=1000):
  """Groups and returns a list of intervals based on the threshold.

  Args:
    intervals (list): List of intervals
    threshold (int, optional): Approx. combined length per group

  Yields:
    list of tuple: The next group of intervals
  """
  # This is where we store grouped intervals
  group = []
  group_start = None
  group_end = 0
  last_contig = None

  for interval in stdin:
    # Update the current combined interval
    # Use 'max' since some intervals overlap others (all we know is that
    # they are sorted on 'start' position)
    group_end = max(group_end, interval[2])

    # If the current combined interval is big enough or a new contig
    # has started
    new_contig = last_contig != interval[0]
    if new_contig or (group_end - group_start) > threshold:
      # Push currently grouped intervals
      if group:
        yield group

      # Start a new combined interval group
      group = [interval]

      # Reset the combined interval bounderies
      group_start, group_end = interval[1], interval[2]

    else:
      # Append to the current combined interval group
      group.append(interval)

  # Push the last group
  yield group


@pipe
def process_interval_group(stdin, bam):
  for interval_group in stdin:
    # Contig is expected to be the same for all intervals
    contig_id = interval_group[0][0]

    # Get the start and end of the group interval, 1:1-based
    overall_start, overall_end = merge_intervals(interval_group)

    # Get read depths for the whole (full) group interval
    # => input should be 1:1-based
    read_depths = bam(contig_id, overall_start, overall_end)

    for interval in interval_group:
      # Convert to relative positions for the interval
      # => 1:1-based, includes optional extension
      # => ouput can be considered as '0:0-based' (e.g. 1-1=0)
      args = (interval[1], interval[2], overall_start)
      rel_start, rel_end = assign_relative_positions(*args)

      # Slice the overall read depth array with the relative coordinates
      # Python expects 0:1-based when slicing => +1 to 'rel_end'
      read_depth_slice = read_depths[rel_start:rel_end + 1]

      yield interval, read_depth_slice


@pipe
def calculate_metrics(stdin, threshold):
  """Calculates mean coverage and completeness for a given read depths
  for a continous interval.

  Args:
    read_depths (array): :class:`numpy.array` of read depths for
      **each** of the positions
    threshold (int): Cutoff to use for the completeness filter

  Returns:
    tuple of float: Coverage and completeness for the interval
      represented by the read depth array.
  """
  for interval, read_depths in stdin:
    yield interval + [read_depths.mean(), completeness(read_depths, threshold)]


@pipe
def read_coverage(stdin, bam):
  for interval in stdin:
    # Get read depths for the whole (full) group interval
    # => input should be 1:1-based
    contig_id = interval[0]
    start = interval[1] + 1
    end = interval[2]

    yield bam(contig_id, start, end)


@pipe
def calculate_coverage(stdin):
  for read_depths in stdin:
    yield read_depths.mean()
