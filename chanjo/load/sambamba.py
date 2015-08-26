# -*- coding: utf-8 -*-
from toolz import cons

from chanjo._compat import iteritems
from chanjo.store import Exon, Sample, ExonStatistic


def rows(session, row_data, group_id=None):
    """Handle rows of sambamba output."""
    first_row = next(iter(row_data))
    sample_obj = sample(first_row, group_id=group_id)
    all_data = cons(first_row, row_data)
    nested_stats = (row(session, data, sample_obj) for data in all_data)
    return (stat for stats in nested_stats for stat in stats)


def row(session, data, sample_obj):
    """Handle sambamba output row."""
    filters = _exon_kwargs(data)
    exon_obj = session.query(Exon).filter_by(**filters).first()
    if exon_obj is None:
        exon_obj = exon(data)
    stats = statistics(data, sample_obj, exon_obj)
    return stats


def sample(data, group_id=None):
    """Create sample model."""
    sample_obj = Sample(sample_id=data['sampleName'], group=group_id)
    return sample_obj


# def _transcript_kwargs(data):
#     """Parse out the values to fill in the Transcript model."""
#     transcripts = [for tx_id, gene_id in data['chanjo']]


def _exon_kwargs(data):
    """Parse out the values to fill in the Exon model fields."""
    return {'exon_id': data['name'], 'chromosome': data['chrom'],
            'start': data['chromStart'], 'end': data['chromEnd']}


def exon(data):
    """Create exon model from an output row."""
    kwargs = _exon_kwargs(data)
    exon_obj = Exon(**kwargs)
    return exon_obj


def statistics(data, sample_obj, exon_obj):
    """Create models from a sambamba output row."""
    relationships = dict(sample=sample_obj)
    stats = [ExonStatistic(metric='mean_coverage', value=data['meanCoverage'],
                           **relationships)]
    for threshold, value in iteritems(data['thresholds']):
        metric = "completeness_{}".format(threshold)
        stat = ExonStatistic(metric=metric, value=value, **relationships)
        stat.parent_data = exon_obj
        stats.append(stat)

    return stats
