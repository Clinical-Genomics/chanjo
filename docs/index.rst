.. Chanjo documentation master file, created by
   sphinx-quickstart on Sun Apr 13 18:46:22 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Home
=====
.. raw:: html

	<div class="intro__wrapper">

		<div class="logo center-content">
			<img alt="Chanjo Mascot" src="_static/chanjo-logo.png">
		</div>

		<div class="intro">
			<h1>Chanjo</h1>
			<div class="sub-header">
				Coverage analysis for clinical sequencing
			</div>
		</div>

	</div>


Simple Sambamba integration
-----------------------------
There's a new kid on the BAM processing block: Sambamba_! You can easily load output into a Chanjo database for further coverage exploration:

.. code-block:: console

    $ sambamba depth region -L exons.bed -t 10 -t 20 alignment.bam > exons.coverage.bed
    $ chanjo load exons.coverage.bed
    $ chanjo calculate region 1 861321 871275 --sample ADM980A2
    {"completeness_10": 100, "completeness_20": 87.123, "mean_coverage": 47.24234}

To learn more about Chanjo and how you can use it to gain a better
understanding of sequencing coverage you can do no better than to:

.. raw:: html

	<a href="introduction.html" class="button--big">
		<div class="button__body">Check out the demo</div>
	</a>


Contents
---------

.. toctree::
	:maxdepth: 1

	installation
	introduction
	interface
	api
	developer
	release-notes
	faq


made by
--------

.. raw:: html

	<a href="http://www.robinandeer.com/" class="outro">
		<div class="intro">
			<img class="robinandeer-logo" src="_static/robinandeer-logo.png" />
		</div>
	</a>


.. _Sambamba: http://lomereiter.github.io/sambamba/
