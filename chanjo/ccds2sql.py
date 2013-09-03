#!/usr/bin/env python
# coding: utf-8
"""
  chanjo.ccds2sql
  ~~~~~~~~~~~~~

  Official importer module for the SQL :class:`ElementAdapter`. Works off of a
  CCDS database dump and extracts all the nessesary data to build up a complete
  genomic database in SQLite.

  :copyright: (c) 2013 by Robin Andeer
  :license: MIT, see LICENSE for more details
"""
import csv
from sql import ElementAdapter


class Importer(object):
  """
  Setup class that takes a CCDS database file and pushes it through to form the
  basis of a SQLite database. Should take only a few minutes to complete.

  :param str dbPath: Full path to the new database
  :param str ccdsPath: Path to location of the CCDS file (Default: ``None``,
                       optional)
  :param bool debug: Debug info is printed to the console (Def. `False`,
                     optional)
  """
  def __init__(self, dbPath, ccdsPath=None, debug=False):
    super(Importer, self).__init__()
    self.dbPath = dbPath
    self.reference(ccdsPath)

    # This is where the elements are stored before begin persisted
    self.genes = {}
    self.txs = {}
    self.exons = {}

    # Set up the Element Adapter
    self.adapter = ElementAdapter(dbPath, debug=debug)

  def reference(self, ccdsPath):
    """
    Public: Sets the path to the CCDS reference file

    :param str ccdsPath: Path to the CCDS file
    :returns: ``self`` for chainability
    """
    self.ccdsPath = ccdsPath

    return self

  def populate(self):
    """
    Public: Where it all happens. Populates the new database with data from the
    CCDS file.

    I think this is "ACID compliant". It only sets up things if everything
    works. I other words. If you have a working database after running this
    method you can be sure all elements were successfully added to the
    database.
    """
    # Setup the new database
    self.adapter.setup()

    self.reader = csv.reader(open(self.ccdsPath, "r"), delimiter="\t")

    for row in self.reader:

      # Skip some rows that don't contain useful information
      commentLine = row[0].startswith("#")
      unofficial = (row[5] != "Public")
      if commentLine or unofficial:
        continue

      (chrom, hgnc, tx_id, strand, tx_start,
       tx_end, exonCoords) = self._extractLineData(row)

      # Collect all transcript related information
      txKwargs = {
        "tx_id": tx_id,
        "chrom": chrom,
        "start": tx_start,
        "end": tx_end,
        "strand": strand,
        "gene_id": hgnc
      }

      # Check if the gene has already been created
      gene = self.genes.get(hgnc, None)
      if gene is None:
        # Collect all gene related information
        gsKwargs = {
          "hgnc": hgnc,
          "chrom": chrom,
          "start": tx_start,
          "end": tx_end,
          "strand": strand
        }

        gene = self.genes[hgnc] = self.adapter.create("gene", **gsKwargs)

      else:
        # Make sure we assign the correct gene coordinates (most extreme)
        if gene.start > tx_start:
          gene.start = tx_start

        if gene.end < tx_end:
          gene.end = tx_end

      tx = self.txs.get(tx_id, None)
      if tx is None:
        # Create a new transcript object
        tx = self.txs[tx_id] = self.adapter.create("transcript", **txKwargs)
        # Add the parent gene to the transcript
        tx.gene = gene

      # Create new exons
      for coord in exonCoords:
        ex_id = "{chrom}-{start}-{end}".format(chrom=chrom, start=coord[0],
                                               end=coord[1])

        if ex_id in self.exons:
          exon = self.exons[ex_id]

        else:
          # Collect all exon information
          exKwargs = {
            "ex_id": ex_id,
            "chrom": chrom,
            "start": coord[0],
            "end": coord[1],
            "strand": strand
          }
          exon = self.exons[ex_id] = self.adapter.create("exon", **exKwargs)

        # Add the gene and transcript parents to the exon
        if not gene in exon.genes:
          exon.genes.extend([gene])

        if not tx in exon.transcripts:
          exon.transcripts.extend([tx])

    # Add elements to session
    self.adapter.add(self.exons.values())
    self.adapter.add(self.genes.values())
    self.adapter.add(self.txs.values())

    self.adapter.commit()

  def _extractLineData(self, row):
    """
    Private: Extracts the useful information from one CCDS file row.

    :param list row: A list of strings from split row
    :returns: A bunch of strings and ints (see order below)
    """
    # Chrom, HGNC, Transcript ID, strand, Transcript start, end, exon coords
    return (row[0], row[2], row[4], row[6], int(row[7])-1, int(row[8])-1,
            self._generateExonCoordinates(row[9]))

  def _generateExonCoordinates(self, rowData):
    """
    Private: Takes the formatted string of exon coordinates from the CCDS row
    and turns it into a more managable list of lists with int start, end
    coordinates for each exon.

    :param str rowData: A csv string of (start,end) pairs
    :returns: A list of lists with the start, end pairs (int)
    """
    # Remove the "[]"
    csvExons = rowData[1:-1].replace(" ", "")

    # 1. Split first into exons coordinates
    # 2. Split into start, end and parse int
    exons = [[int(pos) for pos in item.split("-")]
             for item in csvExons.split(",")]

    # 3. Correct coords to 0,0-based Pythonic standard
    for exon in exons:
      exon[0] -= 1
      exon[1] -= 1

    return exons
