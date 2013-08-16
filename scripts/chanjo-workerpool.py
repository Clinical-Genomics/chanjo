from __future__ import print_function
import workerpool
import time
from chanjo import chanjo, sqlite, bam
import argparse


class Clone(workerpool.Job):
  """Job for annotating a set of genes."""
  def __init__(self, covPath, elemPath, genes, cutoff):
    self.chanjo = chanjo.Core()
    self.chanjo.setAdapters(bam.CoverageAdapter(covPath),
                            sqlite.ElementAdapter(elemPath))
    self.genes = genes
    self.cutoff = cutoff

  def run(self):
    for gene in self.genes:
      self.chanjo.annotate(gene, self.cutoff, True)

def chunks(l, n):
  """Yield successive n-sized chunks from l."""
  for i in xrange(0, len(l), n):
    yield l[i:i+n]

def main(elemPath, covPath, threadCount, cutoff):
  # Start a timer to track how long it takes to run the script
  start = time.time()
  print("Starting up...")

  # Set up an instance of an Element Adapter
  elements = sqlite.ElementAdapter(elemPath)

  # Get a number of genes from the source (SQLite database)
  genes = [gene for gene in elements.classes["gene"].get()][10000:12000]

  # Setup a workerpool with the number of threads the user requested
  pool = workerpool.WorkerPool(size=threadCount)

  # Split genes into 10 sets...
  # Generate the same number of gene groups as threads
  geneBlocks = chunks(genes, 200)

  # For each set of genes, setup a job that will annotate them with coverage.
  for geneBlock in geneBlocks:
    job = Clone(covPath, elemPath, geneBlock, cutoff)
    pool.put(job)
    print("New job submitted...")

  # Send shutdown jobs to all threads, wait until the jobs have been completed
  pool.shutdown()
  pool.join()

  # Persist calculations
  for gene in genes:
    gene.save()

  # Print out the time passed
  end = time.time()
  print("Finished in: {nosec} seconds".format(nosec=(end-start)))

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