#!/usr/bin/env python
# coding: utf-8

from __future__ import division
from nose.tools import assert_equal
import numpy as np
from chanjo.utils.calculate import coverageMetrics, intervals


class TestCalculate:
  def __init__(self):
    pass

  def test_coverageMetrics(self):
    """
    Test calculation of coverage metrics (avg. coverage, completeness) for a
    continous interval.
    """
    # Test for normal depths
    depths = np.array([10, 11, 11, 12, 12, 13, 12, 12, 12, 11, 10, 8])
    cutoff = 12
    posCount = len(depths)
    fun = lambda x: x >= cutoff

    cov_s, comp_s = coverageMetrics(depths, cutoff)
    assert_equal(cov_s, sum(depths)/posCount)
    assert_equal(comp_s, len(filter(fun, depths))/posCount)

    # Test with 0 depth positions
    depths = np.array([0, 10, 0, 5, 0])
    cutoff = 8
    posCount = len(depths)
    cov_m, comp_m = coverageMetrics(depths, cutoff)
    assert_equal(cov_m, sum(depths)/posCount)
    assert_equal(comp_m, len(filter(fun, depths))/posCount)

    # Test with all depths = 0, outside reads
    depths = np.array([0, 0, 0, 0, 0, 0])
    cov_o, comp_o = coverageMetrics(depths, 10)
    assert_equal(cov_o, 0)
    assert_equal(comp_o, 0)

  def test_intervals(self):
    """
    Test calculation of coverage metrics for multiple grouped intervals.
    """
    #                       1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2
    #                       0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    read_depths = np.array([2,3,1,2,2,2,3,4,5,4,3,0,0,0,1,2,3,3,3,4,5,6])

    # Normal (overlapping) intervals
    group = [(5, 10, 21, 3), (7, 15, 19, 3)]
    res = intervals(group, read_depths[5:], cutoff=4)
    # Assess coverage
    assert_equal(res[0][0], 21/6)
    # Assess completeness
    assert_equal(res[0][1], 3/6)

    # [(0, 5, 12, 0), (0, 10, 31, 3)],  # intervals with 0
    # [(8, 8, 5, 1)]  # single base interval

    # Test intervals extending beyond read depths (error)
    grouped_intervals = [(10,15), (20,100)]

    try:
      res = intervals(grouped_intervals, read_depths)
    except IndexError, e:
      assert_equal(e.message, "list index out of range")
