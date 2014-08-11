# -*- coding: utf-8 -*-
"""
chanjo.converter.core
~~~~~~~~~~~~~~~~~~~~~~

Central pipeline for the Chanjo converter module.
"""
from __future__ import absolute_import
from itertools import groupby as lazy_groupby
from operator import attrgetter

from toolz import pipe, partial, concat
from toolz.curried import map, filter, groupby, valmap, pluck

from .._compat import itervalues
from .stages import (
  extract_intervals, grep, merge_related_elements, rename_sex_interval
)


def pipeline(ccds_stream):
  """Convert CCDS dump to Chanjo-style BED stream.

  Main entry point for default Chanjo converter (ccds). It converts
  a sorted (start, chrom) CCDS database to the Chanjo BED-format.

  Args:
    ccds_stream (file): file handle to read CCDS lines from

  Yields:
    Interval: interval with merged block and superblock ids
  """
  return pipe(
    ccds_stream,
    filter(grep('Public')),                    # filter out Public tx
    map(str.rstrip),                           # strip \n and spaces
    map(partial(str.split, sep='\t')),         # split into list
    map(extract_intervals),                    # convert to Interval
    concat,                                    # flatten
    map(rename_sex_interval),                  # rename sex contigs
    partial(lazy_groupby, key=attrgetter('contig')),  # group by contig
    pluck(1),                                  # extract second item
    map(groupby(attrgetter('name'))),          # non-lazy group by id
    map(valmap(merge_related_elements)),       # group intervals
    map(itervalues),                           # extract values
    map(partial(sorted, key=attrgetter('start'))),  # sort by start pos
    concat                                     # flatten
  )
