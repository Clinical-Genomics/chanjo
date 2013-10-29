#!/usr/bin/env python
# coding: utf-8

def group(intervals, threshold=1000):
  """
  Groups and returns a list of intervals based on the length threshold.
  """
  # Initialize stuff
  it = iter(intervals)
  iStart, iEnd = next(it)

  # This is where we store grouped intervals
  group = [(iStart, iEnd)]

  for start, end in it:

    # Updated the current combined interval
    iEnd = max(iEnd, end)

    # If the current combined interval is big enough
    if (iEnd - iStart) > threshold:
      # Return currently grouped intervals
      yield group

      # Start a new combined interval
      group = [(start, end)]

      # Reset the combined interval bounderies
      iStart, iEnd = start, end

    else:
      # Extend the current combined interval
      group.append((start, end))

  # Return the last group
  yield group
