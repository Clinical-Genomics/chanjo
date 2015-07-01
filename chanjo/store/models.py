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
# | Gene ORM
# +--------------------------------------------------------------------+
class Gene(Base):

  """Collection of transcripts and potentially overlapping exons.

  A :class:`Gene` can be related to multiple transcripts and multiple
  exons.

  Args:
    gene_id (str): unique gene id e.g. HGNC gene symbol
  """

  __tablename__ = 'gene'

  id = Column(Integer, primary_key=True)
  gene_id = Column(String(32), unique=True)

# +--------------------------------------------------------------------+
# | Transcript ORM
# +--------------------------------------------------------------------+
class Transcript(Base):

  """Set of non-overlapping exons.

  A :class:`Transcript` can *only* be related to a single gene.

  Args:
    transcript_id (str): unique block id (e.g. CCDS transcript id)
    gene_id (str): related gene
  """

  __tablename__ = 'block'

  id = Column(Integer, primary_key=True)
  transcript_id = Column(String(32))
  exon_id = Column(Integer, ForeignKey('exon.id'))

  # gene_id = Column(String(32), ForeignKey('gene.id'))
  # gene = relationship(Gene, backref=backref('transcripts'))


# +--------------------------------------------------------------------+
# | Exon ORM
# +--------------------------------------------------------------------+
class Exon(Base):

  """A continous genetic interval on a given contig.

  A :class:`Exon` can be related to a multiple :class:`Transcript`.
  Start and end coordinates are 1-based.

  Args:
    exon_id (str): unique exon id
    contig (str): contig/chromosome id
    start (int): 1-based start of the exon
    end (int): 1-based end of the exon
  """

  __tablename__ = 'exon'

  id = Column(Integer, primary_key=True)
  exon_id = Column(String(32), unique=True)
  chromosome = Column(String(32))
  start = Column(Integer)
  end = Column(Integer)

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

  id = Column(Integer, primary_key=True)
  sample_id = Column(String(32), unique=True)
  group = Column(String(32), index=True)
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# +--------------------------------------------------------------------+
# | Exon Data ORM
# +--------------------------------------------------------------------+
class Statistic(Base):

  """Coverage metrics for a single exon interval and a given sample.

  :class:`ExonData` has a many-to-one relationship with it's parent
  interval object through it's ``parent_id`` attribute.

  Args:
    parent_id (int): parent record Exon id
    sample_id (int): unique sample identifier
    group_id (str): group identifier
  """

  __tablename__ = 'exon_data'

  id = Column(Integer, primary_key=True)
  sample_id = Column(Integer, ForeignKey('sample.id'))
  sample = relationship(Sample, backref=backref('exon_data'))
  parent_id = Column(Integer, ForeignKey('exon.id'))
  parent = relationship(Exon, backref=backref('data'))

  metric = Column(String(32))
  value = Column(Float)
