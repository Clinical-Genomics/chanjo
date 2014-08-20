# -*- coding: utf-8 -*-
"""
chanjo.converter.stages
~~~~~~~~~~~~~~~~~~~~~~~~

Pipeline stages only used by the Chanjo converter.
"""
from __future__ import absolute_import
from operator import attrgetter

from toolz import curry, mapcat

from ..utils import BaseInterval


@curry
def grep(pattern, string):
  """Match a simple pattern substring in a given string.

  Note that the function would also work to check for an item in a list,
  a key in a dictionary etc.

  Args:
    pattern (str): substring to match with
    string (str): string to match against

  Returns:
    bool: if ``pattern`` was a substring in ``string``
  """
  return pattern in string


def parse_raw_intervals(str_list):
  """Decode serialized CCDS exons.

  Accepts a formatted string of interval coordinates from the CCDS
  row and turns it into a more manageable list of lists with
  (start, end) coordinates for each interval (exon).

  .. code-block:: python

    >>> parse_raw_intervals('[11-18, 25-30, 32-35]')
    [[11, 18], [25, 30], [32, 35]]

  Args:
    str_list (str): A CSV string of (start, end) pairs, wrapped in '[]'

  Returns:
    list: 2D list with the start ``int``, end ``int`` pairs
  """
  # remove the "[]"
  csv_intervals = str_list[1:-1].replace(' ', '')

  # 1. split first into exons coordinates
  # 2. split into start, end and parse int
  intervals = [[int(pos) for pos in item.split('-')]
               for item in csv_intervals.split(',')]

  return intervals


def extract_intervals(record):
  """Compile an BaseInterval from a single (split) CCDS record row.

  Args:
    record (tuple): split CCDS row

  Yields:
    BaseInterval: namedtuple class representation of an interval
  """
  # extract contig Id as string
  contig = record[0]

  # parse the intervals list-string and yield each of the intervals
  for start, end in parse_raw_intervals(record[9]):

    yield BaseInterval(
      contig,                             # contig
      start,                              # start
      end,                                # end
      "%s-%d-%d" % (contig, start, end),  # unique id
      0,                                  # score, unused but required
      record[6],                          # strand
      [record[4]],                        # block ids
      [record[2]]                         # superblock ids
    )


def rename_sex_interval(interval, sex_contigs=('X', 'Y')):
  """Rename interval ids for intervals on sex chromosomes.

  Doesn't do anything but return non-sex interval.

  The need for this step is that 20 superblocks are present on both sex
  chromosomes (X and Y). However, corresponding intervals should still
  be treated as if they wheren't really homologos.

  Args:
    interval (tuple): tuple representation of an interval

  Returns:
    BaseInterval: namedtuple representation of an interval
  """
  contig = interval.contig
  if contig in sex_contigs:
    # keep the funtion pure, avoid altering input object!
    return interval._replace(
      block_ids=["%s-%s" % (contig, block_id)
                 for block_id in interval.block_ids],
      superblock_ids=["%s-%s" % (contig, superblock_id)
                      for superblock_id in interval.superblock_ids]
    )

  else:
    return interval


def merge_related_elements(interval_group):
  """Merge block and superblock ids for a group of identical intervals.

  Args:
    interval_group (list): list of identical intervals

  Returns:
    BaseInterval: unified interval with merged related element ids
  """
  # extract block and superblock ids from each of the intervals
  block_ids = mapcat(attrgetter('block_ids'), interval_group)
  superblock_ids = mapcat(attrgetter('superblock_ids'), interval_group)

  return BaseInterval(
    *interval_group[0][:6],              # use first interval as base
    block_ids=list(block_ids),           # resolve and add
    superblock_ids=list(superblock_ids)  # do
  )
