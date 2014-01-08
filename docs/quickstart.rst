..  _quickstart:

Quickstart
============
This guide will get you started with **Chanjo** and teach you about some fundamental design concepts. If you haven't already installed **Chanjo**, head on over to the :ref:`installation` instructions first.


Command line interface (CLI)
-----------------------------
**Chanjo** has slowly morphed into a more dedicated command line utility. Most of the functionality is now easily available to the user without additional Python scripting.

The main use of **Chanjo** is to annotate coverage for genetic elements (genes, transcripts, exons). This can be done for multiple samples and everything is stored in a central SQL database. Let's first set up a new skeleton database.

.. code-block:: console
  
  $ cd ~/projects/proj9
  $ ls
  data list_of_genes.txt bam_files

  Cloning the latest release of the CCDS database
  $ cosmid clone ccds
  This is where the magic happens
  $ chanjo build data/coverage.sqlite using resources/ccds/CCDS.txt

If you instead prefer to use a MySQL database the last command would look something like this:

.. code-block:: console

  $ chanjo build username:password@localhost/coverage using resources/ccds/CCDS.txt --dialect "mysql"

.. note::

  What is this `cosmid`? Well, it's a newly developed genomics resource manager. To learn more, visit the official `Cosmid GitHub page`_.

Now that we have a basic datastore setup we want to annotate it with some coverage metrics. We do this with the ``annotate`` command.

.. code-block:: console

  $ chanjo annotate data/coverage.sqlite using bam_files/person42.bam --sample "person_42"

The above command would go through all CCDS genes in the database we just built and annotate coverage for every genetic element. It should take about an 15-20 min to complete for a normal whole exome sample (WES).

Limiting what genes to "cover"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Unlike other sequence coverage tools (`BEDTools`, `PicardTools`) **Chanjo** can look into only a few specified genes instead of having to pre-process the entire dataset upfront.

To limit the annotations to a subset of genes you can supply the corresponding HGNC symbols as either a list.

.. code-block:: console

  $ chanjo annotate data/coverage.sqlite using bam_files/person42.bam EGFR SMS MOGS DOLK --sample "person_42"

\... or point to a text-file with a list of HGNC symbols using the ``--read`` option.

.. code-block:: console

  $ chanjo annotate data/coverage.sqlite using bam_files/person42.bam --read list_of_genes.txt --sample "person_42"

Peaking at the results
~~~~~~~~~~~~~~~~~~~~~~~
Now that have generated some data, perhaps we'd like to have a quick glance at the results to make sure everything looks good. That's just what the ``peak`` command is intended for. It will simply print a JSON-formatted string of coverage metrics for a given gene.

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

That's it for this short introduction to the basic usage of the **chanjo** command line tool. Sounds promising, right? If you want to integrate **chanjo** into your pipeline you probably need to consider parallelizing the software; :ref:`Parallelizing Chanjo <parallel>` will show how.


Python API
-----------
The CLI is really just a bunch of shortcuts that simplifies and integrates the use of **Chanjo** with other command line utilities. To customize your particular use of **Chanjo** you would probably want to look into the :ref:`python-api`.

.. _Cosmid GitHub page: https://github.com/robinandeer/cosmid
.. _MesaSQLite: http://www.desertsandsoftware.com/wordpress/?page_id=17
.. _SQLite Manager: https://addons.mozilla.org/sv-SE/firefox/addon/sqlite-manager/
