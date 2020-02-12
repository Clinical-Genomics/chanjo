"""Functions for calculating operations on database"""
import json
import logging

import click

from chanjo.store.api import ChanjoDB
from chanjo.store.constants import STAT_COLUMNS, OMIM_GENE_IDS

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
@click.option('-p', '--pretty', is_flag=True, help="Print in pretty format")
@click.option('-s', '--sample', multiple=True, type=str, help="Sample to get coverage for")
@click.option('-o', '--omim', is_flag=True, help="Use genes in the OMIM panel")
@click.option('-f', '--gene-file',
              type=click.Path(exists=True),
              help="File with row separated gene IDs")
@click.argument('genes', nargs=-1)
@click.pass_context
def coverage(context, pretty, sample, omim, gene_file, genes):
    """Calculate coverage for sample on specified genes"""
    if omim:
        genes = OMIM_GENE_IDS
    if gene_file:
        with open(gene_file) as file_handle:
            genes = file_handle.read().strip().split("\n")
    query = context.obj['db'].sample_coverage(sample_ids=sample, genes=list(genes))
    click.echo(dump_json(query, pretty=pretty))
