# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from codecs import open
import json
import toml

from click.utils import LazyFile
import pytest

from chanjo.config import Config


def test_init():
  # Test lazy loading (not pointing to a config file)
  config = Config()
  assert config.markup is json

  # Test loading with some defaults
  config = Config(defaults=dict(name='P.T. Anderson'))
  assert config['name'] == 'P.T. Anderson'

  # Test loading with an alternate markup engine
  config = Config(markup=toml)
  assert config.markup is toml

  # Test loading with a non-existent config file
  config = Config(LazyFile('tests/fixtures/nothing.json', 'w'))
  assert config == {}

  # Test loading with an existing config file
  config = Config(LazyFile('tests/fixtures/something.json', 'w'))
  assert config['title'] == 'Magnolia'


class TestConfig:
  def setup(self):
    self.defaults = {
      'type': 'movie',
      'person': {'name': 'P.T. Anderson', 'job': 'Director'}
    }
    self.config = Config(defaults=self.defaults)

  def test_load(self):
    # Test loading non-conflicting data
    with open('tests/fixtures/something.json', encoding='utf-8') as handle:
      self.config.load(handle)

    assert self.config['person']['name'] == 'P.T. Anderson'
    assert self.config['title'] == 'Magnolia'

    # Test loading conflicting data
    with open('tests/fixtures/conflict.json', encoding='utf-8') as handle:
      self.config.load(handle)

    assert self.config['name'] == 'Alfonso Cuarón'

    # Test loading with a non-supported markup engine
    self.config.markup = dict()
    with pytest.raises(NotImplementedError):
      with open('tests/fixtures/something.json', encoding='utf-8') as handle:
        self.config.load(handle)

    # Test loading config with bad syntax
    self.config.markup = json
    with pytest.raises(ValueError):
      with open('tests/fixtures/bad-syntax.json', encoding='utf-8') as handle:
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

    # Test set on a different scope (than ``self``)
    self.config.set('nested.key', 'value', scope=self.config.user_data)
    assert self.config.user_data['nested']['key'] == 'value'

  def test_unset(self):
    # Test removing a global setting
    assert self.config['type'] == 'movie'
    self.config.unset('type')
    assert self.config.get('type') is None

    # Test removing a nested setting
    assert self.config['person']['name'] == 'P.T. Anderson'
    self.config.unset('person.name')
    assert self.config['person'].get('name') is None

    # Test removing a whole sub-group of settings
    assert self.config['person'] is not None
    self.config.unset('person')
    assert self.config.get('person') is None

    # Test removing a setting in a different scope
    scope = {'person': {'name': 'Tarantino'}}
    self.config.unset('person.name', scope=scope)
    assert scope['person'].get('name') is None
