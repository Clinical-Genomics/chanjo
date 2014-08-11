# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from functools import partial
import re

# regular expression to delete ANSI escape sequences (UNIX color codes)
# ref: http://stackoverflow.com/questions/14693701
ansi_escape = re.compile(r'\x1b[^m]*m')

remove_ansi = partial(ansi_escape.sub, '')
remove_ansi.__doc__ = """Remove ANSI escape characters from a string.

.. code-block:: python

  >>> ansi_string = '[\x1b[32m?\x1b[0m] name: '
  >>> remove_ansi(ansi_string)
  '[?] name: '

Args:
  ansi_string (str): string, possibly containing ANSI escape characters

Returns:
  str: input string *guaranteed* without ANSI escape characters
"""
