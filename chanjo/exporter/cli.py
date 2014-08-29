# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import click

from .core import export_intervals


@click.command()
@click.option(
  '--header/--no-header', is_flag=True, default=True, help="include headers")
@click.pass_context
def export(context, header):
  """Export an interval BED stream from an existing Chanjo store."""
  # build a new skeleton SQL interval store
  bed_lines = export_intervals(
    chanjo_db=context.parent.db,
    include_header=header
  )

  # reduce/write the BED lines
  for bed_line in bed_lines:
    click.echo(bed_line)
