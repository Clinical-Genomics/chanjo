# -*- coding: utf-8 -*-
from chanjo.store import Interval, Interval_Block


def test_Interval_Block():
  # test table name
  assert Interval_Block.name == 'interval__block'


def test_Interval():
  # set up
  interval = Interval('interval1', 'chr1', 10, 1000, '-')

  assert len(interval) == 991
