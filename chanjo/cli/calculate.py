# -*- coding: utf-8 -*-
import json
import logging
from pprint import pprint as pp

import click


from chanjo.store.api import ChanjoDB
from chanjo.store.constants import STAT_COLUMNS

LOG = logging.getLogger(__name__)


def dump_json(data, pretty=False):
    """Print JSON to console."""
    if pretty:
        json_args = dict(indent=4, sort_keys=True)
    else:
        json_args = {}
    return json.dumps(data, **json_args)


@click.group()
@click.pass_context
def calculate(context):
    """Calculate statistics across samples."""
    context.obj['db'] = ChanjoDB(uri=context.obj['database'])


@calculate.command()
@click.option('-p', '--pretty', is_flag=True)
@click.option('-s', '--sample', multiple=True, help='sample to limit query to')
@click.pass_context
def mean(context, sample, pretty):
    """Calculate mean statistics."""
    query = context.obj['db'].mean(sample_ids=sample)
    columns = ['sample_id'] + STAT_COLUMNS
    for result in query:
        row = {column: value for column, value in zip(columns, result)}
        click.echo(dump_json(row, pretty=pretty))

@calculate.command()
@click.option('-i', '--gene-id', type=int, help='Gene id for a gene')
@click.option('-s', '--sample', multiple=True, help='sample(s) to limit query to')
@click.option('-p', '--pretty', is_flag=True)
@click.pass_context
def gene(context, gene_id, sample, pretty):
    """Calculate average coverage for a gene"""
    if not (gene_id or gene_symbol):
        LOG.warning('Please specify a gene')
        context.abort()
    if not sample:
        LOG.warning('Please specify at least one sample')
        context.abort()
    
    for sample_id in sample:
        result = context.obj['db'].mean_cov_gene(gene_id, sample_id)
        if result is None:
            LOG.info("No result could be found")
            return
        row = {'average_coverage':result, 'sample_id': sample_id, 'gene': gene_id}
        click.echo(dump_json(row, pretty=pretty))
