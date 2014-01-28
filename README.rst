.. image:: https://raw.github.com/robinandeer/chanjo2/develop/assets/chanjo-banner.png
  :alt: Chanjo banner

.. image:: https://badge.fury.io/py/chanjo.png
  :target: http://badge.fury.io/py/chanjo
  :alt: PyPI version

.. image:: https://travis-ci.org/robinandeer/chanjo.png?branch=develop
  :target: https://travis-ci.org/robinandeer/chanjo
  :alt: Build Status

.. image:: https://d2weczhvl823v0.cloudfront.net/robinandeer/chanjo/trend.png
  :target: https://bitdeli.com/free
  :alt: Bitdeli Badge

*Chanjo* (Swahili, lit. *vaccine*) is a sane coverage analysis tool focusing on clinical sequencing. It aims to simplify answering clinically relevant questions like: *how well is my gene of interest covered?*.

.. code-block:: console

  $ chanjo annotate db.sqlite using align.bam EGFR ALB CD4 BRCA1 --sample "fancy_sample_id"

  $ chanjo peak db.sqlite EGFR
  {
      "EGFR": [
          {
              "sample": "fancy_sample_id",
              "completeness": 1.0,
              "coverage": 227.64
          }
      ]
  }

Overview
----------
Coverage analysis is the sexiest topic in DNA sequencing. No? Don't agree with me? Well, you're probably right... But that doesn't mean we have to give up on making any progress whatsoever when it comes to analyzing coverage and general quality of sequencing. There. I said it: "BEDTools might *not* be the be-all and end-all of coverage analysis".

*Chanjo* was created to

1. progress coverage analysis by introducing fresh new ideas,
2. simplify abstractions to make result interpretation more intuitive.

There are a couple unique aspects that you will benefit from if using *Chanjo*:

1. Completeness: a novel coverage metric that yields the percent of bases with adequate coverage across a genomic interval e.g. a gene.
2. Simple and intuative interface for querying coverage across genes comparing between samples.

If you are convinced already to give *Chanjo* a try I can want to make a few humble promises:

1. Runtime ~15 min for a single whole genome sample
2. One command installation (pip install chanjo)
3. A fully runable example to get you started without any setup (coming soon)

To go ahead a get started I would advice you to check out the official documentation_.

Installation
-------------
Complete instructions are available in the documentation_ but installation (can be) as simple as running:

.. code-block:: console

  $ pip install chanjo

Background & Motivation
------------------------
Clinical sequencing has had great success prioritizing the protein coding regions of the genome. Verifying adequate read coverage is an `important task`_ to ensure the robustness expected in this application. Because of the limited genomic focus it seems only fitting that coverage (or quality) analysis should provide expansive data in these areas specifically.

Since most known genetic disorders are gene specific, it also makes sense to use genes as a low level abstraction for the basic coverage annotations. Because we have a sort of generally accepted set of human genes (through the CCDS project) *Chanjo* can leverage this to automate a lot of the basic setup.

Further, `alternative tools`_ often hide intuitive genetic concepts such as genes, transcripts, and exons behind more fundamental, less descriptive abstractions. When it comes to the most well defined `genetic elements`_, this can be likened to requiring knowledge of programming to use a computer.

*Chanjo* reads coverage directly from a BAM alignment file, making it a good fit in most bioinformatic pipelines. Output is consolidated in a flexible yet powerful SQL database. The long-term ambition is to create a `standardized API`_ for coverage across the exome.

Future
--------
The closest improvement in time will be an optional configuration file that will help to declutter the command line interface (think ".chanjorc").

I reworked large parts of the API before the 0.5.0 relaese. In doing so, I realized an unnessesary reliance on classes which could equally well be represented by simple, standalone functions. Taking this idea even further, I'd like to explore the possibility of a streaming/pipeable interface. It would hopefully be easier to parallelize and maintain with tests and continous improvements.

I would also be open to add support for Python 3.x now that even Numpy have made the jump.

Contribute
-----------
Test and submit issues. Learn more and point out shortcomings in the extended documentation_. For more details I'll try to keep issues and milestones up-to-date as a source of what needs to be worked on.

Contributors
-------------
Robin Andeer

License
--------
MIT

.. _documentation: https://chanjo.readthedocs.org/en/latest/
.. _important task: http://www.pnas.org/content/106/45/19096.abstract
.. _alternative tools: http://bedtools.readthedocs.org/en/latest/
.. _genetic elements: http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2704439/
.. _standardized API: http://gemini.readthedocs.org/en/latest/
