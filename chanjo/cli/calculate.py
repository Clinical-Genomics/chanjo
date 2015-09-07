# -*- coding: utf-8 -*-
import logging

import click

from chanjo.store import ChanjoAPI
from chanjo.store.utils import filter_samples
from .utils import dump_json

logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def calculate(context):
    """Calculate simple metrics from the database."""
    context.api = ChanjoAPI(uri=context.obj['database'])


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
        results = api.region_alt(chromosome, sample_id=sample, per=per)
    else:
        query = api.region(chromosome, start, end, sample_id=sample, per=per)
        results = ({'exon_id': exon_id, 'metrics': data}
                   for exon_id, data in query)
    if per == 'exon':
        dump_json(*results)
    else:
        dump_json(results)
