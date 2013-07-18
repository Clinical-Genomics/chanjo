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
    """docstring for CCDS parser"""
    def __init__(self, element_adaptor):
        super(Importer, self).__init__()
        self.path = None

        self.adaptor = element_adaptor

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

                # Only bother with "Public" transcripts
                if row[5] == "Public":

                    # Transcript ID => unique for each row by definition
                    tx_id = row[4]

                    # Generate exon intervals
                    # 1. Split the string based list of exons by comma.
                    # 2-4. See _limits.
                    # 5. Converst to Interval
                    #=> Now we have a list of lists
                    exon_ivals = [self._limits(i) for i in row[9].split(",")]

                    tx_start = exon_ivals[0][0]

                    # =====================
                    #     GENE objects
                    # =====================
                    # Hold on to genes until all transcripts are imported
                    if gene_id != row[2]:
                        gene_id = row[2]
                        # Get an existing gene or `None`
                        existingGene = self.adaptor.get("gene", gene_id)

                        # If we haven't already initiated the gene
                        if not existingGene:
                            chrom = row[0]
                            strand = row[6]
                            # Gene has id, chrom, strand
                            self.adaptor.set("gene", (gene_id, chrom, strand,
                                                      tx_start))
                        else:
                            # Make sure to get the correct gene start position
                            existingGene.start = tx_start
                            existingGene.save()

                    # =====================
                    #     EXON objects
                    # =====================
                    # Add the exon ranges as immutable tuples to the gene
                    for ex_ival in exon_ivals:
                        # Convert to UCSC standard 0-based/1-based positions
                        # CCDS used 0-based, 0-based (pythonic)
                        ex_start = ex_ival[0]
                        ex_end = ex_ival[1] + 1

                        exon_id = "{0}-{1}-{2}".format(chrom, ex_start, ex_end)
                        existingExon = self.adaptor.get("exon", exon_id)
                        if not existingExon:
                            # Create a new exon instance
                            # Add id, chrom, strand, gene parent, start, end
                            existingExon = (exon_id, chrom, strand, gene_id,
                                            ex_start, ex_end)
                            self.adaptor.set("exon", existingExon)
                        
                        # Add the exon transcript combo
                        self.adaptor.set("transcript_exon", (tx_id, exon_id))

                    # ==========================
                    #     TRANSCRIPT objects
                    # ==========================
                    existingTx = self.adaptor.get("transcript", tx_id)
                    if not existingTx:
                        # Transcripts have id, chrom, strand, and parent gene
                        self.adaptor.set("transcript", (tx_id, chrom, strand,
                                                        gene_id))
                    else:
                        print(tx_id)

        self.path = path

    def _limits(self, str_interval):
        """
        ...
        2. Remove brackets and leading spaces.
        3. Split by "-"
        4. Convert each position to int
        """

        positions = str_interval.strip("[ ]").split("-")
        return int(positions[0]), int(positions[1])
