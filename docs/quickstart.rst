..  _quickstart:

Quickstart
============
This guide will get you started with Chanjo and teach you about the fundamental design concepts. If you haven't already installed Chanjo, head on over to the :ref:`installation` instructions first.

Command line interface (CLI)
-----------------------------
.. note::

  The original command line tool ``chanjo-autopilot`` is deprecated since version 0.2.0. Please use ``chanjo`` instead.

`Chanjo` is built with the intention that most people will interact with mainly through the command line interface (CLI). This let's you automate data processing and even offers some exploration options.

Chanjo is able to annotate genetic elements (genes, transcripts, exons) from multiple samples and store everything in a central SQLite database. Let's first set up a new skeleton database.

.. code-block:: console
  
  $ cd /proj9
  $ ls
  data list_of_genes.txt bam_files

  Downloading the latest release of the CCDS database
  $ curl ftp://ftp.ncbi.nlm.nih.gov/pub/CCDS/current_human/CCDS.current.txt > data/CCDS.txt
  $ chanjo build data/coverage.sqlite using data/CCDS.txt

Now that we have a datastore we want to annotate it with some coverage metrics. We do this with the `annotate` command.

.. code-block:: console

  $ chanjo annotate data/coverage.sqlite using bam_files/person42.bam --sample "person_42"

This above command would go through all genes in the CCDS database and annotate coverage for every genetic element. That should take about an hour to complete.

.. note::

  **TIP** Use the "--verbose" option to print out each succesive gene that is annotated. Don't worry, it will print everything in place.

To limit the annotation to a subset of genes you can supply the corresponding HGNC symbols as either a list.

.. code-block:: console

  $ chanjo annotate data/coverage.sqlite using bam_files/person42.bam EGFR SMS MOGS DOLK --sample "person_42"

\... or point to a text-file with a list of HGNC symbols using the ``--read`` option.

.. code-block:: console

  $ chanjo annotate data/coverage.sqlite using bam_files/person42.bam --read list_of_genes.txt --sample "person_42"

Now that have generated some data we would like to quickly glance at it. That's just what the ``peak`` command is intended for. It will simpy print a JSON-formatted string of coverage metrics for a given gene.

.. code-block:: console

  $ chanjo peak data/coverage.sqlite SMS
  {
      "SMS": [
          {
              "sample": "person_42",
              "completeness": 0.85,
              "coverage": 14.24
          }
      ]
  }

To look at coverage for other elements and do more interesting inspections I would recommend you look into a free SQLite database managers like: `SQLite Manager <https://addons.mozilla.org/sv-SE/firefox/addon/sqlite-manager/>`_ for Firefox or `MesaSQLite <http://www.desertsandsoftware.com/wordpress/?page_id=17>`_ for Mac.

That's it for this short introduction to the basic usage of the `chanjo` command line tool. If you want to integrate `chanjo` into your pipeline you probably need to consider parallelizing the software; :ref:`Parallelizing Chanjo <parallel>` will show how.

Python API
-----------
The CLI is really just a bunch of shortcuts the simplifies and unifies the use of Chanjo with other command line utilities. To customize your particular usage of `Chanjo` you would probably need to look into the Python API. I will here provide a short introduction to do roughly the same things as above.

Boilerplate code
~~~~~~~~~~~~~~~~~
To include Chanjo in your own project you always do:

.. code-block:: python

    from chanjo.core import Hub
    from chanjo.sql import ElementAdapter
    from chanjo.bam import CoverageAdapter

    # This sets up a new Chanjo instance
    hub = Hub()

    # Paths to the SQLite database and alignment BAM files
    sql_path = "data/coverage.sqlite"
    cov_path = "bam_files/person42.bam"

    # Connect the adapters to your Chanjo instance
    hub.connect(CoverageAdapter(cov_path), ElementAdapter(sql_path))

That's it! You are now ready to start using `Chanjo`.

Interactive exploration
~~~~~~~~~~~~~~~~~~~~~~~~
Unlike other sequence coverage tools (`BEDTools`, `PicardTools`) `Chanjo` can look into only a few specified genes instead having to pre-process the entire dataset upfront.

.. note::

  Check back for more information soon. In the mean time I will refer you to the "chanjo" command line tool `source code <https://github.com/robinandeer/chanjo/blob/master/scripts/chanjo>`_ and specifically the "annotate" and "import\_" functions.

What if your genomic region of interest lies outside of the known exome? Glad you should ask! It's perfectly possible to manually "read" coverage in any region of the genome.

.. code-block:: python

    >>> chrom = "1"
    >>> readDepths = hub.cov.read(chrom, 1001, 1102)
    >>> coverage, completeness, _ = hub.calculate(readDepths, cutoff=15)

.. note::

    Reading from a BAM file is a bottleneck when running Chanjo. It's therefore a good idea to read across *multiple* intervals (such as all exons in a gene) all at one. The returned array can then be sliced acording to the exon coordinates to calculate coverage for each exon individually.

Automation
------------
Many times we are interested in coverage across more than a handful of genes. To automate the process of annotating coverage for all genes at once we would run:

.. note::

  Check back for more information soon. In the mean time I will refer you to the "chanjo" command line tool `source code <https://github.com/robinandeer/chanjo/blob/master/scripts/chanjo>`_ and specifically the "annotate" and "import\_" functions.

.. note::
    To work on a subset of genes, just submit a list of HGNC symbols to ``get()``
