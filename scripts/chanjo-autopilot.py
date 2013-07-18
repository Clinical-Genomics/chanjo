import time
from chanjo import chanjo, sqlite, bam
#import workerpool

def annotateGene(options):
  chanjo.annotate(options[0], options[1], options[2])

start = time.time()
print "Let's get started!"

chanjo = chanjo.Analyzer()
bam_path = "/Users/robinandeer/mountpoint/test_data/10-7053/mosaik/10-7053.110713_AD035EACXX.1_sorted_pmd.bam"
elem_path = "tests/data/_CCDS.elements.levels.db"
chanjo.setAdaptors(bam.CoverageAdaptor(bam_path), sqlite.ElementAdaptor(elem_path))

end = time.time()
print "Elapsed time: {nosec} seconds".format(nosec=(end-start))
print "Getting genes..."

genes = [(gene, 15, True) for gene in chanjo.elementAdaptor.classes["gene"].get()]

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