# -*- coding: utf-8 -*-
import logging

import click
from sqlalchemy.orm.exc import NoResultFound

from chanjo.store import Store
from chanjo.store.models import ExonStatistic, Sample
from chanjo.store.models import BASE
from chanjo.store.txmodels import BASE as TXBASE

logger = logging.getLogger(__name__)


@click.group()
@click.option('-t', '--transcripts', is_flag=True,
              help='focus only on transcripts on the database level')
@click.pass_context
def db(context, transcripts):
    """Interact with the database for maintainance tasks."""
    only_tx = transcripts or context.obj.get('transcripts') or False
    base = TXBASE if only_tx else BASE
    context.db = Store(uri=context.obj['database'], base=base)


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
