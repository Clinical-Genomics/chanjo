# -*- coding: utf-8 -*-
"""
chanjo.annotator.core
~~~~~~~~~~~~~~~~~~~~~~

Central pipeline for the Chanjo annotator module.
"""
from __future__ import absolute_import, unicode_literals

from toolz import pipe, concat
from toolz.curried import map

from .._compat import text_type
from ..depth_reader import BamFile
from .stages import (
  calculate_metrics,
  extend_interval,
  group_intervals,
  prepend,
  process_interval_group
)
from ..utils import bed_to_interval, split


def annotate_bed_stream(bed_stream, bam_path, cutoff=10, extension=0,
                        contig_prepend='', bp_threshold=17000):
  """Annotate all intervals from a BED-file stream.

  Yields tuple data for each interval with calculated coverage and
  completeness.

  Args:
    bed_stream (sequence): usually a BED-file handle to read from
    bam_path (str): path to BAM-file
    cutoff (int, optional): threshold for completeness calculation,
      defaults to 10
    extension (int, optional): number of bases to extend each interval
      with (+/-), defaults to 0
    contig_prepend (str, optional): rename contigs by prepending,
      defaults to empty string
    bp_threshold (int, optional): optimization threshold for reading
      BAM-file in chunks, default to 17000

  Yields:
    tuple: :class:`chanjo.BaseInterval`, coverage (float), and
      completeness (float)
  """
  # setup: connect to BAM-file
  bam = BamFile(bam_path)

  # the pipeline
  return pipe(
    bed_stream,
    map(text_type.rstrip),                       # strip non-chars
    map(prepend(contig_prepend)),                # prepend to contig
    map(split(sep='\t')),                        # split line segments
    map(lambda row: bed_to_interval(*row)),      # convert to objects
    map(extend_interval(extension=extension)),   # extend intervals
    group_intervals(bp_threshold=bp_threshold),  # group by threshold
    map(process_interval_group(bam)),            # read coverage
    concat,                                      # flatten
    map(calculate_metrics(threshold=cutoff))     # calculate cov./compl.
  )
