# -*- coding: utf-8 -*-
import click

from chanjo.load import sambamba
from chanjo.parse import bed
from chanjo.store import Store
from chanjo.utils import validate_stdin


@click.command()
@click.argument('bed_stream', callback=validate_stdin,
                type=click.File(encoding='utf-8'), default='-', required=False)
@click.pass_context
def load(context, bed_stream):
    """Load Sambamba output into the database for a sample."""
    chanjo_db = Store(uri=context.obj['database'])
    load_sambamba(chanjo_db, bed_stream)


def load_sambamba(chanjo_db, bed_iterable):
    """Load Sambamba BED output from a stream."""
    rows = bed.chanjo(bed_iterable)
    stats = sambamba.rows(chanjo_db.session, rows)
    for index, stat in enumerate(stats):
        chanjo_db.add(stat)
        if index % 10000 == 0:
            chanjo_db.save()

    chanjo_db.save()
