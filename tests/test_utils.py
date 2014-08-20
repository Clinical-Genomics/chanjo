#!/usr/bin/env python
from __future__ import division

import numpy as np
import pytest

from chanjo._compat import text_type
from chanjo.utils import (
  average,
  _RawInterval,
  bed_to_interval,
  completeness,
  id_generator,
  BaseInterval,
  serialize_interval,
  serialize_interval_plus
)

def test_RawInterval():
  """Test generating a base :class:`_RawInterval`."""
  interval = ('chr1', 10, 20, 'int1', 0, '-', ['block1'], ['superblock1'])
  bed_interval = _RawInterval(*interval)

  assert bed_interval == interval
  assert bed_interval.start == 10
  assert bed_interval.contig == 'chr1'
  assert bed_interval.block_ids == ['block1']


def test_BaseInterval():
  """Test generating an interval without all fields filled in."""
  interval = ('chr1', 10, 20, 'int1')
  bed_interval = BaseInterval(*interval)

  assert bed_interval != interval
  assert bed_interval.start == 10
  assert bed_interval.contig == 'chr1'
  assert bed_interval.score == ''
  assert bed_interval.name == 'int1'
  assert bed_interval.block_ids == []


def test_bed_to_interval():
  """Test converting between BED interval and Chanjo interval."""
  bed_interval = ('22', '101', '220', 'int32', 0, '+', 'block11')
  chanjo_interval = bed_to_interval(*bed_interval)

  assert chanjo_interval.contig == '22'
  # BED specifies 0:1 intervals, Chanjo works with 1:1 mapping
  assert chanjo_interval.start == 102
  assert chanjo_interval.end == 220
  assert chanjo_interval.block_ids == ['block11']
  assert chanjo_interval.superblock_ids == []

  with pytest.raises(ValueError):
    # interval with invalid coordinates/arguments
    bed_to_interval(20, 'X', 24, 'int2', 0, '-')


def test_average():
  """Test calculating average of a list of values."""
  values = [0, 5, 5, 6]
  # 'without' numpy
  assert average(values) == 4.

  # with numpy array
  assert average(np.array(values)) == 4.


def test_completeness():
  """Test calculating completeness of a list of read depths."""
  # test simple case
  assert completeness(np.array([0, 10, 10, 20, 10, 0])) == 4/6

  # test edge case with 0 positions, should *not* raise
  # ``ZeroDivisionError``.
  assert completeness(np.array([])) == 0.

  # test with a different ``threshold``
  assert completeness(np.array([20, 40, 10, 0, 10]), threshold=30) == 1/5


def test_serialize_interval():
  """Test serializing an BaseInterval instance."""
  # simple case, should remove empty fields to the right
  interval = BaseInterval('chr1', 10, 20)
  assert serialize_interval(interval) == 'chr1\t10\t20'

  # with block ids, should maintain empty intermediate fields!
  interval = BaseInterval('chr22', 101, 200, block_ids=['block11', 'block12'])
  serialized_interval = 'chr22\t101\t200\t\t\t\tblock11,block12'
  assert serialize_interval(interval) == serialized_interval

  # test curried function composition
  serialize_interval_alt = serialize_interval(delimiter='|', subdelimiter=';')
  serialized_interval_alt = 'chr22|101|200||||block11;block12'
  assert serialize_interval_alt(interval) == serialized_interval_alt


def test_serialize_interval_plus():
  """Test serializing an BaseInterval with additional fields."""
  # simple case
  interval = BaseInterval('chr1', 10, 100, score=14)
  string = serialize_interval_plus([interval, 14.1, .94])
  assert string == 'chr1\t10\t100\t\t14\t14.1\t0.94'


def test_id_generator():
  """Test generating a random id."""
  # difficult to test randomly generated strings...
  assert len(id_generator()) == 8
  assert isinstance(id_generator(), text_type)

  # test with custom sized id
  assert len(id_generator(3)) == 3

  # test edge case with 0 lenght
  assert id_generator(0) == ''
