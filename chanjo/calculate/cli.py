# -*- coding: utf-8 -*-
import logging

import click

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
