# -*- coding: utf-8 -*-
import logging

import click

from .api import ChanjoDB
from .models import Sample

log = logging.getLogger(__name__)


@click.group()
@click.pass_context
def db(context):
    """Interact with the database for maintainance tasks."""
    context.obj['db'] = ChanjoDB(uri=context.obj['database'])


@db.command()
@click.option('--reset', is_flag=True, help='tear down existing db')
@click.pass_context
def setup(context, reset):
    """Initialize a new datbase from scratch."""
    if reset:
        log.info('tearing down existing database')
        context.obj['db'].tear_down()
    log.info('setting up new database')
    context.obj['db'].set_up()


@db.command()
@click.argument('sample_id', type=str)
@click.pass_context
def remove(context, sample_id):
    """Remove all traces of a sample from the database."""
    db = context.obj['db']
    log.debug('find sample in database with id: %s', sample_id)
    sample_obj = Sample.query.get(sample_id)
    if sample_obj is None:
        log.warn('sample (%s) not found in database', sample_id)
        context.abort()
    log.info('delete sample (%s) from database', sample_id)
    db.session.delete(sample_obj)
    db.save()
