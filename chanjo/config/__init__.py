# -*- coding: utf-8 -*-
"""
chanjo.config
~~~~~~~~~~~~~~

Config module with Click integration.
"""
import yaml as markup

from .core import Config
from .questions import ask, build_prompt, questionnaire
from .utils import remove_ansi

CONFIG_FILE_NAME = ("{program}.{extension}"
                    .format(program='chanjo', extension=markup.__name__))
