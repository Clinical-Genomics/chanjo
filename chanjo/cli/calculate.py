# -*- coding: utf-8 -*-
import logging

import click

from chanjo.store import ChanjoAPI
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
    results = context.parent.api.mean(*samples)
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
@click.argument('start', type=int)
@click.argument('end', type=int)
@click.pass_context
def region(context, sample, per, chromosome, start, end):
    """Report mean statistics for a region of exons."""
    results = context.parent.api.region(chromosome, start, end,
                                        sample_id=sample, per=per)
    if per == 'exon':
        dump_json(*results)
    else:
        dump_json(results)
