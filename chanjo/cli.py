# -*- coding: utf-8 -*-
"""
chanjo.cli
~~~~~~~~~~~

Command line interface (console entry points). Based on Click_.

.. _Click: http://click.pocoo.org/
"""
from __future__ import absolute_import, unicode_literals
import json
from pkg_resources import (
  iter_entry_points, load_entry_point, resource_filename, resource_listdir
)

import click
from path import path
import toml as markup
from toolz import pipe
from toolz.curried import map

from . import (
  __version__,
  __banner__,
  annotate_bed_stream,
  init_db,
  export_intervals,
  import_bed_stream,
  import_json,
  gender_from_bam
)
from ._compat import text_type
from .config import Config, init_pipeline
from .store import Store
from .utils import (
  serialize_interval_plus, serialize_interval, id_generator
)

CONFIG_NAME="%(program)s.%(extension)s" % dict(
  program=__package__,
  extension=markup.__name__  # Works for JSON, TOML, YAML ...
)

# shared options/arguments that don't belong to any specific command
# path to a BAM-file (without opening as a stream)
bam_path_argument = click.argument('bam_path', type=click.Path(exists=True))
# open an input stream from a file (usually a BED-file)
in_argument = click.argument(
  'in_stream', type=click.File(), default='-', required=False)
# open an output stream (default is stdout) to write to
out_option = click.option('--out', type=click.File('w'), default='-',
                          help="define an output file other than 'stdout'")
# string to prefix to the contig ids to match e.g. the BAM-file
prefix_option = click.option(
  '--prefix', default='', help='prefix a string to each contig'
)


@click.group()
@click.option(
  '--config',
  default=CONFIG_NAME,
  type=click.File('w'),
  help='path to config file')
@click.option('--db', type=text_type, help='path/URI of the SQL database')
@click.option(
  '--dialect',
  type=click.Choice(['sqlite', 'mysql']),
  help='type of SQL database')
@click.option(
  '--force', is_flag=True, help='overwrite existing assets without warning')
@click.option('--verbose', is_flag=True)
@click.version_option(__version__)
@click.pass_context
def cli(context, config, db, dialect, force, verbose):
  """Clinical sequencing coverage analysis tool."""
  # avoid setting global defaults in Click options, do it below when
  # updating the config object
  context.obj = Config(config, markup=markup)

  # global defaults
  db_path = db or context.obj.get('db', 'coverage.sqlite')
  db_dialect = dialect or context.obj.get('dialect', 'sqlite')

  context.db = Store(db_path, dialect=db_dialect)
  context.obj['force'] = force

  # update the context with new defaults from the config file
  context.default_map = context.obj


@cli.command()
@click.option('--remove', is_flag=True, help='remove config option')
@click.argument('key')
@click.argument('value', required=False)
@click.pass_context
def config(context, key, value, remove):
  """Only handles string values."""
  # update or delete the config key-value pair
  # the key can be provide as a path to nested commands: "user.name"
  if remove:
    context.obj.unset(key, scope=context.obj.user_data)

  else:
    if value is None:
      raise ValueError("Unless remove a setting, you must submit a 'value'")

    if value.isnumeric():
      value = int(value)

    context.obj.set(key, value, scope=context.obj.user_data)

  # persist updates to the config file
  context.obj.save()


@cli.command()
@click.pass_context
def init(context):
  """Walk user through setting up a new config file."""
  # print a nice welcome message
  click.echo(__banner__)

  questions = [
    ('annotate.cutoff', 'sufficient coverage',
      context.obj.get('annotate', {}).get('cutoff', 10)),
    ('dialect', 'preferred SQL-dialect', context.parent.db.dialect),
    ('db', 'central database path/URI', context.parent.db.uri)
  ]

  # launch init pipeline
  init_pipeline(__package__, context.obj, questions)


@cli.command()
@click.option('--adapter', default='ccds', help='plugin to use for conversion')
@click.option(
  'list_all', '--list', is_flag=True, help='show all installed adapters')
@out_option
@in_argument
@click.pass_context
def convert(context, in_stream, out, adapter, list_all):
  """Convert a reference database file to a Chanjo BED interval file.

  \b
  IN_STREAM: interval reference file (e.g. CCDS database dump)
  """
  if list_all:
    # list the installed converter options
    for entry_point in iter_entry_points('chanjo.converters'):
      # compose and print the message
      segments = dict(
        program=__package__,
        note=click.style('converter', fg='cyan'),
        plugin=entry_point.name
      )
      click.echo("%(program)s %(note)s %(plugin)s" % segments)

  else:
    try:
      # load a single entry point
      converter_pipeline = load_entry_point(
        __package__, 'chanjo.converters', adapter
      )
    except ImportError:
      segments = dict(
        program=__package__,
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
      click.echo(bed_line, file=out)


@cli.command()
@in_argument
@click.pass_context
def build(context, in_stream):
  """Construct a new skeleton SQL interval store.

  \b
  IN_STREAM: Chanjo-style BED-file with interval definitions
  """
  # build a new skeleton SQL interval store
  init_db(
    chanjo_db=context.parent.db,
    bed_stream=in_stream,
    overwrite=context.obj['force']
  )


@cli.command()
@out_option
@click.option(
  '--header/--no-header', is_flag=True, default=True, help="include headers")
@click.pass_context
def export(context, out, header):
  """Export an interval BED stream from an existing Chanjo store."""
  # build a new skeleton SQL interval store
  bed_lines = export_intervals(
    chanjo_db=context.parent.db,
    include_header=header
  )

  # reduce/write the BED lines
  for bed_line in bed_lines:
    click.echo(bed_line, file=out)


@cli.command()
@click.option('--sample', help='unique sample id (otherwise auto-generated)')
@click.option('--group', help='group id to associate samples e.g. in trios')
@click.option('--cutoff', default=10, help='cutoff for completeness')
@click.option(
  '--extend-by', default=0, help='dynamically extend intervals symetrically')
@prefix_option
@click.option(
  '--threshold',
  default=17000,
  help='base pair threshold for optimizing BAM-file reading')
@out_option
@bam_path_argument
@in_argument
@click.pass_context
def annotate(context, bam_path, in_stream, out, sample, group, cutoff,
             extend_by, prefix, threshold):
  """Annotate intervals in a BED-file/stream.

  \b
  BAM_PATH: Path to BAM-file
  IN_STREAM: Chanjo-style BED-file with interval definitions
  """
  # user defined sample id or randomly generated
  sample = (sample or id_generator())

  # step 1: metadata header
  metadata = dict(
    sample_id=sample,
    group_id=group,
    cutoff=cutoff,
    coverage_source=path(bam_path).abspath(),
    extension=extend_by
  )
  click.echo("#%s" % json.dumps(metadata), file=out)

  # step 2: annotate list of intervals with coverage and completeness
  bed_lines = pipe(
    annotate_bed_stream(
      bed_stream=in_stream,
      bam_path=bam_path,
      cutoff=cutoff,
      extension=extend_by,
      contig_prefix=prefix,
      bp_threshold=threshold
    ),
    map(serialize_interval_plus)    # stringify/bedify
  )

  # reduce/write the BED lines
  for bed_line in bed_lines:
    click.echo(bed_line, file=out)


@cli.command(name='import')
@click.option('--json', is_flag=True, help="use legacy JSON 'annotate' output")
@in_argument
@click.pass_context
def import_(context, in_stream, json):
  """Import coverage annotations to an existing database.

  \b
  IN_STREAM: Chanjo-style BED-file with interval definitions
  """
  args = (context.parent.db, in_stream)

  if json:
    # FYI: the ``bed_stream`` really is a JSON-file
    import_json(*args)
  else:
    import_bed_stream(*args)


@cli.command()
@click.argument(
  'location', type=click.Path(), default='./chanjo-demo', required=False)
@click.pass_context
def demo(context, location):
  """Copy demo files to a directory.

  \b
  LOCATION: directory to add demofiles to (default: ./chanjo-demo)
  """
  user_dir = path(location)
  demo_dir = path(resource_filename(__package__, 'demo'))

  # make sure we don't overwrite exiting files
  for demo_file in resource_listdir(__package__, 'demo'):
    user_file_path = user_dir.joinpath(demo_file)
    if user_file_path.exists():
      click.echo(user_file_path + ' exists. Pick a different location.')
      context.abort()

  try:
    # we can copy the directory(tree)
    demo_dir.copytree(user_dir)
  except OSError:
    click.echo('The location must be a non-existing directory.')
    context.abort()

  # inform the user
  click.echo("Successfully copied demo files to %s." % user_dir)


@click.command('sex-check')
@prefix_option
@click.version_option(__version__)
@bam_path_argument
def sex_check(bam_path, prefix):
  """Sex Check - predict gender from a BAM-alignment.

  \b
  BAM_PATH: path to BAM-file
  """
  # run the sex checker pipeline
  gender = gender_from_bam(bam_path, prefix=prefix)

  # print the results to the console for pipeability (csv)
  click.echo("#%(prefix)sX_coverage\t%(prefix)sY_coverage\tsex"
             % dict(prefix=prefix))
  click.echo('\t'.join(map(str, gender)))
