#!/usr/bin/env python
# coding: utf-8

from nose.tools import *
from chanjo.utils import Interval


class TestInterval:
  def setUp(self):
    print "SETUP!"

    # Single position interval
    self.single_interval = Interval(5)
    # Identical to above
    self.single_interval_alt = Interval(5, 5)

    # Multi position interval
    self.multi_interval = Interval(0, 10)

    # Loo0ong position interval
    self.long_interval = Interval(99, 100002)

  def tearDown(self):
    print "TEAR DOWN!"

    del (self.single_interval, self.single_interval_alt,
         self.multi_interval, self.long_interval)

  def test_len(self):
    assert_equal(len(self.single_interval), 1)
    assert_equal(len(self.multi_interval), 11)
    assert_equal(len(self.long_interval), 99904)

  def test_str(self):
    assert_equal(self.single_interval.__str__(), "(5, 5)")
    assert_equal(self.multi_interval.__str__(), "(0, 10)")
    assert_equal(self.long_interval.__str__(), "(99, 100002)")

  def test_eq(self):
    assert_equal(self.single_interval, self.single_interval_alt)
