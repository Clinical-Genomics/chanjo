#!/usr/bin/env python
# coding: utf-8
"""
  chanjo.sql
  ~~~~~~~~~~~~~

  The default :class:`ElementAdapter` that ships with Chanjo. Provides an
  interface to a SQLite database using the SQLAlchemy ORM.

  This module also defines the ORM objects and adds nessesary methods.

  :copyright: (c) 2013 by Robin Andeer
  :license: MIT, see LICENSE for more details
"""

import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

from interval import IntervalSet, Interval
from utils import Interval as Ival

import numpy as np

# Base for declaring a mapping
Base = declarative_base()

# =============================================================================
#   The actual Element Adapter
# -----------------------------------------------------------------------------
class ElementAdapter(object):
  """
  SQLAlchemy-based :class:`ElementAdapter` for Chanjo.

  .. note::

    For testing pourposes; use ":memory:" as the `path` argument to set up
    in-memory version of the database.

  :param str path: Path to the database to connect to
  :param bool debug: Whether to print logging information (optional)
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
      "exon": Exon,
      "exon_gene": Exon_Gene,
      "exon_transcript": Exon_Transcript
    }

  def setup(self):
    """
    Public: Sets up a new database with the default tables and columns.

    Usage::

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

    Usage::

      adapter = ElementAdapter("path/to/element.db")

      # Get all genes in the database
      allGenes = adapter.get("gene")

      # Get a specific gene from the database
      gene = adapter.get("gene", "GIT1")

    :param str elemClass: Elemet to get: "gene", "transcript" or "exon"
    :param str elemID: Element ID of interest. Default case fetches all
                       elements of the ``elemClass`` (optional)
    :returns: One or all element objects of ``elemClass``
    """
    # Get the ORM class
    klass = self._getClass(elemClass)

    # Test is user submitted and element ID
    if elemID is None:
      # Return all `elemClass` elements in the database
      return self.session.query(klass).all()
    else:
      # Return only the requested element object (or `None`) if not found
      return self.session.query(klass).get(elemID)

  def _getClass(self, elemClass):
    """
    Private: Gives access to the raw element ORM objects

    :param elemClass: Choice between "gene", "transcript", "exon"
    :returns: ORM class object
    """
    return self.classes[elemClass]

  def add(self, elements):
    """
    Public: Add one or multiple new elements to the database and commit the
    changes. Chainable.

    :param elements: New ORM object instance or list of such
    :type elements: object or list
    :returns: ``self`` for chainability
    """
    if isinstance(elements, Base):
      # Add the record to the session object
      self.session.add(elements)
    elif isinstance(elements, list):
      # Add all records to the session object
      self.session.add_all(elements)

    return self

  def create(self, elemClass, *args, **kwargs):
    """
    Public: Creates a new instance of an ORM element object filled in with the
    given `attributes`.

    If attributes is a tuple they must be in the correct order. Supplying a
    `dict` doesn't require the attributes to be in any particular order.

    :param str elemClass: Choice between "gene", "transcript", "exon"
    :param \*args: List the element attributes in the *correct order*
    :param \**kwargs: Element attributes in whatever order you like
    :returns: The new ORM instance object
    """
    if args:
      # Unpack tuple
      return self._getClass(elemClass)(*args)
    elif kwargs:
      # Unpack dictionary
      return self._getClass(elemClass)(**kwargs)
    else:
      raise TypeError("Submit attributes as arguments or keyword arguments")

  def commit(self):
    """
    Public: Manually persist changes made to various elements. Chainable.

    :returns: ``self`` for chainability
    """
    # Commit/persist dirty changes to the database
    self.session.commit()

    return self

  def transcriptStats(self):
    """
    What's happening is that we are summing read depths and passed bases for
    each exon in a transcript and then dividing those numbers by the total
    exon length of the transcript.

    .. note::
      This needs to be carried out before annotating genes!
    """

    # I might turn this into a proper SQLAlchemy verison but for now.
    rawSQL = """
    SELECT Exon_Transcript.transcript_id,
    sum((Exon.end - Exon.start + 1) * Exon.coverage) / sum(Exon.end - Exon.start + 1) AS coverage,
    sum((Exon.end - Exon.start + 1) * Exon.completeness) / sum(Exon.end - Exon.start + 1) AS completeness
    FROM Exon
    INNER JOIN Exon_Transcript
    ON Exon.id=Exon_Transcript.exon_id
    GROUP BY Exon_Transcript.transcript_id
    """

    return self.session.execute(rawSQL).fetchall()

  def geneStats(self):
    """
    .. note::
      Annotation of transcripts needs to be acomplished before annotating genes!
    """

    rawSQL = """
    SELECT Gene.id, avg(Transcript.coverage), avg(Transcript.completeness)
    FROM Gene
    INNER JOIN Transcript
    ON Gene.id=Transcript.gene_id
    GROUP BY Transcript.gene_id
    """

    return self.session.execute(rawSQL).fetchall()

  def average(self, elemClass, attr, groupby=None):
    """
    <public> Calculates the average of a given element attribute across all
    elements of that class. This is specifically intended for coverage and
    completeness. It's also possible to group the results by e.g. chromosome.

    :param str elemClass: String representing the element class ("gene",
                      "transcript", or "exon")
    :param str attr: String version of the attribute to calculate average for
    :param str groupby: What attribute to group the elements by (Default:
                        ``None``)
    :returns: ``int``, if grouping a list of ``int`` mapped to a key will be
              returned
    """
    klass = self._getClass(elemClass)

    # Generate the base query
    query = self.session.query(sql.sql.func.avg(getattr(klass, attr)))

    # We can also perform a "group by" operation, for example by "chrom"
    if groupby:
      query = query.group_by(getattr(klass, groupby))

    # Execute the query on all rows/elements
    res = query.all()

    # The average is wrapped in a list and a tuple
    return res[0][0]

  def passing(self, elemClass, attr, cutoff):
    """
    <public> Counts the number of elements that pass a threashold, e.g. how many genes have a completeness of greater than .95?

    :param str elemClass: String representing the element class ("gene",
                          "transcript", or "exon")
    :param str attr: String version of the attribute to filter by
    :param int cutoff: The threashold, lowest acceptable value to pass
    :returns: ``int``, the number of passed elements
    """
    klass = self._getClass(elemClass)
    return self.session.query(klass).filter(getattr(klass, attr) >= cutoff)\
                                    .count()

  def numAnnotatedElements(self, elemClass, attr="coverage"):
    """
    <public> Counts the total number of annotated elements. This calculation
    can be made for any element class and you can decide what annotations to
    target.

    :param str elemClass: String representing the element class ("gene",
                      "transcript", or "exon")
    :param str attr: String version of the attribute to filter by
    :returns: The number of rows with ``attr`` filled in (int).
    """
    # Fetch the element class ORM object
    klass = self._getClass(elemClass)

    # Filter by "WHERE ``attr`` IS NOT NULL".
    return self.session.query(klass).filter(getattr(klass, attr) != None)\
                                    .count()

# =============================================================================
#   Association tables
# -----------------------------------------------------------------------------
Exon_Gene = sql.Table('Exon_Gene', Base.metadata,
    sql.Column('exon_id', sql.String, sql.ForeignKey('Exon.id')),
    sql.Column('gene_id', sql.String, sql.ForeignKey('Gene.id'))
)

Exon_Transcript = sql.Table('Exon_Transcript', Base.metadata,
    sql.Column('exon_id', sql.String, sql.ForeignKey('Exon.id')),
    sql.Column('transcript_id', sql.String, sql.ForeignKey('Transcript.id'))
)

# =============================================================================
#   Gene class
# -----------------------------------------------------------------------------
class Gene(Base):
  """docstring for Gene"""
  __tablename__ = "Gene"

  id = sql.Column(sql.String, primary_key=True)
  chrom = sql.Column(sql.String)
  start = sql.Column(sql.Integer)
  end = sql.Column(sql.Integer)
  strand = sql.Column(sql.String)
  coverage = sql.Column(sql.Float)
  completeness = sql.Column(sql.Float)
  cutoff = sql.Column(sql.Integer)

  def __init__(self, hgnc=None, chrom=None, start=None, end=None, strand=None):
    super(Gene, self).__init__()

    self.id = hgnc
    self.chrom = chrom
    self.start = start
    self.end = end
    self.strand = strand

    # These should be instantiated but are not present for instances
    # for some reason. Therefore I have to use `hasattr` further down.
    self._intervals = None
    self.bgTree = None

  @property
  def intervalSet(self):
    """
    Returns all the non-overlapping exonic intervals.
    """
    if not hasattr(self, "_intervals"):
      self._intervals = IntervalSet([Interval(exon.start, exon.end)
                                     for exon in self.exons])

    return self._intervals

  @property
  def intervals(self):
    """
    Public: Generate Interval objects with start and end attributes
    representing non-overlapping exon intervals.

    :returns: A list of :class:`Interval` objects
    """
    return [Ival(i.lower_bound, i.upper_bound)
            for i in self.intervalSet]

  def extendAnnotations(self):
    # Calculate mean coverage/completeness based on transcript annotations
    # Transcripts need to be annotated first!
    self.coverage = np.mean([tx.coverage for tx in self.transcripts])
    self.completeness = np.mean([tx.completeness for tx in self.transcripts])
    self.cutoff = self.transcripts[0].cutoff

  def toDict(self):
    return {
      "id": self.id,
      "chrom": self.chrom,
      "start": self.start,
      "end": self.end,
      "strand": self.strand,
      "transcript_ids": [tx.id for tx in self.transcripts],
      "exon_ids": [ex.id for ex in self.exons],
      "coverage": self.coverage,
      "completeness": self.completeness,
      "cutoff": self.cutoff
    }


# =============================================================================
#   Transcript class
# -----------------------------------------------------------------------------
class Transcript(Base):
  """docstring for Transcript"""
  __tablename__ = "Transcript"

  id = sql.Column(sql.String, primary_key=True)
  chrom = sql.Column(sql.String)
  start = sql.Column(sql.Integer)
  end = sql.Column(sql.Integer)
  strand = sql.Column(sql.String)
  coverage = sql.Column(sql.Float)
  completeness = sql.Column(sql.Float)
  cutoff = sql.Column(sql.Integer)

  gene_id = sql.Column(sql.String, sql.ForeignKey("Gene.id"))
  gene = relationship("Gene", backref=backref("transcripts", order_by=start))

  def __init__(self, tx_id=None, chrom=None, start=None, end=None, strand=None,
               gene_id=None, coverage=None, completeness=None, cutoff=None):
    super(Transcript, self).__init__()

    self.id = tx_id
    self.chrom = chrom
    self.start = start
    self.end = end
    self.strand = strand
    self.gene_id = gene_id
    self.coverage = coverage
    self.completeness = completeness
    self.cutoff = cutoff

  def __len__(self):
    # Returns combined exon length
    baseCount = 0
    for exon in self.exons:
      baseCount += len(exon)

    return baseCount

  def extendAnnotations(self):
    # Initialize
    readCount = 0
    baseCount = 0
    passedCount = 0

    # Go through each exon (never overlaps!)
    for exon in self.exons:

      # Add the number of bases
      baseCount += len(exon)

      # Add the number of reads
      readCount += len(exon) * exon.coverage

      # Add the number of passed bases
      passedCount += len(exon) * exon.completeness

    self.coverage = readCount / float(baseCount)
    self.completeness = passedCount / float(baseCount)
    # Should be the same for all exons, use the last
    self.cutoff = exon.cutoff

  def toDict(self):
    return {
      "id": self.id,
      "chrom": self.chrom,
      "start": self.start,
      "end": self.end,
      "strand": self.strand,
      "gene_id": self.gene_id,
      "exon_ids": [ex.id for ex in self.exons],
      "coverage": self.coverage,
      "completeness": self.completeness,
      "cutoff": self.cutoff
    }

# =============================================================================
#   Exon class
# -----------------------------------------------------------------------------
class Exon(Base):
  """
  Exon: start and end coordinates are 0-based.
  """
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
    # We add +1 because we count positions and both coordinates are 0-based
    return (self.end - self.start) + 1

  def toDict(self):
    return {
      "id": self.id,
      "chrom": self.chrom,
      "start": self.start,
      "end": self.end,
      "strand": self.strand,
      "coverage": self.coverage,
      "completeness": self.completeness,
      "cutoff": self.cutoff,
      "gene_ids": [gene.id for gene in self.genes],
      "transcript_ids": [tx.id for tx in self.transcripts]
    }
