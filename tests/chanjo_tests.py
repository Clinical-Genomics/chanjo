from nose.tools import *
from chanjo.chanjo import Analyzer
from chanjo.sqlite import ElementAdaptor
from chanjo.bam import CoverageAdaptor, Interval


class TestClass:
  def __init__(self):
    self.chanjo = Analyzer()

    elem_path = "tests/data/_CCDS.elements.full.db"
    bam_path = "tests/data/align.bam"

    self.chanjo.setAdaptors(CoverageAdaptor(bam_path),
                            ElementAdaptor(elem_path))

    self.genes = ("GIT1", "EGFR", "RHO")

    #setattr(self, "{}s".format(element.lower()), self.dfs[element])

  def setUp(self):
    print "SETUP!"

  def tearDown(self):
    print "TEAR DOWN!"

  def test_coverage(self):
    chrom = "chr1"
    intervals = (Interval(1, 10), Interval(25, 35))
    coverage, completeness = self.chanjo.coverage(chrom, intervals, 5)
    assert_equal(coverage, (53+71)/float(10+11))
    assert_equal(completeness, (8+9)/float(10+11))