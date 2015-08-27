# -*- coding: utf-8 -*-
import io
import json

import pytest
import yaml

from chanjo.config import Config


def test_init():
    fake_path = 'tests/fixtures/nothing.json'

    # Test lazy loading (not pointing to a config file)
    config = Config()
    assert config.markup is json

    # Test loading with some defaults
    config = Config(defaults=dict(name='P.T. Anderson'))
    assert config['name'] == 'P.T. Anderson'

    # Test loading with an alternate markup engine
    config = Config(markup=yaml)
    assert config.markup is yaml

    # Test loading with a non-existent config file
    config = Config(fake_path)
    assert config == {}

    # Test loading with an existing config file
    config = Config('tests/fixtures/something.json')
    assert config['title'] == 'Magnolia'


class TestConfig:
    def setup(self):
        self.defaults = {'type': 'movie',
                         'person': {'name': 'P.T. Anderson',
                                    'job': 'Director'}}
        self.config = Config(defaults=self.defaults)

    def test_load(self):
        # Test loading non-conflicting data
        path = 'tests/fixtures/something.json'
        with io.open(path, encoding='utf-8') as handle:
            self.config.load(handle)

        assert self.config['person']['name'] == 'P.T. Anderson'
        assert self.config['title'] == 'Magnolia'

        # Test loading conflicting data
        conflict_path = 'tests/fixtures/conflict.json'
        with io.open(conflict_path, encoding='utf-8') as handle:
            self.config.load(handle)

        assert self.config['name'] == u'Alfonso Cuarón'

        # Test loading with a non-supported markup engine
        self.config.markup = dict()
        with pytest.raises(NotImplementedError):
            with io.open(path, encoding='utf-8') as handle:
                self.config.load(handle)

        # Test loading config with bad syntax
        self.config.markup = json
        json_path = 'tests/fixtures/bad-syntax.json'
        with pytest.raises(ValueError):
            with io.open(json_path, encoding='utf-8') as handle:
                self.config.load(handle)

    def test_resolve_key(self):
        # Test simple case
        section, key = self.config._resolve_key('person.name')
        assert section == self.defaults['person']
        assert key == 'name'

        # Test with a different base
        section, key = self.config._resolve_key('person.job',
                                                base=self.config.user_data)
        assert section == {}  # 'user_data' is an empty ``dict`` in this case
        assert key == 'job'

    def test_set(self):
        # Test setting a global setting
        self.config.set('country', 'United States')
        assert self.config['country'] == 'United States'

        # Test setting a nested setting (in existing sub-group)
        self.config.set('person.name', 'Quentin Tarantino')
        assert self.config['person']['name'] == 'Quentin Tarantino'

        # Test setting a nested setting (in a new sub-group)
        self.config.set('bonus.joke', 'Knock, knock.')
        assert self.config['bonus']['joke'] == 'Knock, knock.'

        # Test multiple nested settings
        value = 'Do not ask me'
        self.config.set('what.is.this.useful.for', value)
        assert self.config['what']['is']['this']['useful']['for'] == value
