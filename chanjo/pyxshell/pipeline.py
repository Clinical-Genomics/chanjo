# -*- coding: utf-8 -*-

from functools import wraps
import itertools


class PipeLine(object):
  """
  A coroutine wrapper which enables pipelining syntax.

  :class:`PipeLine` allows you to flatten once-nested code just by wrapping
  your generators. The class provides combinators in the form of operators,
  allowing you to plug two generators together without having to nest lots of
  function calls. For example::

  >>> def summer(stdin):
  ...     sum = 0
  ...     for item in stdin:
  ...         sum += item
  ...         yield sum
  >>> pipeline = PipeLine(lambda: iter([1, 2, 3, 4])) | PipeLine(summer)
  >>> pipeline
  <PipeLine: <lambda> | summer>
  >>> for item in pipeline:
  ...     print(item)
  1
  3
  6
  10

  The yielded output of each generator in the chain becomes the input for the
  next. The rules for writing a pipeline function are simple:
  :class:`PipeLine` requires a callable which accepts a single argument (the
  input), and returns an iterator. The only exception is the first part of
  the pipeline, which should accept no arguments (as there will be no input).

  To create pipeline functions, use the :func:`pipe` decorator::

  >>> @pipe
  ... def my_generator():
  ...     yield 1
  ...     yield 2
  ...     yield 3
  >>> pl = my_generator()
  >>> pl
  <PipeLine: my_generator>
  >>> for item in pl:
  ...     print(item)
  1
  2
  3

  If your pipeline accepts input, an iterator will be provided as the first
  argument to the function::

  >>> @pipe
  ... def add_one(input):
  ...     for item in input:
  ...         yield item + 1
  >>> pl = my_generator() | add_one()
  >>> pl
  <PipeLine: my_generator | add_one>
  >>> for item in pl:
  ...     print(item)
  2
  3
  4

  Even with input, your functions can still accept other parameters::

  >>> @pipe
  ... def adder(input, amount):
  ...     for item in input:
  ...         yield item + amount
  >>> pl = my_generator() | adder(3)
  >>> pl
  <PipeLine: my_generator | adder>
  >>> for item in pl:
  ...     print(item)
  4
  5
  6

  Some operators are overridden to provide pipeline combinators (methods
  which take multiple pipelines and return a new pipeline). For example,
  multiplying two pipelines gets you their cross product::

  >>> pl = my_generator() | (adder(3) * adder(6))
  >>> pl
  <PipeLine: my_generator | adder * adder>
  >>> for item in pl:
  ...     print(item)
  (4, 7)
  (4, 8)
  (4, 9)
  (5, 7)
  (5, 8)
  (5, 9)
  (6, 7)
  (6, 8)
  (6, 9)

  Adding two pipelines will chain the same input through both::

  >>> pl = my_generator() | (adder(3) + adder(12))
  >>> pl
  <PipeLine: my_generator | adder + adder>
  >>> for item in pl:
  ...     print(item)
  4
  5
  6
  13
  14
  15
  """

  __slots__ = ('coro_func',)

  def __init__(self, coro_func):
    self.coro_func = coro_func

  @property
  def __name__(self):
    return self.coro_func.__name__

  def __repr__(self):
    return '<PipeLine: %s>' % getattr(self.coro_func, '__name__',
                                      repr(self.coro_func))

  # in self
  def __iter__(self):
    return self.coro_func()

  # self | target
  def __or__(self, target):
    """
    Connect a pipe to something.

    If the target is a callable, try to call it as a pipe.

    NOTE: this does not work when connecting data structures to callable,
    like in: `range(5) | tee`,
    because we cannot overload function (FIXME?).

    >>> @pipe
    ... def echo(i):
    ...     yield i
    ...
    >>> @pipe
    ... def tee(l):
    ...     for i in l:
    ...         print(i)
    ...         yield i
    ...
    >>> list(echo("Brian") | tee())
    Brian
    ['Brian']
    >>> list(echo("Brian") | tee)
    Brian
    ['Brian']
    """
    # if target is a callable, the user may ask for a call to a PipeLine
    # without parenthesis, like in: `echo("Brian") | tee`
    if hasattr(target, '__call__'):
      # thus, try to call the target on the input pipe
      return target(iter(self))
    else:
      # if it is not a callable, it may be a pipeable
      # just connect it as a pipe
      return target.__ror__(self)

  # source | self
  def __ror__(self, source):
    r"""
    Connect something to a pipe so that one's output becomes
    the other's input.

    A simple example::

    >>> try:
    ...     from itertools import imap
    ... except ImportError:
    ...     imap = map
    >>> p = (PipeLine(lambda: iter([1, 2, 3, 4])) |
    ...      PipeLine(lambda stdin: imap(lambda x: x + 3, stdin)))
    >>> p
    <PipeLine: <lambda> | <lambda>>
    >>> list(p)
    [4, 5, 6, 7]
    """
    def pipe():
        return self.coro_func(iter(source))

    pipe.__name__ = '%s | %s' % (
      getattr(source, '__name__', repr(source)),
      getattr(self.coro_func, '__name__', repr(self.coro_func)))
    return PipeLine(pipe)

  # self > target
  def __gt__(self, target):
    """
    Redirect the generator output to a file or a variable.
    Erase the existing content of the target.

    >>> @pipe
    ... def echo(i):
    ...     yield i
    ...
    >>> import os
    >>> import sys
    >>> echo("Brian") > sys.stdout
    Brian
    >>> d=[] ; echo("Brian") > d ; print(d)
    ['Brian']
    >>> echo("Brian") > os.devnull
    """
    if isinstance(target, str):
      # w = erase existing content
      with open(target, "w") as fd:
        for line in iter(self):
          fd.write(line)

    elif hasattr(target, "write"):
      for line in iter(self):
        target.write(line)

    elif hasattr(target, "append"):
      # empty the target
      del target[:]
      for line in iter(self):
        target.append(line)
    else:
      raise TypeError

  # self >> target
  def __rshift__(self, target):
    """
    Append the generator output to a file or a variable.
    Do not erase the existing content.

    WARNING: this is an overloading of a binary operator, which have
    priority over |. You should thus use parenthesis around the generators
    sequence before using it.

    >>> @pipe
    ... def no(stdin):
    ...     for line in stdin:
    ...         yield line
    ...
    >>> import os
    >>> import sys
    >>> (["Bri", "an"] | no()) >> sys.stdout
    Brian
    >>> d = []
    >>> (["Bri", "an"] | no()) >> d
    >>> print(d)
    ['Bri', 'an']
    >>> (["Bri", "an"] | no()) >> os.devnull
    >>> try:
    ...     ["Bri", "an"] | no() >> sys.stdout
    ... except Exception as error:
    ...     print(error.__class__.__name__)
    TypeError
    """
    if isinstance(target, str):
      # a = append to file
      with open(target, "a") as fd:
        for line in iter(self):
          fd.write(line)

    elif hasattr(target, "write"):
      for line in iter(self):
        target.write(line)

    elif hasattr(target, "append"):
      for line in iter(self):
        target.append(line)
    else:
      raise TypeError

  # self * other
  def __mul__(self, other):
    """
    Yield the cross product between two alternative pipes.

    A simple example::

    >>> @pipe
    ... def echo(values):
    ...     for x in values:
    ...         yield x
    >>> list(echo([0, 1]) * echo([9, 10]))
    [(0, 9), (0, 10), (1, 9), (1, 10)]
    """
    def product(stdin=None):
      if stdin is None:
        return itertools.product(self, other)
      stdin1, stdin2 = itertools.tee(stdin, 2)
      return itertools.product((stdin1 | self), (stdin2 | other))
    product.__name__ = '%s * %s' % (
      getattr(self.coro_func, '__name__', repr(self.coro_func)),
      getattr(other, '__name__', repr(other)))
    return pipe(product)()

  # self + other
  def __add__(self, other):
    """
    Yield the chained output of two alternative pipes.

    Example::

    >>> @pipe
    ... def echo(values):
    ...     for x in values:
    ...         yield x
    >>> list(echo([1, 2, 3]) + echo([4, 5, 6]))
    [1, 2, 3, 4, 5, 6]
    """
    def concat(stdin=None):
      if stdin is None:
        return itertools.chain(self, other)
      stdin1, stdin2 = itertools.tee(stdin, 2)
      return itertools.chain((stdin1 | self), (stdin2 | other))
    concat.__name__ = '%s + %s' % (
      getattr(self.coro_func, '__name__', repr(self.coro_func)),
      getattr(other, '__name__', repr(other)))
    return pipe(concat)()


def pipe(func):
  """
  Wrap a function as a pipeline.

  >>> @pipe
  ... def printer(stdin, outfile=None):
  ...     for item in stdin:
  ...         print(item)
  ...         yield item
  ...
  >>> @pipe
  ... def echo(*values):
  ...     for value in values:
  ...         yield value
  ...
  >>> p = printer()
  >>> print(p)
  <PipeLine: printer>
  >>> p = echo(1, 2, 3) | p
  >>> print(p)
  <PipeLine: echo | printer>
  >>> output = list(p)
  1
  2
  3
  >>> output
  [1, 2, 3]
  """
  @wraps(func)
  def wrapper(*args, **kwargs):
    @wraps(func)
    def coro_func(stdin=None):
      if stdin is None:
        return func(*args, **kwargs)
      return func(stdin, *args, **kwargs)
    return PipeLine(coro_func)
  return wrapper
