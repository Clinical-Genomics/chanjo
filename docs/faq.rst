====
FAQ
====


Why doesn’t Chanjo work on my remote server?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Chanjo complains when trying to import annotations to my SQLite database.

To get to the point it has to do with the NFS filesystem (Network FileSystem or something). Some more complex SQL queries simply aren’t compatible with NFS. So what can you do?

1. Switch to a MySQL database which should work fine.
2. Only process the data to JSON-files with the “–json” flag. Then on a different computer you could import the annotations.

I’m afraid I can’t offer any other solutions at this point.


Error: (2006, ‘MySQL server has gone away’)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You need to change a setting in the “my.cnf” file. More information here.

- Known limitations
- Parallelization (postpone import) -> Usage examples
- NFS file systems -> Usage examples
- Troubleshooting


Why is the build command failing?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It's important to remember that both the "convert" and "build" commands expect the input to be sorted on both the first and second columns. Forgetting to do this can lead to failed grouping of intervals which in turn leads to the failed import.

Therefore, solving the issue might be as simple as:

.. code-block:: console

  $ sort -k1,1 -k2,2n CCDS.txt | chanjo convert | chanjo build CCDS.sqlite3


I can't overwrite exising files using Chanjo!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
As of the 2.0 release, Chanjo now completely relies on UNIX style output redirection for writing to files. You might, *wisely*, be using ``set -o noclobber`` in your .bashrc. This raises an error in UNIX if you try to overwrite existing files by output redirection.

The way to force overwrite is by using a `special syntax`_:

.. code-block:: console

  $ echo two >| afile
  $ cat afile
  two


How does Chanjo handle genes in `pseudoautosomal regions`_ (X+Y)?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A few genes are present on both sex chromosomes (X+Y). Becuase the chromosomes are treated as separate entities, Chanjo also treat these genes as separate entities. To keep them separated in the SQL database, the default "ccds" converter adapter will prefix their names by "X-" and "Y-" respectively.

.. note::
  It's imporant that all `converter adapters`_ find some consistent way of handling elements in these tricky regions.



.. _pseudoautosomal regions: http://en.wikipedia.org/wiki/Pseudoautosomal_region
.. _converter adapters: developer.html#converter-adapters
.. _special syntax: http://askubuntu.com/questions/236478/how-do-i-make-bash-warn-me-when-overwriting-an-existing-file
