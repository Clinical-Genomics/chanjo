# -*- coding: utf-8 -*-

"""
chanjo.rc
~~~~~~~~~~

Usage:

.. code-block:: python

  # Parse the document string and command line arguments
  args = docopt(__doc__, version='Parser 1.0')

  # Add defaults and user configs
  options = pythonrc(args)
"""

__title__ = 'rc'
__version__ = '0.0.1'
__author__ = 'Robin Andeer'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Robin Andeer'

import json
import os
import yaml

from path import path


def build_config_path(script_name, scope='local'):
  """
  <public> Build the path to the config file.

  :param str script_name: The name of the script/program, usually `__file__`
  :param bool scope:      Whether the config file is in cwd (or $HOME)
  :param str dir_path:    Pointer to parent dir of the config file,
                          overrides 'scope' (optional)
  """
  # Figure out the default .rc config script_name
  rc_name = '.{}rc'.format(path(script_name).basename().replace('.py', ''))

  if scope == 'local':
    # Save absolute path to the current directory
    dir_path = path.getcwd()
  elif scope == 'global':
    # Assume 'global', meaning the config file is placed in the home dir.
    dir_path = path('~').expanduser()
  else:
    # Check if scope if defined as a directory
    dir_path = path(scope)

    # The path needs to be an existing directory path
    if not dir_path.isdir():
      raise ValueError("'{}' must be either 'local', 'global' or an"
                       "existing directory path.".format(scope))

  return os.path.join(dir_path, rc_name)


def convert_docopt_args(dictionary):
  """
  <public>Converts a docopt argument dict to simpler names, more suitable
  for defining options in a config file.

  :param dict dictionary: docopt generated args dictionary
  :returns: Updated dictionary with simpler key names
  """
  new_dict = {}
  for key, value in dictionary.items():
    new_key = key
    if '--' in key:
      # Regular argument, remove leading '--'
      new_key = key.replace('--', '')

      # Avoid None-type
      if value:
        # Also update fake 'boolean' arguments
        if value.lower() in ('yes', 'true'):
          value = True
        elif value.lower() in ('no', 'false'):
          value = False

    elif '<' in key:
      # Positional argument, remove framing '<...>'
      new_key = key[1:-1]

    new_dict[new_key] = value

  return new_dict


def extend_args(args, script, defaults=None, scopes=['global', 'local']):
  """
  <public> Main function that updates the command line args with your
  sensible defaults and potential user configuration options.

  :param dict args: Command line arguments (e.g. from docopt function)
  :param str script: The name of the script (defines .<script>rc)
  :param dict defaults: (optional) Defaults for all/some of the arguments
  :param list scopes: (optional) Which config file(s) to consider: 'local'
                      (per folder), 'global' (`$HOME`), and/or custom path
  """
  # Set up options hash with provided defaults
  if defaults is None:
    defaults = {}

  for scope in scopes:
    # Get path to config file
    rc_path = build_config_path(script, scope=scope)

    # Check if the config file exists
    if rc_path.exists():
      # Open a file stream to the config file
      with rc_path.open('r') as stream:
        # Read in values from the config file
        # YAML is a superset of JSON so we can use the same parser independent
        # of how the config file is written.
        config = yaml.load(stream)

      # Merge defaults and config file options
      defaults.update(config)

  # Convert to simpler argument keys
  simple_args = convert_docopt_args(args)

  # Merge combo and command line options
  for key, value in simple_args.items():
    # If the user hasn't supplied a command line option ('falsy')
    if not value:
      # Don't do anyting if the option exists
      if key in defaults:
        continue

    # Replace/add the command line option to the final options
    defaults[key] = value

  # Serve the final options to the user
  return defaults


def write_config(contents, path_, type='json', overwrite=True):
  """
  <public> Writes/Overwrites a config file with (updated) values in one of
  the supported formats: JSON, YAML.

  :param dict contents: `Dict` with all options
  :param str path_: The path to write to
  :param str type: (optional) Format to write to, options: 'json', 'yaml'
  :param bool overwrite: (optional) Set `False` to raise exception before
                         overwriting an existing file.
  """
  if type == 'json':
    dump = json.dumps(contents)
  elif type == 'yaml':
    dump = yaml.dump(contents, allow_unicode=True, default_flow_style=False)
  else:
    raise ValueError("Only type 'json'/'yaml' are supported, not: " + type)

  if overwrite or not path_.exists():
    # Write/Overwrite file with new contents
    path_ = path(path_).write_text(dump)
  else:
    # The file already exists and the user has choosen not to overwrite it
    raise OSError(errno.EEXIST, path_)


def merge_arguments(defaults, configs, arguments):
  pass


def compare_arguments(defaults, prioritized, diff='--'):
  pass


def docopt_defaults(doc_string, mandatory_arguments=None):
  """Returns the defaults as set a docopt docstring.

  Args:
    doc_string (str): docopt formatted docstring
    mandatory_arguments (list, optional): list of non-optional arguments

  Returns:
    dict: Default set of command line arguments proceseed by docopt
  """
  # Extract only **non-optional** arguments (positional)
  # * Pass docopt patter matching with minimal arguments
  if not mandatory_arguments:
    mandatory_arguments = Args(args=args).grouped['_'].all

  return docopt(doc_string, argv=mandatory_arguments)
