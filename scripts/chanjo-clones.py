import threading
import time
import sys
sys.path.append("/Users/robinandeer/SciLife/modules/chanjo2")
from chanjo import chanjo, sqlite, bam
import argparse

class Clone(threading.Thread):
  """docstring for Thread"""
  def __init__(self, covPath, elemPath, genes, cutoff):
    super(Clone, self).__init__()
    self.chanjo = chanjo.Analyzer()
    self.chanjo.setAdapters(bam.CoverageAdapter(covPath),
                            sqlite.ElementAdapter(elemPath))
    self.genes = genes
    self.cutoff = cutoff

  def run(self):
    for gene in self.genes:
      self.chanjo.annotate(gene, self.cutoff, True)

def main(elemPath, covPath, threadCount, cutoff):
  elements = sqlite.ElementAdapter(elemPath)  
  genes = [gene for gene in elements.classes["gene"].get()][8000:10000]

  block = len(genes)/threadCount

  threads = []
  for i in xrange(0, threadCount):
    if i != threadCount - 1:
      # Create new thread
      threads.append(Clone(covPath, elemPath, genes[block*i:block*(i+1)],
                           cutoff))
    else:
      threads.append(Clone(covPath, elemPath, genes[block*i:], cutoff))

  for thread in threads:
    thread.start()
    print "A new thread initiated..."

  # Wait for all threads to complete
  for thread in threads:
    thread.join()

  # Persist calculations
  for gene in genes:
    gene.save()

if __name__ == "__main__":
  desc = ("This is a multithreading Chanjo autopilot for calculating and"
          "persisting coverage.")
  parser = argparse.ArgumentParser(description=desc)

  parser.add_argument("-i", action="store", dest="covPath", type=str,
                      required=True, help="The path to the coverage-file.")
  parser.add_argument("-e", action="store", dest="elemPath", type=str,
                      required=True, help="The path to the elements-file.")

  parser.add_argument("-t", action="store", dest="threadCount", type=int,
                      default=4, help="The number of threads to use.")
  parser.add_argument("-c", action="store", dest="cutoff", type=int,
                      default=50, help="The cutoff to use for completeness.")

  opts = parser.parse_args()

  main(opts.elemPath, opts.covPath, opts.threadCount, opts.cutoff)