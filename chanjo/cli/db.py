# -*- coding: utf-8 -*-
import json
import logging

import click

from chanjo.store.api import ChanjoDB
from chanjo.store.models import Sample

LOG = logging.getLogger(__name__)


@click.group('db')
@click.pass_context
def db_cmd(context):
    """Interact with the database for maintainance tasks."""
    context.obj['db'] = ChanjoDB(uri=context.obj['database'])


@db_cmd.command()
@click.option('--reset', is_flag=True, help='tear down existing db')
@click.pass_context
def setup(context, reset):
    """Initialize a new datbase from scratch."""
    if reset:
        LOG.info('tearing down existing database')
        context.obj['db'].tear_down()
    LOG.info('setting up new database')
    context.obj['db'].set_up()


@db_cmd.command()
@click.argument('sample_id', type=str)
@click.pass_context
def remove(context, sample_id):
    """Remove all traces of a sample from the database."""
    store = context.obj['db']
    LOG.debug('find sample in database with id: %s', sample_id)
    sample_obj = Sample.query.get(sample_id)
    if sample_obj is None:
        LOG.warning('sample (%s) not found in database', sample_id)
        context.abort()
    LOG.info('delete sample (%s) from database', sample_id)
    store.session.delete(sample_obj)
    store.save()


@db_cmd.command()
@click.option('--group-id', '-g')
@click.option('--sample-id', '-s')
@click.option('--pretty', '-p', is_flag=True)
@click.pass_context
def samples(context, group_id, sample_id, pretty):

    store = context.obj['db']
    query = store.sample(sample_id=sample_id, group_id=group_id)
    indent = None
    if pretty:
        indent=4
    click.echo(json.dumps([dict(result) for result in query], default=str, indent=indent))


@db_cmd.command()
@click.option('--group-id', '-g')
@click.option('--sample-id', '-s')
@click.option('--pretty', '-p', is_flag=True)
@click.pass_context
def transcripts(context, group_id, sample_id, pretty):

    store = context.obj['db']
    query = store.transcripts(sample_id=sample_id)
    indent = None
    if pretty:
        indent=4
    click.echo(json.dumps([dict(result) for result in query], default=str, indent=indent))


@db_cmd.command()
@click.option('--group-id', '-g')
@click.option('--sample-id', '-s')
@click.pass_context
def delete(context, group_id, sample_id):

    store = context.obj['db']
    if sample_id:
        store.delete_sample(sample_id=sample_id)
    elif group_id:
        store.delete_group(group_id=group_id)
