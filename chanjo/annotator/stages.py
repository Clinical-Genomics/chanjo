# -*- coding: utf-8 -*-
"""
chanjo.annotator.stages
~~~~~~~~~~~~~~~~~~~~~~~~

Pipeline stages only used by the Chanjo annotator.
"""
from __future__ import absolute_import
from operator import attrgetter

from toolz import curry, map

from ..utils import average, completeness

# function for getting the end of an interval (__doc__ is read only)
end_getter = attrgetter('end')


def assign_relative_positions(abs_start, abs_end, overall_start):
  """Return relative positions given the absolute interval positions.

  Bases the relative positions from an overall starting position.

  Args:
    abs_start (int): global start of the interval
    abs_end (int): global end of the interval
    overall_start (int): absolute start of overall group of intervals

  Returns:
    tuple of int: relative start and end positions
  """
  assert abs_start < abs_end, 'Interval must be positive'
  assert overall_start <= abs_start, "Interval must overlap 'overall'"

  rel_start = abs_start - overall_start
  rel_end = abs_end - overall_start

  return rel_start, rel_end


@curry
def calculate_metrics(interval_readDepth, threshold=10):
  """Calculate coverage and completeness for a range of read depths.

  Assumes a continous interval.

  TODO: in the future, Interval will hold coverage, completeness,
  read_depths etc.

  Args:
    interval (Interval): just passed on through
    read_depths (array): :class:`numpy.array` of read depths for
      **each** of the positions
    threshold (int, optional): cutoff to use for the completeness
      filter, defaults to 10

  Returns:
    tuple: the ``interval``, coverage, and completeness based on the
      read depth array
  """
  # unpack
  interval, read_depths = interval_readDepth

  return (
    interval,
    average(read_depths),
    completeness(read_depths, threshold=threshold)
  )


@curry
def extend_interval(interval, extension=0):
  """Extend interval symetrically.

  Args:
    interval (:class:`Interval`): Interval object
    extension (int, optional): length to extend interval with,
      defaults to 0

  Returns:
    Interval: interval with start and end replaced
  """
  # extend the interval in both directions, symetrically
  return interval._replace(
    start=interval.start - extension,
    end=interval.end + extension,
  )


@curry
def group_intervals(intervals, bp_threshold=1000):
  """Group and return lists of intervals based on the threshold.

  Args:
    intervals (list): list of intervals
    bp_threshold (int, optional): approx. combined length per group

  Yields:
    list of Interval: next group of intervals
  """
  # this is where we store grouped intervals
  group = []
  group_start = None
  group_end = 0
  last_contig = None

  for interval in intervals:
    # update the current combined interval
    # uses 'max' since some intervals overlap others (all we know is
    # that they are sorted on 'start' position)
    group_end = max(group_end, interval.end)

    # if the current combined interval is big enough or a new contig
    # has started
    new_contig = last_contig != interval.contig
    if new_contig or (group_end - group_start) > bp_threshold:
      # push currently grouped intervals
      if group:
        yield group

      # start a new combined interval group
      group = [interval]
      last_contig = interval.contig

      # reset the combined interval bounderies
      group_start, group_end = interval.start, interval.end

    else:
      # append to the current combined interval group
      group.append(interval)

  # push out the last group
  yield group


def merge_intervals(intervals):
  """Return the ends of a list of intervals.

  Args:
    intervals (list): list of intervals

  Returns:
    tuple of int: the beginning and end of the combined interval
  """
  if len(intervals) == 0:
    raise ValueError("'intervals' must contain at least one interval")

  overall_start = intervals[0].start
  overall_end = max(map(end_getter, intervals))

  return overall_start, overall_end


@curry
def prepend(value, sequence):
  """Prepend "value" to a sequence as ``value + sequence``.

  Args:
    value (variable): item to extend base sequence with
    sequence (sequence): extendable base sequence

  Returns:
    sequence: combination as ``value + sequence``
  """
  return value + sequence


@curry
def process_interval_group(bam, interval_group):
  """Fetch read depths for a group of :class:`Interval`s.

  Args:
    bam (BamFile): initialized BamFile instance
    interval_group (list): list of :class:`Interval`

  Yields:
    tuple of Interval, list: Interval and list of read depths
  """
  # contig is expected to be the same for all intervals
  contig = interval_group[0].contig

  # get the start and end of the group interval, 1:1-based
  overall_start, overall_end = merge_intervals(interval_group)

  # get read depths for the whole (full) group interval
  # => input should be 1:1-based
  read_depths = bam(contig, overall_start, overall_end)

  for interval in interval_group:
    # convert to relative positions for the interval
    # => 1:1-based, includes optional extension
    # => ouput can be considered as '0:0-based' (e.g. 1-1=0)
    args = (interval.start, interval.end, overall_start)
    rel_start, rel_end = assign_relative_positions(*args)

    # slice the overall read depth array with the relative coordinates
    # Python expects 0:1-based when slicing => +1 to 'rel_end'
    read_depth_slice = read_depths[rel_start:rel_end + 1]

    yield interval, read_depth_slice
