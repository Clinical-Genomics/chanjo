# -*- coding: utf-8 -*-
import sys

import click


def groupby_tx(exons, sambamba=False):
    """Group (unordered) exons per transcript."""
    transcripts = {}
    for exon in exons:
        if sambamba:
            ids = zip(exon['extraFields'][-3].split(','),
                      exon['extraFields'][-2].split(','),
                      exon['extraFields'][-1].split(','))
        else:
            ids = exon['elements']
        elements = {}
        for tx_id, gene_id, symbol in ids:
            elements[tx_id] = dict(symbol=symbol, gene_id=gene_id)
        exon['elements'] = elements

        for transcript_id in exon['elements']:
            if transcript_id not in transcripts:
                transcripts[transcript_id] = []
            transcripts[transcript_id].append(exon)
    return transcripts


def validate_stdin(context, param, value):
    """Validate piped input contains some data.

    Raises:
        click.BadParameter: if STDIN is empty
    """
    # check if input is a file or stdin
    if value.name == '<stdin>' and sys.stdin.isatty():  # pragma: no cover
        # raise error if stdin is empty
        raise click.BadParameter('you need to pipe something to stdin')
    return value
