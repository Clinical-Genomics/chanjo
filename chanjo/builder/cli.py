# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import click

from .core import init_db
from ..utils import validate_stdin


@click.command()
@click.option(
  '-f', '--force', is_flag=True, help='overwrite database without warning')
@click.argument(
  'in_stream', callback=validate_stdin, type=click.File(encoding='utf-8'),
  default='-', required=False)
@click.pass_context
def build(context, in_stream, force):
  """Construct a new skeleton SQL interval store.

  \b
  IN_STREAM: Chanjo-style BED-file with interval definitions
  """
  try:
    # build a new skeleton SQL interval store
    init_db(
      chanjo_db=context.parent.db,
      bed_stream=in_stream,
      overwrite=force
    )

  except OSError as error:
    click.echo("[chanjo] %s already exists - use '--force' to overwrite."
               % error.filename)
