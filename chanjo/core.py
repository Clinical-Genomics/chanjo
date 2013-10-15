#!/usr/bin/env python
# coding: utf-8
"""
  chanjo.core
  ~~~~~~~~~~~~~

  This module implements the glue and controlling hub of `Chanjo`. The
  :class:`Hub` is also where the adapters are plugged in to. This will likely
  be pretty much the only part of the package you directly interact with if
  you decide to use the Pythonic API.

  :copyright: (c) 2013 by Robin Andeer
  :license: MIT, see LICENSE for more details
"""


class Hub(object):
  """
  The :class:`Hub` is the core component of `Chanjo`. It's able to prepare
  data and annotate elements, calculate coverage for a range of genomic
  positions, and interact with the element data store.

  .. code-block:: python

    from chanjo.core import Hub
    from chanjo.bam import CoverageAdapter
    from chanjo.sqlite import ElementAdapter

    bam = CoverageAdapter("/path/to/file.bam")
    sql = ElementAdapter("/path/to/sqlite.db")
    hub = Hub(bam, sql)

  :param str coverageAdapter: (optional) Plug in the adapter during init
  :param str elementAdapter: (optional) Plug in the adapter during init

  """
  def __init__(self, coverageAdapter=None, elementAdapter=None):
    super(Hub, self).__init__()

    # Set up the adapters
    if coverageAdapter and elementAdapter:
      self.connect(coverageAdapter, elementAdapter)

  def connect(self, coverageAdapter, elementAdapter):
    """
    <public> Plugs in the required adapters.

    .. code-block:: python

      >>> bam_path = "/path/to/file.bam"
      >>> cov_path = "/path/to/sqlite.db"
      >>> hub.connect(CoverageAdapter(bam_path), ElementAdapter(cov_path))

    :param str coverageAdapter: An instance of a :class:`CoverageAdapter`
    :param str elementAdapter:  An instance of a :class:`ElementAdapter`
    """
    # Customizable adapters
    self.cov = coverageAdapter
    self.db = elementAdapter

  def annotate(self, element, cutoff=10, splice=False):
    """
    <public> Annotates each related exon with coverage data.

    .. code-block:: python

      >>> genes = hub.db.get("gene", ["GIT1", "EGFR", "BRCA1"])
      >>> for gene in genes:
      >>>   hub.annotate(gene, 15)

    :param object element: One element object (gene/transcript)
    :param int cutoff: (optional) Min read depth for completeness [default: 10]
    :param bool splice: (optional) Include splice sites for each exon (+/- 2)
    """
    start = element.start
    end = element.end

    # Include splice sites (+/- 2 bases) when reading from BAM-file
    if splice:
      start -= 2
      end += 2

    # Both transcripts and genes can be used to select exons to annotate
    depth = self.cov.read(element.chrom, start, end)

    # Preallocate list for each exon of the element
    exons = [None]*len(element.exons)

    # Get the exons related to the element
    for i, exon in enumerate(element.exons):
      ex_start = exon.start
      ex_end = exon.end

      # Include splice sites for the exon
      if splice:
        ex_start -= 2
        ex_end += 2

      # Relative start and end positions to slice the ``depth`` array
      rel_start = ex_start - start
      rel_end = ex_end - start

      # Do the heavy lifting
      # +1 to end because ``end`` is 0-based and slicing is 0,1-based
      (coverage,
       completeness) = self.calculate(depth[rel_start:rel_end+1], cutoff)

      exons[i] = {
        "element_id": exon.id,
        "coverage": coverage,
        "completeness": completeness
      }

    return exons

  def calculate(self, depths, cutoff):
    """
    <public> Calculates both coverage and completeness for an interval.

    .. code-block:: python

      >>> gene = hub.db.get("gene", "C3")
      >>> hub.coverage(gene.chrom, gene.intervals, 15)
      (13.43522398231, 0.434122133123)

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
