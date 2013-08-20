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
import interval as ival
from utils import CoverageTree


class Core(object):
  """docstring for Core"""
  def __init__(self, coverageAdapter=None, elementAdapter=None):
    super(Core, self).__init__()

    self.get = None  # 
    self.readIntervals = None  # 

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

    # Shortcut to getting coverage for intervals
    self.readIntervals = self.coverageAdapter.readIntervals
    self.read = self.coverageAdapter.read

  def annotate(self, elem, cutoff=50, levels=False):
    """
    Public: Calculate coverage for a single element.
    ----------
    :param elem_class: [str]    The type of element
    :param element:    [object] The element object to annotate
    :param cutoff:     [int]    The read depth level to use for coverage
                                completeness (Default: 50)

    Usage:
      gene = core.get("gene", "EGFR")
      core.annotate(gene, 15)
      [out] => <chanjo.sqlite2.Gene at 0x1041c4c10>
    """

    (cov, comp,
     str_levels) = self.calculate(elem.chrom, elem.intervals, cutoff, levels)

    # Update the element with the calculated coverage information
    elem.coverage = cov
    elem.completeness = comp
    elem.cutoff = cutoff
    elem.levels = str_levels

  def annotateExons(self, elements, cutoff=50, levels=False):
    """
    Public: Calculates coverage data for exons belonging to submitted elements.
    Saves to database.
    ----------

    :param elements: [list] List of element objects (genes/transcripts)
    :param cutoff:   [int]  The read depth level to use for coverage
                            completeness (Default: 50)
    :param levels:   [bool] Whether to return string representation of
                            coverage across the intervals (Default: False)

    Useage:
      genes = core.get("gene", ["GIT1", "EGFR", "BRCA1"])
      core.annotateExons(genes, 10, levels=True)
    """
    # Both transcripts and genes can be used to select exons to annotate
    for element in elements:
      # Get the exons related to the element
      exons = element.exons
      # Calculate coverage, completeness, and levels for all exon
      exonData = self._processExons(exons, self.readIntervals(element.chrom,
                                    element.intervals), cutoff, levels)

      # Iterate through each exon and accompanying coverage data
      for exon, data in zip(exons, exonData):
        # Fill in all the details for the exon
        exon.coverage = data["coverage"]
        exon.completeness = data["completeness"]
        exon.cutoff = cutoff
        exon.levels = data["levels"]

    # Persist all changes to database
    self.elementAdapter.commit()

  def calculate(self, chrom, intervals, cutoff=50, levels=False,
                bgIntervals=None):
    """
    Public: Calculates both coverage and completeness for a given set of
    intervals. This is accompished using a single method since the bottleneck
    will be reading coverage from a file rather than calculating coverage.

    N.B. Doesn't handle overlapping intervals.
    ----------

    :param chrom:       [string]   The chromosome id for the intervals
    :param intervals:   [iterable] List of `Interval` objects
    :param cutoff:      [int]      The cutoff to calculate completeness
                                   (Def: 50)
    :param levels:      [bool]     Whether to return string representation of
                                   coverage across the intervals (Def: False)
    :param bgIntervals: [iterable] List of BEDGraph intervals instead of
                                   generating them dynamically
    :returns:           [tuple]    Coverage (float), completeness (float),
                                   BEDGraph intervals (str)

    Usage:
      gene = core.get("gene", "C3")
      core.coverage(gene.chrom, gene.intervals, 15)
      [out] => (13.43522398231, 0.434122133123, None)
    """
    # Initialize
    totBaseCount = float(sum([len(interval) for interval in intervals]))
    readCount = 0
    passedCount = 0

    if bgIntervals is None:
      # Get BEDGraph intervals covering all input intervals
      # Minimizes the number of times we have to fetch BEDGraph intervals
      bgIntervals = self.readIntervals(chrom, intervals)

    for chunk in bgIntervals:

      for bgi in chunk:
        bgBases = len(bgi)

        # Add the number of overlapping reads
        readCount += (bgBases * bgi.value)

        # Add the position if it passes `cutoff`
        if bgi.value >= cutoff:
          passedCount += bgBases

    # Also calculate levels if requested
    str_levels = None
    if levels:
      str_levels = self.stringify(bgIntervals)

    return (readCount / totBaseCount), (passedCount / totBaseCount), str_levels

  def stringify(self, intervals):
    """
    Public: Generates BEDGraph intervals as string representation that can be
    persisted in a SQL database.
    ----------

    :param intervals: [iterable] List of `Interval` objects
    :returns:         [str]      String representation of BEDGraph intervals
    """
    levels = ["{start}-{end}-{depth}".format(start=interval.start,
                                             end=interval.end,
                                             depth=interval.value)
              for interval in intervals]

    return ",".join(levels)

  def levels(self, intervals):
    """
    Public: Generates a string representation of discrete coverage levels;
    ok, soso, warn, err. These can be saved to a SQL database and later be
    parsed to vizualize coverage dynamically.
    ----------

    :param intervals: [iterable] A list of BEDGraph `Interval`s
    :returns:         [str]      String representation of the discrete levels
    """
    # Initialize/Reset
    self.lastStart = None
    self.lastLevel = None

    # List comprehend level intervals (or None)
    levels = [self._setLevel(interval) for interval in intervals]

    # First filter out `None` items from the list. Then concat the rest of the
    # items separated by a comma.
    return ",".join(filter(None, levels))

  def _setLevel(self, interval):
    """
    Private: Determines what level an interval belongs to accoding to
    read depth.
    ----------

    :param interval: [obj]      BEDGraph `Interval`
    :returns:        [str/None] String used by `.levels()` or `None` if level
                                hasn't changed.
    """
    # Determine what level the interval belongs to
    if interval.value > 19:
      currLevel = "ok"
    elif interval.value > 9:
      currLevel = "soso"
    elif interval.value > 1:
      currLevel = "warn"
    else:
      currLevel = "err"

    # Check if the level has changed
    if currLevel != self.lastLevel:
      # Yes: begin new level interval
      self.lastStart = interval.start
      self.lastLevel = currLevel

      # Return the start pos of the new interval and level
      return "{start}-{level}".format(start=interval.start, level=currLevel)

    else:
      # Return `None` if the level hasn't changed
      return None

  def _processExons(self, exIntervals, bgIntervals, cutoff=50, levels=False):
    """
    Private: Based on BEDGraph intervals for a whole gene, calculate coverage
    and completeness for each individual exon interval.
    ----------

    :param exIntervals: [list] List of objects with start, end, value
                               attributes.
    :param bgIntervals: [list] List of BEDGraph formatted intervals
    :param cutoff:      [int]  The cutoff to calculate completeness
                               (Default: 50)
    :param levels:      [bool] Whether to return string representation of
                               coverage across the intervals (Default: False)
    :returns:           [list] List of dicts with data on each exon interval
    """

    # Initialize interval tree
    bgTree = CoverageTree()
    for chunk in bgIntervals:
      for bgi in chunk:
        bgTree.insert_interval(bgi)

    # This is for storing exon coverage scores
    exons = [None]*len(exIntervals)

    for exCount, ex in enumerate(exIntervals):
      baseCount = float(ex.end - ex.start)
      readCount = 0
      passedCount = 0

      exBgIntervals = bgTree.get(ex.start, ex.end)
      for bgi in exBgIntervals:

        bgBaseCount = bgi.end - bgi.start

        # Add the number of overlapping reads
        readCount += (bgBaseCount * bgi.value)

        # Add the bases if they pass `cutoff`
        if bgi.value >= cutoff:
          passedCount += bgBaseCount

      # TODO: Also calculate levels if requested
      str_levels = self.stringify(exBgIntervals)

      exons[exCount] = {
        "coverage": readCount / baseCount,
        "completeness": passedCount / baseCount,
        "levels": str_levels
      }

    return exons
