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
import numpy as np


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
    Public: Generates a list of read depths between start, end.

    Positions are 0,0-based throughout Chanjo. If start=0, end=9 you should
    expect the 10 read depths for position 1-10 to be returned.
    ----------

    :param chrom: [str]  The chromosome of interest
    :param start: [int]  The first position of the interval (0-based)
    :param end:   [int]  The last position of the interval (0-based)
    :returns:     [list] A list of read depths for each position in the interval

    Usage:
      adapter.read("17", 100023, 102051)
      [out] => [<chanjo.bam.Interval instance at 0x10f2ea518>,
                <chanjo.bam.Interval instance at 0x10f2ea4d0>]
    """
    # Generate a list of 0 read depth for each position
    positions = np.zeros(end+1-start)

    # Start Pileup iterator and walk through each position in the interval
    # `truncate` will make sure it starts and ends on the given positions!
    # +1 to end because pysam otherwise stops one base short by default
    for col in self.pileup(str(chrom), start, end+1, truncate=True):

      # Overwrite the read depth in the correct position
      # This will allow simple slicing to get at the positions of interest
      positions[col.pos - start] = col.n

    return positions
