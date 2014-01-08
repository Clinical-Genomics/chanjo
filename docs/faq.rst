.. _faq:

FAQ
=====

**Why doesn't Chanjo work on my remote server? It complains when trying to import annotations to my SQLite database.**

To get to the point it has to do with the NFS filesystem (Network FileSystem or something). Some more complex SQL queries simply aren't compatible with NFS. So what can you do?

1. Switch to a MySQL database which should work fine.
2. Only process the data to JSON-files with the "--json" flag. Then on a different computer you could import the annotations.

I'm afraid I can't offer any other solutions at this point.

----------

**FAQ: (2006, 'MySQL server has gone away')**

You need to change a setting in the "my.cnf" file. More information `here <http://stackoverflow.com/a/9479681/2310187>`_.

