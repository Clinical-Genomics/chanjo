#!/usr/bin/env python
# coding: utf-8
"""
  bam.module
  ~~~~~~~~~~~~~

  A certified **Coverage Adapter** should:

    * include a `.read(chrom, start, end)` method that returns BEDGraph
      formatted coverage intervals between `start` and `end`.

    * include a `.readIntervals(chrom, intervals)` method that returns
      BEDGraph formatted coverage intervals in chunks corresponding to the
      overlapping intervals.

    * expect all intervals definitions to be 0,1-based in accordance with
      Python `range()`.

    * take a file path or similar as a required parameter in the initialization
      of each class instance, i.e. `CoverageAdapter(path)`.

    * [UNDER REVIEW] include `maxDepth` option in `.read()`/`.readIntervals()`.
      Should flatten BEDGraph intervals at `maxDepth`

    * exclude regions without aligned reads to be left out completely from the
      returned list of BEDGraph intervals.

  :copyright: 2013 by Robin Andeer, see AUTHORS for more details
  :license: license_name, see LICENSE for more details
"""

import pysam
from utils import Interval, CoverageTree


class CoverageAdapter(pysam.Samfile):
  """
  Chanjo adapter for fetching BEDGraph intervals directly from BAM alignment
  files.
  ----------

  :param bamPath: [str] Path to the BAM alignment file. This is required at
                        setup.

  Usage:
    from chanjo.bam import CoverageAdapter
    path = "/path/to/bam/file.bam"
    adapter = CoverageAdapter(path)
  """

  def __init__(self, bamPath):
    super(CoverageAdapter, self).__init__(bamPath, "rb")

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
      adapter.read("17", 100023, 102051)
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
      adapter.read("17", 100023, 102051)
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
    bgTree = CoverageTree()
    for interval in self.read(chrom, start, end):
      bgTree.insert_interval(interval)

    # Return generator object fintervalor each interval in order
    return (bgTree.get(interval.start, interval.end) for interval in intervals)

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
