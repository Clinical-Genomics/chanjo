# -*- coding: utf-8 -*-
"""
chanjo.config.core
~~~~~~~~~~~~~~~~~~~

Works out of the box with any module that exposes the proper 'load' and
'dump' methods will work. Fox example 'toml' and 'yaml'.
"""
from __future__ import absolute_import, unicode_literals
from codecs import open
import json

from click.termui import echo, style
from path import path

from .questions import questionnaire


class Config(dict):
  """Config object to store nested levels of config values.

  Reads values from a file and updates existing defaults. Can also save
  the updates key-value pairs back to a file.

  Customizable to use e.g. TOML, JSON, or YAML - it just requires an
  object with 'load' and 'dump' methods. Uses built in ``json`` module
  by default.

  Args:
    write_handle (file, optional): Handle to possibly existing file for
      writing to.
    defaults (dict, optional): Lowest priority default values
    markup (object, optional): Markup object, default: json
    save_options (dict, optional): Formatting when saving, e.g.
      ``{'indent': 4, 'sort_keys': True}``
  """
  def __init__(self, write_handle=None, defaults=None, markup=json,
               save_options=None):
    super(Config, self).__init__()
    self.user_data = {}
    self.write_handle = write_handle  # Write-enabled
    self.save_options = (save_options or {})

    # Trust the user knows what she's doing
    self.markup = markup

    # Update the defaults with config data
    self.update((defaults or {}))

    if write_handle:
      self.config_path = path(write_handle.name)

      if self.config_path.isfile():
        # Read data from possible config
        with open(self.config_path, encoding='utf-8') as read_handle:
          self.load(read_handle)

  def _resolve_key(self, dot_key, base=None):
    """Resolve a "dot key" (e.g. person.age).

    Private method.

    Args:
      dot_key (str):
    """
    # The key can be provided as a path to nested pairs
    key_parts = dot_key.split('.')
    key_parts.reverse()

    if base is None:
      section = self
    else:
      section = base

    while len(key_parts) > 1:
      key_part = key_parts.pop()
      if key_part not in section:
        section[key_part] = {}

      section = section[key_part]

    return section, key_parts[0]

  def dotget(self, dot_key, default=None, scope=None):
    # if scope is None:
    #   scope = self

    # section, key = self._resolve_key(dot_key, base=scope)

    # return section.get('key', default)
    raise NotImplementedError

  def set(self, dot_key, value, scope=None):
    """Update a config key-value pair."""
    if scope is None:
      scope = self

    section, key = self._resolve_key(dot_key, base=scope)

    # Set key-value pair
    section[key] = value

    return self

  def unset(self, dot_key, scope=None):
    """Delete a key-value pair."""
    scope = (scope or self)
    section, key = self._resolve_key(dot_key, base=scope)

    # Delete key-value pair
    del section[key]

    return self

  def load(self, read_handle):
    try:
      self.user_data.update(self.markup.load(read_handle))

      self.update(**self.user_data)

    except AttributeError:
      raise NotImplementedError(
        "Markup (%s) must expose a 'load'-method" % str(self.markup)
      )

    except ValueError as ex:
      raise ValueError("Bad syntax: %s" % ex)

    return self

  def save(self, **options):
    """Save the current key-value pairs using the write handle.

    Args:
      options (kwargs, optional): Options to pass to dump (like 'indent')

    Returns:
      Config: returns itself for chainability
    """
    options = (options or self.save_options)
    self.markup.dump(self.user_data, self.write_handle, **options)

    return self


def init_pipeline(program, config, questions):
  """Initializes a config object by interactively asking questions to a
  user. Non-pure."""
  if config.user_data:
    # Some existing user settings were found, warn about overwriting them
    message = "%(program)s %(note)s\tThe existing %(file)s will be updated"
    segments = dict(
      program=program,
      note=style('existing', fg='yellow'),
      file=style(config.config_path.basename(), fg='white')
    )

    echo(message % segments)

  # Launch questionnaire
  user_defaults = questionnaire(questions)

  # Set the selected user defaults
  for dot_key, value in user_defaults.items():
    config.set(dot_key, value, scope=config.user_data)

  # Write to the config file
  config.save()
