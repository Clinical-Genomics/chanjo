# -*- coding: utf-8 -*-
from chanjo.exporter import fetch_records
from chanjo.store import Store, Interval


def test_fetch_records():
  # set up
  chanjo_db = Store(':memory:')
  chanjo_db.set_up()
  chanjo_db.add(chanjo_db.create(
    'interval',
    interval_id='interval1',
    contig='chr1',
    start=10,
    end=100,
    strand='+'
  ))
  chanjo_db.save()

  columns = (Interval.contig, Interval.start, Interval.end)
  intervals = list(fetch_records(chanjo_db, columns))
  assert len(intervals) == 1
  assert intervals[0] == ('chr1', 10, 100)
