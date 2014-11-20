======================
Interface Walkthrough
======================

Table of Contents
------------------
The page provides an extended look into each of the six subcommands that make up the command line interface of Chanjo. In accordance with UNIX philosophy, they each try to do only one thing really well.

1. chanjo_
2. init_
3. convert_
4. build_
5. export_
6. annotate_
7. import_
8. `sex checker`_


.. _chanjo:

chanjo
------
The base command which doesn't do anything on it's own. However, there are a few global options accessible at this level. For example, to log debug information (and anything more important) to a file called ``./chanjo.log`` use this command:

.. code-block:: console

  $ chanjo -vvv --log ./chanjo.log [SUBCOMMAND HERE]

To learn more about the global Chanjo options, run ``chanjo --help``.


.. _init:

chanjo init
-----------
This command doesn't actually do any computations but rather walks you through the setup of a Chanjo config file. With this in place you won't have to worry about missing to specify default options on the command line. You could for example set which type of SQL database to use or which institute you belong to.

The format of the config is ``.toml``.

.. code-block:: console

	$ chanjo init

The generated config file will be stored in the current working directory. This is also where Chanjo will automatically look for it. If you want to share a config file between projects it's possible to point to a global file with the ``--config`` option.


.. _convert:

chanjo convert
---------------
Convert between different input formats using adapters (exposed through setuptools entry points, installed via pip). The output is always a valid Chanjo BED stream. The default adapter is "ccds".

With the default adapter, we can convert a CCDS database dump to Chanjo's extended BED definitions of exonic intervals. It's important to remember that the convert command expects a sorted file based on both contig/chromosome and start position.

.. code-block:: console

	$ sort -k1,1 -k2,2n CCDS.txt | chanjo convert > CCDS.intervals.bed

The converted BED-file contains one exon interval per line plus some additional meta data in the columns 4-7. You can read more about the specific requirements at UCSC_.

.. code-block:: console

	$ cat CCDS.intervals.bed
	#contig	start	end	interval_id	strand	block_ids	superblock_ids
	22	32586758	32587338	22-32586758-32587338	-	CCDS54521.1,CCDS46694.1	RFPL2,RFPL2
	22	32588888	32589173	22-32588888-32589173	-	CCDS54521.1	RFPL2
	22	32588888	32589260	22-32588888-32589260	-	CCDS46694.1	RFPL2
	X	54951423	54951500	X-54951423-54951500	+	X-CCDS59529.1	X-TRO
	X	54952024	54952115	X-54952024-54952115	+	X-CCDS59529.1	X-TRO

Beyond the first 5 columns, Chanjo recognizes an additional two custom and optional columns.

Column 6 contains transcript Ids or more generally "block" Ids. This gives the user a way to group multiple intervals into blocks. These blocks are assumed to contain only **non-overlapping** intervals. It's OK for one interval to belong to multiple blocks.

Column 7 contains gene Ids or more generally "superblock" Ids. They offer a way to group *blocks*. A single *block* should only belong to one single *superblock*.

**Runtime**: seconds (50Mb input)


.. _build:

chanjo build
--------------
Chanjo takes advantage of the power behind SQL databases by providing a way to store coverage annotations in SQL. It all starts with initializing a new database with the interval, block, and superblock definitions generated from ``chanjo convert``.

.. code-block:: console

	$ chanjo build CCDS.coverage.sqlite3 CCDS.intervals.bed

As shown below, it's very important to sort the BED-formatted input file before running ``chanjo build``. The input stream should be sorted on:

1. chromosome/contid id - whatever orders works as long as all intervals from on each contig is grouped together.
2. start position - the order should be **decending**

It's worth noting that setting up a database with the *build* subcommand only needs to be done once. After the basic structure is in place, you can add how ever many samples you want to the database.

**Runtime**: ~5 min (<200Mb)


.. _export:

chanjo export
--------------
This is a convenience command to export a BED stream of all intervals as defined in an existing SQL database. The resulting stream can be directly piped to ``chanjo annotate``.

.. code-block:: console

	$ chanjo export CCDS.coverage.sqlite3 > CCDS.intervals.min.bed

Exporting intervals from a database can be handy since you only need to store the definitions in *one* place (the database). Otherwise it can be easy to forget which original BED-file was initially used.

**Runtime**: seconds (~200 Mb)

.. note::
	The *export* subcommand only generates the minimum BED-file to use with ``chanjo annotate``. Piping it to ``chanjo build`` would **not** setup an identical "twin" database.


.. _annotate:

chanjo annotate
-----------------
The "annotate" subcommand takes a *regular* (or extended) BED-file with interval definitions and annotates it with coverage and completeness metrics.

.. code-block:: console

	$ chanjo annotate alignment.bam CCDS.intervals.min.bed > CCDS.intervals.coverage.bed

The output is again in the BED-format but with the added coverage and completeness columns for each interval to the end of each line.

.. note::
	Out of ideas for good sample ids? Chanjo can automatically generate random yet memorable strings like "bolitimo", "tetesolu", "mivetote", "bidigugi", or perhaps "dobopeto".

There are a lot of options to customize this command.

.. csv-table::
   :header: "Option", "Description"
   :widths: 10, 50
   :file: annotate-options.csv
   :delim: ;

You now have the choice to roll your own downstream data analysis or import the annotations into a SQL database.

**Runtime**: <10 min (~40 Mb)


.. _import:

chanjo import
--------------
If you decide to move on from the text-based output from ``chanjo annotate`` and have a SQL database set up, the *import* subcommand is the endpoint for the overall Chanjo pipeline.

Simply speaking, "import" will take the output from ``chanjo annotate`` and import the annotations to a SQL database. It will then take the coverage metrics on the interval level and extend them to both block and superblock levels.

.. code-block:: console

	$ chanjo annotate alignment.bam CCDS.intervals.min.bed [...] \
	> | chanjo import CCDS.coverage.sqlite3

**Runtime**: ~1 min (<800 Mb)

.. note::
	If you have old coverage annotation files in the legacy JSON format, you can still import them into the new SQL structure by adding the ``--json`` flag.


.. _sex checker:

sex-check [bonus]
-------------------
Along with chanjo, a bonus command line utility is installed that can predict the sex of a sample given a BAM alignment file. The very basic script uses the "depth reader" from Chanjo to read and compare coverage across regions of the X and Y chromosomes. The "algorithm" is very naive but should still be very robust in determining the gender of a properly aligned BAM-file.

.. code-block:: console

  $ sex-check alignment.bam
  #X_coverage Y_coverage  sex
  0.898022446555  0.322524716855  male

**Runtime**: seconds (any size)

.. note::
  ``sex-check`` works for human samples only!


Closing words
--------------
The command line interface is really just a bunch of shortcuts that simplifies the use of Chanjo in a UNIX environment. To customize your particular use of Chanjo you would probably want to look into the `API Reference`_.



.. _UCSC: http://genome.ucsc.edu/FAQ/FAQformat.html#format1
.. _API Reference: api.html
