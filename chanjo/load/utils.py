# -*- coding: utf-8 -*-
from chanjo.store import Exon


def _exon_kwargs(data):
    """Parse out the values to fill in the Exon model fields.

    Args:
        data (dict): parsed sambamba output row

    Returns:
        dict: kwargs prepared for Exon model
    """
    exon_id = data.get('name') or data['extraFields'][0]
    return {'exon_id': exon_id, 'chromosome': data['chrom'],
            'start': data['chromStart'], 'end': data['chromEnd']}


def get_or_build_exon(session, exon_filters):
    """Fetch exon from database or build a new instance.

    Args:
        session (Session): database session object
        exon_filters (dict): uniquely identifying exon information
    """
    exon_obj = session.query(Exon).filter_by(**exon_filters).first()
    if exon_obj is None:
        # no existing exon object, create a new one
        exon_obj = Exon(**exon_filters)
    return exon_obj


def groupby_tx(exons, sambamba=False):
    """Group (unordered) exons per transcript."""
    transcripts = {}
    for exon in exons:
        if sambamba:
            exon['elements'] = dict(zip(exon['extraFields'][-2].split(','),
                                        exon['extraFields'][-1].split(',')))
        else:
            exon['elements'] = dict(exon['elements'])
        for transcript_id in exon['elements']:
            if transcript_id not in transcripts:
                transcripts[transcript_id] = []
            transcripts[transcript_id].append(exon)
    return transcripts
