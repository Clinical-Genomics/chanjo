# -*- coding: utf-8 -*-
"""
chanjo.annotator.core
~~~~~~~~~~~~~~~~~~~~~~

Central pipeline for the Chanjo annotator module.
"""
from __future__ import absolute_import, unicode_literals

from toolz import concat, pipe
from toolz.curried import complement, filter, map, do

from .._compat import text_type
from ..depth_reader import BamFile
from .stages import (
  calculate_metrics,
  comment_sniffer,
  extend_interval,
  group_intervals,
  prefix,
  process_interval_group
)
from ..utils import bed_to_interval, split, validate_bed_format


def annotate_bed_stream(bed_stream, bam_path, cutoff=10, extension=0,
                        contig_prefix='', bp_threshold=17000):
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
    contig_prefix (str, optional): rename contigs by prefixing,
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
    filter(complement(comment_sniffer)),         # filter out comments
    map(text_type.rstrip),                       # strip invisble chars.
    map(prefix(contig_prefix)),                  # prefix to contig
    map(split(sep='\t')),                        # split lines
    map(do(validate_bed_format)),                # check correct format
    map(lambda row: bed_to_interval(*row)),      # convert to objects
    map(extend_interval(extension=extension)),   # extend intervals
    group_intervals(bp_threshold=bp_threshold),  # group by threshold
    map(process_interval_group(bam)),            # read coverage
    concat,                                      # flatten list of lists
    map(calculate_metrics(threshold=cutoff))     # calculate cov./compl.
  )
