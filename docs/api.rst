============
Public API
============
This is the *public* API documentation. The functions and classes
listed below *exclusively* make up the code scope which is guaranteed
to stay consistent.

If you plan to make use of the Public API it would be a good idea to also check out the `Developer's Guide`_ that coveres some additional implementation details.

Chanjo exclusively uses unicode strings throughout the interface. It therefore important to always specify 'utf-8' encoding when e.g. reading files from the OS. In Python 2:

.. code-block:: python

  >>> import io
  >>> handle = io.open('./LICENSE', encoding='utf-8')
  >>> next(handle)
  u'The MIT License (MIT)\n'


Chanjo coverage store module
-----------------------------
The central API for Chanjo SQL databases. Built on SQLAlchemy. From here you have access to contents of the database (models) and can access query interface that SQLAlchemy exposes.

.. autoclass:: chanjo.store.Store
  :members:


.. _`Developer's Guide`: developer.html
