#!/usr/bin/env python
# coding: utf-8
"""
  chanjo.sql
  ~~~~~~~~~~~~~

  The default :class:`ElementAdapter` that ships with Chanjo. Provides a basic
  interface to a `SQLite` database using the `SQLAlchemy` ORM. The SQL
  structure extends a parallel project `Elemental` that provides the tables
  and relationships between genes, transcripts, and exons.

  The module defines a few extra ORM objects for adding sample specific
  coverage annotations.

  :copyright: (c) 2013 by Robin Andeer
  :license: MIT, see LICENSE for more details
"""
import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref

from elemental.core import Base, ElementalDB


# ---------------------------------------------------------
#  Data ORM classes
# ---------------------------------------------------------
class GeneData(Base):
  """
  Stores coverage metrics for a single gene and a given sample. It has a
  many-to-one relationship with it's parent gene object through it's
  ``element_id`` attribute.

  :param str element_id: HGNC gene symbol
  :param str sample_id: Unique sample identifier
  :param int group_id: "Unique" group identifier
  :param float coverage: Average coverage for the gene
  :param float completeness: Ratio of adequately covered bases
  """
  __tablename__ = "GeneData"

  id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
  coverage = sa.Column(sa.Float)
  completeness = sa.Column(sa.Float)

  # These column maps coverage/completeness to an individual+group
  sample_id = sa.Column(sa.String)
  group_id = sa.Column(sa.Integer)

  # Genetic relationship
  element_id = sa.Column(sa.String, sa.ForeignKey("Gene.id"))
  element = relationship("Gene", backref=backref("data"))

  def __init__(self, element_id, sample_id=None, group_id=None,
               coverage=None, completeness=None):
    super(GeneData, self).__init__()
    
    self.element_id = element_id
    self.sample_id = sample_id
    self.group_id = group_id
    self.coverage = coverage
    self.completeness = completeness


class TranscriptData(Base):
  """
  Stores coverage metrics for a single transcript and a given sample. It has a
  many-to-one relationship with it's parent transcript object through it's
  ``element_id`` attribute.

  :param str element_id: Unique CCDS transcript identifier
  :param str sample_id: Unique sample identifier
  :param int group_id: "Unique" group identifier
  :param float coverage: Average coverage for the transcript
  :param float completeness: Ratio of adequately covered bases
  """
  __tablename__ = "TranscriptData"

  id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
  coverage = sa.Column(sa.Float)
  completeness = sa.Column(sa.Float)

  # These column maps coverage/completeness to an individual+group
  sample_id = sa.Column(sa.String)
  group_id = sa.Column(sa.Integer)

  # Genetic relationship
  element_id = sa.Column(sa.String, sa.ForeignKey("Transcript.id"))
  element = relationship("Transcript", backref=backref("data"))

  def __init__(self, element_id, sample_id=None, group_id=None,
               coverage=None, completeness=None):
    super(TranscriptData, self).__init__()
    
    self.element_id = element_id
    self.sample_id = sample_id
    self.group_id = group_id
    self.coverage = coverage
    self.completeness = completeness


class ExonData(Base):
  """
  Stores coverage metrics for a single exon and a given sample. It has a
  many-to-one relationship with it's parent exon object through it's
  ``element_id`` attribute.

  :param str element_id: HGNC gene symbol
  :param str sample_id: Unique sample identifier
  :param int group_id: "Unique" group identifier
  :param float coverage: Average coverage for the exon
  :param float completeness: Ratio of adequately covered bases
  """
  __tablename__ = "ExonData"

  id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
  coverage = sa.Column(sa.Float)
  completeness = sa.Column(sa.Float)

  # These column maps coverage/completeness to an individual+group
  sample_id = sa.Column(sa.String)
  group_id = sa.Column(sa.Integer)

  # Genetic relationship
  element_id = sa.Column(sa.String, sa.ForeignKey("Exon.id"))
  element = relationship("Exon", backref=backref("data"))

  def __init__(self, element_id, sample_id=None, group_id=None,
               coverage=None, completeness=None):
    super(ExonData, self).__init__()
    
    self.element_id = element_id
    self.sample_id = sample_id
    self.group_id = group_id
    self.coverage = coverage
    self.completeness = completeness


# =========================================================
#   The actual Element Adapter
# ---------------------------------------------------------
class ElementAdapter(ElementalDB):
  """
  SQLAlchemy-based :class:`ElementAdapter` for Chanjo. Inherits the basic SQL
  table structure from `ElementalDB`.

  .. note::

    For testing pourposes; use ":memory:" as the ``path`` parameter to set up
    an in-memory instance of the database.

  :param str path: Path to the database to connect to
  :param bool debug: Whether to print logging information (optional)
  """
  def __init__(self, path, debug=False):
    super(ElementAdapter, self).__init__(path, debug=debug)

    # Add new data classes to the supported ORM classes
    self.classes.update({
      "gene_data": GeneData,
      "transcript_data": TranscriptData,
      "exon_data": ExonData
    })

  def transcriptStats(self, sample_id):
    """
    <public> Calculates transcript level metrics to annotate transcripts.
    Requires all related exons to already be properly annotated.

    What's happening is that we are summing read depths and adequately covered
    bases for each exon in a transcript and then dividing those numbers by the
    total exon length of the transcript.

    .. note::

      Transcript annotation needs to be carried out before annotating genes!

    :param str sample_id: Sample ID to match with coverage annotations
    :returns: List of tuples: ``(<tx_id>, <coverage>, <completeness>)``
    """
    # I might turn this into a proper SQLAlchemy verison but for now.
    rawSQL = """
    SELECT Exon_Transcript.transcript_id,
           sum((Exon.end-Exon.start+1) * ExonData.coverage) / sum(Exon.end-Exon.start+1) AS coverage,
           sum((Exon.end-Exon.start+1) * ExonData.completeness) / sum(Exon.end-Exon.start+1) AS completeness
    FROM Exon
    INNER JOIN Exon_Transcript ON Exon.id=Exon_Transcript.exon_id
    INNER JOIN ExonData ON Exon.id=ExonData.element_id
    WHERE ExonData.sample_id="{sample_id}"
    GROUP BY Exon_Transcript.transcript_id
    """.format(sample_id=sample_id)

    return self.session.execute(rawSQL).fetchall()

  def geneStats(self, sample_id):
    """
    <public> Calculates gene level metrics to annotate genes. Requires all
    related transcripts to already be properly annotated.

    What's happening is that we are simply taking the average of the metrics
    on the transcript level and applying that as gene metrics. This gives a
    decent, albeit not perfect, represenation of gene level metrics.

    .. note::

      Annotation of transcripts needs to be acomplished before annotating genes!

    :param str sample_id: Sample ID to match with coverage annotations
    :returns: List of tuples: ``(<gene_id>, <coverage>, <completeness>)``
    """
    rawSQL = """
    SELECT Gene.id,
           avg(TranscriptData.coverage),
           avg(TranscriptData.completeness)
    FROM Transcript
    INNER JOIN Gene ON Transcript.gene_id=Gene.id
    INNER JOIN TranscriptData ON Transcript.id=TranscriptData.element_id
    WHERE TranscriptData.sample_id="{sample_id}"
    GROUP BY Transcript.gene_id
    """.format(sample_id=sample_id)

    return self.session.execute(rawSQL).fetchall()
