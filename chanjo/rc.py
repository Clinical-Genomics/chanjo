# -*- coding: utf-8 -*-
import sys
import errno
import json
from collections import OrderedDict

from clint import Args
from clint.textui import puts, colored, indent
from docopt import docopt
from path import path

from .config.questions import questionnaire


def read_config(config_path, config=None, docopt=False):
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


def config_name(script_name, prefix='.', affix='rc'):
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


def config_location(scope='local'):
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
  name = config_name(script_name, prefix='', affix='.json')
  config_path = path.joinpath(config_location(), name)

  # Guess that the owner of current dir has something to do with institute
  defaults = OrderedDict(institute=path('.').owner)
  defaults['cutoff'] = 10
  defaults['dialect'] = 'sqlite'
  defaults['db'] = './coverage.sqlite'

  # Read existing defaults if the file exists
  existing_defaults = read_config(config_path, config={})

  if existing_defaults:
    # There was already some config setup, warn about overwriting it
    puts('chanjo {note}\tThe existing {name} will be used and filled in'
         .format(note=colored.yellow('existing'), name=colored.white(name)))

  # Update the defaults with existing values (add+overwrite)
  defaults.update(existing_defaults)

  prompts = {
    'institute': 'What institute do you belong to?',
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


def rc_path(script_name, scope='local'):
  """Builds the path to the config file.

  Args:
    script_name (str): The name of the script/program, usually `__file__`
    scope (bool): Whether the config file is in cwd (or $HOME)
    dir_path (str): Pointer to parent dir of the config file, overrides
      'scope' (optional)

  Returns:
    str: path to the 
  """
  if path(scope).isdir():
    location = path(scope)
  else:
    location = rc_location(scope)

  return location.joinpath(rc_name(script_name))


def docopt_defaults(doc_string, args=sys.argv[1:], mandatory_args=None):
  """Returns the defaults as set in a docopt docstring.

  Args:
    doc_string (str): docopt formatted docstring
    mandatory_arguments (list, optional): list of non-optional arguments

  Returns:
    dict: Default set of command line arguments proceseed by docopt
  """
  # Extract only **non-optional** arguments (positional)
  # * Pass docopt pattern-matching with minimal arguments
  mandatory_args = mandatory_args or Args(args=args).grouped['_'].all

  return docopt(doc_string, argv=mandatory_args)
