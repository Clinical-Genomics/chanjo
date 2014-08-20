# -*- coding: utf-8 -*-
import numpy as np
import pytest

from chanjo.annotator import (
  assign_relative_positions,
  calculate_metrics,
  extend_interval,
  group_intervals,
  merge_intervals,
  prepend,
  process_interval_group
)
from chanjo.depth_reader import BamFile
from chanjo.utils import BaseInterval


def test_assign_relative_positions():
  """Test recalibrating a position relative to a new absolute start."""
  # test at the start of a larger overall interval
  assert assign_relative_positions(0, 10, 0) == (0, 10)

  # test some random interval
  assert assign_relative_positions(55, 170, 42) == (13, 128)

  # test edge case
  assert assign_relative_positions(2131334, 2132671, 2131334) == (0, 1337)

  # test something that shouldn't be valid; reversed interval
  with pytest.raises(AssertionError):
    assign_relative_positions(123, 100, 90)

  # test something that shouldn't be valid; non-inclusive inverval
  with pytest.raises(AssertionError):
    assign_relative_positions(100, 123, 150)


def test_calculate_metrics():
  """Test calculating multiple metrics."""
  # at this point, completeness can only be calculated with a
  # numpy array of read depths
  # read depts, coverage=4, bp_count=8
  read_depths = np.array([0, 5, 3, 3, 4, 5, 5, 7])
  fake_interval = None
  interval, coverage, completeness = calculate_metrics(
    (fake_interval, read_depths), threshold=5)

  assert interval == fake_interval
  assert coverage == 4
  assert completeness == .5


def test_extend_interval():
  """Test extending an interval in both directions."""
  interval = BaseInterval('chr1', 10, 100)

  # test default which is no extension
  assert extend_interval(interval) == interval

  # test simple extension
  extended_interval = extend_interval(interval, extension=5)
  assert extended_interval.start == 5
  assert extended_interval.end == 105


def test_group_intervals():
  """Test aggregating intervals in groups."""
  # intervals on the same contig
  intervals = [
    BaseInterval('1', 10, 100),
    BaseInterval('1', 90, 150),
    BaseInterval('1', 200, 250)
  ]
  grouped_intervals = [intervals[:2], intervals[2:]]
  groups = group_intervals(intervals, bp_threshold=150)
  assert list(groups) == grouped_intervals

  # intervals on multiple contigs
  intervals = [
    BaseInterval('X', 10, 100),
    BaseInterval('Y', 90, 150),
    BaseInterval('Y', 200, 250)
  ]
  grouped_intervals = [intervals[:1], intervals[1:]]
  groups = group_intervals(intervals, bp_threshold=1000)
  assert list(groups) == grouped_intervals


def test_merge_intervals():
  """Test merging multiple intervals."""
  # only makes sense for intervals on the same contig
  intervals = [
    BaseInterval('1', 10, 100),
    BaseInterval('1', 90, 150),
    BaseInterval('1', 200, 250)
  ]
  assert merge_intervals(intervals) == (10, 250)

  # test with tricky overlapping intervals
  intervals = [
    BaseInterval('1', 505, 585),
    BaseInterval('1', 520, 550),
    BaseInterval('1', 545, 580)
  ]
  assert merge_intervals(intervals) == (505, 585)

  # test with 1 interval
  assert merge_intervals([BaseInterval('1', 10, 10)]) == (10, 10)

  # test with 0 intervals
  with pytest.raises(ValueError):
    merge_intervals([])


def test_prepend():
  """Test prepending values to sequences."""
  assert prepend('chr', '1') == 'chr1'
  assert prepend([10], [11, 12, 13]) == [10, 11, 12, 13]
  assert prepend('', 'X') == 'X'


def test_process_interval_group():
  """Test processing an entire group of intervals."""
  bam = BamFile('tests/fixtures/alignment.bam')
  interval_group = [
    BaseInterval('chr1', 1, 5), BaseInterval('chr1', 10, 13)
  ]

  intervals_coverage = list(process_interval_group(bam, interval_group))

  interval1 = intervals_coverage[0][0]
  read_depths1 = list(intervals_coverage[0][1])
  assert interval1 == interval_group[0]
  assert read_depths1 == [2, 4, 5, 5, 5]

  interval2 = intervals_coverage[1][0]
  read_depths2 = list(intervals_coverage[1][1])
  assert interval2 == interval_group[1]
  assert read_depths2 == [7, 7, 7, 7]
