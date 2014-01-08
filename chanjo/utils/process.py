#!/usr/bin/env python
# coding: utf-8

import itertools

from .calculate import intervals
from .group import group


def process(bamFile, chrom, segments, extend=0, cutoff=10, threshold=10000):
  """
  <public> Annotates each related exon with coverage data.

  .. code-block:: python

    >>> from chanjo import utils, bam
    >>> bamFile = bam.CoverageAdaper("myBamFile.bam")
    >>> exons = [(1, 10, "exon1"), (15, 30, "exon2"), ...]
    >>> data = utils.process(bamFile, 1, exons, 0, 10, 50)

  :param object bamFile: Initialized CoverageAdaper object
  :param str chrom: Chromosome ID
  :param list segments: List of continous genomic segments
  :param int extend: How much to extend each segment with [default: 0]
  :param int cutoff: Min read depth for completeness [default: 10]
  :param bool threshold: Target length for grouping segments [default: 10000]
  """
  groups = group(segments, threshold=threshold, extend=extend)
  list_groups = list(groups)
  data = [0] * len(list_groups)

  for i, group_ in enumerate(list_groups):

    read_depth = bamFile.read(chrom, group_[0][0], group_[-1][1])
    data[i] = intervals(group_, read_depth, cutoff=cutoff)

  # Flatten the "2D" list
  return itertools.chain.from_iterable(data)
