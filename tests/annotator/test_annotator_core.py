# -*- coding: utf-8 -*-
from __future__ import division, unicode_literals

from chanjo.annotator import annotate_bed_stream
from chanjo.utils import BaseInterval


def test_annotator_pipeline():
  """Test the entire annotator pipeline."""
  bam_path = 'tests/fixtures/alignment.bam'

  # test with minimal BED "file"
  bed_stream = ['#chrom\tstart\tend', '1\t0\t5', '1\t9\t20']
  read_depths1 = [2, 4, 5, 5, 5]
  read_depths2 = [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
  result = annotate_bed_stream(
    bed_stream, bam_path, cutoff=5, contig_prefix='chr', bp_threshold=100
  )

  interval1, coverage1, completeness1 = next(result)
  interval2, coverage2, completeness2 = next(result)

  assert interval1 == BaseInterval('chr1', 1, 5)
  assert coverage1 == sum(read_depths1) / len(read_depths1)
  assert completeness1 == 3 / 5

  assert interval2 == BaseInterval('chr1', 10, 20)
  assert coverage2 == sum(read_depths2) / len(read_depths2)
  assert completeness2 == 1.
