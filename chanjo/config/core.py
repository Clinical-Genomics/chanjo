# -*- coding: utf-8 -*-
"""
chanjo.config.rc
~~~~~~~~~~~~~~~~~
"""
import sys
import json
from collections import OrderedDict

from clint.textui import puts, colored
from path import path

from .questions import questionnaire


def reader(config_path, config=None, docopt=False):
  config_path = path(config_path)

  # Raise an error for non-existing files
  if config_path.isfile():
    with config_path.open() as handle:
      # Read from the config file, overwrite the default
      config = json.load(handle)

    if docopt:
      # Convert to docopt style options
      for key, value in config.items():
        config['--' + key] = config.pop(key)

  return config


def prepare_questions(defaults, prompts):
  for key, value in defaults.items():
    yield (key, prompts.get(key, key), value)


def name(script_name, prefix='.', affix='rc'):
  """Return the name of a script without extentions (e.g. ".py")

  Args:
    script_name (str): name of the script file

  Returns:
    str: the name of the script wihtout extention
  """
  # Figure out the standard ".rc" config script_name
  parts = {
    'prefix': prefix,
    'script': path(script_name).namebase,
    'affix': affix
  }
  return '{prefix}{script}{affix}'.format(**parts)


def location(scope='local'):
  if scope == 'local':
    # Save absolute path to the current directory
    dir_path = path.getcwd()

  elif scope == 'global':
    # Assume 'global', meaning the config file is placed in the home dir.
    dir_path = path('~').expanduser()

  else:
    raise ValueError("scope can only be 'local' or 'global'")

  return dir_path


def init_pipeline(script_name, defaults={}):
  # Determine config path
  config_name = name(script_name, prefix='', affix='.json')
  config_path = path.joinpath(location(), config_name)

  # Guess that the owner of current dir has something to do with
  defaults = OrderedDict(cutoff=10)
  defaults['dialect'] = 'sqlite'
  defaults['db'] = './coverage.sqlite'

  # Read existing defaults if the file exists
  existing_defaults = reader(config_path, config={})

  if existing_defaults:
    # There was already some config setup, warn about overwriting it
    puts('chanjo {note}\tThe existing {name} will be used and filled in'
         .format(note=colored.yellow('existing'),
                 name=colored.white(config_name)))

  # Update the defaults with existing values (add+overwrite)
  defaults.update(existing_defaults)

  prompts = {
    'cutoff': 'Sufficient coverage',
    'dialect': 'Preferred SQL-dialect',
    'db': 'Central database path/URI'
  }

  # Combine defaults and prompts
  questions = prepare_questions(defaults, prompts)

  # Launch questionnaire
  user_defaults = questionnaire(questions)

  # Filter out values that are still ``None``
  user_defaults = filter_none(user_defaults)

  # Write to the config file
  with open(config_path, 'w') as config_file:
    json.dump(user_defaults, config_file, indent=4, sort_keys=True)


def filter_none(kwargs):
  return dict((key, value) for key, value in kwargs.items()
              if value is not None)
