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
@click.pass_context
def mean(context, pretty):
    """Calculate mean statistics."""
    query = context.obj['db'].mean()
    columns = ['sample_id'] + STAT_COLUMNS
    for sample in query:
        result = {column: value for column, value in zip(columns, sample)}
        click.echo(dump_json(result, pretty=pretty))


@calculate.command()
@click.option('-p', '--pretty', is_flag=True)
@click.argument('gene')
@click.pass_context
def gene(context, pretty, gene):
    """Calculate stats for a given gene."""
    query = context.obj['db'].gene_metrics(gene)
    columns = ['sample_id'] + STAT_COLUMNS + ['gene_id']
    for sample in query:
        result = {column: value for column, value in zip(columns, sample)}
        click.echo(dump_json(result, pretty=pretty))
