============
Public API
============
This is the *public* API documentation. The functions and classes
listed below *exclusively* make up the code scope which is guaranteed
to stay consistent across all 2.x releases.

If you plan to make use of the Public API it would be a good idea to also check out the `Developer's Guide`_ that coveres some additional implementation details.

Chanjo exclusively uses unicode strings throughout the interface. It therefore important to always specify 'utf-8' encoding when e.g. reading files from the OS. In Python 2:

.. code-block:: python

  >>> import io
  >>> handle = io.open('./LICENSE', encoding='utf-8')
  >>> next(handle)
  u'The MIT License (MIT)\n'


Submodule pipeline functions
------------------------------
These are the main entry points for each of the exposed subcommands. They make out the different pipelines for processing data from config setup to database import. You also have access to the gender predictor that makes it's guess from a BAM alignment file.

.. autofunction:: chanjo.annotate_bed_stream

.. autofunction:: chanjo.init_db

.. autofunction:: chanjo.ccds_to_bed

.. autofunction:: chanjo.export_intervals

.. autofunction:: chanjo.import_bed

.. autofunction:: chanjo.import_json

.. autofunction:: chanjo.gender_from_bam


Chanjo coverage store module
-----------------------------
The central API for Chanjo SQL databases. Built on SQLAlchemy. From here you have access to contents of the database (models) and can access query interface that SQLAlchemy exposes.

.. autoclass:: chanjo.Store
  :members:


Chanjo utility module
----------------------
Various general utility functions that might also be useful outside Chanjo. They all have in common that they are used throughout multiple modules across Chanjo. If you are building a Chanjo plugin, you are welcome and even encouraged to make use of these functions.

.. autofunction:: chanjo.average

.. autoclass:: chanjo.BaseInterval
  :members:

.. autofunction:: chanjo.bed_to_interval

.. autofunction:: chanjo.completeness

.. autofunction:: chanjo.id_generator

.. autofunction:: chanjo.serialize_interval

.. autofunction:: chanjo.split



.. _`Developer's Guide`: developer.html
