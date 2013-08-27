#!/usr/bin/env python
# coding: utf-8
"""
  chanjo.utils
  ~~~~~~~~~~~~~

  A number of utilities used elsewhere in Chanjo.

  :copyright: (c) 2013 by Robin Andeer
  :license: MIT, see LICENSE for more details
"""
from bx.intervals.intersection import IntervalTree


class Interval(object):
  """
  (Genomic) Interval object. Note that both start and end is 0-based.
  """
  def __init__(self, start, end=None, value=None, chrom=None):
    super(Interval, self).__init__()
    self.start = start
    # A single position interval can be set up by omitting end argument
    self.end = end or start
    self.value = value
    self.chrom = chrom

  def __len__(self):
    # We are counting the number of positions in the interval
    return (self.end - self.start) + 1

  def __str__(self):
    # This is the BED standard definition of an interval
    return "({start}, {end})".format(start=self.start, end=self.end)

  def __eq__(self, other):
    # This compares Interval instances by matches values
    return (self.start == other.start and self.end == other.end and
            self.value == other.value and self.chrom == other.chrom)


class CoverageTree(IntervalTree):
  """
  Superset of IntervalTree implementation (bx-python) that wraps the default
  `find` method so as to only return intervals trimmed to the original input
  start + end arguments.
  ----------
  """
  def __init__(self):
    super(CoverageTree, self).__init__()
    
  def get(self, start, end):
    """
    Public: Return trimmed intervals overlapping the given input range. Wraps
    the default find method that otherwise returns intervals that can extend
    beyond (start, end).
    ----------

    :param start: [int]  The start of the input range
    :param end:   [int]  The end of the input range
    :returns:     [list] List of `Interval` objects between `start`-`end`.
    """
    # Use default `find` method to return all intervals overlapping the given
    # range (start, end)
    intervals = self.find(start, end)

    try:
      # Check if first interval begins before the input (start), trim!
      if intervals[0].start < start:
        intervals[0].start = start

      # Check if last BEDGraph interval ends after the input interval, trim!
      if intervals[-1].end > end:
        intervals[-1].end = end

    except IndexError:
      # Apparently we didn't find any intervals matching the given range
      return []

    return intervals
