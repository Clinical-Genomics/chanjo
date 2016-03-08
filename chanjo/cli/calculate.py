# -*- coding: utf-8 -*-
import logging

import click

from chanjo.store import ChanjoAPI
from chanjo.store.utils import filter_samples
from chanjo.store.models import BASE
from chanjo.store.txmodels import BASE as TXBASE
from .utils import dump_json

logger = logging.getLogger(__name__)


@click.group()
@click.option('-t', '--transcripts', is_flag=True,
              help='focus only on transcripts on the database level')
@click.pass_context
def calculate(context, transcripts):
    """Calculate simple metrics from the database."""
    only_tx = transcripts or context.obj.get('transcripts') or False
    base = TXBASE if only_tx else BASE
    context.api = ChanjoAPI(uri=context.obj['database'], base=base)


@calculate.command()
@click.argument('samples', nargs=-1)
@click.pass_context
def mean(context, samples):
    """Report mean coverage for a list of samples."""
    api = context.parent.api
    query = filter_samples(api.query(), sample_ids=samples)
    results = ({'sample_id': sample_id, 'metrics': data}
               for sample_id, data in api.means(query))
    dump_json(*results)


@calculate.command()
@click.argument('gene_ids', nargs=-1)
@click.pass_context
def gene(context, gene_ids):
    """Report aggregate statistics for particular genes."""
    results = context.parent.api.gene(*gene_ids)
    dump_json(*results)


@calculate.command()
@click.option('-s', '--sample', help='limit to a single sample')
@click.option('-p', '--per', type=click.Choice(['exon', 'sample']),
              help='report stats per sample/exon')
@click.argument('chromosome', type=str)
@click.argument('start', type=int, required=False)
@click.argument('end', type=int, required=False)
@click.pass_context
def region(context, sample, per, chromosome, start, end):
    """Report mean statistics for a region of exons."""
    api = context.parent.api
    if start is None:
        logger.debug('region id detected, parse string')
        try:
            results = api.region_alt(chromosome, sample_id=sample, per=per)
        except ValueError as error:
            click.echo(error.message)
            context.abort()
    else:
        results = api.region(chromosome, start, end, sample_id=sample, per=per)
    if per == 'exon':
        processed_results = ({'exon_id': exon_id, 'metrics': data}
                             for exon_id, data in results)
        dump_json(*processed_results)
    else:
        dump_json(results)
