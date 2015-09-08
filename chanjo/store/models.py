# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        Table, UniqueConstraint)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# base for declaring a mapping
BASE = declarative_base()


# +--------------------------------------------------------------------+
# | Association tables
# | ~~~~~~~~~~~~~~~~~~~
# | Provides the many-to-many relationships between:
# | - Exon<->Transcript
# +--------------------------------------------------------------------+
Exon_Transcript = Table(
    'exon__transcript',
    BASE.metadata,
    Column('exon_id', Integer, ForeignKey('exon.id')),
    Column('transcript_id', Integer, ForeignKey('transcript.id')))


# +--------------------------------------------------------------------+
# | Gene ORM
# +--------------------------------------------------------------------+
class Gene(BASE):

    """Collection of transcripts and potentially overlapping exons.

    A :class:`Gene` can be related to multiple transcripts and multiple
    exons.

    Args:
        gene_id (str): unique gene id e.g. HGNC gene symbol
    """

    __tablename__ = 'gene'
    __table_args__ = (UniqueConstraint('chromosome', 'start', 'end',
                                       name='_coordinates'),)

    id = Column(Integer, primary_key=True)
    gene_id = Column(String(32), unique=True)
    chromosome = Column(String(32))
    start = Column(Integer)
    end = Column(Integer)


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

    id = Column(Integer, primary_key=True)
    transcript_id = Column(String(32))

    gene_id = Column(String(32), ForeignKey('gene.id'))
    gene = relationship(Gene, backref=backref('transcripts'))


# +--------------------------------------------------------------------+
# | Exon ORM
# +--------------------------------------------------------------------+
class Exon(BASE):

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
    __table_args__ = (UniqueConstraint('chromosome', 'start', 'end',
                                       name='_coordinates'),)

    id = Column(Integer, primary_key=True)
    exon_id = Column(String(32), unique=True)
    chromosome = Column(String(32))
    start = Column(Integer)
    end = Column(Integer)

    transcripts = relationship(Transcript, secondary=Exon_Transcript,
                               backref=backref('exons', order_by=start))

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

    id = Column(Integer, primary_key=True)
    sample_id = Column(String(32), unique=True)
    group_id = Column(String(32), index=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# +--------------------------------------------------------------------+
# | Exon Data ORM
# +--------------------------------------------------------------------+
class Statistic(object):

    """Coverage metrics for a single element and a given sample.

    Args:
        metric (str): identifier for the metric
        value (float): value for the metric
    """

    id = Column(Integer, primary_key=True)
    metric = Column(String(32))
    value = Column(Float)


class ExonStatistic(Statistic, BASE):

    """Statistics on the exon level, related to sample and exon.

    Args:
        sample (Sample): parent record Sample
        exon (Exon): parent record Exon
        sample_id (int): parent record Sample id
        exon_id (int): parent record Exon id
    """

    __tablename__ = 'exon_stat'

    sample_id = Column(Integer, ForeignKey('sample.id'))
    sample = relationship(Sample, backref=backref('exon_stats'))
    exon_id = Column(Integer, ForeignKey('exon.id'))
    exon = relationship(Exon, backref=backref('stats'))
