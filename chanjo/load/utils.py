# -*- coding: utf-8 -*-
from chanjo.store import Exon


def _exon_kwargs(data):
    """Parse out the values to fill in the Exon model fields."""
    return {'exon_id': data['name'], 'chromosome': data['chrom'],
            'start': data['chromStart'], 'end': data['chromEnd']}


def exon(data):
    """Create exon model from an output row."""
    kwargs = _exon_kwargs(data)
    exon_obj = Exon(**kwargs)
    return exon_obj


def get_or_build_exon(session, data):
    """Fetch exon from database or build a new instance."""
    ex_filters = _exon_kwargs(data)
    exon_obj = session.query(Exon).filter_by(**ex_filters).first()
    if exon_obj is None:
        exon_obj = exon(data)

    return exon_obj
