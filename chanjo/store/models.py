# -*- coding: utf-8 -*-
from collections import namedtuple
from datetime import datetime

from alchy import ModelBase, make_declarative_base
from sqlalchemy import Column, types, ForeignKey, UniqueConstraint, orm

Exon = namedtuple('Exon', ['chrom', 'start', 'end', 'completeness'])

# base for declaring a mapping
BASE = make_declarative_base(Base=ModelBase)


class Transcript(BASE):

    """Set of non-overlapping exons.

    A :class:`Transcript` can *only* be related to a single gene.

    Args:
        id (str): unique transcript id (e.g. CCDS)
        gene_id (str): related gene
        chromosome (str): related contig id
        lenght (int): number of exon bases in transcript
    """

    __tablename__ = 'transcript'

    id = Column(types.String(32), primary_key=True)
    gene_id = Column(types.Integer, index=True, nullable=False)
    gene_name = Column(types.String(32), index=True)
    chromosome = Column(types.String(10))
    length = Column(types.Integer)

    stats = orm.relationship('TranscriptStat', backref='transcript')


class Sample(BASE):

    """Metadata for a single sample.

    Args:
        id (str): unique sample id
        group_id (str): unique group id
        source (str): path to coverage source Sambamba output/BAM file
        created_at (DateTime): date of addition to database
    """

    __tablename__ = 'sample'

    id = Column(types.String(32), primary_key=True)
    group_id = Column(types.String(128), index=True)
    source = Column(types.String(256))
    created_at = Column(types.DateTime, default=datetime.now)

    name = Column(types.String(128))
    group_name = Column(types.String(128))

    sample = orm.relationship('TranscriptStat', cascade='all,delete',
                              backref='sample')


class TranscriptStat(BASE):

    """Statistics on transcript level, related to sample and transcript.

    Args:
        sample_id (str): link to sample record
        sample (Sample): parent Sample record
        transcript_id (str): link to transcript record
        transcript (Transcript): parent transcript record
        mean_coverage (Float): mean coverage across all exons
        completeness_XX (Float): percentage of exon bases coverage at XX
        _incomplete_exons (str): comma separated list of exon ids
    """

    __tablename__ = 'transcript_stat'
    __table_args__ = (UniqueConstraint('sample_id', 'transcript_id',
                                       name='_sample_transcript_uc'),)

    id = Column(types.Integer, primary_key=True)
    mean_coverage = Column(types.Float, nullable=False)
    completeness_10 = Column(types.Float)
    completeness_15 = Column(types.Float)
    completeness_20 = Column(types.Float)
    completeness_50 = Column(types.Float)
    completeness_100 = Column(types.Float)

    threshold = Column(types.Integer)
    _incomplete_exons = Column(types.Text)

    sample_id = Column(types.String(32), ForeignKey('sample.id'),
                       nullable=False)
    transcript_id = Column(types.String(32), ForeignKey('transcript.id'),
                           nullable=False)

    @property
    def incomplete_exons(self):
        """Return a list of exons ids."""
        raw_exons = (self._incomplete_exons.split(',') if
                     self._incomplete_exons else [])
        for raw_exon in raw_exons:
            data = raw_exon.split('|')
            yield Exon(chrom=data[0], start=int(data[1]), end=int(data[2]),
                       completeness=float(data[3]))

    @incomplete_exons.setter
    def incomplete_exons(self, exon_list):
        raw_exons = ['|'.join(map(str, exon)) for exon in exon_list]
        self._incomplete_exons = ','.join(raw_exons) if raw_exons else None
