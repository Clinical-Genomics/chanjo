#!/usr/bin/env python
# coding: utf-8
"""
  ccds2sql.module
  ~~~~~~~~~~~~~

  A description which can be long and explain the complete
  functionality of this module even with indented code examples.
  Class/Function however should not be documented here.

  :copyright: year by my name, see AUTHORS for more details
  :license: license_name, see LICENSE for more details
"""
import csv
from sql import ElementAdapter

class Importer(object):
  """docstring for Importer"""
  def __init__(self, dbPath, ccdsPath=None):
    super(Importer, self).__init__()
    self.dbPath = dbPath
    self.ccdsPath = ccdsPath

  def reference(self, ccdsPath):
    # Set the path to the CCDS reference file
    self.ccdsPath = ccdsPath

  def populate(self):
    self.reader = csv.reader(open(self.ccdsPath, "r"), delimiter="\t")

    # Continue past the comment line(s)
    row = self._moveToFirstLine()

    while True:
      row = self.reader.next()

  def _moveToFirstLine(self):
    """
    Private: Steps through the file until we are past the comment lines.
    """
    row = ["#"]
    while row[0].startswith("#"):
      row = self.reader.next()

    return row

  def _extractLineData(self):
    pass

  def _generateExons(self):
    pass