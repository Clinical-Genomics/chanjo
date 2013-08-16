from nose.tools import *
from chanjo.ccds2sql import Importer


class TestClass:
  def __init__(self):
    self.importer = Importer(":memory:")

  def setUp(self):
    print "SETUP!"

    self.ccdsLine = ["1", "NC_000001.10", "SAMD11", "148398", "CCDS2.2",
                     "Public", "+", "861321", "879532",
                     "[861321-861392, 865534-865715, 866418-866468, 871151-"
                     "871275, 874419-874508, 874654-874839, 876523-876685, "
                     "877515-877630, 877789-877867, 877938-878437, 878632-"
                     "878756, 879077-879187, 879287-879532]",
                     "Identical"]

    self.exonString = "[861321-861392, 865534-865715, 866418-866468]"

  def tearDown(self):
    print "TEAR DOWN!"

  def test_moveToFirstLine(self):
    commentLines = self.importer._moveToFirstLine()
    assert_true(self.ccdsFile.next()[0] != "#")

  def test_extractLineData(self):
    chrom,
    hgnc,
    txId,
    txStart,
    exons,
    strand = self.importer.extractLineData(self.ccdsLine)

    assert_equal(chrom, "1")
    assert_equal(hgnc, "SAMD11")
    assert_equal(txId, "CCDS2.2")
    assert_equal(txStart, 861321)
    # assert_equal(exons, )
    assert_equal(strand, "+")

  def test_genereateExons(self):
    exons = self.importer._generateExons(self.exonString)

    assert_equal(exons, [(861321, 861392), (865534, 865715), (866418, 866468)])

  def function(self):
    pass
