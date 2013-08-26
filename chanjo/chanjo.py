#!/usr/bin/env python
# coding: utf-8
"""
  chanjo.module
  ~~~~~~~~~~~~~

  The glue and control hub of the `chanjo` package.
  Borrows many structural ideas from Ember.js in the way you add in adapters to
  add in modular functionality that can be switched out to support multiple
  "backends".

  :copyright: 2013 by Robin Andeer, see AUTHORS for more details
  :license: MIT, see LICENSE for more details
"""

from __future__ import print_function
import zlib


class Core(object):
  """docstring for Core"""
  def __init__(self, coverageAdapter=None, elementAdapter=None):
    super(Core, self).__init__()

    self.get = None  # See your Element Adapter for documentation

    # Set up the adapters
    if coverageAdapter and elementAdapter:
      self.connect(coverageAdapter, elementAdapter)

  def connect(self, coverageAdapter, elementAdapter):
    """
    Public: Plugs in the required adapters and sets up a few shortcuts.
    ----------

    :param coverageAdapter: [object] A class instance of a Coverage Adapter
    :param elementAdapter:  [object] A class instance of a Element Adapter

    Usage:
      from chanjo.chanjo import Core
      from chanjo.bam import CoverageAdapter
      from chanjo.sqlite import ElementAdapter

      core = Core()
      bam_path = "/path/to/file.bam"
      cov_path = "/path/to/sqlite.db"
      core.connect(CoverageAdapter(bam_path), ElementAdapter(cov_path))
    """
    # Customizable adapters
    self.coverageAdapter = coverageAdapter
    self.elementAdapter = elementAdapter

    # Shortcut to getting elements by ID
    self.get = self.elementAdapter.get
    self.commit = self.elementAdapter.commit

    # Shortcut to getting coverage for intervals
    self.read = self.coverageAdapter.read

  def annotate(self, element, cutoff=50):
    """
    Public: Calculates coverage data for exons belonging to submitted elements.
    Saves to database.
    ----------

    :param element: [obj]  One element objects (genes/transcripts)
    :param cutoff:  [int]  The read depth level to use for coverage
                           completeness (Default: 50)
    :param levels:  [bool] Whether to return string representation of
                           coverage across the intervals (Default: False)

    Useage:
      genes = core.get("gene", ["GIT1", "EGFR", "BRCA1"])
      core.annotate(genes, 10, levels=True)
    """
    # Both transcripts and genes can be used to select exons to annotate
    depth = self.read(element.chrom, element.start, element.end)

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

  def calculate(self, depths, cutoff=50):
    """
    Public: Calculates both coverage and completeness for a given set of
    intervals. This is accompished using a single method since the bottleneck
    will be reading coverage from a file rather than calculating coverage.

    N.B. Doesn't handle overlapping intervals.
    ----------

    :param depths: [list]  List of `Interval` objects
    :param cutoff: [int]   The cutoff to calculate completeness
                           (Def: 50)
    :param levels: [bool]  Whether to return string representation of
                           coverage across the intervals (Def: False)
    :returns:      [tuple] Coverage (float), completeness (float),
                           BEDGraph intervals (str)

    Usage:
      gene = core.get("gene", "C3")
      core.coverage(gene.chrom, gene.intervals, 15)
      [out] => (13.43522398231, 0.434122133123, None)
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

    # totBaseCount should never be able to be 0! Exons be >= 1 bp
    return readCount / totBaseCount, passedCount / totBaseCount, str_levels

  def stringify(self, depths):
    """
    Public: Compress the string of depths. Because of how compression works I
    believe this will be sort of the same as generating BEDGraph intervals to
    compress the information.
    ----------

    :param depths: [list] Array of read depth floats
    :returns:      [str]  Compressed string of read depths
    """
    # Turn floats to ints, then to strings, then concat with "|"-separator
    str_depths = "|".join(map(str, map(int, depths)))

    # Compress and return compressed string
    return zlib.compress(str_depths)
