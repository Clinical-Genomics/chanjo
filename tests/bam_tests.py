from nose.tools import *
from chanjo.bam import CoverageAdaptor, Interval


class CoverageAdaptorClass:
  def __init__(self):
    bam_path = "tests/data/align.bam"
    self.adaptor = CoverageAdaptor(bam_path)

  def setUp(self):
    print "SETUP!"
    # Test interval with multiple reads
    self.mono_intervals = [Interval(0, 30)]
    self.poly_intervals = [Interval(10, 20), Interval(30, 35)]

  def tearDown(self):
    print "TEAR DOWN!"

    del self.mono_intervals, self.poly_intervals

  def test_intervals(self):

    intervals = self.adaptor.intervals("chr1", self.mono_intervals)
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
    intervals = self.adaptor.intervals("chr1", self.poly_intervals)
    assert_equal(len(intervals), 4)

    # Test first
    interval1 = intervals[0]
    assert_equal(interval1.start, 10)
    assert_equal(interval1.end, 20)
    assert_equal(len(interval1), 10)
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
