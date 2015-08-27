# -*- coding: utf-8 -*-
"""
chanjo.config.core
~~~~~~~~~~~~~~~~~~~

Works out of the box with any module that exposes the proper 'load' and
'dump' methods will work. Fox example 'toml' and 'yaml'.
"""
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
            self.user_data.update(self.markup.load(read_handle))
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

    def set(self, dot_key, value, base=None):
        """Update a config key-value pair."""
        section, key = _resolve_key((base or self), dot_key)
        # Set key-value pair
        section[key] = value
        return self


def _resolve_key(base, dot_key):
    """Resolve a "dot key" (e.g. person.age).

    Private method.

    Args:
        base (dict): nested dictionary
        dot_key (str):
    """
    # the key can be provided as a path to nested pairs
    key_parts = dot_key.split('.')
    key_parts.reverse()

    while len(key_parts) > 1:
        key_part = key_parts.pop()
        if key_part not in base:
            base[key_part] = {}
        base = base[key_part]

    return base, key_parts[0]
