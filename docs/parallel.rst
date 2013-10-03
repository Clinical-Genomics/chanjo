..  _parallel:

Parallelizing Chanjo
=====================
Who'd a known, using a SQLite database wasn't always going to be painless? For example, writing to a SQLite database from multiple instances is not as simple as you'd hope unfortunatly. `Chanjo` therefore provides a "--json" flag as part of the command line interface to let you save annotations in a temporary JSON file that can be imported into a SQLite database at a later occasion.

.. code-block:: console

  $ chanjo annotate data/coverage.sqlite using bam_files/person42.bam --json data/person42.coverage.json && \
  > chanjo annotate data/coverage.sqlite using bam_files/person43.bam --json data/person43.coverage.json

Later when both processes have had time to finish we could import coverage annotations into ``data/coverage.sqlite``.

.. code-block:: console

  $ chanjo data/coverage.sqlite import data/person42.coverage.json data/person43.coverage.json

And that is how you allow `Chanjo` to run in parallel.