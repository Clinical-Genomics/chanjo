# -*- coding: utf-8 -*-
import logging

import click
from sqlalchemy.orm.exc import NoResultFound

from chanjo.store import Store
from chanjo.store.models import ExonStatistic, Sample

logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def db(context):
    """Interact with the database for maintainance tasks."""
    context.db = Store(uri=context.obj['database'])


@db.command()
@click.option('--reset', is_flag=True, help='tear down existing db')
@click.pass_context
def setup(context, reset):
    """Initialize a new datbase from scratch."""
    if reset:
        logger.info('tearing down existing database')
        context.parent.db.tear_down()
    logger.info('setting up new database')
    context.parent.db.set_up()


@db.command()
@click.argument('sample_id', type=str)
@click.pass_context
def remove(context, sample_id):
    """Remove all traces of a sample from the database."""
    db = context.parent.db
    logger.debug('find sample in database with id: %s', sample_id)
    try:
        sample_obj = db.query(Sample).filter_by(sample_id=sample_id).one()
    except NoResultFound:
        logger.warn('sample (%s) not found in database', sample_id)
        context.abort()
    logger.debug('delete all related exon statistics')
    (db.query(ExonStatistic)
       .filter(ExonStatistic.sample_id == sample_obj.id)
       .delete())
    logger.debug('delete sample from database')
    db.session.delete(sample_obj)
    logger.info('remove sample (%s) from database', sample_id)
    db.save()
