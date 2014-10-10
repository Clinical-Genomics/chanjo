# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from toolz.curried import get, map


def get_sample_id(bam_header):
  """Attempt to read sample ID directly from a BAM header ``dict``.

  Args:
    bam_header (dict): BAM file header as parsed by pysam

  Returns:
    str or None: sample ID if successful, otherwise ``None``
  """
  # grab all sample names in the file and merge identical IDs
  sample_ids = set(map(get('SM'), bam_header.get('RG', [])))

  if len(sample_ids) == 1:
    # this is OK, success
    return sample_ids.pop()

  else:
    # couldn't read sample ID
    return None
