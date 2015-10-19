# -*- coding: utf-8 -*-
import logging

import click

from chanjo.load import link as link_mod
from chanjo.parse import bed
from chanjo.store import Store
from chanjo.utils import validate_stdin

logger = logging.getLogger(__name__)


@click.command()
@click.argument('bed_stream', callback=validate_stdin,
                type=click.File(encoding='utf-8'), default='-', required=False)
@click.pass_context
def link(context, bed_stream):
    """Link related genomic elements."""
    chanjo_db = Store(uri=context.obj['database'])
    link_elements(chanjo_db, bed_stream)


def link_elements(chanjo_db, bed_iterable, batch_size=10000):
    """Load Sambamba BED output from a stream."""
    rows = bed.chanjo(bed_iterable)
    stats = link_mod.rows(chanjo_db.session, rows)
    for index, stat in enumerate(stats):
        chanjo_db.add(stat)
        if index % batch_size == 0:
            chanjo_db.save()
            logger.debug('processed %s exons...', index)

    chanjo_db.save()
