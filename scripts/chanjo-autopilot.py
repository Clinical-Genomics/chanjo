#!/usr/bin/env python
# coding: utf-8
"""
Chanjo.
Process all or a subset of exons, get coverage from a BAM alignment and
commit changes to a SQLite database.

Usage:
  chanjo.py <sql_path> <bam_path> [--ccds=<ccds_path>] [--cutoff=<int>] [--read=<path> | --pipe] [-p | --print]
  chanjo.py -h | --help
  chanjo.py --version

Arguments:
  <sql_path>  path to the SQLite database file
  <bam_path>  path to the BAM alignment file

Options:
  -h --help       Show this screen.
  --version       Show version.
  --ccds=<path>   Path to CCDS txt file, initiates creation of new database. 
  --cutoff=<int>  Lowest read depth to pass [default: 50].
  --read=<path>   Path to file with HGNC symbols.
  --pipe          Read piped list of HGNC symbols.
  -p --print      Just print the input variables to the console
"""
from __future__ import print_function
from docopt import docopt
import time
import sys
sys.path.append("/Users/robinandeer/SciLife/modules/chanjo")

import chanjo
from chanjo import core, sql, bam, ccds2sql

def main(args):
  # Start a timer to be able to print out the runtime
  start = time.time()

  # We can set up a brand new database if the user wants to
  if args["--ccds"]:
    # Setup CCDS importer
    imp = ccds2sql.Importer(args["<sql_path>"], args["--ccds"])
    # Populate the new database with elements
    imp.populate()

  # Setup adapters and the main Hub
  cov = bam.CoverageAdapter(args["<bam_path>"])
  db = sql.ElementAdapter(args["<sql_path>"])
  hub = core.Hub(cov, db)

  # Convert cutoff to int
  cutoff = int(args["--cutoff"])

  if args["--pipe"]:
    # Get all genes with matching hgnc symbols from stdin
    genes = [hub.db.get("gene", hgnc) for hgnc in sys.stdin]

  elif args["--read"]:
    # Read HGCN symbols from a file
    with open(args["--read"], "r") as f:
      genes = [hub.db.get("gene", hgnc) for hgnc in f.readlines()]

  else:
    # Get all genes
    genes = hub.db.get("gene")
  
  for gene in genes:
    # Annotate the gene
    hub.annotate(gene, cutoff)

    # Also make the same coverage calculations for transcripts, based on the
    # annotations for the exons
    for tx in gene.transcripts:
      tx.extendAnnotations()

    # Lastly extend annotations to genes
    gene.extendAnnotations()

  # Persist all annotations
  hub.db.commit()

  end = time.time()
  print("Elapsed time: {time} seconds".format(time=(end-start)))

if __name__ == "__main__":
  # Parse arguments based on docstring above
  args = docopt(__doc__, version="Chanjo {v}".format(v=chanjo.__version__))

  # Just print the different inputs
  if args["--print"]:
    print(args)

  else:
    main(args)
