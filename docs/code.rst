Code walkthrough
=================
This guide will take you through the Python API. It will introduce you to the coding concepts and explain how the different components are strung together to form the different pipelines.

Components
-----------

1. Converter
~~~~~~~~~~~~~
Converts between different input formats using adapters (exposed through setuptools entry points). The end point is the Chanjo BED format and the default adapter is "CCDS".

2. Builder
~~~~~~~~~~~~
Initializes a new Chanjo SQL database with basic genomics elements (intervals, block, and superblocks). Uses the Chanjo BED format but should be able to fall back to using any properly formatted BED file.

-	Should "build" export a BED file on request to enable piping?
	Probably a bad idea since "import" downstream will also write to the database and this could cause unexpected issues.
	Might work if it calls export AFTER building the database! (--tee)
-	Should it have an option to sort the input?
-	Should I commit each element right after I add it to the session?

3. Exporter
~~~~~~~~~~~~~
Leverages an existing Chanjo database and exportes a sorted and properly formatted Chanjo-BED file that is ready to go straight into the "Annotater".

4. Annotator
~~~~~~~~~~~~~
Uses a (Chanjo-)Bed file and calculates coverage and completeness for each of the intervals for a given BAM alignment file. The output is an extended version of the original input file.

5. Importer
~~~~~~~~~~~~~
Accepts the output from the "Annotater" and loads it as a new sample into an existing Chanjo database.

-	Should "import" build a new database unless it already exists?

6. [bonus] Sex Checker
~~~~~~~~~~~~~~~~~~~~~~~
Predicts the sex of a sample given a BAM alignment file (only works for human samples).


.. Generator pipelines with bash-like syntax.
	 Core pipelines
	 Introduce SQL structure
	 Adding colums is pretty cheap (how?)
