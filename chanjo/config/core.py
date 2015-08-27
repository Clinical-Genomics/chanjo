# -*- coding: utf-8 -*-
"""
chanjo.config.core
~~~~~~~~~~~~~~~~~~~

Works out of the box with any module that exposes the proper 'load' and
'dump' methods will work. Fox example 'toml' and 'yaml'.
"""
from __future__ import absolute_import
import io
import json

from path import path


class Config(dict):

    """Config object to store nested levels of config values.

    Reads values from a file and updates existing defaults. Can also save
    the updates key-value pairs back to a file.

    Customizable to use e.g. TOML, JSON, or YAML - it just requires an
    object with 'load' and 'dump' methods. Uses built in ``json`` module
    by default.

    Args:
        config_path (Optional[path]): location of the config file
        defaults (Optional[dict]): lowest priority default values
        markup (Optional[object]): markup object, default: json
        save_options (Optional[dict]): formatting when saving, e.g.
            ``{'indent': 4, 'sort_keys': True}``
    """

    def __init__(self, config_path=None, defaults=None, markup=json,
                 save_options=None):
        super(Config, self).__init__()
        self.user_data = {}
        self.save_options = (save_options or {})
        # trust the user knows what she's doing
        self.markup = markup
        # update the defaults with config data
        self.update((defaults or {}))

        self.config_path = path(config_path) if config_path else None
        if self.config_path and self.config_path.isfile():
            # Read data from possible config
            with io.open(self.config_path, encoding='utf-8') as handle:
                self.load(handle)

    def load(self, read_handle):
        try:
            values = self.markup.load(read_handle) or {}
            self.user_data.update(values)
            self.update(**self.user_data)
        except AttributeError:
            raise NotImplementedError("Markup (%s) must expose a 'load'-method"
                                      % str(self.markup))
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

        with self.config_path.open('w') as write_handle:
            self.markup.dump(self.user_data, write_handle, **options)
        return self

    def set(self, dot_key, value, scope=None):
        """Update a config key-value pair."""
        if scope is None:
            scope = self
        section, key = self._resolve_key(dot_key, base=scope)
        # Set key-value pair
        section[key] = value
        return self

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
