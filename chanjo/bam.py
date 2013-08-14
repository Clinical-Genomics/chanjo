#!/usr/bin/env python
# coding: utf-8
"""
  bam.module
  ~~~~~~~~~~~~~

  A certified CoverageAdaptor should:

    * include a `.read(chrom, start, end)` method that returns BEDGraph
      formatted coverage intervals between `start` and `end`.

    * include a `.readIntervals(chrom, intervals)` method that returns
      BEDGraph formatted coverage intervals in chunks corresponding to the
      overlapping intervals.

    * expect all intervals definitions to be 0,1-based in accordance with
      Python `range()`.

    * take a file path or similar as a required parameter in the initialization
      of each class instance, i.e. `CoverageAdaptor(path)`.

    * [UNDER REVIEW] include `maxDepth` option in `.read()`/`.readIntervals()`.
      Should flatten BEDGraph intervals at `maxDepth`

    * exclude regions without aligned reads to be left out completely from the
      returned list of BEDGraph intervals.

  :copyright: 2013 by Robin Andeer, see AUTHORS for more details
  :license: license_name, see LICENSE for more details
"""

import pysam
from bx.intervals.intersection import IntervalTree


class CoverageAdaptor(pysam.Samfile):
  """
  Chanjo adaptor for fetching BEDGraph intervals directly from BAM alignment
  files.
  ----------

  :param bamPath: [str] Path to the BAM alignment file. This is required at
                        setup.

  Usage:
    from chanjo.bam import CoverageAdaptor
    path = "/path/to/bam/file.bam"
    adaptor = CoverageAdaptor(path)
  """

  def __init__(self, bamPath):
    super(CoverageAdaptor, self).__init__(bamPath, "rb")

  def read(self, chrom, start, end):
    """
    Public: Generates BEDGraph intervals of equal coverage between start and end
    on the given chromosome. Expect regions without aligned reads to be left out
    completely from the returned list of BEDGraph intervals.
    ----------

    :param chrom:     [str]  The chromosome of interest
    :param start:     [int]  The first position of the interval
    :param end:       [int]  The last position of the interval
    :returns:         [list] A list of `Interval` objects representing BEDGraph
                             intervals

    Usage:
      adaptor.read("17", 100023, 102051)
      [out] => [<chanjo.bam.Interval instance at 0x10f2ea518>,
                <chanjo.bam.Interval instance at 0x10f2ea4d0>]
    """
    # Set temporary chromosome for current interval
    self.chrom = chrom

    # Preallocate an list with enough space (worst case scenario; read depth
    # changes for every base)
    self.bgIntervals = [None]*(end-start)
    # Pointer for the above list
    self.count = 0

    # Init
    lastStart = 0
    lastDepth = 0

    # Start Pileup iterator and walk through each position in the interval
    # `truncate` will make sure it start and ends on the given positions!
    for col in self.pileup(str(chrom), start, end, truncate=True):

      # Tests whether coverage has changed
      if col.n != lastDepth:

        # Stuff the latest interval into the array
        self._persist(lastStart, col.pos, lastDepth)

        # Start new interval
        lastDepth = col.n
        lastStart = col.pos

    try:
      # Stuff the last interval into the array. To get 0,1-based coordinates we
      # have to add 1 to the position of this the last BEDGraph interval.
      self._persist(lastStart, col.pos + 1, lastDepth)
    except UnboundLocalError:
      # This means pileup didn't find any reads across the intervals
      return []

    # Return the subset of the list actually containing calculated intervals
    return self.bgIntervals[:self.count]

  def readIntervals(self, chrom, intervals):
    """
    Public: Generates BEDGraph intervals of equal coverage for each interval on
    the given chromosome. Intervals can be overlapping.
    ----------

    :param chrom:     [str]    The chromosome of interest
    :param intervals: [list]   List of `Interval` instances
    :returns:         [object] A generator object yielding BEDGraph `Interval`
                               objects for each input interval

    Usage:
      adaptor.read("17", 100023, 102051)
      [out] => [<chanjo.bam.Interval instance at 0x10f2ea518>,
                <chanjo.bam.Interval instance at 0x10f2ea4d0>]
    """
    # First figure out the outer bounderies of the intervals
    try:
      start = intervals[0].start
      end = intervals[-1].end
    except IndexError:
      # If the user submitted an empty list...
      return []

    # Initialize interval tree
    bgTree = IntervalTree()
    for interval in self.read(chrom, start, end):
      bgTree.insert_interval(interval)

    # Return generator object for each interval in order
    return (self._cutIntervals(bgTree.find(interval.start, interval.end),
                               interval) for interval in intervals)

  def _cutIntervals(self, bgIntervals, interval):
    """
    Private: Trims the first and last BEDGraph interval in a list to match a
    query interval to an `IntervalTree`.
    ----------

    :param bgIntervals: [int]  BEDGraph intervals for the interval
    :param interval:    [int]  The input interval for the BEDGraph intervals
    :returns:           [list] The modified list of BEDGraph intervals
    """
    try:
      # If first BEDGraph interval begins before the input interval, trim!
      if bgIntervals[0].start < interval.start:
        bgIntervals[0].start = interval.start

      # If last BEDGraph interval ends after the input interval, trim!
      if bgIntervals[-1].end > interval.end:
        bgIntervals[-1].end = interval.end

    except IndexError:
      return []

    return bgIntervals

  def _persist(self, lastStart, currentPos, lastDepth):
    """
    Private: Stores a BEDGraph interval of equal coverage in `bgIntervals`.
    ----------

    :param lastStart:   [int] The start position of the interval
    :param currentPos:  [int] The end position of the interval
    :param lastDepth:   [int] The read depth for the interval
    """

    if lastDepth > 0:

      self.bgIntervals[self.count] = Interval(lastStart, currentPos, lastDepth)

      # Move the save pointer one step forward
      self.count += 1

class Interval(object):
  """
  Interval
  Input start is 0-based and input end is 1-based like range().
  """
  def __init__(self, start, end, value=None, chrom=None):
    super(Interval, self).__init__()
    self.start = start
    self.end = end
    self.value = value
    self.chrom = chrom

  def __len__(self):
    # We are counting the number of positions in the interval
    return self.end - self.start

  def __str__(self):
    # This is the BED standard definition of an interval
    return "({start}, {end}]".format(start=self.start, end=self.end)

  def __eq__(self, other):
    # This compares Interval instances by matches values
    return (self.start == other.start and self.end == other.end and
            self.value == other.value and self.chrom == other.chrom)
