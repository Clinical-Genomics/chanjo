#!/usr/bin/env python
# coding: utf-8

from __future__ import division
from nose.tools import assert_equal
from chanjo.utils.group import group


class TestGroup:
  def __init__(self):
    pass

  def test_group(self):
    """
    Test grouping of intervals based on length threshold
    """
    # Very basic example
    intervals = [(5,7), (6,10), (12,15), (20,25), (22,28)]
    res = group(intervals, threshold=10)
    assert_equal(list(res), [[(5,7), (6,10), (12,15)], [(20,25), (22,28)]])

    # Add more complexity, don't commit to early
    intervals = [(0,10), (5,7), (15,20), (20,25), (25,25)]
    res = group(intervals, threshold=10)
    assert_equal(list(res), [[(0,10), (5,7)], [(15,20), (20,25), (25,25)]])
