# -*- coding: utf-8 -*-
import json
import logging

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
    if context.obj['database'] is None:
        LOG.warning('Please point to a database')
        context.abort()
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
