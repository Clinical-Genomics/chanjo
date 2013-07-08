from nose.tools import *
from chanjo.sqlite import ElementAdaptor
import os

class TestClass:
  def __init__(self):
    self.adaptor = ElementAdaptor()

  def setUp(self):
    print "SETUP!"

    path = "tests/data/_CCDS.elements.db"
    self.adaptor.connect(path)

  def tearDown(self):
    print "TEAR DOWN!"

    del self.adaptor

  def test_get(self):
    gene = self.adaptor.get("gene", "GIT1")
    # The correct chromosome
    assert_equal(gene.chrom, "17")
    # The correct number of transcripts
    assert_equal(len(gene.transcripts), 2)
    # The correct number of exons
    assert_equal(len(gene.exons), 21)
    # The correct strand
    assert_equal(gene.strand, "-")

    tx = self.adaptor.get("transcript", "CCDS47587.1")
    # The correct chromosome
    assert_equal(tx.chrom, "7")
    # The correct parent gene_id
    assert_equal(tx.gene.id, "EGFR")
    # The correct number of exons
    assert_equal(len(tx.exons), 10)
    # The correct strand
    assert_equal(tx.strand, "+")

    ex = self.adaptor.get("exon", "19-13051354-13051467")
    # The correct chromosome
    assert_equal(ex.chrom, "19")
    # The correct parent gene_id
    assert_equal(ex.gene.id, "CALR")
    # The correct number of parent transcripts
    assert_equal(len(ex.transcripts), 1)
    # The correct strand
    assert_equal(ex.strand, "+")

