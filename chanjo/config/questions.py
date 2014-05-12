# -*- coding: utf-8 -*-
"""
chanjo.questions
~~~~~~~~~~~~~~~~~~
"""
from clint.textui import puts, colored

# Python 2.x compatability
try:
  input = raw_input
except NameError:
  pass


def build_prompt(prompt, replacement=''):
  """Crafts a prompt to ask a question. Provides a few modifications
  that should make it as simple as possible to ask questions.

  .. code-block:: python

    >>> build_prompt('name', '(Heisenberg)')
    'name: (Heisenberg)'
    >>> build_prompt('What is your name?', '(Heisenberg)')
    'What is your name? (Heisenberg)'
    >>> build_prompt('I {}ed to China', '[colored.red(walk)]')
    'I [walk]ed to China'

  Args:
    prompt (str): Base prompt, ``{}`` will be substituted with 'replacement'
    replacement (str, optional): String to substitute ``{}`` with

  Returns:
    str: The full, modified prompt string
  """
  # Prefix the question-prefix
  prompt = '[{}] '.format(colored.green('?')) + prompt

  # Determine whether it seems user has tried to format the prompt
  if '{}' not in prompt:
    # Automate some formatting for the sake of convenience
    if not prompt.endswith(' '):
      if not prompt.endswith('?') or prompt.endswith(':'):
        prompt += ':'

    # Add the default option to the end of prompt unless specified elsewhere
    prompt += ' {}'

  # Make the default-substitution and ensure an empty space at the end
  return prompt.format(replacement).rstrip() + ' '


def ask(prompt, default=None, color=colored.cyan):
  """Meant to be used in place of input. Asks a question, waits for user
  input, updates the same line by replacing the default.

  .. code-block:: python

    >>> my_name = ask('Say my name: {} ', 'Heisenberg')
    # Wait for user input
    Say my name: (Heisenberg) Walter
    # Updates *the same* line with 'Walter' in green
    Say my name: Walter
    >>> print(my_name)
    Walter

  Inspired by 'bower_ init' which confirms user input by replacing the
  default option in line (ref_).

  Args:
    prompt (str): Question to print to user, '{}' will be replaced by default
    default (str, optional): Default option unless replaced by user
    color (function, optional): :func:`clint.textui.colored` function

  Returns:
    str: User input or default

  .. _bower: http://bower.io/
  .. _ref: http://stackoverflow.com/questions/12586601
  """
  # Helper variables
  MOVE_CURSOR_UP = '\x1b[1A'
  ERASE_LINE = '\x1b[2K'

  # Determine if a default was submitted
  if default:
    # Prepare the default-part of the prompt
    default_string = '({})'.format(default)
  else:
    # Not relevant since ``promt`` shouldn't include a '{}'
    default_string = ''

  # Pass question to user and wait for response
  # Write default option in parentheses, use it as response if nothing
  # was submitted by user.
  response = input(build_prompt(prompt, default_string)) or default

  # Print the updated confirmation line by replacing the previous
  puts(MOVE_CURSOR_UP + ERASE_LINE 
       + build_prompt(prompt, color(response or '')))

  return response


def questionnaire(questions, confirm_color=colored.cyan):
  """Asks a set of questions á la 'bower_ init' and returns a dict with
  responses (or defaults). Abstraction for multiple consecutive calls
  to :func:`ask`.

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
    questions (list): List of tuples on the form: (<question id>,
      [<prompt>], [<default>]).
    confirm_color (function): ``clint.textui.colored.xxx`` function to
      color the confirm messages.

  Returns:
    dict: Each question Id is returned with either user input or the
      default value (**unmodified**)

  .. _bower: http://bower.io/
  """
  # Initialize dict to store responses (or defaults)
  responses = {}

  # Ask each question to sending to :func:`ask`
  for question in questions:
    # Save responses with question Ids
    responses[question[0]] = ask(*question[-2:], color=confirm_color)

  return responses
