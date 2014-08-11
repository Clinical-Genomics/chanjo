# -*- coding: utf-8 -*-
"""
chanjo.builder.consumers
~~~~~~~~~~~~~~~~~~~~~~~~~

*Reduce* friendly functions to consume a sequence of items.
"""
from toolz import curry


@curry
def commit_per_contig(chanjo_db, prev_contig, next_superblock):
  """Commit freshly created elements to the database.

  Built up to be used as the reducing function in the Python ``reduce``
  function.

  .. code-block:: python

    >>> reduce(commit_per_contig(chanjo_db), superblocks, 'chr0')

  Args:
    chanjo_db (Store): Chanjo store connected to an existing database
    prev_contig (str): contig id of the previous superblock
    next_superblock (str): contig id of the next/current superblock
  """
  # commit once for every finished contig
  if prev_contig != next_superblock.contig:
    chanjo_db.save()

  return next_superblock.contig
