# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from datetime import datetime

from sqlalchemy import (
  Table, Column, ForeignKey, String, Integer,
  DateTime, Text, Float, Boolean
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# base for declaring a mapping
Base = declarative_base()

# +--------------------------------------------------------------------+
# | Association tables
# | ~~~~~~~~~~~~~~~~~~~
# | Provides the many-to-many relationships between:
# | - Interval<->Block
# +--------------------------------------------------------------------+
Interval_Block = Table('interval__block', Base.metadata,
  Column('interval_id', String(32), ForeignKey('interval.id')),
  Column('block_id', String(32), ForeignKey('block.id'))
)


# +--------------------------------------------------------------------+
# | Superblock ('gene') ORM
# +--------------------------------------------------------------------+
class Superblock(Base):

  """Collection of blocks and potentially overlapping intervals.

  A :class:`Superblock` can be related to multiple blocks and multiple
  intervals.

  Args:
    superblock_id (str): unique superblock id e.g. HGNC gene symbol
    contig (str): contig/chromosome id
    start (int): 1-based start of the superblock (first interval)
    end (int): 1-based end of the superblock (last interval, no UTR)
    strand (str): strand +/-
    secondary_id (str): e.g. Entrez gene id
  """

  __tablename__ = 'superblock'

  id = Column(String(32), primary_key=True)
  secondary_id = Column(String(32))
  contig = Column(String(5))
  start = Column(Integer)
  end = Column(Integer)
  strand = Column(String(1))

  def __init__(self, superblock_id=None, contig=None, start=None,
               end=None, strand=None, secondary_id=None):
    super(Superblock, self).__init__()

    self.id = superblock_id
    self.secondary_id = secondary_id
    self.contig = contig
    self.start = start
    self.end = end
    self.strand = strand


# +--------------------------------------------------------------------+
# | Block ('transcript') ORM
# +--------------------------------------------------------------------+
class Block(Base):

  """Set of non-overlapping intervals.

  A :class:`Block` can *only* be related to a single superset.

  Args:
    block_id (str): unique block id (e.g. CCDS transcript id)
    contig (str): contig/chromosome id
    start (int): 1-based start of the block (first interval)
    end (int): 1-based end of the block (last interval, no UTR)
    strand (str): strand +/-
    superblock_id (str): related superblock id, e.g. HGNC gene symbol
    secondary_id (str, optional): secondard block id
  """

  __tablename__ = 'block'

  id = Column(String(32), primary_key=True)
  secondary_id = Column(String(32))
  contig = Column(String(5))
  start = Column(Integer)
  end = Column(Integer)
  strand = Column(String(1))

  superblock_id = Column(String(32), ForeignKey('superblock.id'))
  superblock = relationship(
    Superblock, backref=backref('blocks', order_by=start))

  def __init__(self, block_id=None, contig=None, start=None, end=None,
               strand=None, superblock_id=None, secondary_id=None):
    super(Block, self).__init__()

    self.id = block_id
    self.contig = contig
    self.start = start
    self.end = end
    self.strand = strand
    self.superblock_id = superblock_id
    self.secondary_id = secondary_id

  def __len__(self):
    """Return the combined number of exon bases.

    Excludes intronic bases.

    Returns:
      int: total 'intervalic' (exonic) length of the block
    """
    base_count = 0
    for interval in self.intervals:
      base_count += len(interval)

    return base_count


# +--------------------------------------------------------------------+
# | Interval ('exon') ORM
# | TODO: rename this class to not be the same as named tuple!!
# +--------------------------------------------------------------------+
class Interval(Base):

  """A continous genetic interval on a given contig (e.g. exon).

  A :class:`Interval` can be related to a multiple :class:`Block`
  (transcripts). Start and end coordinates are 1-based.

  Args:
    interval_id (str): unique interval id
    contig (str): contig/chromosome id
    start (int): 1-based start of the interval
    end (int): 1-based end of the interval
    strand (str): strand +/-
  """

  __tablename__ = 'interval'

  id = Column(String(32), primary_key=True)
  contig = Column(String(5))
  start = Column(Integer)
  end = Column(Integer)
  strand = Column(String(1))
  first = Column(Boolean)
  last = Column(Boolean)

  # defines the ``backref`` to give transcripts an exons property
  blocks = relationship(Block, secondary=Interval_Block,
                        backref=backref('intervals', order_by=start))

  def __init__(self, interval_id, contig, start, end, strand):
    super(Interval, self).__init__()

    self.id = interval_id
    self.contig = contig
    self.start = start
    self.end = end
    self.strand = strand

  def __len__(self):
    """Return the number of bases.

    Returns:
      int: length of interval in number of bases
    """
    # add +1 because both coordinates are 1-based (number of *bases*)
    return (self.end - self.start) + 1


# +--------------------------------------------------------------------+
# | Sample ORM classes
# +--------------------------------------------------------------------+
class Sample(Base):

  """Metadata for a single (unique) sample.

  :class:`Sample` helps out in consolidating important information in
  one place.

  .. versionadded:: 0.4.0

  Args:
    sample_id (str): unique sample id
    group_id (str): unique group id
    cutoff (int): cutoff used for completeness
    extension (bool): number of bases added to each interval
    coverage_source (str): path to the BAM file used
  """

  __tablename__ = 'sample'

  id = Column(String(32), primary_key=True)
  group_id = Column(String(32), index=True)

  cutoff = Column(Integer)
  extension = Column(Integer)
  coverage_source = Column(Text)
  element_source = Column(Text)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

  def __init__(self, sample_id, **kwargs):
    super(Sample, self).__init__()

    self.id = sample_id

    for key, value in kwargs.items():
      setattr(self, key, value)


# +--------------------------------------------------------------------+
# | Interval Data ORM
# +--------------------------------------------------------------------+
class IntervalData(Base):

  """Coverage metrics for a single interval and a given sample.

  :class:`IntervalData` has a many-to-one relationship with it's parent
  interval object through it's ``parent_id`` attribute.

  Args:
    parent_id (int): parent record Interval id
    sample_id (str): unique sample identifier
    group_id (str): group identifier
    coverage (float): average coverage for the exon
    completeness (float): ratio of adequately covered bases
  """

  __tablename__ = 'interval_data'

  id = Column(Integer, primary_key=True, autoincrement=True)
  coverage = Column(Float)
  completeness = Column(Float)

  # These columns map coverage/completeness to sample+group
  sample_id = Column(String(32), ForeignKey('sample.id'))
  sample = relationship(Sample, backref=backref('intervals'))
  group_id = Column(String(32), index=True)

  # Genetic relationship
  parent_id = Column(String(32), ForeignKey('interval.id'))
  parent = relationship(Interval, backref=backref('data'))

  def __init__(self, **kwargs):
    super(IntervalData, self).__init__()

    for key, value in kwargs.items():
      setattr(self, key, value)


# +--------------------------------------------------------------------+
# | Block Data ORM
# +--------------------------------------------------------------------+
class BlockData(Base):

  """Coverage metrics for a single block and a given sample.

  It has a many-to-one relationship with it's parent set object through
  it's ``parent_id`` attribute.

  Args:
    parent_id (int): Set id
    sample_id (str): unique sample identifier
    group_id (str): group identifier
    coverage (float): average coverage for the set
    completeness (float): ratio of adequately covered bases
  """

  __tablename__ = 'block_data'

  id = Column(Integer, primary_key=True, autoincrement=True)
  coverage = Column(Float)
  completeness = Column(Float)

  # These columns map coverage/completeness to an individual+group
  sample_id = Column(String(32), ForeignKey('sample.id'))
  sample = relationship(Sample, backref=backref('blocks'))
  group_id = Column(String(32), index=True)

  # Genetic relationship
  parent_id = Column(String(32), ForeignKey('block.id'))
  parent = relationship(Block, backref=backref('data'))

  def __init__(self, **kwargs):
    super(BlockData, self).__init__()

    for key, value in kwargs.items():
      setattr(self, key, value)


# +--------------------------------------------------------------------+
# | Superset Data ORM classes
# +--------------------------------------------------------------------+
class SuperblockData(Base):

  """Coverage metrics for a single superblock and a given sample.

  It has a many-to-one relationship with it's parent superset object
  through it's ``parent_id`` attribute.

  Args:
    parent_id (int): Superblock id
    sample_id (str): unique sample identifier
    group_id (str): group identifier
    coverage (float): average coverage for the superset
    completeness (float): ratio of adequately covered bases
  """

  __tablename__ = 'superblock_data'

  id = Column(Integer, primary_key=True, autoincrement=True)
  coverage = Column(Float)
  completeness = Column(Float)

  # These columns map coverage/completeness to an individual+group
  sample_id = Column(String(32), ForeignKey('sample.id'))
  sample = relationship(Sample, backref=backref('superblocks'))
  group_id = Column(String(32), index=True)

  # Genetic relationship
  parent_id = Column(String(32), ForeignKey('superblock.id'))
  parent = relationship(Superblock, backref=backref('data'))

  def __init__(self, **kwargs):
    super(SuperblockData, self).__init__()

    for key, value in kwargs.items():
      setattr(self, key, value)
