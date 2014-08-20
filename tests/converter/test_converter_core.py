# -*- coding: utf-8 -*-
from codecs import open

from chanjo.converter import ccds_to_bed


def test_builder_pipeline():
  """Test the entire converter pipeline."""
  # test with minimal BED "file"
  ccds_stream = open('tests/fixtures/CCDS.mini.txt', 'r', encoding='utf-8')
  intervals = list(ccds_to_bed(ccds_stream))

  assert len(intervals) == 19

  # test interval belonging to two blocks
  special_interval = intervals[3]
  assert special_interval.block_ids == ['CCDS54521.1', 'CCDS46694.1']
  assert special_interval.superblock_ids == ['RFPL2', 'RFPL2']
