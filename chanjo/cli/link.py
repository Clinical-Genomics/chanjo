# -*- coding: utf-8 -*-
import click

from chanjo.load import link as link_mod
from chanjo.parse import bed
from chanjo.store import Store
from chanjo.utils import validate_stdin


@click.command()
@click.argument('bed_stream', callback=validate_stdin,
                type=click.File(encoding='utf-8'), default='-', required=False)
@click.pass_context
def link(context, bed_stream):
    """Load Sambamba output into the database for a sample."""
    chanjo_db = Store(uri=context.obj['database'])
    link_elements(chanjo_db, bed_stream)


def link_elements(chanjo_db, bed_iterable):
    """Load Sambamba BED output from a stream."""
    rows = bed.chanjo(bed_iterable)
    stats = link_mod.rows(chanjo_db.session, rows)
    for index, stat in enumerate(stats):
        chanjo_db.add(stat)
        if index % 10000 == 0:
            chanjo_db.save()

    chanjo_db.save()
