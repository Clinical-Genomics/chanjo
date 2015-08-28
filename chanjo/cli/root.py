# -*- coding: utf-8 -*-
"""
chanjo.cli
~~~~~~~~~~~

Command line interface (console entry points). Based on Click_.

.. _Click: http://click.pocoo.org/
"""
import sys

import click

import chanjo

from chanjo._compat import text_type
from chanjo.config import Config, CONFIG_FILE_NAME, markup
from chanjo.log import init_log, LEVELS
from chanjo.utils import EntryPointsCLI


@click.group(cls=EntryPointsCLI)
@click.option('-c', '--config', default=CONFIG_FILE_NAME, type=click.Path(),
              help='path to config file')
@click.option('-d', '--database', type=text_type,
              help='path/URI of the SQL database')
@click.option('-v', '--verbose', count=True)
@click.option('--log_file', type=click.Path())
@click.version_option(chanjo.__version__)
@click.pass_context
def root(context, config, database, verbose, log_file):
    """Clinical sequencing coverage analysis tool."""
    # setup logging
    from chanjo import logger
    loglevel = LEVELS.get(verbose, "WARNING")

    init_log(logger, loglevel=loglevel, filename=log_file)
    logger.info("version %s", chanjo.__version__)

    # avoid setting global defaults in Click options, do it below when
    # updating the config object
    context.obj = Config(config, markup=markup)
    context.obj['database'] = (database or
                               context.obj.get('database', 'coverage.sqlite3'))

    # update the context with new defaults from the config file
    context.default_map = context.obj
