# -*- coding: utf-8 -*-
"""
Command line interface (console entry points). Based on Click_.

.. _Click: http://click.pocoo.org/
"""
from datetime import date
import logging
import os
import pkg_resources

import click
import yaml

from chanjo import __version__, __title__
from chanjo.compat import text_type
from chanjo.log import init_log

logger = logging.getLogger(__name__)
TODAY = str(date.today())


class EntryPointsCLI(click.MultiCommand):
    """Add subcommands dynamically to a CLI via entry points."""

    def _iter_commands(self):
        """Iterate over all subcommands as defined by the entry point."""
        return {entry_point.name: entry_point for entry_point in
                pkg_resources.iter_entry_points('chanjo.subcommands.4')}

    def list_commands(self, ctx):
        """List the available commands."""
        commands = self._iter_commands()
        return commands.keys()

    def get_command(self, ctx, name):
        """Load one of the available commands."""
        commands = self._iter_commands()
        if name not in commands:
            click.echo("no such command: {}".format(name))
            ctx.abort()
        return commands[name].load()


@click.group(cls=EntryPointsCLI)
@click.option('-c', '--config', default='~/.chanjo.yaml',
              type=click.Path(), help='path to config file')
@click.option('-d', '--database', type=text_type,
              help='path/URI of the SQL database')
@click.option('-l', '--log-level', default='INFO')
@click.option('--log-file', type=click.Path())
@click.version_option(__version__, prog_name=__title__)
@click.pass_context
def root(context, config, database, log_level, log_file):
    """Clinical sequencing coverage analysis tool."""
    init_log(logging.getLogger(), loglevel=log_level, filename=log_file)
    logger.info("version {0}".format(__version__))

    # avoid setting global defaults in Click options, do it below when
    if os.path.exists(config):
        with open(config) as conf_handle:
            context.obj = yaml.load(conf_handle)
    else:
        context.obj = {}
    context.obj['database'] = (database or context.obj.get('database'))

    # update the context with new defaults from the config file
    context.default_map = context.obj
