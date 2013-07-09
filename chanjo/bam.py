#!/usr/bin/env python
# coding: utf-8
"""
  bam.module
  ~~~~~~~~~~~~~

  Responsible for returning BEDGraph intervals given start, end coordinates on
  a specified chromosome.

  :copyright: 2013 by Robin Andeer, see AUTHORS for more details
  :license: license_name, see LICENSE for more details
"""

import pysam


class CoverageAdaptor(pysam.Samfile):
  """
  Chanjo adaptor for fetching BEDGraph intervals directly from BAM alignment
  files.

  :param bam_path: [str] Path to the BAM alignment file. This is required at
                   setup.

  Usage:
    from chanjo.bam import CoverageAdaptor
    path = "/path/to/bam/file.bam"
    adaptor = CoverageAdaptor(path)
  """

  def __init__(self, bam_path):
    super(CoverageAdaptor, self).__init__(bam_path, "rb")

  def intervals(self, chrom, start, end, maxDepth=float("inf")):
    """
    Public: Generates BEDGraph intervals of equal coverage between start and end
    on the given chromosome.

    :param chrom:    [str] The chromosome of interest
    :param start:    [int] The first position of the interval
    :param end:      [int] The last position of the interval
    :param maxDepth: [int] The highest read depth to consider

    Usage:
      adaptor.intervals("17", 100023, 102051, 50)
      [out] => [<chanjo.bam.Interval instance at 0x10f2ea518>,
                <chanjo.bam.Interval instance at 0x10f2ea4d0>]
      """

    # Start positions are 0 based in the genomics world
    start -= 1

    # An empty string is evaluated larger than any integer
    iterator = self.pileup(str(chrom), start, end)

    lastDepth = None
    lastStart = None

    # Move the iterator until start of given interval
    for col in iterator:
      if col.pos < start:
        continue
      else:
        # Initialize using the first position in the interval
        lastDepth = col.n
        lastStart = col.pos

        break

    if not lastDepth:
      # Pilup came up empty for the interval
      return []

    # Preallocate an array and hope we have enough space
    self._intervals = [None]*50*(end - start)
    # Pointer for the array
    self.count = 0

    # Pick up the iterator and go through one position at a time
    for col in iterator:

      # Don't move beyond the given interval
      if col.pos >= end:
        break

      # Testing whether coverage has changed or
      # if both the beginning and the current position in the current interval
      # is above the specified max.
      if col.n != lastDepth and (col.n < maxDepth or lastDepth < maxDepth):

        # Stuff the latest interval into the array
        self._persistCoverage(chrom, lastStart, col.pos, lastDepth, maxDepth)

        # Start new interval
        lastDepth = col.n
        lastStart = col.pos

        # Move the save pointer one step forward
        self.count += 1

    # Stuff the last interval into the array
    self._persistCoverage(chrom, lastStart, col.pos, lastDepth, maxDepth)
    # `count` now is the number of intervals that was created
    self.count += 1

    # Return the subset of the list actually containing calculated intervals
    return self._intervals[:self.count]

  def _persistCoverage(self, chrom, lastStart, currentPos, lastDepth, maxDepth):
    """
    Private.
    """

    if lastDepth > 0:

      # Limit the max reported read depth
      if lastDepth > maxDepth:
        reportedDepth = maxDepth
      else:
        reportedDepth = lastDepth

      self._intervals[self.count] = Interval(lastStart, currentPos,
                                             reportedDepth)
    else:
      print("Positions with 0 reads: {}".format(currentPos))

class Interval(object):
  """docstring for Interval"""
  def __init__(self, start, end, value=None, chrom=None):
    super(Interval, self).__init__()
    self.start = start
    self.end = end
    self.value = value

  def __len__(self):
    return self.end - self.start
