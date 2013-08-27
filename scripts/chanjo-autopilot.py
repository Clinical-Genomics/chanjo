#!/usr/bin/env python
# coding: utf-8
"""
Usage: chanjo-autopilot.py <bam_path> <sql_path> [--cutoff=<kn>]
       chanjo-autopilot.py new <bam_path> <sql_path> <ccds_path> [--cutoff=<kn>]
       chanjo-autopilot.py -h | --help
       chanjo-autopilot.py --version

Process all exons in the SQLite database, get coverage from BAM alignment and
commit changes to SQLite again.

Arguments:
  <bam_path> path to the BAM alignment file
  <sql_path> path to the SQLite database file
  <ccds_path> path to the CCDS database dump

Options:
  -h --help   Show this screen.
  --version   Show version.
"""
from docopt import docopt
import time
import sys
sys.path.append("/Users/robinandeer/SciLife/modules/chanjo2")

from chanjo import core, sql, bam, ccds2sql

def main(args):
  start = time.time()

  # We can set up a brand new database
  if args["new"]:
    imp = ccds2sql.Importer(args["<sql_path>"], args["<ccds_path>"])
    imp.populate()

  cov = bam.CoverageAdapter(args["<bam_path>"])
  db = sql.ElementAdapter(args["<sql_path>"])
  hub = core.Hub(cov, db)

  genes = hub.db.get("gene")
  for gene in genes:
    # Annotate the gene
    hub.annotate(gene, args["--cutoff"])

  # Persist all annotations
  hub.db.commit()

  end = time.time()
  print "Elapsed time: {nosec} seconds".format(nosec=(end-start))

if __name__ == '__main__':
  # parse arguments based on docstring above
  arguments = docopt(__doc__, version='Chanjo 0.0.1')

  main(arguments)
