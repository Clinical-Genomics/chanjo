..  _python-api:

Python API
============
I will introduce the Python API by explaining esentially how to accomplish the same thing as in the :ref:`quickstart` guide.

.. note::

  The API has undergone significant changes since v0.5.0 - so read carefully if you are user of Chanjo v0.4.0 or earlier.

Boilerplate code
-----------------
To include Chanjo in your own project you would pretty much always do:

.. code-block:: python

  from chanjo import sql, bam, utils

  # Paths to a SQLite database and alignment BAM files
  sql_path = "data/coverage.sqlite"
  cov_path = "bam_files/person42.bam"

  # Setup the adapters
  db = sql.ElementAdapter(sql_path, dialect="sqlite")
  bamFile = bam.CoverageAdapter(cov_path)


That's it! You are now ready to start using `Chanjo`.

Building skeleton DB
---------------------
For this we really only need the :class:`CoverageAdapter`, but it works either way. We also need to grab a class from a `Chanjo` dependency: Elemental_. Building on the example setup above:

.. code-block:: python

  from elemental.adapters import ccds

  # Parser for CCDS database dump
  ccds_path = "resources/ccds/CCDS.txt"
  parser = ccds.CCDSAdapter()

  # Parse information into genetic element data
  genes, txs, exons = parser.connect(ccds_path).parse()

  # 1. Setup the new database with tables etc.
  # 2. Import elements into the database by converting to ORM objects
  # 3. Commit all elements added during the session
  db.setup().convert(genes, txs, exons).commit()

Now we have a basic SQLite database with genetic elements, complete with relationships and other useful annotations, all wrapped in a very functional SQLAlchemy ORM.

Getting genes
--------------
Fetching genes (or any element) from the database we just built is simple. Let's get all genes at once.

.. code-block:: python

  genes = db.find("gene")

\... or just a few genes we happen to be interested in:

.. code-block:: python
  
  gene_ids = ["EGFR", "SMS", "MOGS", "DOLK"]
  genes = db.find("gene", query=gene_ids)


Annotating genes
------------------
Really what happens is that we annotate each of the exons belonging to the the genes we are interested in. Extending those annotations will come later.

.. code-block:: python

  # The cutoff is used when calculating completeness
  cutoff = 15
  sample_id = "person_42"
  group_id = 3  # Family 3

  # List all 24 different chromosomes
  chromosomes = utils.chromosome()

  # Lets store all information in a list
  data = []

  # We need to process all exons for each chromosome separately
  for chrom in chromosomes:

    exon = db.get("class", "exon")
    
    # List all exons that we want to annotate with coverage
    # We only need some of the data about each exon
    exons = db.session.query(exon.start, exon.end, exon.id)\
              .filter_by(chrom=chrom).order_by(exon.start).all()

    # Now we can process the exons to get coverage for each
    # Don't worry about the "17000" number now
    data += utils.process(cov, chrom, exons, 0, cutoff, 17000)

That's the basic idea for annotating exons with coverage. Now we just need to store all this information in our SQL database of choice and extend the annotations to include transcripts and genes.

.. code-block:: python

  import itertools

  # Flatten data list
  flat_data = itertools.chain.from_iterable(data)

  ... More to come soon!

.. note::

  This isn't the most efficient way I've presented above. For a more real world implementation you should check out the source code for the `Command line interface`_.


Extending annotations
----------------------
This is a bit of a logical leap but I think it is justified because of the performance benefits. What we want is to extend the exon level annotations in two steps; first to transcripts and then to genes.

.. code-block:: python
  
  # Extend exon annotations to transcripts
  db.add([db.create("transcript_data",
            element_id=tx[0],
            sample_id=sample_id,
            group_id=group_id,
            coverage=tx[1],
            completeness=tx[2]
          ) for tx in db.transcriptStats(sample_id)]).commit()

  # Extend transcript annotations to genes
  db.add([db.create("gene_data",
            element_id=gene[0],
            sample_id=sample_id,
            group_id=group_id,
            coverage=gene[1],
            completeness=gene[2]
          ) for gene in db.geneStats(sample_id)]).commit()

That's about it! We now have all the annotations calculated and saved to the database.


Peaking at annotations
------------------------
This is really the first time that directly interacting with the Python API will prove a great benefit over the command line interface.

Let's take a look at the "SMS" gene:

.. code-block:: python

  >>> gene = db.find("gene", "SMS")

  # Getting all coverage annotations
  >>> gene.data
  [<chanjo.sql.GeneData Object>]

  >>> data = gene.data[0]
  >>> data.coverage
  93.324124719823
  >>> data.completeness
  0.9821242312321
  >>> data.sample_id
  'person_42'

But we can also look at any related elements to the gene.

.. code-block:: python

  >>> exon = gene.exons[1]
  >>> exon.data[0].coverage
  45.902123123121

Interactive exploration
------------------------
What if your genomic region of interest lies outside of the known exome? Glad you should ask! It's perfectly possible to manually "read" coverage in any region of the genome.

.. code-block:: python

  >>> chrom = "1"
  >>> read_depths = bamFile.read(chrom, 1001, 1102)
  >>> coverage, completeness = utils.calculate(read_depths, cutoff=15)

Reading from a BAM file is a bottleneck when running Chanjo. It's therefore a good idea to read across *multiple* intervals (such as all exons in a gene) all at once. The returned numpy array can then be sliced acording to the exon coordinates to calculate coverage for each exon individually.

.. code-block:: python

  >>> gene = db.find("gene", "SMS")
  >>> read_depths = bamFile.read(gene.chrom, gene.start, gene.end)
  >>> exon = gene.exons[0]
  # Extract the read depths for the first exon by slicing the coverage array
  >>> exon_rd = read_depths[(exon.start-gene.start):(exon.end-gene.start)]
  >>> coverage, completeness = calculate(exon_rd, cutoff=15)


.. _Elemental: https://github.com/robinandeer/elemental
.. _Command line interface: https://github.com/robinandeer/chanjo/blob/master/scripts/chanjo
