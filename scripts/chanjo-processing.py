#!/usr/bin/env python
# Simple processing example

import time
import sys
from processing import Process
sys.path.append("/Users/robinandeer/SciLife/modules/chanjo2")
from chanjo import chanjo, sqlite, bam


class Clone(object):
  """docstring for Thread"""
  def __init__(self, covPath, elemPath, genes, cutoff):
    super(Clone, self).__init__()
    self.chanjo = chanjo.Core()
    self.chanjo.setAdapters(bam.CoverageAdapter(covPath),
                            sqlite.ElementAdapter(elemPath))

  def run(self, gene):
    for gene in self.genes:
      self.chanjo.annotate(gene, 10, True)

if __name__ == '__main__':
  start = time.time()
  print "Let's get started!"

  bam_path = "/Users/robinandeer/mountpoint/test_data/10-7053/mosaik/10-7053.110713_AD035EACXX.1_sorted_pmd.bam"
  elem_path = "tests/data/CCDS.db"
  worker = Clone(bam_path, elem_path)

  q = Queue()

  p = Process(target=worker.run, args=[gene])
  p.start()
  p.join()