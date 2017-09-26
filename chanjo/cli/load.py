# -*- coding: utf-8 -*-
import os.path
import logging
import sys

import click
from sqlalchemy.exc import IntegrityError

from chanjo.store.api import ChanjoDB
from chanjo.load.link import link_elements
from chanjo.load.sambamba import load_transcripts

LOG = logging.getLogger(__name__)


def validate_stdin(context, param, value):
    """Validate piped input contains some data.

    Raises:
        click.BadParameter: if STDIN is empty
    """
    # check if input is a file or stdin
    if value.name == '<stdin>' and sys.stdin.isatty():  # pragma: no cover
        # raise error if stdin is empty
        raise click.BadParameter('you need to pipe something to stdin')
    return value


@click.command()
@click.option('-s', '--sample', help='override sample id from file')
@click.option('-g', '--group', help='id to group related samples')
@click.option('-n', '--name', help='display name for sample')
@click.option('-gn', '--group-name', help='display name for sample group')
@click.option('-r', '--threshold', default=10,
              help='completeness level to disqualify exons')
@click.argument('bed_stream', callback=validate_stdin,
                type=click.File(encoding='utf-8'), default='-', required=False)
@click.pass_context
def load(context, sample, group, name, group_name, threshold, bed_stream):
    """Load Sambamba output into the database for a sample."""
    chanjo_db = ChanjoDB(uri=context.obj['database'])
    source = os.path.abspath(bed_stream.name)

    result = load_transcripts(bed_stream, sample_id=sample, group_id=group,
                              source=source, threshold=threshold)

    result.sample.name = name
    result.sample.group_name = group_name
    try:
        chanjo_db.add(result.sample)
        with click.progressbar(result.models, length=result.count,
                               label='loading transcripts') as bar:
            for tx_model in bar:
                chanjo_db.add(tx_model)
        chanjo_db.save()
    except IntegrityError as error:
        LOG.error('sample already loaded, rolling back')
        LOG.debug(error.args[0])
        chanjo_db.session.rollback()
        context.abort()


@click.command()
@click.argument('bed_stream', callback=validate_stdin,
                type=click.File(encoding='utf-8'), default='-', required=False)
@click.pass_context
def link(context, bed_stream):
    """Link related genomic elements."""
    chanjo_db = ChanjoDB(uri=context.obj['database'])
    result = link_elements(bed_stream)
    with click.progressbar(result.models, length=result.count,
                           label='adding transcripts') as bar:
        for tx_model in bar:
            chanjo_db.add(tx_model)
    try:
        chanjo_db.save()
    except IntegrityError:
        LOG.exception('elements already linked?')
        chanjo_db.session.rollback()
        click.echo("use 'chanjo db setup --reset' to re-build")
        context.abort()
