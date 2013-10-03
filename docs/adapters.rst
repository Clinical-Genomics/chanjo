..  _adapters:

Adapters
============
`Chanjo` uses adapters to interface with sources of coverage and genetic elements + coverage annotations. This makes it at least theoretically possible to tailor `Chanjo` to work with any pipeline. It would for example be possible to persist coverage in a MySQL database or simply in a .txt-file.

Two default adapters are included in the package. Using these, coverage will be read directly from a BAM alignment file, and genetic elements + coverage will be stored in a SQLite database.

Requirements
------------------
If you know your way around python you could build your own adapter! However, to work well with Chanjo it needs to follow the following requirements.

.. note::

  These requirements are not complete and should be seen as merely pointing you in the right direction. They **will** be modified in the future. I would refrain from building your own adapters until I approach a stable 1.0 relase.

Coverage Adapter
^^^^^^^^^^^^^^^^^^^^^
A :class:`CoverageAdapter` needs to:

1. accept a path as an argument when setting up the adapter:

.. code-block:: python

  from module import CoverageAdapter
  adapter = CoverageAdapter("path/to/source")

2. include a `.read(chrom, start, end)` method that returns an array-like list if depths for *each* position in the interval:

.. code-block:: python

    adapter.read("17", 0, 10)
    #=> [3, 4, 4, 4, 5, 7, 7, 6, 5, 5]

3. treat all interval definitions as 0,0-based in accordance with the rest of the python ecosystem.

Element Adapter
^^^^^^^^^^^^^^^^^^^^^
A Element Adapter needs to:

1. accept a path as an argument when setting up the adapter:

.. code-block:: python

    from module import ElementAdapter
    adapter = ElementAdapter("path/to/source")

2. implement a ``get(elem_class, [elem_ids])`` method that fetches gene, transcript, and exon objects based on the element ID(s). It should be valid to supply a single ID, a list of IDs or nothing. If no IDs are supplied, the method should return all elements matching the element class:

.. code-block:: python

    adapter.get("gene", "GIT1")
    #=> returns a single "gene" object matching the ID; "GIT1".

    adapter.get("gene")
    #=> returns a list of all genes in the database

3. implement a `commit()` method to persist all dirty changes made to element objects:

.. code-block:: python

    # Save all dirty changes at once
    adapter.commit()

4. provide at least a basic `setup()` method that initializes the storage medium by setting up the necessary foundations, e.g. tables in a SQL database.

5. come associated with a script automating the import/setup of elements and relationships from a source file. The default adapter e.g. can import data from a CCDS database text file with one command. It's probably also fine to provide a baseline package for download online.

Further information
--------------------
To find out more details about the default adapters in Chanjo you should read the :ref:`source documentation <api>`.