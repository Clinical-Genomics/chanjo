# -*- coding: utf-8 -*-
"""
chanjo.config
~~~~~~~~~~~~~~

Config module with Click integration.
"""
from __future__ import absolute_import
import toml as markup

from .cli import init, config
from .core import Config, init_pipeline
from .questions import ask, build_prompt, questionnaire
from .utils import remove_ansi, rget


config_file_name="%(program)s.%(extension)s" % dict(
  program='chanjo',
  extension=markup.__name__  # Works for JSON, TOML, YAML ...
)
