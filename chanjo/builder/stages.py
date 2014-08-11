# -*- coding: utf-8 -*-
"""
chanjo.builder.stages
~~~~~~~~~~~~~~~~~~~~~~

Pipeline stages only used by the Chanjo builder.
"""
from toolz import curry

from .._compat import zip, itervalues


def aggregate(interval_payloads):
  """Group elements together based on a given parent id.

  Aggregates elements based on the key (first item in the payload
  tuple). Yields each group at the end of each new contig.

  Args:
    interval_payloads (list of tuple): consist of (key, element)

  Yields:
    list of tuple: where each item consist of (key, element)
  """
  # store created groups
  groups = {}
  # optimize loading (per contig)
  last_contig = None

  for payload in interval_payloads:
    parent_id = payload[0]
    element = payload[1]

    # yield a batch (per contig)
    if last_contig != element.contig:
      for group in itervalues(groups):
        yield group

      # reset
      groups = {}
      last_contig = element.contig

    if parent_id not in groups:
      groups[parent_id] = [payload]

    else:
      groups[parent_id].append(payload)

  # yield also the groups for the last contig
  for group in itervalues(groups):
    yield group


@curry
def build_interval(chanjo_db, interval):
  """Create a new interval and add it to the current session.

  Yields each combination of the new database interval together with
  related block and superblock ids.

  Args:
    chanjo_db (Store): Chanjo store connected to an existing database
    interval (Interval): interval instance

  Yields:
    tuple: block id, new database interval, related superblock id
  """
  # create a brand new interval
  new_interval = chanjo_db.create(
    'interval',
    interval_id=interval.name,
    contig=interval.contig,
    start=interval.start,
    end=interval.end,
    strand=interval.strand
  )

  # add new interval to the current session
  chanjo_db.add(new_interval)

  # yield the new interval for each of the related blocks
  related_ids = zip(interval.block_ids, interval.superblock_ids)
  for block_id, superblock_id in related_ids:
    yield block_id, new_interval, superblock_id


@curry
def build_block(chanjo_db, interval_group):
  """Create a new block and add it to the current session.

  Args:
    chanjo_db (Store): Chanjo store connected to an existing database
    interval_group (list): group of related database intervals

  Returns:
    tuple: superblock id, new database block
  """
  block_id, some_interval, superblock_id = interval_group[0]

  # create a brand new block
  new_block = chanjo_db.create(
    'block',
    block_id=block_id,
    contig=some_interval.contig,
    start=min([payload[1].start for payload in interval_group]),
    end=max([payload[1].end for payload in interval_group]),
    strand=some_interval.strand,
    superblock_id=superblock_id
  )

  # add the new block to the current session
  chanjo_db.add(new_block)

  # relate the intervals to the block
  new_block.intervals = [interval for _, interval, _ in interval_group]

  return superblock_id, new_block


@curry
def build_superblock(chanjo_db, block_group):
  """Create a new superblock and add it to the current session.

  Args:
    chanjo_db (Store): Chanjo store connected to an existing database
    block_group (list): group of related database blocks

  Returns:
    object: new database block
  """
  superblock_id, some_block = block_group[0]

  # create a brand new superblock
  new_superblock = chanjo_db.create(
    'superblock',
    superblock_id=superblock_id,
    contig=some_block.contig,
    start=min([payload[1].start for payload in block_group]),
    end=max([payload[1].end for payload in block_group]),
    strand=some_block.strand
  )

  # add the new superblock to the current session
  chanjo_db.add(new_superblock)

  # relate the blocks to the superblock
  new_superblock.blocks = [block for _, block in block_group]

  return new_superblock
