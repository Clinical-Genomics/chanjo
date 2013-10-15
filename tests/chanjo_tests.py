#!/usr/bin/env python
# coding: utf-8

from nose.tools import *
from chanjo.core import Hub
from chanjo.sql import ElementAdapter
from chanjo.bam import CoverageAdapter


class TestHub:
  def __init__(self):
    self.hub = Hub()

    elem_path = ":memory:"
    bam_path = "tests/data/align.bam"

    self.hub.connect(CoverageAdapter(bam_path), ElementAdapter(elem_path))

  def test_calculate(self):
    # Test for normal depths
    depths = [10, 11, 11, 12, 12, 13, 12, 12, 12, 11, 10, 8]
    cutoff = 12
    posCount = float(len(depths))
    fun = lambda x: x >= cutoff

    cov_s, comp_s = self.hub.calculate(depths, cutoff)
    assert_equal(cov_s, sum(depths)/posCount)
    assert_equal(comp_s, len(filter(fun, depths))/posCount)

    # Test with 0 depth positions
    depths = [0, 10, 0, 5, 0]
    cutoff = 8
    posCount = float(len(depths))
    cov_m, comp_m = self.hub.calculate(depths, cutoff)
    assert_equal(cov_m, sum(depths)/posCount)
    assert_equal(comp_m, len(filter(fun, depths))/posCount)

    # Test with all depths = 0, outside reads
    depths = [0, 0, 0, 0, 0, 0]
    cov_o, comp_o = self.hub.calculate(depths, 10)
    assert_equal(cov_o, 0)
    assert_equal(comp_o, 0)
