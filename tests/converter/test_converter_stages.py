# -*- coding: utf-8 -*-

from chanjo.converter import (
  grep,
  extract_intervals,
  merge_related_elements,
  parse_raw_intervals,
  rename_sex_interval
)
from chanjo.utils import BaseInterval


def test_grep():
  string = 'Paul Thomas Anderson is a fantastic director.'
  pattern = 'fantastic'

  assert grep(pattern, string)
  assert grep('Kubrick', string) == False


def test_parse_raw_intervals():
  result = parse_raw_intervals('[11-18, 25-30, 32-35]')
  assert result == [[11, 18], [25, 30], [32, 35]]


def test_extract_intervals():
  record = ['1', 'NC_000001.10', 'SAMD11', '148398', 'CCDS2.2', 'Public',
            '+', '11', '35', '[11-18, 25-30, 32-35]', 'Identical']

  intervals = list(extract_intervals(record))
  interval1 = BaseInterval(
    '1', 11, 18, '1-11-18', 0, '+', ['CCDS2.2'], ['SAMD11']
  )

  assert intervals[0] == interval1


def test_merge_related_elements():
  interval_group = [
    BaseInterval(
      'X', 10, 100,block_ids=['block1'], superblock_ids=['sblock1']),
    BaseInterval(
      'X', 10, 100, block_ids=['block2'], superblock_ids=['sblock1']),
    BaseInterval(
      'X', 10, 100, block_ids=['block3'], superblock_ids=['sblock2'])
  ]

  merged_interval = merge_related_elements(interval_group)

  assert merged_interval[:3] == ('X', 10, 100)
  assert merged_interval.block_ids == ['block1', 'block2', 'block3']
  assert merged_interval.superblock_ids == ['sblock1', 'sblock1', 'sblock2']


def test_rename_sex_interval():
  sex = BaseInterval('X', 11, 111, block_ids=['block1', 'block2'])
  non_sex = BaseInterval('chr22', 4, 55, superblock_ids=['sblock1'])
  alt_sex = BaseInterval('chrY', 99, 921, superblock_ids=['sblock2'])

  # test with sex interval
  renamed_interval = rename_sex_interval(sex)
  assert renamed_interval.block_ids == ['X-block1', 'X-block2']

  # test non-sex interval
  same_interval = rename_sex_interval(non_sex)
  assert same_interval == non_sex

  # test sex interval with alternate contig names
  renamed_interval = rename_sex_interval(alt_sex, sex_contigs=['chrX', 'chrY'])
  assert renamed_interval.superblock_ids == ['chrY-sblock2']
