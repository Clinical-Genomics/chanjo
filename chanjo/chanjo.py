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

  def annotate(self, options):
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
    elem_class = options[0]
    element = options[1]
    cutoff = options[2]
    levels = options[3]

    if elem_class == "gene" or elem_class == "transcript":
      cov, comp, str_levels = self.coverage(element.chrom,
                                            element.simpleIntervals(),
                                            cutoff, levels=levels)
    else:
      # Exon only a single interval
      cov, comp, str_levels = self.coverage(element.chrom, (element,), cutoff,  
                                            levels=levels)

    # Update the element with the calculated coverage information
    element.coverage = cov
    element.completeness = comp
    element.cutoff = cutoff
    element.levels = str_levels

  def coverage(self, chrom, intervals, cutoff=50, bgIntervals=None,
               levels=False):
    """
    Doesn't handle overlapping intervals
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
    levels = ["{start}-{end}-{depth}".format(start=interval.start,
                                             end=interval.end,
                                             depth=interval.value)
              for interval in intervals if interval.value < 10]

    return ",".join(levels)

  def levels(self, intervals):
    """
    Public: Generates a string representation of discrete coverage levels;
    ok, soso, warn, err. These can be saved to a SQL database and later be
    parsed to vizualize coverage dynamically.

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
    