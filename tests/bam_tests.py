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

  def test_coverage(self):
    coverage, completeness = self.adaptor("1")