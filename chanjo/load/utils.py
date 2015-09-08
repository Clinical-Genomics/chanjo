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


def exon(data):
    """Create exon model from an output row.

    Args:
        data (dict): parsed sambamba output row

    Return:
        Exon: filled in Exon database model
    """
    kwargs = _exon_kwargs(data)
    exon_obj = Exon(**kwargs)
    return exon_obj


def get_or_build_exon(session, data):
    """Fetch exon from database or build a new instance.

    Args:
        session (Session): database session object
        data (dict): parsed sambamba output row
    """
    ex_filters = _exon_kwargs(data)
    exon_obj = session.query(Exon).filter_by(**ex_filters).first()
    if exon_obj is None:
        # no existing exon object, create a new one
        exon_obj = exon(data)

    return exon_obj
