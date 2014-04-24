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

	$ sort -k1,1 -k2,2n CCDS.txt | chanjo convert | chanjo build CCDS.sqlite
