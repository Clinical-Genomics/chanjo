# -*- coding: utf-8 -*-
import logging

import click

from chanjo.store.api import ChanjoDB
from chanjo.store.mongo import ChanjoMongoDB
from chanjo.store.models import Sample

LOG = logging.getLogger(__name__)


@click.group('db')
@click.pass_context
def db_cmd(context):
    """Interact with the database for maintainance tasks."""
    backend = context.obj['backend']
    if backend == 'mongodb':
        chanjo_db = ChanjoMongoDB(uri=context.obj['database'])
    else:
        chanjo_db = ChanjoDB(uri=context.obj['database'])
    
    context.obj['db'] = chanjo_db


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
    sample_obj = store.sample(sample_id)
    if sample_obj is None:
        LOG.warning('sample (%s) not found in database', sample_id)
        context.abort()
    LOG.info('delete sample (%s) from database', sample_id)
    store.session.delete(sample_obj)
    store.save()
