#!/usr/bin/env python
# coding: utf-8

from nose.tools import *
from chanjo.bam import CoverageAdapter


class TestCoverageAdapter:
  def __init__(self):
    bam_path = "tests/data/align.bam"
    self.adapter = CoverageAdapter(bam_path)

    # These are the main results from "align.bam"
    self.depths = [2., 4., 5., 5., 5., 5., 6., 7., 7., 7., 7., 7., 7., 7., 7., 7., 7., 7., 7., 7., 7., 7., 7., 8., 8., 7., 7., 7., 7., 7., 7., 7., 6., 4., 4., 3., 3., 2., 2.]

  def setUp(self):
    print "SETUP!"

  def tearDown(self):
    print "TEAR DOWN!"

  def test_read(self):
    # Read BAM from position [1,10]
    depths = self.adapter.read("chr1", 0, 9)

    # Make assertions: we expect the read depths from 1st to 10th pos to be
    # included.
    answer = self.depths[0:10]
    assert_equal(list(depths), answer)

    # Test also an interval that extends beyond the reads
    depths = self.adapter.read("chr1", 35, 45)
    assert_equal(list(depths), self.depths[35:] + [0, 0, 0, 0, 0, 0, 0])

    # Test interval completely outside the reads
    depths = self.adapter.read("chr1", 50, 60)
    assert_equal(list(depths), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    # Test submitting a false chromosome ID
    try:
      bgi = self.adapter.read("crh1", 10, 20)
    except ValueError, e:
      assert_true(e.message == "invalid reference `crh1`")
