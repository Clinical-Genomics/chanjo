#!/usr/bin/env python
# coding: utf-8
from __future__ import division


def coverageMetrics(depths, cutoff):
  """
  Calculates both coverage and completeness for an array of read depths for a
  continous genomic interval such as an exon.

  The array can be a simple list but a Numpy array is recommended for speed
  optimization.

  :param list depths: List/array of the read depth for each position/base
  :param int cutoff: The cutoff for lowest passable read depth (completeness)
  :returns: ``(<coverage (float)>, <completeness (float)>)``
  :rtype: tuple
  """
  # Initialize
  totBaseCount = float(len(depths))
  readCount = 0
  passedCount = 0

  for depth in depths:
    # Add the number of overlapping reads
    readCount += depth

    # Add the position if it passes `cutoff`
    if depth >= cutoff:
      passedCount += 1

  # totBaseCount should never be able to be 0! Exons be >= 1 bp long
  return readCount / totBaseCount, passedCount / totBaseCount


def intervals(grouped_intervals, depths, cutoff=10):
  """
  Calculates coverage metrics for a grouped set of intervals. Intervals are
  expected to be from the same chromosome and sorted by start position.

  It works by fetching read depth data for the combined total interval, and
  calculates metrics for *each* of the individual intervals.

  :param list grouped_intervals: Sorted intervals to calculate metrics for
  :param list depths: Read depth data for each position
  :param int cutoff: Threshold to use for completeness [default: 10]
  :returns: Coverage and completeness per grouped interval
  :rtype: list
  """
  # Get start of the boundery from the total combined interval
  start = grouped_intervals[0][0]

  # Preallocate list for each exon of the element
  values = [None] * len(grouped_intervals)

  # Get the exons related to the element
  for i, interval in enumerate(grouped_intervals):
    iStart = interval[0]
    iEnd = interval[1]
    interval_id = interval[2]

    # Relative start and end positions to slice the ``depths`` array
    rStart = iStart - start
    rEnd = iEnd - start

    # Do the heavy lifting
    # +1 to end because ``end`` is 0-based and slicing is 0,1-based
    values[i] = coverageMetrics(depths[rStart:rEnd+1], cutoff) + (interval_id,)

  return values
