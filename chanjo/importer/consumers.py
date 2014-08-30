# -*- coding: utf-8 -*-
from toolz import curry


@curry
def build_interval_data(chanjo_db, sample_id, group_id, interval_data):
  # create a new intervals data entry
  return chanjo_db.add(chanjo_db.create(
    'interval_data',
    parent_id=interval_data[3],
    sample_id=sample_id,
    group_id=group_id,
    coverage=float(interval_data[-2]),      # second to last field
    completeness=float(interval_data[-1])   # last field
  ))
