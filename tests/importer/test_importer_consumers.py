# -*- coding: utf-8 -*-
from chanjo.importer import build_interval_data
from chanjo.store import Store


def test_build_interval_data():
  # setup
  chanjo_db = Store(':memory:')
  chanjo_db.set_up()

  sample_id = 'rokinerl'
  group_id = 'group1'
  interval_data = []
