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

    self.single_intervals = [Interval(0, 10, 20)]
    self.multi_intervals = [Interval(5, 10, 1), Interval(25, 35, 10)]

    # Interval outside reads
    self.outside_intervals = [Interval(60, 70, 20)]

    self.many_intervals = [Interval(10, 20, 0), Interval(20, 35, 1),
                           Interval(40, 45, 35), Interval(45, 60, 5),
                           Interval(70, 75, 9), Interval(75, 85, 10)]

  def tearDown(self):
    print "TEAR DOWN!"

    del self.single_intervals, self.multi_intervals

  def test_coverage(self):
    chrom = "chr1"
    cov_s, comp_s, levels = self.chanjo.coverage(chrom, self.single_intervals,
                                                 5)
    assert_equal(cov_s, 53/float(10))
    assert_equal(comp_s, 8/float(10))

    cov_m, comp_m, levels = self.chanjo.coverage(chrom, self.multi_intervals, 5)
    assert_equal(cov_m, (32+63)/float(5+10))
    assert_equal(comp_m, (5+8)/float(5+10))

    # Tests interval without reads
    cov_o, comp_o, levels = self.chanjo.coverage(chrom, self.outside_intervals)
    assert_equal(cov_o, 0)
    assert_equal(comp_o, 0)

  def test_levels(self):
    # Single interval, ok coverage
    levels_s = self.chanjo.levels(self.single_intervals)
    assert_equal(levels_s, "0-ok")

    # Many intervals
    levels_m = self.chanjo.levels(self.many_intervals)
    assert_equal(levels_m, "10-err,40-ok,45-warn,75-soso")
