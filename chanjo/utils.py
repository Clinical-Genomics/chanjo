# -*- coding: utf-8 -*-
"""
chanjo.utils
~~~~~~~~~~~~~
A few general utility functions.
"""
import errno
import random
import sys

from docopt import docopt
from path import path

from . import rc


def id_generator(size=8):
  """Randomly generates an Id of length N (size) we can recognise.
  Think Italian or Japanese or Native American.

  Modified from: `Stackoverflow <http://stackoverflow.com/questions/2257441>`_
  and `ActiveState <http://code.activestate.com/recipes/526619-friendly-readable-id-strings/>`_.

  Usage:

  .. code-block:: python

    >>> id_generator()
    'G5G74W'
    >>> id_generator(3, '6793YUIO')
    'Y3U'

  Args:
    size (int, optional): Length of Id, number of characters.
    chars (str, optional): Pool of characters to choose from

  Returns:
    str: Randomly generated string
  """
  variables = 'aeiou'
  consonants = 'bdfghklmnprstvw'

  return ''.join([random.choice(variables if i % 2 else consonants)
                  for i in range(size)])


def open_or_stdx(file_path=None, open_args=('r',), force=False):
  """Opens a file or else returns a UNIX stream "stdin" (read from) or
  "stdout" (write to).

  Args:
    file_path (str, optional): Path to file, leave as ``None`` for
      the corresponding UNIX stream
    open_args (list, optional): List of arguments to pass to ``open``

  Returns:
    file: File handle for either the file or a UNIX stream
  """
  # Extend string with a path object
  # We need to use *or* since ``file_path`` can't be ``None``
  the_path = path(file_path or '/__nonexistant')

  # First case we are planning to **write** data
  if 'w' in open_args:
    if file_path is None:
      return sys.stdout

    else:
      # Unless we are sure to overwrite we should avoid it
      if not force and the_path.isfile():
        raise OSError(errno.EEXIST, the_path)

  else:
    # Now we are only interested in reading from an *existing* file
    if file_path is None:
      return sys.stdin

    else:
      # There is no point in reading from a file that doesn't exists,
      # but that's only me...
      if not force and not the_path.isfile():
        raise OSError(errno.ENOENT, the_path)

  # Open the file for reading or writing
  return the_path.open(*open_args)


def convert_old_interval_id(old_id):
  """Deprecated function for converting a 0:0-based exon Id to the
  new 1:1-based interval Id.

  Args:
    old_id (str): Old exon Id, '0:0-based'

  Returns:
    str: New interval Id, '1:1-based'
  """
  # Split into parts (contig, start, end)
  parts = old_id.split('-')

  # Recombine but with converted coordinates from 0:0 to 1:1
  return '-'.join([parts[0], str(int(parts[1]) + 1), str(int(parts[2]) + 1)])


def completeness(read_depths, threshold=10):
  """Calculates completeness across a number of positions.

  Note:
    The function catches the edge case where ``read_depths`` is an empty array
    which would lead to a ``ZeroDivisionError`` and returns 0% by default.

  Args:
    read_depths (array): :class:`numpy.array` of read depths for **each**
      of the positions
    threshold (int, optional): Cutoff to use for the filter

  Returns:
    float: The calculated completeness in percent
  """
  base_pair_count = len(read_depths)

  # Dodge rare division by zero error when `read_depths` is an empty array
  try:
    # Filter, then count bases with greater read depth than `threshold`
    # Divide by the total number of bases
    return len(read_depths[read_depths >= threshold]) / base_pair_count

  except ZeroDivisionError:
    # Without any bases to check, 0% pass the threshold
    return 0.


def assign_relative_positions(abs_start, abs_end, overall_start):
  """Return relative positions given the absolute positions and the overall
  starting position.

  Args:
    abs_start (int): Global start of the interval
    abs_end (int): Global end of the interval

  Returns:
    tuple of int: Relative start and end positions
  """
  rel_start = abs_start - overall_start
  rel_end = abs_end - overall_start

  return rel_start, rel_end


def merge_intervals(intervals):
  """Returns the ends of a groups list of intervals

  Args:
    intervals (list): List of intervals

  Returns:
    tuple of int: The beginning and end of the combined interval
  """
  try:
    return intervals[0][1], intervals[-1][2]

  except IndexError:
    # The interval group didn't contain any intervals... why?
    return (0, 0)


def read_config(script_name, docopt_string, args, config_path=None):
  # Extract docopt defaults
  defaults = rc.docopt_defaults(docopt_string)

  # Extract positional arguments only
  positional_args = {}
  for key, value in docopt(docopt_string, argv=args.grouped['_'].all).items():
    if key.startswith('<'):
      positional_args[key] = value

  # Extract command line options only with Clint
  options = {}
  for key, value in args.grouped.items():
    if key.startswith('--'):
      if value:
        options[key] = value.all[0]
      else:
        # Flag
        options[key] = True

  # Read values from potential config file
  name = rc.config_name(script_name, prefix='', affix='.json')
  config_path = config_path or path.joinpath(rc.config_location(), name)
  config = rc.read_config(config_path, config={}, docopt=True)

  # Replace defaults with config values
  defaults.update(config)
  # Replace config with command line arguments
  defaults.update(positional_args)
  defaults.update(options)

  return defaults
