from nose.tools import *
from chanjo.bam import CoverageAdaptor
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
    intervals = self.adaptor.intervals("chr1", 1, 30)
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
