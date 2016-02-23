# -*- coding: utf-8 -*-
"""
chanjo.utils
~~~~~~~~~~~~~

A few general utility functions that might also be useful outside
Chanjo.
"""
import logging
import pkg_resources
import random
import sys

import click

logger = logging.getLogger(__name__)


def list_get(list_obj, index, default=None):
    """Like ``.get`` for list object.

    Args:
        list_obj (list): list to look up an index in
        index (int): index position to look up
        default (Optional[object]): default return value. Defaults to None.

    Returns:
        object: any object found at the index or ``default``
    """
    try:
        return list_obj[index]
    except IndexError:
        return default


def id_generator(size=8):
    """Randomly generate an id of length N (size) we can recognize.

    Think Italian or Japanese or Native American.
    Modified from: `Stackoverflow <http://stackoverflow.com/questions/2257441>`_
    and `ActiveState <http://code.activestate.com/recipes/526619/>`_.

    Args:
        size (Optional[int]): length of id, number of characters.
                              Defaults to 8.

    Returns:
        str: randomly generated string

    Examples:

    .. code-block:: python

        >>> id_generator()
        'palevedu'
        >>> id_generator(3)
        'sun'
    """
    variables = u'aeiou'
    consonants = u'bdfghklmnprstvw'

    return ''.join([random.choice(variables if i % 2 else consonants)
                    for i in range(size)])


def validate_stdin(context, param, value):
    """Validate piped input contains some data.

    Raises:
        click.BadParameter: if STDIN is empty
    """
    # check if input is a file or stdin
    if value.name == '<stdin>':
        # raise error if stdin is empty
        if sys.stdin.isatty():
            raise click.BadParameter('you need to pipe something to stdin')
    return value


class EntryPointsCLI(click.MultiCommand):

    """Add subcommands dynamically to a CLI via entry points."""

    def _iter_commands(self):
        """Iterate over all subcommands as defined by the entry point."""
        return {entry_point.name: entry_point for entry_point in
                pkg_resources.iter_entry_points('chanjo.subcommands.3')}

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
