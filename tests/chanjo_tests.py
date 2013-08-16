from nose.tools import *
from chanjo.chanjo import Core
from chanjo.sqlite import ElementAdapter
from chanjo.bam import CoverageAdapter, Interval


class TestClass:
  def __init__(self):
    self.chanjo = Core()

    elem_path = "tests/data/CCDS.db"
    bam_path = "tests/data/align.bam"

    self.chanjo.connect(CoverageAdapter(bam_path), ElementAdapter(elem_path))

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

  def test_calculate(self):
    chrom = "chr1"
    cov_s, comp_s, levels = self.chanjo.calculate(chrom,self.single_intervals,5)
    assert_equal(cov_s, 53/float(10))
    assert_equal(comp_s, 8/float(10))

    cov_m, comp_m, levels = self.chanjo.calculate(chrom, self.multi_intervals, 5)
    assert_equal(cov_m, (32+63)/float(5+10))
    assert_equal(comp_m, (5+8)/float(5+10))

    # Tests interval without reads
    cov_o, comp_o, levels = self.chanjo.calculate(chrom, self.outside_intervals)
    assert_equal(cov_o, 0)
    assert_equal(comp_o, 0)
