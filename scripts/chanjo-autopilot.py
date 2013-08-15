import time
import sys
sys.path.append("/Users/robinandeer/SciLife/modules/chanjo2")
from chanjo import chanjo, sqlite, bam
#import workerpool

def annotateGene(options):
  chanjo.annotate(options[0], options[1], options[2])

start = time.time()
print "Let's get started!"

chanjo = chanjo.Analyzer()
bam_path = "/Users/robinandeer/mountpoint/test_data/10-7053/mosaik/10-7053.110713_AD035EACXX.1_sorted_pmd.bam"
elem_path = "tests/data/CCDS.db"
chanjo.setAdapters(bam.CoverageAdapter(bam_path), sqlite.ElementAdapter(elem_path))

end = time.time()
print "Elapsed time: {nosec} seconds".format(nosec=(end-start))
print "Getting genes..."

genes = [(gene, 20, True) for gene in chanjo.elementAdapter.classes["gene"].get()][6000:8000]

#pool = workerpool.WorkerPool(size=4)

end = time.time()
print "Elapsed time: {nosec} seconds".format(nosec=(end-start))
print "Calculating coverage..."
#pool.map(annotateGene, genes[:100])
bgIntervals = map(annotateGene, genes)

#pool.shutdown()
#pool.join()

end = time.time()
print "Elapsed time: {nosec} seconds".format(nosec=(end-start))
print "Saving genes..."

for gene in genes:
  gene[0].save()

end = time.time()
print "Elapsed time: {nosec} seconds".format(nosec=(end-start))