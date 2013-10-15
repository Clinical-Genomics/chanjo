#!/usr/bin/env python
# coding: utf-8
"""
  chanjo.bam
  ~~~~~~~~~~~~~

  The default :class:`CoverageAdapter` that ships with Chanjo. Talks directly
  to a BAM alignment file to extract read depth data.

  Depends on the Pysam_ package and requires Samtools_ to be installed in your
  ``$PATH`` to work.

  :copyright: (c) 2013 by Robin Andeer
  :license: MIT, see LICENSE for more details

  .. _Pysam: http://www.cgat.org/~andreas/documentation/pysam/contents.html
  .. _Samtools: http://samtools.sourceforge.net/
"""
import pysam
import numpy as np


class CoverageAdapter(pysam.Samfile):
  """
  Adapter for interfacing directly with BAM alignment files. Inherits from
  :class:`Samfile` which requires a second init parameter that tells it to
  expect a *binary* BAM-file rather than the plain text cousin SAM-file format.

  .. code-block:: python

    >>> from chanjo.bam import CoverageAdapter
    >>> bam_path = "/path/to/bam/file.bam"
    >>> adapter = CoverageAdapter(bam_path)

  :param str bam_path: Path to a BAM alignment file
  """

  def __init__(self, bam_path):
    super(CoverageAdapter, self).__init__(bam_path, "rb")

  def read(self, chrom, start, end):
    """
    <public> Generates a list of read depths for each position between
    (start, end). The `numpy` array is used to optimize performance when
    building and slicing the list.

    This method depends on `Pysam` >=0.7.5 since using the `truncate` which
    wasn't working in previous versions.

    .. code-block:: python

      >>> adapter.read("17", 0, 5)
      array([3., 3., 4., 4., 5., 4.])

    .. note::

      Positions are 0,0-based throughout `Chanjo`. If start=0, end=9 you should
      expect the 10 read depths for position 1-10 to be returned.

    :param str chrom: The chromosome ID (str) of interest
    :param int start: The first position of the interval (0-based)
    :param int end: The last position of the interval (0-based)
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
