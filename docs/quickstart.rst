Quickstart
================
This guide will get you started with Chanjo and teach you about the fundamental design concepts. If you haven't already installed Chanjo, head on over to the :ref:`installation` instructions.

Boilerplate code
------------------
To include Chanjo in your own python project you would first::

    from chanjo.chanjo import Core
    from chanjo.sql import ElementAdapter
    from chanjo.bam import CoverageAdapter

    # This sets up a new Chanjo instance
    hub = Core()

    # Paths to the SQLite database and alignment BAM files
    elem_path = "path/to/sqlite.db"
    cov_path = "/path/to/alignment.bam/"

    # Connect the adapters to your Chanjo instance
    hub.connect(CoverageAdapter(cov_path), ElementAdapter(elem_path))

That's it! You are now ready to start using Chanjo.

Interactive exploration
------------------------
Unlike other sequence coverage tools like `BEDTools` and `PicardTools` Chanjo works well if you just want to look into a few specified genes without processing the entire dataset::

    # Genes are referenced by HGNC symbol
    gene = hub.get("gene", "GIT1")

    # Now we first need to annotate the gene with coverage statistics
    hub.annotate(gene, cutoff=20)

    # We can access coverage and completeness across the gene
    gene.coverage
    #=> 9.782388431
    gene.completeness
    #=> 0.34551213

    # To persist calculations so you don't have to annotate every time
    hub.commit()

Automation
------------------------
Many times we are interested in coverage across more than a handful of genes. To automate the process of annotating coverage for all gene at once we would run::

    # Get all genes (don't supply HGNC)
    genes = hub.get("gene")

    # Loop over each gene
    for gene in genes:
        hub.annotate(gene, 20)

    # Don't forget to save annotations to the database
    hub.commit()

.. note::
    To work on a subset of genes, just submit a list of HGNC symbols

Command line interface (CLI)
-----------------------------
If you just want to stick to the standards and plug in Chanjo in your existing pipeline you can use the included `chanjo-autopilot.py` script. Coming soon.