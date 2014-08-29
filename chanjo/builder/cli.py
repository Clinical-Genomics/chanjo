# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import click

from .core import init_db


@click.command()
@click.option(
  '-f', '--force', is_flag=True, help='overwrite database without warning')
@click.argument(
  'in_stream', type=click.File(encoding='utf-8'), default='-', required=False)
@click.pass_context
def build(context, in_stream, force):
  """Construct a new skeleton SQL interval store.

  \b
  IN_STREAM: Chanjo-style BED-file with interval definitions
  """
  # build a new skeleton SQL interval store
  init_db(
    chanjo_db=context.parent.db,
    bed_stream=in_stream,
    overwrite=force
  )
