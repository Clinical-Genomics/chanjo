# -*- coding: utf-8 -*-
"""
chanjo.cli
~~~~~~~~~~~

Command line interface (console entry points). Based on Click_.

.. _Click: http://click.pocoo.org/
"""
import logging
import click

from chanjo.compat import text_type
from chanjo.config import Config, CONFIG_FILE_NAME, markup
from chanjo.log import init_log, LEVELS
from chanjo.utils import EntryPointsCLI

from chanjo import __version__

logger = logging.getLogger(__name__)


def print_version(ctx, param, value):
    """Callback function for printing version and exiting
    Args:
        ctx (object) : Current context
        param (object) : Click parameter(s)
        value (boolean) : Click parameter was supplied or not
    Returns:
        None
    """
    if not value or ctx.resilient_parsing:
        return
    click.echo("chanjo version: {0}".format(__version__))
    ctx.exit()

@click.group(cls=EntryPointsCLI)
@click.option('-c', '--config',
                default=CONFIG_FILE_NAME,
                type=click.Path(),
                help='path to config file'
)
@click.option('-d', '--database',
                type=text_type,
                help='path/URI of the SQL database'
)
@click.option('-v', '--verbose',
                count=True,
                default=1,
                help="Increase output verbosity. Can be used multiple times, eg. -vv"
)
@click.option('--log_file',
                type=click.Path()
)
@click.option('--version',
                is_flag=True,
                callback=print_version,
                expose_value=False,
                is_eager=True
)
@click.pass_context
def root(context, config, database, verbose, log_file):
    """Clinical sequencing coverage analysis tool."""
    # setup logging
    loglevel = LEVELS.get(min(verbose, 2), 'WARNING')
    init_log(logging.getLogger(), loglevel=loglevel, filename=log_file)
    logger.info("version {0}".format(__version__))

    # avoid setting global defaults in Click options, do it below when
    # updating the config object
    context.obj = Config(config, markup=markup)
    context.obj['database'] = (database or
                               context.obj.get('database', 'coverage.sqlite3'))

    # update the context with new defaults from the config file
    context.default_map = context.obj
