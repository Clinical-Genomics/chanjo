# -*- coding: utf-8 -*-
"""
chanjo.builder.core
~~~~~~~~~~~~~~~~~~~~

Central pipeline for the Chanjo builder module.
"""
from __future__ import absolute_import
import errno

from path import path
from toolz import pipe, reduce, concat
from toolz.curried import map

from .._compat import text_type
from .consumers import commit_per_contig
from .stages import aggregate, build_block, build_interval, build_superblock
from ..utils import bed_to_interval, split


def init_db(chanjo_db, bed_stream, overwrite=False):
  """Build a new database instance from the Chanjo BED stream.

  Args:
    chanjo_db (Store): initialized Store class instance
    bed_stream (sequence): Chanjo-style BED-stream
    overwrite (bool, optional): whether to automatically overwrite an
      existing database, defaults to False
  """
  # check if the database already exists (expect 'mysql' to exist)
  # 'dialect' is in the form of '<db_type>+<connector>'
  if chanjo_db.dialect == 'mysql' or path(chanjo_db.uri).exists():
    if overwrite:
      # wipe the database clean with a warning
      chanjo_db.tare_down()
    elif chanjo_db.dialect == 'sqlite':
      # prevent from wiping existing database to easily
      raise OSError(errno.EEXIST, chanjo_db.uri)

  # set up new tables
  chanjo_db.set_up()

  superblocks = pipe(
    bed_stream,
    map(text_type.rstrip),
    map(split(sep='\t')),
    map(lambda row: bed_to_interval(*row)),
    map(build_interval(chanjo_db)),
    concat,
    aggregate,
    map(build_block(chanjo_db)),
    aggregate,
    map(build_superblock(chanjo_db))
  )

  # reduce the superblocks and commit every contig
  reduce(commit_per_contig(chanjo_db), superblocks, 'chr0')

  # commit also the last contig
  chanjo_db.save()
