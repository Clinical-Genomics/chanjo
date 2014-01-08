..  _adapters:

Adapters
==========
*Chanjo* uses adapters to interface with sources of coverage and data storage. The idea has been to create an environment where it would be possible to switch in and out adapters at will. This has during development proven to be a valuable design decision.

.. note::

  However, even if the general principle still stands (separation of concern) I believe the actual need to replace existing adapters will deminish over time.

Two default adapters are included in the package. Using these, coverage will be read directly from a BAM alignment file, and genetic elements + coverage will be stored in a SQL database (SQLite or MySQL are officially supported).

Requirements
------------------
If you know your way around python you could build your own adapter! However, to work well with Chanjo it needs to follow the following requirements.

.. note::

  I advice against attempting to build custom adapters until *Chanjo* approaches its stable 1.0 release.

Coverage Adapter
~~~~~~~~~~~~~~~~~
A :class:`CoverageAdapter` needs to:

1. accept a path as an argument when setting up the class instance:

.. code-block:: python

  from custom_module import CoverageAdapter
  adapter = CoverageAdapter("path/to/source.bam")

2. include a "read"-method that returns a list-like object. The list should include the read depth for *each* position in the interval:

.. code-block:: python

    adapter.read(chrom="17", start=0, end=10)
    #=> [3, 4, 4, 4, 5, 7, 7, 6, 5, 5]

3. treat all interval definitions as 0,0-based in accordance with the rest of the Python ecosystem. This is important as there is no standard convention in the genomics world.

Element Adapter
~~~~~~~~~~~~~~~~~
An :class:`ElementAdapter` needs to:

1. accept a path as an argument when setting up the class instance:

.. code-block:: python

    from custom_module import ElementAdapter
    adapter = ElementAdapter("path/to/source.sqlite")

2. implement a "get"-method that fetches gene, transcript, and exon objects based on the element ID(s). It should be valid to supply a single ID, a list of IDs or nothing. If no IDs are supplied, the method should return all elements matching the element class:

.. code-block:: python

    adapter.get("gene", "GIT1")
    #=> <custom_module.Gene instance at 0x107098e18>

    adapter.get("gene")
    #=> [<custom_module.Gene instance>, <custom_module.Gene instance>, ...]

3. implement a `commit()` method to persist all dirty changes made to element objects:

.. code-block:: python

    # Save all dirty changes at once
    adapter.commit()

4. provide at least a basic `setup()` method that initializes the storage medium by setting up the necessary foundations, e.g. tables in a SQL database.

5. come associated with a script automating the import/setup of elements and relationships from a source file. The default adapter e.g. can import data from a CCDS database text file with one command. It's probably also fine to provide a baseline package for download online.

Further information
--------------------
To find out more details about the default adapters in Chanjo you should read the :ref:`source documentation <api>`.
