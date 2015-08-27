# -*- coding: utf-8 -*-
from toolz import cons

from chanjo._compat import iteritems
from chanjo.store import Exon, ExonStatistic, Gene, Sample, Transcript


def rows(session, row_data, group_id=None):
    """Handle rows of sambamba output."""
    first_row = next(iter(row_data))
    sample_obj = sample(first_row, group_id=group_id)
    all_data = cons(first_row, row_data)
    nested_stats = (row(session, data, sample_obj) for data in all_data)
    return (stat for stats in nested_stats for stat in stats)


def row(session, data, sample_obj):
    """Handle sambamba output row."""
    ex_filters = _exon_kwargs(data)
    exon_obj = session.query(Exon).filter_by(**ex_filters).first()
    if exon_obj is None:
        exon_obj = exon(data)

    genes = {}
    for tx_id, gene_id in data['elements']:
        gene_obj = session.query(Gene).filter_by(gene_id=gene_id).first()
        if gene_obj is None:
            genes[gene_id] = gene_obj = (genes.get(gene_id) or
                                         Gene(gene_id=gene_id))

        tx_filters = {'transcript_id': tx_id}
        tx_obj = session.query(Transcript).filter_by(**tx_filters).first()
        if tx_obj is None:
            tx_obj = Transcript(**tx_filters)
            tx_obj.gene = gene_obj

        if tx_obj not in exon_obj.transcripts:
            exon_obj.transcripts.append(tx_obj)

    stats = statistics(data, sample_obj, exon_obj)
    return stats


def sample(data, group_id=None):
    """Create sample model."""
    sample_obj = Sample(sample_id=data['sampleName'], group=group_id)
    return sample_obj


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
    relationships = dict(sample=sample_obj, exon=exon_obj)
    stats = [ExonStatistic(metric='mean_coverage', value=data['meanCoverage'],
                           **relationships)]
    for threshold, value in iteritems(data['thresholds']):
        metric = "completeness_{}".format(threshold)
        stat = ExonStatistic(metric=metric, value=value, **relationships)
        stats.append(stat)

    return stats
