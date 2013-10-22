.. Chanjo documentation master file, created by
   sphinx-quickstart on Thu Aug 22 16:36:15 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Chanjo: A sane sequence coverage analysis tool
===============================================
Release |version|. (:ref:`Installation <installation>`)

Chanjo is a sane coverage analysis tool for DNA sequencing. It's written in Python and aims to make it easy to answer clinically relevant questions.

.. code-block:: console

   $ chanjo annotate db.sqlite using test.bam EGFR ALB CD4 BRCA1 --sample "fancy_id"
   $ chanjo peak db.sqlite EGFR
   {
      "EGFR": [
         {
            "sample": "fancy_id",
            "completeness": 1.0,
            "coverage": 227.64
         }
      ]
   }


User's Guide:
----------------
This resource aims to cover everything from getting setup and started, diving into the Python API, forging a deeper understanding of Chanjo, as well as catching up on the latest developments.

.. toctree::
   :maxdepth: 2

   installation
   quickstart
   python-api
   parallel
   adapters
   sql
   design
   development


API reference
--------------

.. toctree::
   :maxdepth: 2

   api
   cli


Wallpapers
-----------
Download the official Chanjo `wallpapers <https://dl.dropboxusercontent.com/u/116686/chanjo-wp.zip>`_!

.. image:: _static/chanjo-wp.001.small.jpg


.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`
