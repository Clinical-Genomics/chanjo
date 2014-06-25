# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Table, Column, ForeignKey, String, Integer, \
  DateTime, Text, Float, Boolean, UniqueConstraint, ForeignKeyConstraint, \
  PrimaryKeyConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# Base for declaring a mapping
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
  """The :class:`Superblock` represents a collection of blocks and potentially
  overlapping intervals. It can be related to multiple blocks and multiple
  intervals.

  Args:
    superblock_id (str): Unique superblock Id e.g. HGNC gene symbol
    contig (str): Contig/Chromosome Id
    start (int): 1-based start of the superblock (first interval)
    end (int): 1-based end of the superblock (last interval, no UTR)
    strand (str): Strand +/-
    secondary_id (str): E.g. Entrez gene Id
  """
  __tablename__ = 'superblock'

  id = Column(String(32), primary_key=True)
  secondary_id = Column(String(32))
  contig_id = Column(String(5))
  start = Column(Integer)
  end = Column(Integer)
  strand = Column(String(1))

  def __init__(self, superblock_id=None, contig_id=None, start=None,
               end=None, strand=None, secondary_id=None):
    super(Superblock, self).__init__()

    self.id = superblock_id
    self.secondary_id = secondary_id
    self.contig_id = contig_id
    self.start = start
    self.end = end
    self.strand = strand


# +--------------------------------------------------------------------+
# | Block ('transcript') ORM
# +--------------------------------------------------------------------+
class Block(Base):
  """The :class:`Block` represents a set of non-overlapping intervals. It can
  *only* be related to a single superset.

  Args:
    block_id (str): Unique block Id (e.g. CCDS transcript Id)
    contig_id (str): Contig/Chromosome Id
    start (int): 1-based start of the block (first interval)
    end (int): 1-based end of the block (last interval, no UTR)
    strand (str): Strand +/-
    superblock_id (str): Related superblock Id, e.g. HGNC gene symbol
    secondary_id (str): Optional secondard block Id
  """
  __tablename__ = 'block'

  id = Column(String(32), primary_key=True)
  secondary_id = Column(String(32))
  contig_id = Column(String(5))
  start = Column(Integer)
  end = Column(Integer)
  strand = Column(String(1))

  superblock_id = Column(String(32), ForeignKey('superblock.id'))
  superblock = relationship(
    Superblock, backref=backref('blocks', order_by=start))

  def __init__(self, block_id=None, contig_id=None, start=None, end=None,
               strand=None, superblock_id=None, secondary_id=None):
    super(Block, self).__init__()

    self.id = block_id
    self.contig_id = contig_id
    self.start = start
    self.end = end
    self.strand = strand
    self.superblock_id = superblock_id
    self.secondary_id = secondary_id

  def __len__(self):
    """Returns the combined number of exon bases. Excludes intronic bases.

    Returns:
      int: Total 'intervalic' (exonic) length of the block
    """
    base_count = 0
    for interval in self.intervals:
      base_count += len(interval)

    return base_count


# +--------------------------------------------------------------------+
# | Interval ('exon') ORM
# +--------------------------------------------------------------------+
class Interval(Base):
  """The :class:`Interval` represents a continous genetic interval on a given
  contig (e.g. exon).

  It can be related to a multiple :class:`Block` (transcripts). Start and end
  coordinates are 1-based.

  Args:
    interval_id (str): Unique interval Id
    contig_id (str): Contig/Chromosome Id
    start (int): 1-based start of the interval
    end (int): 1-based end of the interval
    strand (str): Strand +/-
  """
  __tablename__ = 'interval'

  id = Column(String(32), primary_key=True)
  contig_id = Column(String(5))
  start = Column(Integer)
  end = Column(Integer)
  strand = Column(String(1))
  first = Column(Boolean)
  last = Column(Boolean)

  # This also defines the ``backref`` to give transcripts an exons property
  blocks = relationship(Block, secondary=Interval_Block,
                        backref=backref('intervals', order_by=start))

  def __init__(self, interval_id, contig_id, start, end, strand):
    super(Interval, self).__init__()

    self.id = interval_id
    self.contig_id = contig_id
    self.start = start
    self.end = end
    self.strand = strand

  def __len__(self):
    """<magic> Returns the number of bases.

    Returns:
      int: Length of interval in number of bases
    """
    # We add +1 because we count positions and both coordinates are 1-based
    return (self.end - self.start) + 1


# +--------------------------------------------------------------------+
# | Sample ORM classes
# +--------------------------------------------------------------------+
class Sample(Base):
  """Stores metadata about each sample. This helps out in consolidating
  important information in one place.

  .. versionadded:: 0.4.0

  Args:
    sample_id (str): Unique sample Id
    group_id (str): Unique group Id
    cutoff (int): Cutoff used for completeness
    extension (bool): Number of bases added to each interval
    coverage_source (str): Path to the BAM file used
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
  """Stores coverage metrics for a single interval and a given sample. It has a
  many-to-one relationship with it's parent interval object through it's
  ``parent_id`` attribute.

  Args:
    parent_id (int): Parent record ID
    sample_id (str): Unique sample identifier
    group_id (str): Group identifier
    coverage (float): Average coverage for the exon
    completeness (float): Ratio of adequately covered bases
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
  """Stores coverage metrics for a single block and a given sample. It has a
  many-to-one relationship with it's parent set object through it's
  ``parent_id`` attribute.

  Args:
    parent_id (int): Set ID
    sample_id (str): Unique sample identifier
    group_id (str): Group identifier
    coverage (float): Average coverage for the set
    completeness (float): Ratio of adequately covered bases
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
  """Stores coverage metrics for a single superblock and a given sample.
  It has a many-to-one relationship with it's parent superset object
  through it's ``parent_id`` attribute.

  Args:
    parent_id (int): Superblock Id
    sample_id (str): Unique sample identifier
    group_id (str): Group identifier
    coverage (float): Average coverage for the superset
    completeness (float): Ratio of adequately covered bases
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
