# -*- coding: utf-8 -*-
from toolz import cons

from chanjo.compat import iteritems
from chanjo.store import ExonStatistic, Sample, Exon

from .utils import get_or_build_exon, _exon_kwargs


def rows(session, row_data, sample_id=None, group_id=None):
    """Handle rows of sambamba output.

    N.B. only handles single sample annotations.

    Args:
        session (Session): database session object
        row_data (List[dict]): parsed sambamba output rows
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

    exons = {exon.exon_id: exon.id for exon in session.query(Exon)}
    sample_obj = Sample(sample_id=sample_id, group_id=group_id)
    nested_stats = (row(session, data, sample_obj, exons) for data in all_data)
    # flatten 2D nested list
    return (stat for stats in nested_stats for stat in stats)


def row(session, data, sample_obj, exons):
    """Handle sambamba output row.

    Args:
        session (Session): database session object
        data (dict): parsed sambamba output row
        sample_obj (Sample): linked sample model
        exons (dict): mapping between Exon.exon_id and Exon.id

    Returns:
        List[ExonStatistic]: stats models linked to exon and sample
    """
    exon_filters = _exon_kwargs(data)
    if exon_filters['exon_id'] in exons:
        # get primary key for existing exon
        primary_exon_id = exons[exon_filters['exon_id']]
        stats = statistics(data, sample_obj, exon_id=primary_exon_id)
    else:
        exon_obj = get_or_build_exon(session, exon_filters)
        stats = statistics(data, sample_obj, exon_obj=exon_obj)
    return stats


def statistics(data, sample_obj, exon_obj=None, exon_id=None):
    """Create models from a sambamba output row.

    Args:
        data (dict): parsed sambamba output row
        sample_obj (Sample): linked sample model
        exon_obj (int): primary key for related Exon

    Returns:
        List[ExonStatistic]: stats models linked to exon and sample
    """
    if exon_obj:
        relationships = dict(sample=sample_obj, exon=exon_obj)
    else:
        relationships = dict(sample=sample_obj, exon_id=exon_id)
    stats = [ExonStatistic(metric='mean_coverage', value=data['meanCoverage'],
                           **relationships)]
    for threshold, value in iteritems(data['thresholds']):
        metric = "completeness_{}".format(threshold)
        stat = ExonStatistic(metric=metric, value=value, **relationships)
        stats.append(stat)

    return stats
