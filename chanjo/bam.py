#!/usr/bin/env python
# coding: utf-8
"""
  chanjo.bam
  ~~~~~~~~~~~~~

  The default :class:`CoverageAdapter` that ships with Chanjo. Talks directly
  to a BAM alignment file to extract read depth data.

  :copyright: (c) 2013 by Robin Andeer
  :license: MIT, see LICENSE for more details
"""

import pysam
import numpy as np


class CoverageAdapter(pysam.Samfile):
  """
  Adapter for interfacing directly with BAM alignment files.

  Usage::
    from chanjo.bam import CoverageAdapter
    path = "/path/to/bam/file.bam"
    adapter = CoverageAdapter(path)

  :param bamPath: Path to the BAM alignment file
  """

  def __init__(self, bamPath):
    super(CoverageAdapter, self).__init__(bamPath, "rb")

  def read(self, chrom, start, end):
    """
    Public: Generates a list of read depths, for each position, between start,
    end.

    .. note::
      Positions are 0,0-based throughout Chanjo. If start=0, end=9 you should
      expect the 10 read depths for position 1-10 to be returned.

    Usage:
      adapter.read("17", 0, 5)
      #=> array([3., 3., 4., 4., 5., 4.])

    :param chrom: The chromosome ID (str) of interest
    :param start: The first position of the interval (0-based)
    :param end: The last position of the interval (0-based)
    :returns: A numpy array of read depths for *each* position in the interval
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
