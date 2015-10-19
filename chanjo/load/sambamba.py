# -*- coding: utf-8 -*-
from toolz import cons

from chanjo.compat import iteritems
from chanjo.store import ExonStatistic, Sample

from .utils import get_or_build_exon


def rows(session, row_data, sample_id=None, group_id=None):
    """Handle rows of sambamba output.

    N.B. only handles single sample annotations.

    Args:
        session (Session): database session object
        row_data (dict): parsed sambamba output rows
        sample_id (Optional[str]): id to reference sample
        group_id (Optional[str]): id to group samples together

    Yields:
        ExonStatistic: stats model linked to exon and sample
    """
    if sample_id is None:
        # use first row to get information on sample
        first_row = next(iter(row_data))
        sample_id = first_row['sampleName']
        # place the first row back in the stream
        all_data = cons(first_row, row_data)
    else:
        all_data = row_data

    sample_obj = Sample(sample_id=sample_id, group_id=group_id)
    nested_stats = (row(session, data, sample_obj) for data in all_data)
    # flatten 2D nested list
    return (stat for stats in nested_stats for stat in stats)


def row(session, data, sample_obj):
    """Handle sambamba output row.

    Args:
        session (Session): database session object
        data (dict): parsed sambamba output row
        sample_obj (Sample): linked sample model

    Returns:
        List[ExonStatistic]: stats models linked to exon and sample
    """
    exon_obj = get_or_build_exon(session, data)
    stats = statistics(data, sample_obj, exon_obj)
    return stats


def statistics(data, sample_obj, exon_obj):
    """Create models from a sambamba output row.

    Args:
        data (dict): parsed sambamba output row
        sample_obj (Sample): linked sample model
        exon_obj (Exon): linked exon model

    Returns:
        List[ExonStatistic]: stats models linked to exon and sample
    """
    relationships = dict(sample=sample_obj, exon=exon_obj)
    stats = [ExonStatistic(metric='mean_coverage', value=data['meanCoverage'],
                           **relationships)]
    for threshold, value in iteritems(data['thresholds']):
        metric = "completeness_{}".format(threshold)
        stat = ExonStatistic(metric=metric, value=value, **relationships)
        stats.append(stat)

    return stats
