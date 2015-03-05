# -*- coding: utf-8 -*-
"""
chanjo.cli
~~~~~~~~~~~

Command line interface (console entry points). Based on Click_.

.. _Click: http://click.pocoo.org/
"""
from __future__ import absolute_import, unicode_literals
import sys

import click

from . import __version__
from ._compat import text_type
from .config import Config, config_file_name, markup
from .log import logger, make_handler, LEVELS
from .store import Store
from .utils import EntryPointsCLI


@click.group(cls=EntryPointsCLI)
@click.option('-c', '--config', default=config_file_name,
              type=click.File('w', encoding='utf-8'),
              help='path to config file')
@click.option('--db', type=text_type, help='path/URI of the SQL database')
@click.option('-d', '--dialect', type=click.Choice(['sqlite', 'mysql']),
              help='type of SQL database')
@click.option('-v', '--verbose', count=True)
@click.option('-l', '--log', type=click.File('a', encoding='utf-8'),
              default=sys.stderr)
@click.version_option(__version__)
@click.pass_context
def cli(context, config, db, dialect, verbose, log):
  """Clinical sequencing coverage analysis tool."""
  # setup logging
  make_handler(log, level=LEVELS.get(min(verbose, 3)))
  logger.info("version %s", __version__)

  # avoid setting global defaults in Click options, do it below when
  # updating the config object
  context.obj = Config(config, markup=markup)

  # global defaults
  db_path = db or context.obj.get('db', 'coverage.sqlite3')
  db_dialect = dialect or context.obj.get('dialect', 'sqlite')

  context.db = Store(db_path, dialect=db_dialect)

  # update the context with new defaults from the config file
  context.default_map = context.obj
