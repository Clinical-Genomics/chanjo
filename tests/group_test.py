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
    intervals = [(5,7,"1"), (6,10,"2"), (12,15,"3"), (20,25,"4"), (22,28,"5")]
    res = group(intervals, threshold=10)
    assert_equal(list(res), [[(5,7,"1"), (6,10,"2"), (12,15,"3")],
                             [(20,25,"4"), (22,28,"5")]])

    # Add more complexity, don't commit to early
    intervals = [(0,10,"1"), (5,7,"2"), (15,20,"3"), (20,25,"4"), (25,25,"5")]
    res = group(intervals, threshold=10)
    assert_equal(list(res), [[(0,10,"1"), (5,7,"2")], [(15,20,"3"),
                              (20,25,"4"), (25,25,"5")]])
