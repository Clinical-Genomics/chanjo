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

  $ chanjo annotate db.sqlite using test.bam EGFR ALB CD4 BRCA1 --sample "fancy_sample_id"
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

Are you more interested in the Python API? Check out the official documentation_.

Introduction
--------------
Verifying adequate read coverage is an `important task`_ to ensure robustness in clinical sequencing. Enabling this in collaboration with clinicians demand new software developed with physicians rather than researchers in mind.

`Alternative tools`_ often hide intuitive genetic concepts such as genes, transcripts, and exons behind more fundamental, less descriptive abstractions. When it comes to the most well defined `genetic elements`_, this can be likened to requiring knowledge of programming to use a computer.

*Chanjo* reads coverage directly from a BAM alignment making it a good fit in most bioinformatic pipelines. A portable yet powerful SQLite database consolidates the output. The ambitions is to create a `standardized API`_ for coverage across the exome.

Completeness (NEW)
~~~~~~~~~~~~~~~~~~~
The *completeness* metric is one concrete new feature you will get for free using Chanjo. It's meant as a complement to average coverage as a measure of the success of coverage.

Completeness works as such. Decide on a cutoff "X" representing the lower limit of adequate coverage (e.g. 10x reads). Completeness is simply the percentage of bases across an element/interval that with coverage >= X.

I believe completeness to be a more useful assessment of coverage success than average coverage for at least many clinical purposes.

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

.. _Alternative tools: http://bedtools.readthedocs.org/en/latest/

.. _genetic elements: http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2704439/

.. _standardized API: http://gemini.readthedocs.org/en/latest/