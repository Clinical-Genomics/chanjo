# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import Column, types, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# base for declaring a mapping
BASE = declarative_base()


# +--------------------------------------------------------------------+
# | Transcript ORM
# +--------------------------------------------------------------------+
class Transcript(BASE):

    """Set of non-overlapping exons.

    A :class:`Transcript` can *only* be related to a single gene.

    Args:
        transcript_id (str): unique block id (e.g. CCDS transcript id)
        gene_id (str): related gene
    """

    __tablename__ = 'transcript'

    id = Column(types.String(32), primary_key=True)
    gene_id = Column(types.String(32), index=True, nullable=False)
    chromosome = Column(types.String(10))
    length = Column(types.Integer)


# +--------------------------------------------------------------------+
# | Sample ORM classes
# +--------------------------------------------------------------------+
class Sample(BASE):

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

    id = Column(types.String(32), primary_key=True)
    group_id = Column(types.String(32), index=True)
    source = Column(types.String(256))
    created_at = Column(types.DateTime, default=datetime.now)


# +--------------------------------------------------------------------+
# | Transcript Stat ORM
# +--------------------------------------------------------------------+
class TranscriptStat(BASE):

    """Statistics on transcript level, related to sample and transcript.

    Args:
        metric (str): identifier for the metric
        value (float): value for the metric
        sample (Sample): parent record Sample
        exon (Exon): parent record Exon
        sample_id (int): parent record Sample id
        exon_id (int): parent record Exon id
    """

    __tablename__ = 'transcript_stat'
    __table_args__ = (UniqueConstraint('sample_id', 'transcript_id',
                                       name='_sample_transcript_uc'),)

    id = Column(types.Integer, primary_key=True)
    sample_id = Column(types.String(32), ForeignKey('sample.id'),
                       nullable=False)
    sample = relationship(Sample, backref=backref('stats'))
    transcript_id = Column(types.String(32), ForeignKey('transcript.id'),
                           nullable=False)
    transcript = relationship(Transcript, backref=backref('stats'))
    mean_coverage = Column(types.Float, nullable=False)
    completeness_10 = Column(types.Float)
    completeness_15 = Column(types.Float)
    completeness_20 = Column(types.Float)
    completeness_50 = Column(types.Float)
    completeness_100 = Column(types.Float)
