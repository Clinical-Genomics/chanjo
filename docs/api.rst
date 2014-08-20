============
Public API
============
This is the *public* API documentation. The functions and classes
listed below *exclusively* make up the code scope which is guaranteed
to stay consistent across all 2.x releases.


Chanjo utility module
----------------------

.. autofunction:: chanjo.average

.. autoclass:: chanjo.BaseInterval
	:members:

.. autofunction:: chanjo.bed_to_interval

.. autofunction:: chanjo.completeness

.. autofunction:: chanjo.id_generator

.. autofunction:: chanjo.serialize_interval

.. autofunction:: chanjo.split


Chanjo coverage store module
-----------------------------

.. autoclass:: chanjo.Store
	:members:


Submodule pipeline functions
------------------------------

.. autofunction:: chanjo.annotate_bed_stream

.. autofunction:: chanjo.init_db

.. autofunction:: chanjo.ccds_to_bed

.. autofunction:: chanjo.export_intervals

.. autofunction:: chanjo.import_bed_stream

.. autofunction:: chanjo.import_json

.. autofunction:: chanjo.gender_from_bam
