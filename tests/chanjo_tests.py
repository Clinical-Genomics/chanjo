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

    #setattr(self, "{}s".format(element.lower()), self.dfs[element])

  def setUp(self):
    print "SETUP!"

    self.single_intervals = [Interval(0, 10)]
    self.multi_intervals = [Interval(5, 10), Interval(25, 35)]

  def tearDown(self):
    print "TEAR DOWN!"

    del self.single_intervals, self.multi_intervals

  def test_coverage(self):
    chrom = "chr1"
    cov_s, comp_s = self.chanjo.coverage(chrom, self.single_intervals, 5)
    assert_equal(cov_s, 53/float(10))
    assert_equal(comp_s, 8/float(10))

    cov_m, comp_m = self.chanjo.coverage(chrom, self.multi_intervals, 5)
    assert_equal(cov_m, (32+53)/float(5+10))
    assert_equal(comp_m, (5+9)/float(5+10))