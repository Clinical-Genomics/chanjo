# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import click

from .core import import_bed, import_json
from ..utils import validate_stdin


@click.command(name='import')
@click.option(
  '-j', '--json', is_flag=True, help="use legacy JSON 'annotate' output")
@click.argument(
  'in_stream', callback=validate_stdin, type=click.File(encoding='utf-8'),
  default='-', required=False)
@click.pass_context
def import_data(context, in_stream, json):
  """Import coverage annotations to an existing database.

  \b
  IN_STREAM: Chanjo-style BED-file with interval definitions
  """
  args = (context.parent.db, in_stream)

  if json:
    # FYI: the ``bed_stream`` really is a JSON-file
    import_json(*args)
  else:
    import_bed(*args)
