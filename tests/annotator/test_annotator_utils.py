# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from chanjo.annotator.utils import get_sample_id


def test_get_sample_id():
  empty_bam_header = {}
  simple_bam_header = {'SQ': [{'SN': 'chr1'}], 'RG': [{'SM': 'sample1'}]}
  multi_lane_bam_header = {'RG': [{'SM': 'sample2'}, {'SM': 'sample2'}]}
  multi_sample_bam_header = {'RG': [{'SM': 'sample1'}, {'SM': 'sample2'}]}

  assert get_sample_id(empty_bam_header) == None
  assert get_sample_id(simple_bam_header) == 'sample1'
  assert get_sample_id(multi_lane_bam_header) == 'sample2'
  assert get_sample_id(multi_sample_bam_header) == None
