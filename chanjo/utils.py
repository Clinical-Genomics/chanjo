# -*- coding: utf-8 -*-
"""
chanjo.utils
~~~~~~~~~~~~~

A few general utility functions that might also be useful outside
Chanjo.
"""
from __future__ import absolute_import, division, unicode_literals
from collections import namedtuple
import random

from toolz import concat, curry

from ._compat import text_type


_RawInterval = namedtuple('RawInterval', [
  'contig', 'start', 'end', 'name', 'score', 'strand',
  'block_ids', 'superblock_ids'
])


class BaseInterval(_RawInterval):

  """Immutable interval tuple based on the `BED format`_.

  Args:
    contig (str): chromosome or generic contig id
    start (int): chromosomal start position, 1-based
    end (int): chromosomal end position, 1-based
    name (str, optional): unique name/id of interval
    score (int, optional): value between 0-1000, not used in Chanjo
    strand (str, optional): +/-
    block_ids (list, optional): list of unique block ids
    superblock_ids (list, optional): list of unique superblock ids

  .. _BED format: http://genome.ucsc.edu/FAQ/FAQformat.html#format1
  """

  def __new__(cls, contig, start, end, name='', score='', strand='',
              block_ids=None, superblock_ids=None):
    """Initialize a new namedtuple instance."""
    return super(BaseInterval, cls).__new__(
      cls,
      contig,
      start,
      end,
      name,
      score,
      strand,
      (block_ids or []),       # default to empty lists
      (superblock_ids or [])   # do
    )


def bed_to_interval(contig, bed_start, bed_end, name='', score='', strand='',
                    block_ids='', superblock_ids=''):
  """Convert from a BED row to an immutable BaseInterval object.

  Args:
    contig (str): chromosome or generic contig id
    start (str): chromosomal start position, 1-based
    end (str): chromosomal end position, 1-based
    name (str): unique name/id of interval
    score (str): value between 0-1000, not used in Chanjo
    strand (str): +/-
    block_ids (str): list of unique block ids for related blocks
    superblock_ids (str): list of unique superblock ids

  Returns:
    namedtuple: processed and sanity checked interval object
  """
  try:
    # assure positions to be integers
    # convert from 0,1-based to 1,1-based positions
    start = int(bed_start) + 1
    end = int(bed_end)
  except ValueError:
    raise ValueError("'start' and 'end' should be integers")

  # perform sanity check to check for incorrect formatting
  assert (end - start) > 0, ("Not a valid BED interval."
                             "(bedEnd - bedStart) must be > 0.")

  # fallback to empty list for optional element ids
  ids = [element_ids.split(',') if element_ids else []
         for element_ids in (block_ids, superblock_ids)]

  return BaseInterval(contig, start, end, name, score, strand, *ids)


def average(sequence):
  """Calculate the mean across an array of e.g. read depths.

  Defaults to the mean calculated using numpy and falls back to the
  naive Python solution.

  Args:
    sequence (list): ``numpy.array`` or list of values

  Returns:
    float: calculated average value
  """
  try:
    # first assume that numpy is installed for the fastest approach
    return sequence.mean()

  except AttributeError:
    # no numpy available, fall back to support regular list
    return sum(sequence) / len(sequence)


def completeness(read_depths, threshold=10):
  """Calculate completeness across a range of read depths.

  Note:
    This function catches the corner case where ``read_depths`` is an
    empty array which would lead to a ``ZeroDivisionError`` and returns
    0% by default.

  Args:
    read_depths (array): :class:`numpy.array` of read depths for
      **each** of the positions
    threshold (int, optional): cutoff to use for the filter

  Returns:
    float: calculated completeness in percent
  """
  base_pair_count = len(read_depths)

  # dodge rare division by zero error when `read_depths` is an empty array
  try:
    # filter, then count bases with greater read depth than `threshold`
    # divide by the total number of bases
    return len(read_depths[read_depths >= threshold]) / base_pair_count

  except ZeroDivisionError:
    # without any bases to check, 0% pass the threshold
    return 0.


@curry
def serialize_interval(interval, delimiter='\t', subdelimiter=',', bed=False):
  r"""Stringify :class:`BaseInterval`.

  Args:
    interval (:class:`BaseInterval`): interval object to serialize
    delimiter (str, optional): main delimiter, defaults to "\t"
    subdelimiter (str, optional): secondary delimiter, defaults to ","
    bed (bool, optional): convert to BED interval (0:1-based)

  Returns:
    str: stringified version of the :class:`BaseInterval`

  Examples:

  .. code-block:: python

    >>> interval = BaseInterval('chr1', 10, 100, score=14)
    >>> serialize_interval(interval)
    'chr1\t10\t100\t\t14'
  """
  # serialize the list of block/superblock Ids
  block_ids = subdelimiter.join(interval.block_ids)
  superblock_ids = subdelimiter.join(interval.superblock_ids)

  # on request, convert positions from 1:1 to BED-style 0:1
  if bed:
    base = interval._replace(start=interval.start - 1)[:6]
  else:
    base = interval[:6]

  return text_type.rstrip(
    delimiter.join(
      map(text_type, concat([base, [block_ids, superblock_ids]]))
    ),
    delimiter   # strip trailing delimiters
  )


@curry
def serialize_interval_plus(interval_combo, delimiter='\t', subdelimiter=','):
  r"""Stringify :class:`BaseInterval` with additional fields.

  Sometimes it's useful to use the ``BaseInterval`` with additional,
  non-standard fields tacked on to the end.

  Args:
    interval_combo (:class:`BaseInterval`, tuple): interval + list combo
    delimiter (str, optional): main delimiter, defaults to "\t"
    subdelimiter (str, optional): secondary delimiter, defaults to ","

  Returns:
    str: stringified version of the :class:`BaseInterval`

  Examples:

  .. code-block:: python

    >>> interval = BaseInterval('chr1', 10, 100, score=14)
    >>> serialize_interval([interval, 14.1, .94])
    'chr1\t10\t100\t\t14\t14.1\t0.94'
  """
  # split the interval combo tuple into components
  interval, rest = interval_combo[0], interval_combo[1:]

  return delimiter.join([
    serialize_interval(interval, delimiter, subdelimiter),
    delimiter.join(map(str, rest))
  ])


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

  return ''.join(
    [random.choice(variables if i % 2 else consonants) for i in range(size)]
  )


@curry
def split(string, sep='\t'):
  r"""Split string based on a delimiter/separator.

  This wrapper around ``str.split`` harmonize Python 2/3 syntax.

  Args:
    string (str): string to "explode"
    sep (str, optional): delimiter to separate on. Default: \t.

  Returns:
    list: "exploded" string parts as a list

  Examples:

  .. code-block:: python

    >>> split('change|of|pace', sep='|')
    ['change', 'of', 'pace']
  """
  return text_type.split(string, sep)
