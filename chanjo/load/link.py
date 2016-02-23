# -*- coding: utf-8 -*-
from chanjo.store import Gene, Transcript

from .utils import get_or_build_exon, _exon_kwargs


def rows(session, row_data):
    """Handle rows of sambamba output."""
    exons = (row(session, data) for data in row_data)
    return exons


def row(session, data):
    """Link transcripts and genes."""
    # start with exons object
    exon_filters = _exon_kwargs(data)
    exon_obj = get_or_build_exon(session, exon_filters)
    # store created gene objects
    genes = {}
    for tx_id, gene_id in data['elements']:
        gene_obj = session.query(Gene).filter_by(gene_id=gene_id).first()
        if gene_obj is None:
            # create new gene and store to avoid conflicts
            genes[gene_id] = gene_obj = (genes.get(gene_id) or
                                         Gene(gene_id=gene_id))

        tx_filters = {'transcript_id': tx_id}
        tx_obj = session.query(Transcript).filter_by(**tx_filters).first()
        if tx_obj is None:
            # create new transcript and link with gene
            tx_obj = Transcript(**tx_filters)
            tx_obj.gene = gene_obj

        if tx_obj not in exon_obj.transcripts:
            # link exon to the transcript
            exon_obj.transcripts.append(tx_obj)

    return exon_obj
