# -*- coding: utf-8 -*-
import logging

import click
from sqlalchemy.exc import IntegrityError

from chanjo.load.sambamba import rows as sambamba_rows
from chanjo.parse import sambamba
from chanjo.store import Store
from chanjo.utils import validate_stdin

logger = logging.getLogger(__name__)


@click.command()
@click.option('-s', '--sample', help='override sample id from file')
@click.option('-g', '--group', help='id to group related samples')
@click.argument('bed_stream', callback=validate_stdin,
                type=click.File(encoding='utf-8'), default='-', required=False)
@click.pass_context
def load(context, sample, group, bed_stream):
    """Load Sambamba output into the database for a sample."""
    chanjo_db = Store(uri=context.obj['database'])
    try:
        load_sambamba(chanjo_db, bed_stream, sample_id=sample, group_id=group)
    except IntegrityError:
        logger.error('sample already loaded, rolling back')
        chanjo_db.session.rollback()
        context.abort()


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
