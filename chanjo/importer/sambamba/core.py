# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from chanjo.store import Exon, get_or_create


def process_line(line, cutoffs, session, group=None):
    """Process Sambamba output"""
    kwargs = parse_sambamba(line)
    entry = SambambaEntry(**kwargs)
    filters = {'chromosome': entry.chromosome, 'start': entry.start,
               'end': entry.start, 'exon_id': entry.id}
    exon = get_or_create(session, Exon, **filters)
    sample = Sample(sample_id=entry.sample, group=group)

    # create metrics
    coverage = Statistic(metric='coverage-avg', value=entry.coverage,
                         sample=sample, parent=exon)

    models = [coverage]
    for cutoff, completeness in zip(cutoffs, completeness_levels):
        metric_name = "completeness-{}".format(cutoff)
        completeness = Statistic(metric=metric_name, value=completeness,
                                 sample=sample, parent=exon)
        models.append(completeness)

    return models
