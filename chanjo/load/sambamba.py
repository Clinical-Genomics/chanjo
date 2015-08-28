# -*- coding: utf-8 -*-
from toolz import cons

from chanjo._compat import iteritems
from chanjo.store import ExonStatistic, Sample

from .utils import get_or_build_exon


def rows(session, row_data, group_id=None):
    """Handle rows of sambamba output."""
    first_row = next(iter(row_data))
    sample_obj = sample(first_row, group_id=group_id)
    all_data = cons(first_row, row_data)
    nested_stats = (row(session, data, sample_obj) for data in all_data)
    return (stat for stats in nested_stats for stat in stats)


def row(session, data, sample_obj):
    """Handle sambamba output row."""
    exon_obj = get_or_build_exon(session, data)
    stats = statistics(data, sample_obj, exon_obj)
    return stats


def sample(data, group_id=None):
    """Create sample model."""
    sample_obj = Sample(sample_id=data['sampleName'], group=group_id)
    return sample_obj


def statistics(data, sample_obj, exon_obj):
    """Create models from a sambamba output row."""
    relationships = dict(sample=sample_obj, exon=exon_obj)
    stats = [ExonStatistic(metric='mean_coverage', value=data['meanCoverage'],
                           **relationships)]
    for threshold, value in iteritems(data['thresholds']):
        metric = "completeness_{}".format(threshold)
        stat = ExonStatistic(metric=metric, value=value, **relationships)
        stats.append(stat)

    return stats
