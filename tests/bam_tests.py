from nose.tools import *
from chanjo.bam import CoverageAdaptor, Interval
import os

class TestClass:
  def __init__(self):
    bam_path = "tests/data/align.bam"
    self.adaptor = CoverageAdaptor(bam_path)

  def setUp(self):
    print "SETUP!"

  def tearDown(self):
    print "TEAR DOWN!"

  def test_intervals(self):
    # Test interval with multiple reads
    intervals = self.adaptor.intervals("chr1", [Interval(1, 30)])
    assert_equal(len(intervals), 7)

    # Test first
    interval1 = intervals[0]
    assert_equal(interval1.start, 0)
    assert_equal(interval1.end, 1)
    assert_equal(len(interval1), 1)
    assert_equal(interval1.value, 2)

    # Test mid interval
    interval2 = intervals[4]
    assert_equal(interval2.start, 7)
    assert_equal(interval2.end, 23)
    assert_equal(len(interval2), 16)
    assert_equal(interval2.value, 7)

    # Test last interval
    interval3 = intervals[-1]
    assert_equal(interval3.start, 25)
    assert_equal(interval3.end, 30)
    assert_equal(len(interval3), 5)
    assert_equal(interval3.value, 7)

    # Test multiple input intervals
    intervals = [Interval(10, 20), Interval(30, 35)]
    intervals = self.adaptor.intervals("chr1", intervals)
    assert_equal(len(intervals), 4)

    # Test first
    interval1 = intervals[0]
    assert_equal(interval1.start, 9)
    assert_equal(interval1.end, 20)
    assert_equal(len(interval1), 11)
    assert_equal(interval1.value, 7)

    # Test mid interval
    interval2 = intervals[2]
    assert_equal(interval2.start, 32)
    assert_equal(interval2.end, 33)
    assert_equal(len(interval2), 1)
    assert_equal(interval2.value, 6)

    # Test last interval
    interval3 = intervals[-1]
    assert_equal(interval3.start, 33)
    assert_equal(interval3.end, 35)
    assert_equal(len(interval3), 2)
    assert_equal(interval3.value, 4)
