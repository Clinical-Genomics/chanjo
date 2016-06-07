# -*- coding: utf-8 -*-
import logging
from collections import namedtuple

from chanjo.compat import iteritems
from chanjo.store.models import Transcript
from .parse import bed as parse_bed
from .utils import groupby_tx

Result = namedtuple('Result', ['models', 'count'])
log = logging.getLogger(__name__)


def link_elements(sequence):
    """Process a sequence of exon lines.

    Args:
        sequence (sequence): list of chanjo bed lines

    Returns:
        Result: iterators of transcript models, number of transcripts processed
    """
    exons = parse_bed.chanjo(sequence)
    transcripts = groupby_tx(exons)
    models = (make_model(tx_id, exons) for tx_id, exons in
              iteritems(transcripts))
    return Result(models=models, count=len(transcripts))


def make_model(transcript_id, exons):
    """Generate transcript model from a list of exons.

    Args:
        transcript_id (str): unique transcript id
        exons (List[dict]): list of exon dictionaries

    Returns:
        Transcript: uncommitted transcript model
    """
    # assume the same chromosome and gene for all exons
    chromosome = exons[0]['chrom']
    gene_id = exons[0]['elements'][transcript_id]
    tot_length = sum((exon['chromEnd'] - exon['chromStart']) for exon in exons)
    tx_model = Transcript(id=transcript_id, chromosome=chromosome,
                          length=tot_length, gene_id=gene_id)
    return tx_model
