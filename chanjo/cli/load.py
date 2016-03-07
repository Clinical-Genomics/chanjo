# -*- coding: utf-8 -*-
import os.path
import logging

import click
from sqlalchemy.exc import IntegrityError

from chanjo.load.sambamba import rows as sambamba_rows
from chanjo import load as load_mod
from chanjo.parse import sambamba
from chanjo.store import Store
from chanjo.utils import validate_stdin
from chanjo.store.models import BASE
from chanjo.store.txmodels import BASE as TXBASE

logger = logging.getLogger(__name__)


@click.command()
@click.option('-s', '--sample', help='override sample id from file')
@click.option('-g', '--group', help='id to group related samples')
@click.option('-t', '--transcripts', is_flag=True,
              help='focus only on transcripts on the database level')
@click.option('-r', '--threshold', type=int,
              help='completeness level to disqualify exons')
@click.argument('bed_stream', callback=validate_stdin,
                type=click.File(encoding='utf-8'), default='-', required=False)
@click.pass_context
def load(context, sample, group, transcripts, threshold, bed_stream):
    """Load Sambamba output into the database for a sample."""
    only_tx = transcripts or context.obj.get('transcripts') or False
    base = TXBASE if only_tx else BASE
    chanjo_db = Store(uri=context.obj['database'], base=base)
    try:
        if only_tx:
            source = os.path.abspath(bed_stream.name)
            load_transcripts(chanjo_db, bed_stream, sample=sample, group=group,
                             source=source, threshold=threshold)
        else:
            load_sambamba(chanjo_db, bed_stream, sample_id=sample,
                          group_id=group)
    except IntegrityError as error:
        logger.error('sample already loaded, rolling back')
        logger.debug(error.message)
        chanjo_db.session.rollback()
        context.abort()


def load_transcripts(chanjo_db, bed_stream, sample=None, group=None,
                     source=None, threshold=None):
    kwargs = dict(sample_id=sample, sequence=bed_stream,
                  group_id=group, source=source, threshold=threshold)
    result = load_mod.load_transcripts(**kwargs)
    with click.progressbar(result.models, length=result.count,
                           label='loading transcripts') as bar:
        for tx_model in bar:
            chanjo_db.session.add(tx_model)
    chanjo_db.save()


def load_sambamba(chanjo_db, bed_iterable, sample_id=None, group_id=None):
    """Load Sambamba BED output from a stream."""
    rows = sambamba.depth_output(bed_iterable)
    stats = sambamba_rows(chanjo_db.session, rows, sample_id=sample_id,
                          group_id=group_id)
    for index, stat in enumerate(stats):
        chanjo_db.add(stat)
        if index % 10000 == 0:
            chanjo_db.save()
            logger.info("processed %s annotations", index)

    chanjo_db.save()
    logger.info("processed %s annotations", index)
