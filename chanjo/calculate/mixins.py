# -*- coding: utf-8 -*-
from sqlalchemy.sql import func

from chanjo.store.models import Sample, Transcript, TranscriptStat


class CalculateMixin:

    """Methods for calculating various metrics."""

    def mean(self, sample_ids=None):
        """Calculate the mean values of all metrics per sample."""
        sql_query = (self.query(TranscriptStat.sample_id,
                                func.avg(TranscriptStat.mean_coverage),
                                func.avg(TranscriptStat.completeness_10),
                                func.avg(TranscriptStat.completeness_15),
                                func.avg(TranscriptStat.completeness_20),
                                func.avg(TranscriptStat.completeness_50),
                                func.avg(TranscriptStat.completeness_100))
                         .group_by(TranscriptStat.sample_id))
        if sample_ids:
            sql_query = sql_query.filter(TranscriptStat.sample_id.in_(sample_ids))
        return sql_query

    def gene_metrics(self, *genes):
        """Calculate gene statistics."""
        query = (self.mean()
                     .add_column(Transcript.gene_id)
                     .join(TranscriptStat.transcript)
                     .filter(Transcript.gene_id.in_(genes))
                     .group_by(Transcript.gene_id))
        return query
