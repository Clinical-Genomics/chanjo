#!/usr/bin/env python
# coding: utf-8

import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

from interval import IntervalSet, Interval
from utils import Interval as Ival

# Base for declaring a mapping
Base = declarative_base()

# ==============================================================================
#   The actual Element Adapter
# ------------------------------------------------------------------------------
class ElementAdapter(object):
  """
  SQLAlchemy based Element Adapter for Chanjo.
  """
  def __init__(self, path, debug=False):
    super(ElementAdapter, self).__init__()
    self.path = path

    # Connect to the database
    self.engine = sql.create_engine("sqlite:///{path}".format(path=path),
                                    echo=debug)

    # Make sure the same engine is propagated to the Base classes
    Base.metadata.bind = self.engine

    # Start a session
    self.Session = sessionmaker(bind=self.engine)
    self.session = self.Session()

    # Element Class dict
    self.classes = {
      "gene": Gene,
      "transcript": Transcript,
      "exon": Exon
    }

  def setup(self):
    # Create the tables
    Base.metadata.create_all(self.engine)

  def get(self, elemClass, elemID=None):
    klass = self.getClass(elemClass)
    if elemID is None:
      return self.session.query(klass).all()
    else:
      return self.session.query(klass).get(elemID)

  def getClass(self, elemClass):
    return self.classes[elemClass]

  def set(self, elements):
    if isinstance(elements, Base):
      # Add the record to the session object
      session.add(elements)
    elif isinstance(elements, list):
      # Add all records to the session object
      session.add_all(elements)

    # Commit the record(s) the database
    session.commit()

    return self

  def new(self, elemClass, attributes):
    return self.getClass(elemClass)(*attributes)

# ==============================================================================
#   Association tables
# ------------------------------------------------------------------------------
Exon_Gene = sql.Table('Exon_Gene', Base.metadata,
    sql.Column('exon_id', sql.String, sql.ForeignKey('Exon.id')),
    sql.Column('gene_id', sql.String, sql.ForeignKey('Gene.id'))
)

Exon_Transcript = sql.Table('Exon_Transcript', Base.metadata,
    sql.Column('exon_id', sql.String, sql.ForeignKey('Exon.id')),
    sql.Column('transcript_id', sql.String, sql.ForeignKey('Transcript.id'))
)

# ==============================================================================
#   Gene class
# ------------------------------------------------------------------------------
class Gene(Base):
  """docstring for Gene"""
  __tablename__ = "Gene"

  id = sql.Column(sql.String, primary_key=True)
  chrom = sql.Column(sql.String)
  start = sql.Column(sql.Integer)
  end = sql.Column(sql.Integer)
  strand = sql.Column(sql.String)

  def __init__(self, hgnc, chrom, start, end, strand):
    super(Gene, self).__init__()

    self.id = hgnc
    self.chrom = chrom
    self.start = start
    self.end = end
    self.strand = strand

    self._intervals = None

  @property
  def intervals(self):
    """
    Returns all the non-overlapping exonic intervals.
    """
    if self._intervals is None:
      self._intervals = IntervalSet([Interval(exon.start, exon.end)
                                     for exon in self.exons])

    return self._intervals

  def simpleIntervals(self):
    return [Ival(i.lower_bound, i.upper_bound)
            for i in self.intervals]

# ==============================================================================
#   Transcript class
# ------------------------------------------------------------------------------
class Transcript(Base):
  """docstring for Transcript"""
  __tablename__ = "Transcript"

  id = sql.Column(sql.String, primary_key=True)
  chrom = sql.Column(sql.String)
  start = sql.Column(sql.Integer)
  end = sql.Column(sql.Integer)
  strand = sql.Column(sql.String)

  gene_id = sql.Column(sql.String, sql.ForeignKey("Gene.id"))
  gene = relationship("Gene", backref=backref('transcripts', order_by=start))

  def __init__(self, tx_id, chrom, start, end, strand, gene_id):
    super(Transcript, self).__init__()

    self.id = tx_id
    self.chrom = chrom
    self.start = start
    self.end = end
    self.strand = strand

    self.gene_id = gene_id

  def __len__(self):
    baseCount = 0
    for exon in self.exons:
      baseCount += len(exon)

    return baseCount

# ==============================================================================
#   Exon class
# ------------------------------------------------------------------------------
class Exon(Base):
  """docstring for Exon"""
  __tablename__ = "Exon"

  id = sql.Column(sql.String, primary_key=True)
  chrom = sql.Column(sql.String)
  start = sql.Column(sql.Integer)
  end = sql.Column(sql.Integer)
  strand = sql.Column(sql.String)

  coverage = sql.Column(sql.Float)
  completeness = sql.Column(sql.Float)
  cutoff = sql.Column(sql.Integer)

  transcripts = relationship("Transcript", secondary=Exon_Transcript,
                             backref=backref("exons", order_by=start))

  genes = relationship("Gene", secondary=Exon_Gene,
                       backref=backref("exons", order_by=start))

  def __init__(self, ex_id, chrom, start, end, strand):
    super(Exon, self).__init__()

    self.id = ex_id
    self.chrom = chrom
    self.start = start
    self.end = end
    self.strand = strand

  def __len__(self):
    return self.end - self.start
