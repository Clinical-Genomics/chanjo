# -*- coding: utf-8 -*-
"""
Sorting the CCDS dump is required! And simple::

  $ sort CCDS.txt > CCDS.sorted.txt
"""
from collections import OrderedDict

from ...producers import more
from ...pyxshell.common import grep, cut, append
from ...pyxshell.pipeline import pipe


def parse_raw_intervals(str_list):
  """Takes the formatted string of interval coordinates from the CCDS
  row and turns it into a more managable list of lists with (start, end)
  coordinates for each interval.

  Args:
    str_list (str): A csv string of (start,end) pairs, wrapped in '[]'

  Returns:
    list: 2D list with the start ``int``, end ``int`` pairs
  """
  # Remove the "[]"
  csv_intervals = str_list[1:-1].replace(' ', '')

  # 1. Split first into exons coordinates
  # 2. Split into start, end and parse int
  intervals = [[int(pos) for pos in item.split('-')]
               for item in csv_intervals.split(',')]

  return intervals


@pipe
def extract_intervals(stdin):
  """Filter. Compiles interval tuples from a single (split) CCDS record
  row.
  """
  for record in stdin:
    # Extract contig Id as string
    contig_id = record[0]

    # Parse the intervals list-string and yield each of the intervals
    for raw_interval in parse_raw_intervals(record[9]):
      yield [
        contig_id,        # contig
        raw_interval[0],  # start
        raw_interval[1],  # end
        '{}-{}-{}'.format(contig_id, *raw_interval),
        record[6],        # strand
        record[4],        # block Ids
        record[2]         # superblock Ids
      ]


@pipe
def rename_sex_blocks(stdin):
  for interval in stdin:
    contig_id = interval[0]
    # 20 supersets are present on both X/Y
    if contig_id in ('X', 'Y'):
      # Rename block Id
      interval[5] = '{}-{}'.format(contig_id, interval[5])
      interval[6] = '{}-{}'.format(contig_id, interval[6])

    yield interval


@pipe
def aggregate_intervals(stdin):
  # Store added intervals
  intervals = OrderedDict()
  # To optimize loading
  last_contig = None

  for interval in stdin:
    if last_contig != interval[0]:
      # Yield a batch (chromosome) of intervals
      for complete_interval in intervals.values():
        yield complete_interval

      # Reset
      intervals = OrderedDict()
      last_contig = interval[0]

    old_interval = intervals.get(interval[3], None)
    if old_interval:
      # Add new block and possibly new superblock Ids
      old_interval[5].append(interval[5])
      old_interval[6].append(interval[6])
    else:
      # Transform block/superblock Ids to lists
      interval[5] = [interval[5]]
      interval[6] = [interval[6]]
      intervals[interval[3]] = interval

  # Yield the last batch of intervals
  for complete_interval in intervals.values():
    yield complete_interval


@pipe
def serialize_interval(stdin, delimiter='\t', subdelimiter=','):
  for interval in stdin:
    # Serialize the list of block/superblock Ids
    interval[5] = subdelimiter.join(interval[5])
    interval[6] = subdelimiter.join(interval[6])

    yield delimiter.join(map(str, interval))


def pipeline(ccds_stream, end_point):
  """

  Args:
    end_point: Where to store output e.g. ``sys.stdout``, useful for
      testing
  """
  # Convert CCDS to BED
  more(ccds_stream) \
    | grep('Public') \
    | cut(delimiter='\t') \
    | extract_intervals() \
    | rename_sex_blocks() \
    | aggregate_intervals() \
    | serialize_interval() \
    | append('\n') \
    > end_point
