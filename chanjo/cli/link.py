# -*- coding: utf-8 -*-
import logging

import click
from sqlalchemy.exc import IntegrityError

from chanjo.load import link as link_mod
from chanjo import load
from chanjo.parse import bed
from chanjo.store import Store
from chanjo.utils import validate_stdin
from chanjo.store.models import BASE
from chanjo.store.txmodels import BASE as TXBASE

logger = logging.getLogger(__name__)


@click.command()
@click.option('-t', '--transcripts', is_flag=True,
              help='focus only on transcripts on the database level')
@click.argument('bed_stream', callback=validate_stdin,
                type=click.File(encoding='utf-8'), default='-', required=False)
@click.pass_context
def link(context, transcripts, bed_stream):
    """Link related genomic elements."""
    only_tx = transcripts or context.obj.get('transcripts') or False
    base = TXBASE if only_tx else BASE
    chanjo_db = Store(uri=context.obj['database'], base=base)
    try:
        if only_tx:
            result = load.link_transcripts(bed_stream)
            with click.progressbar(result.models, length=result.count,
                                   label='adding transcripts') as bar:
                for tx_model in bar:
                    chanjo_db.session.add(tx_model)
            chanjo_db.save()
        else:
            link_elements(chanjo_db, bed_stream)
    except IntegrityError:
        click.echo("elements already linked, use 'chanjo db setup --reset' "
                   "to re-build")


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
