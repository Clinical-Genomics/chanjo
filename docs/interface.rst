======================
Interface Walkthrough
======================

Table of Contents
------------------
The page provides an extended look into each of the six subcommands that make up the command line interface of Chanjo. In accordance with UNIX philosophy, they each try to do only one thing really well.

1. chanjo_
2. init_
3. load_
4. link_
5. calculate_
6. db_


.. _chanjo:

chanjo
------
The base command doesn't do anything on it's own. However, there are a few global options accessible at this level. For example, to log debug information to a file called ``./chanjo.log`` use this command:

.. code-block:: console

  $ chanjo -v --log ./chanjo.log [SUBCOMMAND HERE]

This is also where you can define what database to connect to using the ``-d/--database`` option. Chanjo will otherwise use the database defined in the config. To learn more about the global Chanjo options, run ``chanjo --help``.


.. _init:

chanjo init
-----------
Walks you through the setup of a Chanjo config file and optionally initialized a new database. With a config you won't have to worry about missing to specify default options on the command line.

The format of the config is ``.yaml``.

.. code-block:: console

	$ chanjo init

The generated config file will be stored in the current working directory. This is also where Chanjo will automatically look for it. If you want to share a config file between projects it's possible to point to a global file with the ``--config`` option.


.. _load:

chanjo load
--------------
Chanjo takes advantage of the power behind SQL databases by providing a way to store coverage annotations in SQL. You load coverage annotations from ``sambamba depth region`` output. It's possible to pipe directly to this command:

.. code-block:: console

	$ sambamba depth region -L exons.bed alignment.bam | chanjo load

Each line is added independently so it doesn't really matter if the file is sorted.

Most of the information is already stored in the BED output file from Sambamba but to link multiple samples into logical related groups you can future specify a group identifier when calling the load command:

.. code-block:: console

    $ chanjo load --group group1 exons.coverage.bed


.. _link:

chanjo link
--------------
Another main benefit of Chanjo is the ability to get coverage for related genomic elements: exons, transcripts, and genes. The "link" only need to be run ones (at any time) and accepts a similar BED file to "load_".

.. code-block:: console

    $ chanjo link exons.coverage.bed

Each line is added independently so it doesn't really matter if the file is sorted.


.. _calculate:

chanjo calculate
-----------------
This is where the exiting exploration happens! Chanjo exposes a few powerful ways to investigate coverage ones it's been loaded into the databse.

mean
~~~~~
Extract basic coverage stats across all exons for samples.

.. code-block:: console

    $ chanjo calculate mean
    {"complateness_10": 78.93, "mean_coverage": 114.21, "sample_id": "sample1"}
    {"complateness_10": 45.92, "mean_coverage": 78.42, "sample_id": "sample2"}

gene
~~~~~
Extract metrics for particular genes. This requries that the exons have been linked using the "link_" command to the related transcripts and genes. It should be noted that this information is only an approximation since we don't take overlapping exons into consideration.

.. code-block:: console

    $ chanjo calculate gene ADK
    {"ADK": {"complateness_10": 78.93, "mean_coverage": 114.21}, "sample_id": "sample1"}

The calculation is based on simple averages across all exons related to the gene.

region
~~~~~~~
Metrics can also be extracted for a continous interval of exons. This enables some interesting opportunities for exploration. The base command reports average metrics for all included exons across all samples:

.. code-block:: console

    $ chanjo calculate region 1 122544 185545
    {"complateness_10": 50.45, "mean_coverage": 56.12}

We can split this up into each individual exon as well for more detail:

.. code-block:: console

    $ chanjo calculate region 1 122544 185545 --per exon
    {"complateness_10": 10.12, "mean_coverage": 12.00, "exon_id": "exon1"}
    {"complateness_10": 90.76, "mean_coverage": 114.98, "exon_id": "exon2"}

We can of course also filter the results down to individual samples as well:

.. code-block:: console

    $ chanjo calculate region 1 122544 185545 --per exon --sample sample1
    {"complateness_10": 23.56, "mean_coverage": 34.05, "exon_id": "exon1"}
    {"complateness_10": 91.86, "mean_coverage": 157.02, "exon_id": "exon2"}


.. _db:

chanjo db
-----------
Enables you to quickly perform housekeeping tasks on the database.

setup
~~~~~~~~~~~~~~~~
Set up and tear down a Chanjo database.

remove
~~~~~~~~~~~~~~~~~
Remove all traces of a sample from the database.

.. code-block:: console

    $ chanjo db remove sample1



Closing words
--------------
The command line interface is really just a bunch of shortcuts that simplifies the use of Chanjo in a UNIX environment. To customize your particular use of Chanjo you would probably want to look into the `API Reference`_.



.. _API Reference: api.html
