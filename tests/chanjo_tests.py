from nose.tools import *
from chanjo.chanjo import Analyzer
from chanjo.sqlite import ElementAdaptor
from chanjo.bam import CoverageAdaptor


class TestClass:
  def __init__(self):
    self.chanjo = Analyzer()

    elem_path = "tests/data/_CCDS.elements.full.db"
    bam_path = "tests/data/align.bam"

    self.chanjo.setAdaptors(CoverageAdaptor(bam_path), ElementAdaptor())
    self.chanjo.importElements(elem_path)

    self.genes = ("GIT1", "EGFR", "RHO")

    #setattr(self, "{}s".format(element.lower()), self.dfs[element])

  def setUp(self):
    print "SETUP!"

  def tearDown(self):
    print "TEAR DOWN!"

  def test_elementCoverage(self):
    genes = [self.chanjo.elementCoverage("gene", gene_id, 10) for gene_id in self.genes]

    assert_equal(self.test.path, "tests/data/CCDS.current.txt")
