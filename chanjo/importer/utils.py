# -*- coding: utf-8 -*-


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
