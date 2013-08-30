#!/usr/bin/env python
# coding: utf-8
"""
  chanjo.core
  ~~~~~~~~~~~~~

  This module implements the glue and controlling hub. The :class:`Hub` is
  also where the adapters are plugged in to. This will likely be pretty much
  the only part of the package you directly interact with.

  :copyright: (c) 2013 by Robin Andeer
  :license: MIT, see LICENSE for more details
"""

import zlib


class Hub(object):
  """
  The :class:`Hub` is the core component of Chanjo. When you plug in the
  adapters, it will create handy shortcuts to easily reach common methods.

  The :class:`Hub` is able to prepare data and annotate elements, calculate
  coverage for a range of genomic positions, and interact with the
  element data store.

  Usage::

    from chanjo.core import Hub
    from chanjo.bam import CoverageAdapter
    from chanjo.sqlite import ElementAdapter

    hub = Hub()
    bam_path = "/path/to/file.bam"
    cov_path = "/path/to/sqlite.db"
    hub.connect(CoverageAdapter(bam_path), ElementAdapter(cov_path))

  :param coverageAdapter: (optional) Plug in the adapter during init
  :param elementAdapter: (optional) Plug in the adapter during init

  """
  def __init__(self, coverageAdapter=None, elementAdapter=None):
    super(Hub, self).__init__()

    # Set up the adapters
    if coverageAdapter and elementAdapter:
      self.connect(coverageAdapter, elementAdapter)

  def connect(self, coverageAdapter, elementAdapter):
    """
    Public: Plugs in the required adapters and sets up a few shortcuts.

    Usage::

      from chanjo.core import Hub
      from chanjo.bam import CoverageAdapter
      from chanjo.sqlite import ElementAdapter

      hub = Hub()
      bam_path = "/path/to/file.bam"
      cov_path = "/path/to/sqlite.db"
      hub.connect(CoverageAdapter(bam_path), ElementAdapter(cov_path))

    :param coverageAdapter: An instance of a :class:`CoverageAdapter`
    :param elementAdapter:  An instance of a :class:`ElementAdapter`
    """
    # Customizable adapters
    self.cov = coverageAdapter
    self.db = elementAdapter

  def annotate(self, element, cutoff=10):
    """
    Public: Annotates each related exon with coverage data.

    Useage::

      genes = hub.db.get("gene", ["GIT1", "EGFR", "BRCA1"])
      for gene in genes:
        hub.annotate(gene, 15)

    :param element: One element object (gene/transcript)
    :param cutoff: (optional) The min read depth to use for completeness
                   (Default: 10)
    """
    # Both transcripts and genes can be used to select exons to annotate
    depth = self.cov.read(element.chrom, element.start, element.end)

    # Get the exons related to the element
    for exon in element.exons:
      # Relative start and end positions to slice the ``depth`` array
      start = exon.start - element.start
      end = exon.end - element.start

      # Do the heavy lifting
      # +1 to end because ``end`` is 0-based and slicing is 0,1-based
      (coverage, completeness,
       levels) = self.calculate(depth[start:end+1], cutoff)

      exon.coverage = coverage
      exon.completeness = completeness
      exon.cutoff = cutoff
      exon.levels = levels

  def calculate(self, depths, cutoff):
    """
    Public: Calculates both coverage and completeness for a interval.

    Usage::

      gene = hub.db.get("gene", "C3")
      hub.coverage(gene.chrom, gene.intervals, 15)
      #=> (13.43522398231, 0.434122133123, None)

    :param depths: List/array of the read depth for each position/base
    :param cutoff: The cutoff for lowest passable read depth (completeness)
    :returns: Coverage (float), completeness (float), compressed levels (str)
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

    # Stringify and compress the levels to enable storage in SQL database
    str_levels = self.stringify(depths)

    # totBaseCount should never be able to be 0! Exons be >= 1 bp long
    return readCount / totBaseCount, passedCount / totBaseCount, str_levels

  def stringify(self, depths):
    """
    Public: Compresses the string of read depths.

    Because of how compression works I believe this will be sort of the same
    as generating BEDGraph intervals to compress the information.

    :param depths: Array of read depth (float or int)
    :returns: Compressed string of read depths
    """
    # Turn floats to ints, then to strings, then concat with "|"-separator
    str_depths = "|".join(map(str, map(int, depths)))

    # Compress and return compressed string
    return zlib.compress(str_depths)
