#!/usr/bin/env python
# coding: utf-8
"""
  ccds.module
  ~~~~~~~~~~~~~

  A description which can be long and explain the complete
  functionality of this module even with indented code examples.
  Class/Function however should not be documented here.

  :copyright: year by my name, see AUTHORS for more details
  :license: license_name, see LICENSE for more details
"""

import csv


class Importer(object):
  """docstring for the CCDS parser/importer"""
  def __init__(self, element_adapter):
    super(Importer, self).__init__()

    # Plug in the Element Adapter
    self.adapter = element_adapter

  def open(self, path):
    # Have we bypassed all comment lines?
    commentLine = True
    gene_id = None

    with open(path, "r") as handle:
      # Loop through each row or transcript
      for row in csv.reader(handle, delimiter="\t"):

        # Skip the first comment line
        if commentLine:
          commentLine = False
          continue

        # Only bother with "Public" transcripts not on chr Y
        if row[5] == "Public" and row[0] != "Y":
          # Transcript ID => unique for each row by definition
          tx_id = row[4]
          tx_start = int(row[7])
          chrom = row[0]
          strand = row[6]
          gene_id = row[2]

          # ====================================================================
          #     GENE objects
          # --------------------------------------------------------------------
          # Get an existing gene or `None`
          existingGene = self.adapter.get("gene", gene_id)

          # If we haven't already initiated the gene
          if existingGene is None:
            # Gene has id, chrom, strand
            self.adapter.set("gene", (gene_id, chrom, strand,
                                      tx_start))
          else:
            # Make sure to get the correct gene start position to be able to
            # sort genes
            existingGene.start = tx_start
            existingGene.save()

          # ====================================================================
          #     EXON objects
          # --------------------------------------------------------------------
          # Generate exon intervals
          # 1. Split the string based list of exons by comma.
          # 2-4. See _limits.
          # 5. Converst to Interval
          #=> Now we have a list of lists
          exon_ivals = [self._limits(i) for i in row[9].split(",")]

          # Add the exon ranges as immutable tuples to the gene
          for ex_ival in exon_ivals:
            # Convert to UCSC standard 0-based/1-based positions
            # CCDS used 0-based, 0-based (pythonic)
            ex_start = ex_ival[0]
            ex_end = ex_ival[1] + 1

            exon_id = "{chrom}-{start}-{end}".format(chrom=chrom,
                                                     start=ex_start, end=ex_end)
            existingExon = self.adapter.get("exon", exon_id)
            if existingExon is None:
              # Create a new exon instance
              # Add id, chrom, strand, start, end
              self.adapter.set("exon", (exon_id, chrom, strand, ex_start,
                                        ex_end))

            # Add the transcript-exon combo
            self.adapter.set("transcript_exon", (tx_id, exon_id))

            # Test if the exon has been connected with the current gene
            results = self.adapter.getClass("gene_exon").get(gene_id=gene_id,
                                                             exon_id=exon_id)
            if len(results) != 1:
              # Add the gene-exon combo
              self.adapter.set("gene_exon", (gene_id, exon_id))

          # ====================================================================
          #     TRANSCRIPT objects
          # --------------------------------------------------------------------
          existingTx = self.adapter.get("transcript", tx_id)
          if not existingTx:
            # Transcripts have id, chrom, strand, and parent gene
            self.adapter.set("transcript", (tx_id, chrom, strand, gene_id))
          else:
            print(tx_id)

  def _limits(self, str_interval):
    """
    ...
    2. Remove brackets and leading spaces.
    3. Split by "-"
    4. Convert each position to int
    """

    positions = str_interval.strip("[ ]").split("-")
    return int(positions[0]), int(positions[1])
