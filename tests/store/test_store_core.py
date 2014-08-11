# -*- coding: utf-8 -*-
from chanjo.store import Store


class TestStore(object):
  def setup(self):
    self.store = Store(':memory:')
    self.store.set_up()

  def test_init(self):
    pass
