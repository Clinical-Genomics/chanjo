#!/usr/bin/env python
# coding: utf-8

import itertools
import numpy as np

from calculate import intervals
from group import group


def process(self, bamFile, chrom, segments,
            extend=0, cutoff=10, threshold=10000):
  """
  <public> Annotates each related exon with coverage data.

  .. code-block:: python

  :param object element: One element object (gene/transcript)
  :param int cutoff: (optional) Min read depth for completeness [default: 10]
  :param bool splice: (optional) Include splice sites for each exon (+/- 2)
  """
  groups = group(segments, threshold=threshold, extend=extend)
  data = np.zeros(len(groups))

  for i, group_ in enumerate(groups):
    
    read_depth = bamFile.read(chrom, group_[0][0], group_[-1][1])
    data[i] = intervals(group_, read_depth, cutoff=cutoff)

  return itertools.chain.from_iterable(data)
