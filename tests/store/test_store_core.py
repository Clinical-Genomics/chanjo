# -*- coding: utf-8 -*-
from chanjo.store import Store


class TestStore(object):
    def setup(self):
        self.store = Store('sqlite://')
        self.store.set_up()

    def test_init(self):
        pass


def test_lazy_load():
    """Test connection after post-init."""
    store = Store()

    store.connect('sqlite://')

    # ... but now we do!
    assert hasattr(store, 'query')
    assert store.dialect == 'sqlite'
