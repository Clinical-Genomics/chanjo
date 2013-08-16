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
  SQLAlchemy based Element Adapter for Chanjo. Use ":memory:" as the `path`
  argument for testing purposes to set up in-memory version of the database.

  :param path:  [str]  Path to the database to connect to
  :param debug: [bool] Whether to print logging information
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
    """
    Public: Setup a new database with the default tables and columns.
    ----------

    Usage:
      from chanjo.sql import ElementAdapter

      # Point the adapter to the location of a new database
      adapter = ElementAdapter("path/to/new_database.db")

      # Commit to setting it up
      adapter.setup()

      # Add some elements...
    """
    # Create the tables
    Base.metadata.create_all(self.engine)

  def get(self, elemClass, elemID=None):
    """
    Public: Fetches one or multiple elements from the database
    ----------

    :param elemClass: [str]      Choice between "gene", "transcript", "exon"
    :param elemID:    [str/None] A single element ID or `None`. The latter
                                 returns all elements of the `elemClass`.
    :returns:         [object/list] One or all element objects

    Usage:
      adapter = ElementAdapter("path/to/element.db")

      # Get all genes in the database
      allGenes = adapter.get("gene")

      # Get a specific gene from the database
      git1 = adapter.get("gene", "GIT1")
    """
    # Get the ORM class
    klass = self._getClass(elemClass)

    # Test is user submitted and element ID
    if elemID is None:
      # Return all `elemClass` elements in the database
      return self.session.query(klass).all()
    else:
      # Return only the requested element object (or `None`) if not found
      return self.session.querty(klass).get(elemID)

  def _getClass(self, elemClass):
    """
    Private: Gives access to the raw element ORM objects
    ----------

    :param elemClass: [str]    Choice between "gene", "transcript", "exon"
    :returns:         [object] ORM class object
    """
    return self.classes[elemClass]

  def add(self, elements):
    """
    Public: Add one or multiple new elements to the database and commit the
    changes. Chainable.
    ----------

    :param elements: [object/list] New ORM object instance or list or such
    :returns:        [self]        Chainability
    """
    if isinstance(elements, Base):
      # Add the record to the session object
      self.session.add(elements)
    elif isinstance(elements, list):
      # Add all records to the session object
      self.session.add_all(elements)

    # Commit the record(s) the database
    self.session.commit()

    return self

  def create(self, elemClass, attributes):
    """
    Public: Creates a new instance of an ORM element object filled in with the
    given `attributes`.

    If attributes is a tuple they must be in the correct order. Supplying a
    `dict` doesn't require the attributes to be in any particular order.
    ----------

    :param elemClass:  [str]         Choice between "gene", "transcript", "exon"
    :param attributes: [tuple/dict]  Instance attr in order for new element
    :returns:          [object/None] The new ORM instance object
    """
    if isinstance(attributes, tuple):
      # Unpack tuple
      return self._getClass(elemClass)(*attributes)
    elif isinstance(attributes, dict):
      # Unpack dictionary
      return self._getClass(elemClass)(**attributes)
    else:
      raise TypeError("Use tuple or dict for attributes")

  def commit(self):
    """
    Public: Manually persist changes made to various elements. Chainable.
    ----------

    :returns: [self] Chainability
    """
    # Commit/persist dirty changes to the database
    self.session.commit()

    return self

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

  def __init__(self, hgnc=None, chrom=None, start=None, end=None, strand=None):
    super(Gene, self).__init__()

    self.id = hgnc
    self.chrom = chrom
    self.start = start
    self.end = end
    self.strand = strand

    self._intervals = None

  @property
  def intervalSet(self):
    """
    Returns all the non-overlapping exonic intervals.
    """
    if self._intervals is None:
      self._intervals = IntervalSet([Interval(exon.start, exon.end)
                                     for exon in self.exons])

    return self._intervals

  @property
  def intervals(self):
    """
    Public: Generate Interval objects with start and end attributes representing
    non-overlapping exon intervals.
    ----------

    :returns: [list] A list of `Interval` objects
    """
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
  gene = relationship("Gene", backref=backref("transcripts", order_by=start))

  def __init__(self, tx_id=None, chrom=None, start=None, end=None, strand=None,
               gene_id=None):
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

  def __init__(self, ex_id=None, chrom=None, start=None, end=None, strand=None):
    super(Exon, self).__init__()

    self.id = ex_id
    self.chrom = chrom
    self.start = start
    self.end = end
    self.strand = strand

  def __len__(self):
    return self.end - self.start
