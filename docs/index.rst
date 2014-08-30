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


Simple & intuitive analysis pipeline
--------------------------------------

.. code-block:: console

	$ cat intervals.bed | chanjo annotate alignment.bam
	#{"sample_id": "bavewira", ...}
	1	10	15	interval-1	9.922	0.97231
	2	45	55	interval-2	14.231	1.0

Chanjo adds two columns to each row describing **average coverage** and
how many percent of bases that are covered at 10x reads;
**completeness**.

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
	code
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
