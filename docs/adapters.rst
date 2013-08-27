..  _adapters:

Adapters
============
Chanjo uses adapters to interface with sources of coverage and elements and relationships between them. This makes it possible to tailor Chanjo to work with your existing pipeline.

Two default adapters are included in the package. Coverage can be read directly from a BAM alignment file. Elements, relationships, and annotations are stored in and accessed from a SQLite database. Your possible choice of `Element Adapter` will therefore determine your output format.

Requirements
------------------
If you know your way around python you totally build your own adapter! However, be certified it needs to follow the following requirements.

Coverage Adapter
^^^^^^^^^^^^^^^^^^^^^
A Coverage Adapter needs to:

1. accept a path as an argument when setting up the adapter::

    from module import CoverageAdapter
    adapter = CoverageAdapter("path/to/source")

2. include a `.read(chrom, start, end)` method that returns an array-like list if depths for *each* position in the interval::

    adapter.read("17", 0, 10)
    #=> [3, 4, 4, 4, 5, 7, 7, 6, 5, 5]

3. treat all interval definitions as 0,0-based in accordance with the rest of the python ecosystem.

Element Adapter
^^^^^^^^^^^^^^^^^^^^^
A Element Adapter needs to:

1. accept a path as an argument when setting up the adapter::

    from module import ElementAdapter
    adapter = ElementAdapter("path/to/source")

2. implement a ``get(elem_class, [elem_ids])`` method that fetches gene, transcript, and exon objects based on the element ID(s). It should be valid to supply a single ID, a list of IDs or nothing. If no IDs are supplied, the method should return all elements matching the element class::

    adapter.get("gene", "GIT1")
    #=> returns a single "gene" object matching the ID; "GIT1".

    adapter.get("gene")
    #=> returns a list of all genes in the database

3. implement a `commit()` method to persist all dirty changes made to element objects::

    # Save all dirty changes at once
    adapter.commit()

4. provide at least a basic `setup()` method that initializes the storage medium by setting up the necessary foundations, e.g. tables in a SQL database.

5. come associated with a script automating the import/setup of elements and relationships from a source file. The default adapter e.g. can import data from a CCDS database text file with one command. It's probably also fine to provide a baseline package for download online.

Further information
--------------------
To find out more details about the default adapters in Chanjo you should read...