# -*- coding: utf-8 -*-
"""
chanjo.questions
~~~~~~~~~~~~~~~~~~
"""
from __future__ import absolute_import, unicode_literals

from click.termui import echo, style

# Python 2.x compatability
try:
  input = raw_input
except NameError:
  pass


def build_prompt(prompt, replacement=''):
  """Craft a prompt to ask a question.

  Provides a few modifications that should make it as simple as possible
  to ask questions.

  .. code-block:: python

    >>> build_prompt('name', '(Heisenberg)')
    'name: (Heisenberg)'
    >>> build_prompt('What is your name?', '(Heisenberg)')
    'What is your name? (Heisenberg)'
    >>> build_prompt('I %sed to China', '[style(walk, fg='red')]')
    'I [walk]ed to China'

  Args:
    prompt (str): Base prompt, ``%s`` will be substituted with 'replacement'
    replacement (str, optional): String to substitute ``%s`` with

  Returns:
    str: The full, modified prompt string
  """
  # prefix the question-prefix
  prompt = ("[%s] " % style('?', fg='green')) + prompt

  # determine whether it seems user has tried to format the prompt
  if '%s' not in prompt:
    # automate some formatting for the sake of convenience
    if not prompt.endswith(' '):
      if not prompt.endswith('?') or prompt.endswith(':'):
        prompt += ':'

    # add the default option to the end of prompt unless specified elsewhere
    prompt += " %s"

  # make the default-substitution and ensure an empty space at the end
  return (prompt % replacement).rstrip() + ' '


def ask(prompt, default=None, color='cyan'):
  """Ask a question, waits for user input.

  Replacement for "input". Updates the same line by replacing "default".

  .. code-block:: python

    >>> my_name = ask('Say my name: %s ', 'Heisenberg')
    # Wait for user input
    Say my name: (Heisenberg) Walter
    # Updates *the same* line with 'Walter' in green
    Say my name: Walter
    >>> print(my_name)
    Walter

  Inspired by 'bower_ init' which confirms user input by replacing the
  default option in line (ref_).

  Args:
    prompt (str): Question to print to user, '%s' will be replaced by default
    default (str, optional): Default option unless replaced by user
    color (str, optional): Some common color like 'red', 'green', 'yellow'

  Returns:
    str: User input or default

  .. _bower: http://bower.io/
  .. _ref: http://stackoverflow.com/questions/12586601
  """
  # helper variables
  MOVE_CURSOR_UP = '\x1b[1A'
  ERASE_LINE = '\x1b[2K'

  # determine if a default was submitted
  if default:
    # prepare the default-part of the prompt
    default_string = "(%s)" % default
  else:
    # not relevant since ``promt`` shouldn't include a '%s'
    default_string = ''

  # pass question to user and wait for response
  # write default option in parentheses, use it as response if nothing
  # was submitted by user.
  response = input(build_prompt(prompt, default_string)) or default

  # print the updated confirmation line by replacing the previous
  echo(MOVE_CURSOR_UP + ERASE_LINE
       + build_prompt(prompt, style(str(response) or '', fg=color)))

  return response


def questionnaire(questions, confirm_color='cyan'):
  """Ask a set of questions á la 'bower_ init'.

  Returns a dict with responses (or defaults). Abstraction for multiple
  consecutive calls to :func:`ask`.

  Note that the function doesn't try to be smart about what types
  (e.g. 'int' or 'str') the user is typing in. You should do any
  nessesary conversions downstream.

  .. code-block:: python

    >>> questions = [('name', 'Heisenberg'), ('age', 'How old are you?', 50)]
    >>> questionnaire(questions)
    name: (Heisenberg) Walter       # -> name: Walter
    How old are you? (25)           # -> How old are you? 25
    [out] {'age': 25, 'name': 'Walter'}

  Args:
    questions (list): List of tuples on the form:
      ``(<question id>, [<prompt>], [<default>])``.
    confirm_color str, optional): Some common color like to color the
      confirm messages.

  Returns:
    dict: Each question Id is returned with either user input or the
      default value (**unmodified**)

  .. _bower: http://bower.io/
  """
  # initialize dict to store responses (or defaults)
  responses = {}

  # ask each question to sending to :func:`ask`
  for question in questions:
    # save responses with question Ids
    responses[question[0]] = ask(*question[-2:], color=confirm_color)

  return responses
