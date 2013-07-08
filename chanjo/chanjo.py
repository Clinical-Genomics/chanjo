#!/usr/bin/env python
# coding: utf-8
"""
  chanjo.module
  ~~~~~~~~~~~~~

  The clue and control center of the `chanjo` system.
  Works in some ways similar to Ember.js in the way you add in adaptors to
  add in modular functionality that can be switched out to support multiple
  "backends".

  A description which can be long and explain the complete
  functionality of this module even with indented code examples.
  Class/Function however should not be documented here.

  :copyright: 2013 by Robin Andeer, see AUTHORS for more details
  :license: MIT, see LICENSE for more details
"""

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
      analyzer.setAdaptors(CoverageAdaptor(), ElementAdaptor())
    """
    # Customizable adaptors
    self.coverageAdaptor = coverageAdaptor
    self.elementAdaptor = elementAdaptor

    # Shortcuts to the import methods
    self.importElements = self.elementAdaptor.connect

    # Shortcut to getting an elements by ID
    self.get = self.elementAdaptor.get

    # Shortcut to getting an elements by ID
    self.getCoverage = self.coverageAdaptor.intervals

  def calculateCoverage(self, genes, cutoff=50):
    """
    Public: Calculate and annotate coverage for a list of genes and related
            transcripts and exons.
    ----------
    :param genes:  [iterable] A list of gene IDs
    :param cutoff: [int] The read depth level to use for coverage completeness
                   (Default: 50)

    Usage:
      genes = ["EGFR", "GIT1"]
      analyzer.calculateCoverage(genes, 10)
      > 'Done and done ... and I mean done.'
    """

    for count, gene_id in enumerate(genes):

      if count%100 == 0:
        print count

      # Calculate and persist coverage for the gene
      gene = self.elementCoverage("gene", gene_id, cutoff)

      # for tx_child in gene.transcripts:
      #   # Calculate and persist coverage for each transcript
      #   tx = self.elementCoverage("transcript", tx_child.id, cutoff)

      # for ex in gene.exons:
      #   # Calculate and persist coverage for each exon
      #   self.elementCoverage("exon", ex.id, cutoff)

    print "Done and done ... and I mean done."

  def elementCoverage(self, elem_class, elem_id, cutoff=50):
    """
    Public: Calculate and persist coverage for a single element.
    ----------
    :param elem_class: [str] The class of element, e.g. "gene"
    :param elem_id:    [str] The unique element id
    :param cutoff:     [int] The read depth level to use for coverage completeness
                       (Default: 50)

    Usage:
      analyzer.elementCoverage("gene", "EGFR", 50)
      [out] => <chanjo.sqlite2.Gene at 0x1041c4c10>
    """
    # For some reason, unicode string doesn't work
    element = self.get(elem_class, str(elem_id))
    if elem_class == "gene" or elem_class == "transcript":
      cov, comp = self.coverage(element.chrom, element.simpleIntervals(),
                                cutoff=cutoff)
    else:
      # Exon (already satisfies interval demands)
      cov, comp = self.coverage(element.chrom, element, cutoff=cutoff)

    # Update the element with the calculated coverage information
    element.coverage = cov
    element.completeness = comp
    element.cutoff = cutoff

    # Persist the changes
    element.save()

    return element

  def coverage(self, chrom, intervals, cutoff=50):
    """
    Public: Calculates coverage across *non-overlapping* intervals.
    ----------
    :param chrom:     [str] The chromosome related to the intervals
    :param intervals: [iterable] A list of `Interval`-like classes. Must have
                      start and end attributes.
    :param cutoff:    [int] The read depth level to use for coverage completeness
                      (Default: 50)
    :returns:         [tuple] The mean read depth and the % coverage at the
                      given cutoff

    Usage:
      gene = analyzer.get("gene", "SDF4")
      analyzer.coverage(gene.chrom, gene.simpleIntervals(), 10)
      [out] => (7.605809128630705, 0.5253112033195021)
    """
    # The chromosome ID must be submitted as a string
    chrom = str(chrom)

    # If you only supply one interval
    if not isinstance(intervals, collections.Iterable):
      # Just make iterable
      intervals = (intervals,)

    # Always need to know the number of bases across the intervals
    baseCount = 0.

    # Preallocate result lists
    readCounts = [None]*len(intervals)
    passedCounts = list(readCounts)
    for count, interval in enumerate(intervals):
      # Assumes no overlap between them
      # Add the length of the current interval
      baseCount += interval.end - interval.start
      # Add the accumulated read depth and the number of passed bases
      (readCounts[count],
       passedCounts[count]) = self.readPassedCount(chrom, interval.start,
                                                   interval.end, cutoff)

    # Return mean read depth and % covered at cutoff
    return (sum(readCounts) / baseCount,
            sum(passedCounts) / baseCount)

  def readPassedCount(self, chrom, start, end, cutoff=50):
    """
    Public: Calculates the read count and positions passing a cutoff.
    ----------
    :param chrom:  [str] The chromosome for the interval
    :param start:  [int] The start position of the interval
    :param end:    [int] The end position of the interval
    :param cutoff: [int] The cutoff for accepting a position (Default: 50)
    :returns:      [int, int] The sum of read depth across the interval, the
                   sum of positions passing the cutoff. 

    Usage:
      analyzer.readPassedCount("17", 134839488, 134933418, cutoff=10)
      [out] => (234961, 93929)
    """
    chrom = str(chrom)
    intervals = self.getCoverage(chrom, start, end, cutoff)
    readCount = 0
    passedCount = 0

    for interval in intervals:
      length = interval.end - interval.start
      depth = interval.value
      readCount += depth * length

      # Count all bases as passed if at least equal to the cutoff
      if depth >= cutoff:
        passedCount += length

    # Return accumulated read depth
    return readCount, passedCount

  def levels(self, element, intervals=None, save=True):
    if not intervals:
      # Assume gene
      intervals = self.getCoverage(element.chrom, element.intervals.lower_bound,
                                   element.intervals.upper_bound)

    levels = [IntervalSet(), IntervalSet(), IntervalSet()]
    for interval in intervals:
      readDepth = interval.value
      if readDepth < 50:
        if readDepth > 10:
          levels[0].add(Interval(start, end))
        elif readDepth > 0:
          levels[1].add(Interval(start, end))
        else:
          levels[2].add(Interval(start, end))

    for count, level in enumerate(levels):
      intervals = ",".join(["{0}-{1}".format(ival.lower_bound, ival.upper_bound)
                            for ival in level])
      if count == 0:
        element.intervals_10_50x = intervals
      elif count == 1:
        element.intervals_1_10x = intervals
      else:
        element.intervals_0x = intervals
