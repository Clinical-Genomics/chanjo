.. Chanjo documentation master file, created by
   sphinx-quickstart on Thu Aug 22 16:36:15 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Chanjo: Clinical sequencing coverage. Evolved.
===============================================
Release |version|.

.. note::

   I promise that the documentation will be a priority for the next release and will be brought up to speed on the latest development.

A sane coverage analysis tool for clinical DNA sequencing.

**Motivation**: `BEDtools` and `PicardTools` are both powerful and universally used in DNA sequencing analysis. However, they were built for doing research, not continuous clinic quality checking. This means that simple tasks like finding out coverage for a gene are obscured behind abstract BED intervals. Chanjo chooses genes over intervals and handles the rest behind the scenes.

Command line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   $ chanjo annotate db.sqlite using test.bam EGFR ALB CD4 BRCA1 --sample "my_fancy_sample_id"
   $ chanjo peak db.sqlite EGFR
   {
      "EGFR": [
         {
            "sample": "my_fancy_sample_id",
            "completeness": 1.0,
            "coverage": 227.64
         }
      ]
   }


Chanjo sets out be part of a new breed of tools aimed at solving problems more or less specific to *clinical* sequencing. Chanjo follows a few general guidelines:

1. Interaction should be as intuative as possible.

2. Coverage analysis can't afford to stop at "average coverage".

.. note::

   Download the official Chanjo `wallpapers <https://dl.dropboxusercontent.com/u/116686/chanjo-wp.zip>`_!

   **Preview**

   .. image:: _static/chanjo-wp.001.small.jpg

This resource will help get :ref:`up and running <installation>`, :ref:`introduce <quickstart>` you to working with Chanjo, provide a :ref:`deeper look <api>` at the guts of Chanjo, :ref:`design philosophies <design>` for those looking for a broader overview, and lastly catch you up on :ref:`development <development>`.

User's Guide:
----------------

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   adapters
   design
   development

API reference
--------------

.. toctree::
   :maxdepth: 2

   api
   cli

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

