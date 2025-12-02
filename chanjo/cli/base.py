# -*- coding: utf-8 -*-
"""
Command line interface (console entry points). Based on Click_.

.. _Click: http://click.pocoo.org/
"""
import logging
import os

try:
    from importlib.metadata import entry_points
except ImportError:  # Backport support for importlib metadata on Python 3.7
    from importlib_metadata import entry_points

import click
import coloredlogs
import yaml

from chanjo import __title__, __version__

LOG = logging.getLogger(__name__)

COMMAND_GROUP_KEY = "chanjo.subcommands.4"


class EntryPointsCLI(click.MultiCommand):
    """Add sub-commands dynamically to a CLI via entry points."""

    def _iter_commands(self):
        """Iterate over all sub-commands as defined by the entry point."""
        # Get all entry points for the specified group
        if hasattr(entry_points(), "select"):
            # Python >3.10, importlib
            eps = entry_points(group=COMMAND_GROUP_KEY)
        else:
            eps = entry_points().get(COMMAND_GROUP_KEY, [])
        return {ep.name: ep for ep in eps}

    def list_commands(self, ctx):
        """List the available commands."""
        commands = self._iter_commands()
        return commands.keys()

    def get_command(self, ctx, name):
        """Load one of the available commands."""
        commands = self._iter_commands()
        if name not in commands:
            click.echo(f"no such command: {name}")
            ctx.abort()
        return commands[name].load()


@click.group(cls=EntryPointsCLI)
@click.option(
    "-c", "--config", default="./chanjo.yaml", type=click.Path(), help="path to config file"
)
@click.option("-d", "--database", help="path/URI of the SQL database")
@click.option("-l", "--log-level", default="INFO")
@click.option("--log-file", type=click.File("a"))
@click.version_option(__version__, prog_name=__title__)
@click.pass_context
def root(context, config, database, log_level, log_file):
    """Clinical sequencing coverage analysis tool."""
    logout = log_file or click.get_text_stream("stderr")
    coloredlogs.install(level=log_level, stream=logout)
    LOG.debug("version %s", __version__)

    # Load configuration from the provided file
    if os.path.exists(config):
        with open(config) as conf_handle:
            context.obj = yaml.safe_load(conf_handle)
    else:
        context.obj = {}
    context.obj["database"] = database or context.obj.get("database")

    # Update the context with new defaults from the config file
    context.default_map = context.obj
