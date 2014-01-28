#!/usr/bin/env python
# coding: utf-8

def group(intervals, threshold=1000, extend=0):
  """
  Groups and returns a list of intervals based on the length threshold.
  """
  # Initialize stuff
  it = iter(intervals)
  interval = next(it)

  iStart = interval[0]
  iEnd = interval[1]
  interval_id = interval[2]

  # This is where we store grouped intervals + interval ID
  group = [(iStart-extend, iEnd+extend, interval_id)]

  for interval in it:

    start = interval[0]
    end = interval[1]
    interval_id = interval[2]

    # Optionally extend (widen) the segments
    start -= extend
    end += extend

    # Updated the current combined interval
    iEnd = max(iEnd, end)

    # If the current combined interval is big enough
    if (iEnd - iStart) > threshold:
      # Return currently grouped intervals
      yield group

      # Start a new combined interval
      group = [(start, end, interval_id)]

      # Reset the combined interval bounderies
      iStart, iEnd = start, end

    else:
      # Extend the current combined interval
      group.append((start, end, interval_id))

  # Return the last group
  yield group
