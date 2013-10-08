#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
from nose.tools import *
from chanjo.sql import ElementAdapter


class TestCoverageAdapter:
  adapter = ElementAdapter(":memory:")

  def __init__(self):
    pass

  def setUp(self):
    print("SETUP!")

  def tearDown(self):
    print("TEAR DOWN!")
