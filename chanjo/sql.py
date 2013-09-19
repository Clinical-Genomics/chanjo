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
from elemental.core import Base, ElementalDB
import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref


# =========================================================
#   Data ORM classes
# ---------------------------------------------------------
class GeneData(Base):
  """docstring for GeneData"""
  __tablename__ = "GeneData"

  id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
  coverage = sa.Column(sa.Float)
  completeness = sa.Column(sa.Float)

  # These column maps coverage/completeness to an individual+group
  sample_id = sa.Column(sa.String)
  group_id = sa.Column(sa.Integer)

  # Genetic relationship
  gene_id = sa.Column(sa.String, sa.ForeignKey("Gene.id"))
  gene = relationship("Gene", backref=backref("data"))

  def __init__(self, gene_id, sample_id=None, group_id=None,
               coverage=None, completeness=None):
    super(GeneData, self).__init__()
    
    self.gene_id = gene_id
    self.sample_id = sample_id
    self.group_id = group_id
    self.coverage = coverage
    self.completeness = completeness


class TranscriptData(Base):
  """docstring for TranscriptData"""
  __tablename__ = "TranscriptData"

  id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
  coverage = sa.Column(sa.Float)
  completeness = sa.Column(sa.Float)

  # These column maps coverage/completeness to an individual+group
  sample_id = sa.Column(sa.String)
  group_id = sa.Column(sa.Integer)

  # Genetic relationship
  transcript_id = sa.Column(sa.String, sa.ForeignKey("Transcript.id"))
  transcript = relationship("Transcript", backref=backref("data"))

  def __init__(self, tx_id, sample_id=None, group_id=None,
               coverage=None, completeness=None):
    super(TranscriptData, self).__init__()
    
    self.transcript_id = tx_id
    self.sample_id = sample_id
    self.group_id = group_id
    self.coverage = coverage
    self.completeness = completeness


class ExonData(Base):
  """docstring for ExonData"""
  __tablename__ = "ExonData"

  id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
  coverage = sa.Column(sa.Float)
  completeness = sa.Column(sa.Float)

  # These column maps coverage/completeness to an individual+group
  sample_id = sa.Column(sa.String)
  group_id = sa.Column(sa.Integer)

  # Genetic relationship
  exon_id = sa.Column(sa.String, sa.ForeignKey("Exon.id"))
  exon = relationship("Exon", backref=backref("data"))

  def __init__(self, exon_id, sample_id=None, group_id=None,
               coverage=None, completeness=None):
    super(ExonData, self).__init__()
    
    self.exon_id = exon_id
    self.sample_id = sample_id
    self.group_id = group_id
    self.coverage = coverage
    self.completeness = completeness


# =========================================================
#   The actual Element Adapter
# ---------------------------------------------------------
class ElementAdapter(ElementalDB):
  """
  SQLAlchemy-based :class:`ElementAdapter` for Chanjo.

  .. note::

    For testing pourposes; use ":memory:" as the `path` argument to set up
    in-memory version of the database.

  :param str path: Path to the database to connect to
  :param bool debug: Whether to print logging information (optional)
  """
  def __init__(self, path, debug=False):
    super(ElementAdapter, self).__init__(path, debug=debug)

    # Add new classes to the supported ORM classes
    self.classes.update({
      "gene_data": GeneData,
      "transcript_data": TranscriptData,
      "exon_data": ExonData
    })

  def transcriptStats(self, sample_id):
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
           sum((Exon.end-Exon.start+1) * ExonData.coverage) / sum(Exon.end-Exon.start+1) AS coverage,
           sum((Exon.end-Exon.start+1) * ExonData.completeness) / sum(Exon.end-Exon.start+1) AS completeness
    FROM Exon
    INNER JOIN Exon_Transcript ON Exon.id=Exon_Transcript.exon_id
    INNER JOIN ExonData ON Exon.id=ExonData.exon_id
    WHERE ExonData.sample_id="{sample_id}"
    GROUP BY Exon_Transcript.transcript_id
    """.format(sample_id=sample_id)

    return self.session.execute(rawSQL).fetchall()

  def geneStats(self):
    """
    .. note::
      Annotation of transcripts needs to be acomplished before annotating genes!
    """
    rawSQL = """
    SELECT Gene.id,
           avg(TranscriptData.coverage),
           avg(TranscriptData.completeness)
    FROM Transcript
    INNER JOIN Gene ON Transcript.gene_id=Gene.id
    INNER JOIN TranscriptData ON Transcript.id=TranscriptData.transcript_id
    GROUP BY Transcript.gene_id
    """

    return self.session.execute(rawSQL).fetchall()
