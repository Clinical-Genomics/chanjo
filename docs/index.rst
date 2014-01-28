.. Chanjo documentation master file, created by
   sphinx-quickstart on Thu Aug 22 16:36:15 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Chanjo
=======
Release |version|. (:ref:`Installation <installation>`)

**Chanjo** is a sane coverage analysis tool focusing on clinical sequencing. Finding answers to clinically relevant questions (*how well is my favorite gene covered?*) has never been this easy:

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


What's new in |version|?
-------------------------
This version includes a lot of internal restructuring which hopefully will provide significant speed improvements while still moving towards saner/Pythonic code design. The main point is that Chanjo now more intelligently splits up different parts of the exome when annotating coverege.

v0.5.0 also marks the first release with support for a second popular database scheme: MySQL. This is great not only because it increases flexibility but also because MySQL is more of a production ready tool compared to SQLite. More databases could be quite easily added in the future but let's start with the biggest one first.


User's Guide:
----------------
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
   faq


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
