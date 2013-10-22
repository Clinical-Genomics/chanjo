#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
import json
import datetime
from nose.tools import *

from chanjo.sql import ElementAdapter
from elemental.adapters.ccds import CCDSAdapter


class TestElementAdapter:
  def __init__(self):
    pass

  def setUp(self):
    # Build a new skeleton database
    self.db = ElementAdapter(":memory:")

    # Parse the provided CCDS database dump
    parser = CCDSAdapter()

    # Parse information from the CCDS txt-file
    genes, txs, exons = parser.connect("tests/data/CCDS.mini.txt").parse()

    # 1. Setup the new database with tables etc.
    # 2. Import elements into the database by converting to ORM objects
    # 3. Commit all elements added during the setup session
    self.db.setup().convert(genes, txs, exons).commit()

    with open("tests/data/sample.json", "r") as handle:
      data = json.load(handle)

      sample_id = data["sample_id"]
      group_id = data["group_id"]
      cutoff = data["cutoff"]
      source = data["source"]
      splice = data["splice"]

    # Import ExonData examples
    self.db.add([self.db.create("exon_data",

              element_id=anno["element_id"],
              coverage=anno["coverage"],
              completeness=anno["completeness"],
              sample_id=sample_id,
              group_id=group_id

            ) for anno in data["annotations"]]).commit()

    self.db.add([self.db.create("transcript_data",
              element_id=tx[0],
              sample_id=sample_id,
              group_id=group_id,
              coverage=tx[1],
              completeness=tx[2]
            ) for tx in self.db.transcriptStats(sample_id)]).commit()

    # Extend annotations to genes
    self.db.add([self.db.create("gene_data",
              element_id=gs[0],
              sample_id=sample_id,
              group_id=group_id,
              coverage=gs[1],
              completeness=gs[2]
            ) for gs in self.db.geneStats(sample_id)]).commit()

    self.db.add(self.db.create("sample",
      sample=sample_id,
      group=group_id,
      cutoff=cutoff,
      source=source,
      splice=splice
    ))

  def test_exons(self):
    exon = self.db.get("exon", "7-55231424-55231514")
    assert_equal(exon.chrom, "7")

    data = exon.data[0]
    assert_equal(data.coverage, 178.37362637363)

  def test_transcripts(self):
    tx = self.db.get("transcript", "CCDS14203.1")
    data = tx.data[0]

    # # CCDS14203.1
    # len1 = [21958989-21958941+1, 21985432-21985312+1, 21990106-21990013+1, 21990687-21990623+1, 21995352-21995177+1, 21996230-21996076+1, 21997082-21996993+1, 22002534-22002420+1, 22003339-22003260+1, 22010828-22010713+1, 22012467-22012428+1]

    # comp1 = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    # cov1 = [2.1020408163265, 25.900826446281, 22.074468085106, 73.907692307692, 150.94886363636, 136.57419354839, 38.155555555556, 154.66086956522, 30.425, 20.98275862069, 134.125]

    # Test averages
    assert_almost_equal(data.coverage, 81.11262488646696)
    assert_almost_equal(data.completeness, 0.9554950045413261)

    tx = self.db.get("transcript", "CCDS59161.1")
    data = tx.data[0]

    # # CCDS59161.1
    # len2 = [21958989-21958941+1, 21985432-21985312+1, 21995352-21995177+1, 21996230-21996076+1, 21997082-21996993+1, 22002534-22002420+1, 22003339-22003260+1, 22010828-22010713+1, 22012467-22012428+1]

    # comp2 = [0, 1, 1, 1, 1, 1, 1, 1, 1]

    # cov2 = [2.1020408163265, 25.900826446281, 150.94886363636, 136.57419354839, 38.155555555556, 154.66086956522, 30.425, 20.98275862069, 134.125]

    # Test averages
    assert_almost_equal(data.coverage, 87.50106157112546)
    assert_almost_equal(data.completeness, 0.9479830148619958)

  def test_genes(self):
    gene = self.db.get("gene", "SMS")
    data = gene.data[0]

    # Test averages
    assert_almost_equal(data.coverage, 84.306843228796211)
    assert_almost_equal(data.completeness, 0.95173900970166092)

  def test_sample(self):
    sample = self.db.get("sample", "99-1-1A")

    assert_equal(len(sample.genes), 4)
    assert_equal(sample.group_id, 99)
    assert_equal(sample.cutoff, 10)
    assert_equal(sample.source, "align.bam")
    assert_equal(sample.splice, False)

    assert_equal(sample.created_at.date(), datetime.date.today())
