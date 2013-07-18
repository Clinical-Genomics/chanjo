#!/usr/bin/env python
# coding: utf-8
"""
  chanjo.module
  ~~~~~~~~~~~~~

  The clue and control hub of the `chanjo` package.
  Borrows many structural ideas from Ember.js in the way you add in adaptors to
  add in modular functionality that can be switched out to support multiple
  "backends".

  :copyright: 2013 by Robin Andeer, see AUTHORS for more details
  :license: MIT, see LICENSE for more details
"""

from __future__ import print_function
import collections
from interval import Interval, IntervalSet


class Analyzer(object):
  """docstring for Analyzer"""
  def __init__(self, coverageAdaptor=None, elementAdaptor=None):
    super(Analyzer, self).__init__()

    # Set up the adaptors
    if coverageAdaptor and elementAdaptor:
      self.setAdaptors(coverageAdaptor, elementAdaptor)

  def setAdaptors(self, coverageAdaptor, elementAdaptor):
    """
    Public: Plugs in the required adaptors and sets up a few shortcuts.
    ----------

    :param coverageAdaptor: [object] A class instance of a Coverage Adaptor
    :param elementAdaptor: [object] A class instance of a Element Adaptor

    Usage:
      from chanjo.bigBed import CoverageAdaptor
      from chanjo.sqlite import ElementAdaptor

      analyzer = Analyzer()
      bam_path = "/path/to/file.bam"
      cov_path = "/path/to/database.db"
      analyzer.setAdaptors(CoverageAdaptor(bam_path), ElementAdaptor(cov_path))
    """
    # Customizable adaptors
    self.coverageAdaptor = coverageAdaptor
    self.elementAdaptor = elementAdaptor

    # Shortcut to getting elements by ID
    self.get = self.elementAdaptor.get

    # Shortcut to getting coverage for intervals
    self.intervals = self.coverageAdaptor.intervals

  def annotate(self, elem, cutoff=50, levels=False):
    """
    Public: Calculate coverage for a single element.
    ----------
    :param elem_class: [str] The type of element
    :param element:    [object] The element object to annotate
    :param cutoff:     [int] The read depth level to use for coverage
                       completeness (Default: 50)

    Usage:
      gene = analyzer.get("gene", gene_id)
      analyzer.annotate("gene", gene, 50)
      [out] => <chanjo.sqlite2.Gene at 0x1041c4c10>
    """

    cov, comp, str_levels = self.coverage(elem.chrom, elem.simpleIntervals(),
                                          cutoff, levels)

    # Update the element with the calculated coverage information
    elem.coverage = cov
    elem.completeness = comp
    elem.cutoff = cutoff
    elem.levels = str_levels

  def coverage(self, chrom, intervals, cutoff=50, levels=False,
               bgIntervals=None):
    """
    Public: Calculates both coverage and completeness for a given set of
    intervals. This is accompished using a single method since the bottleneck
    will be reading coverage from a file rather than calculating coverage.

    N.B. Doesn't handle overlapping intervals.
    ----------

    :param chrom:       [string] The chromosome id for the intervals
    :param intervals:   [iterable] List of `Interval` objects
    :param cutoff:      [int] The cutoff to calculate completeness (Default: 50)
    :param levels:      [bool] Whether to return string representation of
                        coverage across the intervals (Default: False)
    :param bgIntervals: [iterable] List of BEDGraph intervals instead of
                        generating them dynamically
    :returns:           [float, float, str] coverage, completeness, BEDGraph
                        intervals as string
    """
    # Initialize
    totBaseCount = float(sum([len(interval) for interval in intervals]))
    readCount = 0
    passedCount = 0

    if bgIntervals is None:
      # Get BEDGraph intervals covering all input intervals
      # Minimizes the number of times we have to fetch BEDGraph intervals
      bgIntervals = self.intervals(chrom, intervals)

    for bgInterval in bgIntervals:
      bgBases = len(bgInterval)

      # Add the number of overlapping reads
      readCount += (bgBases * bgInterval.value)

      # Add the position if it passes `cutoff`
      if bgInterval.value >= cutoff:
        passedCount += bgBases

    # Also calculate levels if requested
    str_levels = None
    if levels:
      str_levels = self.allLevels(bgIntervals)

    return (readCount / totBaseCount), (passedCount / totBaseCount), str_levels

  def allLevels(self, intervals):
    """
    Public: Generates BEDGraph intervals as string representation that can be
    persisted in a SQL database.
    ----------

    :param intervals: [iterable] List of `Interval` objects
    :returns:         [str] String representation of BEDGraph intervals
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
    :returns:         [str] String representation of the discrete levels
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

    :param interval: [obj] BEDGraph `Interval`
    :returns:        [str/None] String used by `.levels()` or `None` if level
                     hasn't changed.
    """

    # score = interval.value / 5

    # self.score2level = {
    #   1: None,
    #   2: 10,
    #   3: 15,
    #   4: 20,
    #   5: 25
    # }

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
    