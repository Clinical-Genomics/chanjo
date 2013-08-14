#!/usr/bin/env python
# coding: utf-8

from nose.tools import *
from chanjo.bam import CoverageAdaptor, Interval


class TestCoverageAdaptor:
  def __init__(self):
    bam_path = "tests/data/align.bam"
    self.adaptor = CoverageAdaptor(bam_path)

    # These are the main results from "align.bam"
    self.trueIntervals = [Interval(0,1,2), Interval(1,2,4), Interval(2,6,5),
                          Interval(6,7,6), Interval(7,23,7), Interval(23,25,8),
                          Interval(25,32,7), Interval(32,33,6),
                          Interval(33,35,4), Interval(34,37,3),
                          Interval(37,39,2)]

  def setUp(self):
    print "SETUP!"
    # Different combinations of intervals
    self.mono_intervals = [Interval(0, 30)]
    self.poly_intervals = [Interval(10, 20), Interval(30, 35)]
    self.partly_outside_intervals = [Interval(35, 45), Interval(60, 70)]
    self.outside_intervals = [Interval(60, 70)]

  def tearDown(self):
    print "TEAR DOWN!"

    del self.mono_intervals, self.poly_intervals

  def test_read(self):
    # Read BAM from position [1,10]
    bgi = self.adaptor.read("chr1", 0, 10)

    # The actual BEDGraph intervals, the 4 first + modified 5th
    trueIntervals = self.trueIntervals[:4] + [Interval(7,10,7)]
    assert_equal(bgi, trueIntervals)

    # Test also an interval that extends beyond reads
    bgi = self.adaptor.read("chr1", 50, 60)
    assert_equal(bgi, [])

    # Test submitting a false chromosome ID
    try:
      bgi = self.adaptor.read("crh1", 10, 20)
    except ValueError, e:
      assert_true(e.message == "invalid reference `crh1`")

  def test_readIntervals(self):
    # Test a single interval
    bgi = self.adaptor.readIntervals("chr1", self.mono_intervals)

    # This step is important becuase it should be possible to return a generator
    # object insted of a list of BEDGraph intervals.
    chunks = [chunk for chunk in bgi]
    assert_equal(chunks, self.trueIntervals[:6] + [Interval(25,30,7)])

    # Test multiple non-overlapping intervals
    bgi = self.adaptor.readIntervals("chr1", self.poly_intervals)
    chunks = [chunk for chunk in bgi]
    assert_equal(chunks, [Interval(20,30,7), Interval(30,32,7),
                          Interval(32,33,6), Interval(33,35,4)])

    # Test multiple intervals extending beyond reads
    bgi = self.adaptor.readIntervals("chr1", self.partly_outside_intervals)
    chunks = [chunk for chunk in bgi]
    assert_equal(chunks, [Interval(35,37,4), Interval(37,39,2)])

    # Test interval outside reads
    bgi = self.adaptor.readIntervals("chr1", self.outside_intervals)
    chunks = [chunk for chunk in bgi]
    assert_equal(chunks, [])

class TestInterval:
  def setUp(self):
    print "SETUP!"

    # Single position interval
    self.single_interval = Interval(0, 1)

    # Multi position interval
    self.multi_interval = Interval(0, 10)

    # Long position interval
    self.long_interval = Interval(99, 100002)

  def tearDown(self):
    print "TEAR DOWN!"

    del self.single_interval, self.multi_interval, self.long_interval

  def test_len(self):    
    assert_equal(len(self.single_interval), 1)
    assert_equal(len(self.multi_interval), 10)
    assert_equal(len(self.long_interval), 99903)

  def test_str(self):
    assert_equal(self.single_interval.__str__(), "(0, 1]")
    assert_equal(self.multi_interval.__str__(), "(0, 10]")
    assert_equal(self.long_interval.__str__(), "(99, 100002]")
