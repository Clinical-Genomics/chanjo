# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from pkg_resources import iter_entry_points, load_entry_point

import click
from toolz import pipe
from toolz.curried import map

from ..utils import serialize_interval, validate_stdin


@click.command()
@click.option(
  '-a', '--adapter', default='ccds', help='plugin to use for conversion')
@click.option(
  '-l', '--list', 'list_all', is_flag=True, help='show all installed adapters')
@click.argument(
  'in_stream', callback=validate_stdin, type=click.File(encoding='utf-8'),
  default='-', required=False)
@click.pass_context
def convert(context, in_stream, adapter, list_all):
  """Convert a reference database file to a Chanjo BED interval file.

  \b
  IN_STREAM: interval reference file (e.g. CCDS database dump)
  """
  program_name = __package__.split('.')[0]

  if list_all:
    # list the installed converter options
    for entry_point in iter_entry_points('chanjo.converters'):
      # compose and print the message
      segments = dict(
        program=program_name,
        note=click.style('converter', fg='cyan'),
        plugin=entry_point.name
      )
      click.echo("%(program)s %(note)s %(plugin)s" % segments)

  else:
    try:
      # load a single entry point
      converter_pipeline = load_entry_point(
        program_name, 'chanjo.converters', adapter
      )
    except ImportError:
      segments = dict(
        program=program_name,
        note=click.style('error', fg='red'),
        message="No such converter installed: %s" % adapter
      )
      click.echo("%(program)s %(note)s %(message)s" % segments)
      context.abort()

    # execute converter pipeline
    bed_lines = pipe(
      converter_pipeline(in_stream),
      map(serialize_interval(bed=True))     # stringify/bedify
    )

    # reduce/write the BED lines
    for bed_line in bed_lines:
      click.echo(bed_line)
