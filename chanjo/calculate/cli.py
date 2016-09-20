# -*- coding: utf-8 -*-
import logging

import click

from chanjo.compat import zip
from chanjo.store.api import ChanjoDB
from chanjo.store.constants import STAT_COLUMNS
from .utils import dump_json

log = logging.getLogger(__name__)


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
@click.option('-p', '--pretty', is_flag=True)
@click.argument('gene', nargs=-1)
@click.pass_context
def gene(context, pretty, gene):
    """Calculate stats for a given gene."""
    query = context.obj['db'].gene_metrics(*gene)
    columns = ['sample_id'] + STAT_COLUMNS + ['gene_id']
    for result in query:
        row = {column: value for column, value in zip(columns, result)}
        click.echo(dump_json(row, pretty=pretty))
