# -*- coding: utf-8 -*-
"""
chanjo.builder
~~~~~~~~~~~~~~~

Module for initializing a new instance of a Chanjo SQL database.

Accepts a Chanjo-BED stream as input defining intervals and how they
relate to blocks and superblocks. You can think about these as the
eqivalent of exons, transcripts, and genes. It's required that the
input BED stream is sorted by start position and chromosome for the
function to work.

The component build a base SQL database of genomic elements. It also
sets up foreign keys between elements. There's nothing to pipe to a
post-process.

Usage:

.. code-block:: python

  >>> from chanjo import builder
  >>> with open('intervals.sorted.bed', 'r') as stream:
  ...   # use the BED stream to build a new SQLite database
  ...   # overwrite any potentially existing database
  ...   builder.init_db(stream, './coverage.sqlite', overwrite=True)

"""
from __future__ import absolute_import

from .core import init_db
from .consumers import commit_per_contig
from .stages import aggregate, build_block, build_interval, build_superblock
