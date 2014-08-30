# -*- coding: utf-8 -*-
from chanjo.exporter import export_intervals
from chanjo.store import Store


def test_exporter_pipeline():
  # set up
  chanjo_db = Store(':memory:')
  chanjo_db.set_up()
  chanjo_db.add(chanjo_db.create(
    'interval',
    interval_id='intervalY',
    contig='Y',
    start=123,
    end=501,
    strand='-'
  ))
  chanjo_db.save()

  bed_lines = list(export_intervals(chanjo_db))

  assert bed_lines[0] == '#chrom\tchromStart\tchromEnd\tname\tscore\tstrand'
  assert bed_lines[1:] == ['Y\t122\t501\tintervalY\t0\t-']
