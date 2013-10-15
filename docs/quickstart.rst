..  _quickstart:

Quickstart
============
This guide will get you started with Chanjo and teach you about the fundamental design concepts. If you haven't already installed Chanjo, head on over to the :ref:`installation` instructions first.


Command line interface (CLI)
-----------------------------
`Chanjo` is built with the intention that most people will interact with it, through the command line interface (CLI). Therefore, most functionality is available to the user this way.

The main use of `Chanjo` is to annotate genetic elements (genes, transcripts, exons) from multiple samples and store everything in a central SQLite database. Let's first set up a new skeleton database.

.. code-block:: console
  
  $ cd /proj9
  $ ls
  data list_of_genes.txt bam_files

  Cloning the latest release of the CCDS database
  $ cosmid clone ccds
  $ chanjo build data/coverage.sqlite using resources/ccds/CCDS.txt

.. note::

  `Cosmid` is a newly developed genomics resource manager. To learn more, visit the official `Cosmid GitHub page`_.

Now that we have a basic datastore we want to annotate it with some coverage metrics. We do this with the ``annotate`` command.

.. code-block:: console

  $ chanjo annotate data/coverage.sqlite using bam_files/person42.bam --sample "person_42"

The above command would go through all genes in the CCDS database and annotate coverage for every genetic element. It should take about an hour to complete.

.. note::

  **TIP** Use the "--verbose" option to print out each succesive gene that is annotated.

Unlike other sequence coverage tools (`BEDTools`, `PicardTools`) `Chanjo` can look into only a few specified genes instead of having to pre-process the entire dataset upfront.

To limit the annotations to a subset of genes you can supply the corresponding HGNC symbols as either a list.

.. code-block:: console

  $ chanjo annotate data/coverage.sqlite using bam_files/person42.bam EGFR SMS MOGS DOLK --sample "person_42"

\... or point to a text-file with a list of HGNC symbols using the ``--read`` option.

.. code-block:: console

  $ chanjo annotate data/coverage.sqlite using bam_files/person42.bam --read list_of_genes.txt --sample "person_42"

Now that have generated some data, perhaps we'd like to have a quick glance at it to make sure everything looks good. That's just what the ``peak`` command is intended for. It will simply print a JSON-formatted string of coverage metrics for a given gene.

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

To look at coverage for other elements and do more interesting things I would recommend you look into a free SQLite database managers like: `SQLite Manager`_ for Firefox or MesaSQLite_ for Mac.

That's it for this short introduction to the basic usage of the `chanjo` command line tool. Sounds promising, right? If you want to integrate `chanjo` into your pipeline you probably need to consider parallelizing the software; :ref:`Parallelizing Chanjo <parallel>` will show how.


Python API
-----------
The CLI is really just a bunch of shortcuts that simplifies and integrates the use of `Chanjo` with other command line utilities. To customize your particular use of `Chanjo` you would probably need to look into the :ref:`python-api`.

.. _Cosmid GitHub page: https://github.com/robinandeer/cosmid
.. _MesaSQLite: http://www.desertsandsoftware.com/wordpress/?page_id=17
.. _SQLite Manager: https://addons.mozilla.org/sv-SE/firefox/addon/sqlite-manager/