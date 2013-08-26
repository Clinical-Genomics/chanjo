from nose.tools import *
from chanjo.chanjo import Core
from chanjo.sql import ElementAdapter
from chanjo.bam import CoverageAdapter
from chanjo.utils import Interval
import zlib


class TestCore:
  def __init__(self):
    self.chanjo = Core()

    elem_path = ":memory:"
    bam_path = "tests/data/align.bam"

    self.chanjo.connect(CoverageAdapter(bam_path), ElementAdapter(elem_path))

  def setUp(self):
    print "SETUP!"

  def tearDown(self):
    print "TEAR DOWN!"

  def test_calculate(self):
    # Test for normal depths
    depths = [10, 11, 11, 12, 12, 13, 12, 12, 12, 11, 10, 8]
    cutoff = 12
    posCount = float(len(depths))
    fun = lambda x: x >= cutoff

    (cov_s, comp_s, __) = self.chanjo.calculate(depths, cutoff)
    assert_equal(cov_s, sum(depths)/posCount)
    assert_equal(comp_s, len(filter(fun, depths))/posCount)

    # Test with 0 depth positions
    depths = [0, 10, 0, 5, 0]
    cutoff = 8
    posCount = float(len(depths))
    (cov_m, comp_m, __) = self.chanjo.calculate(depths, cutoff)
    assert_equal(cov_m, sum(depths)/posCount)
    assert_equal(comp_m, len(filter(fun, depths))/posCount)

    # Test with all depths = 0, outside reads
    depths = [0, 0, 0, 0, 0, 0]
    (cov_o, comp_o, __) = self.chanjo.calculate(depths)
    assert_equal(cov_o, 0)
    assert_equal(comp_o, 0)

  def test_stringify(self):
    # Test function stringifying and compressing level representations
    depths = [1,2,2,3,5,5,6,7,7,7,7]
    answer = "1|2|2|3|5|5|6|7|7|7|7"
    compressed = self.chanjo.stringify(depths)

    # Decompress the string and compare with the expected answer
    assert_equal(zlib.decompress(compressed), answer)
