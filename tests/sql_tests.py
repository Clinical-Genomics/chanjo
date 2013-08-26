#!/usr/bin/env python
# coding: utf-8

from nose.tools import *
from chanjo.sql import ElementAdapter


class TestCoverageAdapter:
  adapter = ElementAdapter(":memory:")

  def __init__(self):
    pass

  def setUp(self):
    print "SETUP!"
    # Set up all tables
    self.adapter.setup()
    # Create a single gene object, add and commit to database
    gene = self.adapter.create("gene", hgnc="GIT1", chrom="17", start=12345,
                               end=14641, strand="+")
    self.adapter.add(gene)
    self.adapter.commit()

  def tearDown(self):
    print "TEAR DOWN!"

  def test_get(self):
    gene = self.adapter.get("gene", "GIT1")
    assert_equal(gene.chrom, "17")
