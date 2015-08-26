# -*- coding: utf-8 -*-
"""
chanjo.utils
~~~~~~~~~~~~~

A few general utility functions that might also be useful outside
Chanjo.
"""
from __future__ import absolute_import, division, unicode_literals
import pkg_resources
import random
import sys

import click


def list_get(list_obj, index, default=None):
    """Like ``.get`` for list object."""
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
    size (int, optional): length of id, number of characters

  Returns:
    str: randomly generated string

  Examples:

  .. code-block:: python

    >>> id_generator()
    'palevedu'
    >>> id_generator(3)
    'sun'
  """
  variables = 'aeiou'
  consonants = 'bdfghklmnprstvw'

  return ''.join([random.choice(variables if i % 2 else consonants)
                  for i in range(size)])


def validate_stdin(context, param, value):
  """Validate piped input contains some data."""
  # check if input is a file or stdin
  if value.name == '<stdin>':
    # raise error if stdin is empty
    if sys.stdin.isatty():
      raise click.BadParameter('you need to pipe something to stdin')

  return value


def validate_bed_format(row):
  """Error check correct BED file formatting.

  Does a quick assert that row was successfully split into multiple
  fields (on tab-character).

  Args:
    row (list): list of BED fields

  Returns:
    None
  """
  assert len(row) >= 3, 'Bed Files must have at least 3 tab separated fields.'

  return True


class EntryPointsCLI(click.MultiCommand):
  """Add subcommands dynamically to a CLI via entry points."""
  def _iter_commands(self):
    """Iterate over all subcommands as defined by the entry point."""
    return {entry_point.name: entry_point for entry_point in
            pkg_resources.iter_entry_points('chanjo.subcommands')}

  def list_commands(self, ctx):
    """List the available commands."""
    commands = self._iter_commands()
    return commands.keys()

  def get_command(self, ctx, name):
    """Load one of the available commands."""
    commands = self._iter_commands()
    return commands[name].load()
