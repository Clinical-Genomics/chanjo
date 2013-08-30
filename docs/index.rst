.. Chanjo documentation master file, created by
   sphinx-quickstart on Thu Aug 22 16:36:15 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Chanjo: Clinical sequencing coverage. Evolved.
=======================================
Release |version|.

Chanjo is a coverage analysis tool for clinical DNA sequencing.

`BEDtools` and `PicardTools` are both powerful and universally used in DNA sequencing. However, they were built for doing research, not clinic analysis. This means that simple tasks like finding out coverage for a gene are obscrured behind abstract BED intervals.

::

   >>> gene = hub.get("gene", "GIT1")
   >>> hub.annotate(gene)
   >>> gene.coverage  # Average coverage across the gene
   9.2131342342
   >>> gene.completeness  # Percent of bases covered at x read depth
   0.8234234234
   >>> hub.commit()  # Persists annotation(s) to data store

Chanjo sets out be part of a new breed of tools aimed at solving problems more or less specific to *clinical* sequencing. Chanjo follows a few general guidelines:

1. Interaction should be as intuative as possible.

2. Coverage analysis can't afford to stop at "average coverage".

.. note::

   Download the official Chanjo `wallpapers <https://dl.dropboxusercontent.com/u/116686/chanjo-wp.zip>`_!

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

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`

