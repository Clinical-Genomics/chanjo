# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import collections
import fnmatch

from .pipeline import pipe


# Python 2/3 compatibility
if sys.version < '3':
  basestring = (str, unicode)
else:
  basestring = (bytes, str)


@pipe
def sleep(stdin, seconds):
  """
  Yield the current item after having waited a given number of seconds

  >>> for i in (range(2) | sleep(1)):
  ...     print(i)
  0
  1
  """
  for i in stdin:
    time.sleep(seconds)
    yield i


@pipe
def echo(item):
  """
  Yield a single item. Equivalent to ``iter([item])``, but nicer-looking.

  >>> list(echo(1))
  [1]
  >>> list(echo('hello'))
  ['hello']
  """
  yield item


@pipe
def cat(*args, **kwargs):
  r"""
  Read a file. Passes directly through to a call to `open()`.

  >>> src_file = __file__.replace('.pyc', '.py')
  >>> for line in cat(src_file):
  ...     if line.startswith('def cat'):
  ...          print(repr(line))
  'def cat(*args, **kwargs):\n'
  """
  return iter(open(*args, **kwargs))


@pipe
def tee(stdin, out=sys.stdout):
  """
  Save the input stream in a given file and forward it to the next pipe.

  >>> out = []
  >>> range(10) | map(str) | glue(",") | tee(sys.stdout) > out
  0,1,2,3,4,5,6,7,8,9
  >>> out
  ['0,1,2,3,4,5,6,7,8,9']
  """
  if out is None:
    for line in stdin:
      yield line
  else:
    if not hasattr(out, "write"):
      raise TypeError

    for line in stdin:
      out.write(str(line))
      yield line


@pipe
def head(stdin, size=None):
  """
  Yield only a given number of lines, then stop.

  If size=None, yield all the lines of the stream.

  >>> list(iter(range(10)) | head())
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  >>> list(iter(range(10)) | head(5))
  [0, 1, 2, 3, 4]
  >>> list(iter(range(10)) | head(0))
  []
  """
  count = 0
  for line in stdin:
    if size is not None and count >= size:
      raise StopIteration
    else:
      yield line
    count += 1


@pipe
def tail(stdin, size=None):
  """
  Yield  the given number of lines at the end of the stream.

  If size=None, yield all the lines. If size!=None, it will wait for the data
  stream to end before yielding lines.

  >>> list(iter(range(10)) | tail())
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  >>> list(iter(range(10)) | tail(5))
  [5, 6, 7, 8, 9]
  >>> list(iter(range(10)) | tail(0))
  []
  """
  if size is None:
    for line in stdin:
      yield line
  else:
    # to compute the size from the end, it is mandatory to expand
    # the generator in a list
    data = list(stdin)
    # once expanded, we can access via ranges
    for line in data[len(data) - size:]:
      yield line


@pipe
def skip(stdin, size=0):
  """
  Skip the given number of lines, then yield the remaining ones.

  >>> list(range(10) | skip(5))
  [5, 6, 7, 8, 9]
  >>> list(range(10) | skip())
  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
  """
  # first, loop that count
  count = 0
  for line in stdin:
    if count >= size:
      yield line
      break
    count += 1

  # then, simple loop
  for line in stdin:
    yield line


@pipe
def traverse(stdin):
  """
  Recursively browse all items, as if nested levels where flatten.
  Yield all items in the corresponding flatten list.

  >>> list([[1],[[2,3]],[[[4],[5]]]] | traverse())
  [1, 2, 3, 4, 5]
  """
  for item in stdin:
    try:
      if isinstance(item, str):
        yield item
      else:
        for i in traverse(item):
          yield i
    except TypeError:
      yield item  # not an iterable, yield the last item


@pipe
def wc(stdin, opt=None):
  """
  Return a list indicating the total number of [lines, words, characters]
  in the whole stream.

  >>> list([["It's every man's right to have babies if he wants them."],
  ...       ["But you can't have babies. "],
  ...       ["Don't you oppress me."]] | wc())
  [3, 20, 103]
  >>> list([["It's every man's right to have babies if he wants them."],
  ...       ["But you can't have babies. "],
  ...       ["Don't you oppress me."]] | wc("lines"))
  [3]
  >>> list([["It's every man's right to have babies if he wants them."],
  ...       ["But you can't have babies. "],
  ...       ["Don't you oppress me."]] | wc("words"))
  [20]
  >>> list([["It's every man's right to have babies if he wants them."],
  ...      ["But you can't have babies. "],
  ...      ["Don't you oppress me."]] | wc("characters"))
  [103]
  """
  lines = 0
  words = 0
  characters = 0
  # use traverse to un-nest any lists
  for data in traverse(stdin):
    lines += 1
    for w in data.split():
      words += 1
    for c in data:
      characters += 1

  res = {"lines": lines, "words": words, "characters": characters}
  if opt is None:
    # keys are given in a specific order, thus we cannot just use "in res"
    return iter([res[k] for k in ["lines", "words", "characters"]])
  else:
    return iter([res[opt]])


@pipe
def curl(url):
  """
  Fetch a URL, yielding output line-by-line.

  >>> UNLICENSE = 'http://unlicense.org/UNLICENSE'
  >>> for line in curl(UNLICENSE):  # doctest: +SKIP
  ...     print(line)
  This is free and unencumbered software released into the public domain.
  """
  import urllib2
  conn = urllib2.urlopen(url)
  try:
    line = conn.readline()
    while line:
      yield line
      line = conn.readline()
  finally:
    conn.close()


@pipe
def grep_e(stdin, pattern_src):
  """
  Filter strings on stdin for the given regex (uses :func:`re.search`).

  >>> list(iter(['cat', 'cabbage', 'conundrum', 'cathedral']) |
  ...      grep_e(r'^ca'))
  ['cat', 'cabbage', 'cathedral']
  """
  pattern = re.compile(pattern_src)
  for line in stdin:
    if pattern.search(line):
      yield line


def is_in(line, patterns=[]):
  for pattern in patterns:
    if hasattr(line, '__contains__'):
      if pattern in line:
        return True
    else:
      # for non iterable types (e.g. int)
      if pattern == line:
        return True
  return False


@pipe
def grep_in(stdin, patterns=[]):
  """
  Filter strings on stdin for any string in a given list (uses :func:`in`).

  >>> list(iter(['cat', 'cabbage', 'conundrum', 'cathedral']) |
  ...      grep_in(["cat","cab"]))
  ['cat', 'cabbage', 'cathedral']
  >>> list(range(10) | grep_in(5))
  [5]
  """
  # We may want to use grep_in(5) instead of grep_in([5])
  if not hasattr(patterns, '__contains__'):
    patterns = [patterns]

  for line in stdin:
    if is_in(line, patterns):
      yield line


@pipe
def grep(stdin, pattern):
  """
  Filters strings on stdin acconding to a given pattern.
  Use a regular expression if the pattern can be compiled,
  else use built-in operators (:func:`in` or :func:`==`).

  >>> list(range(10) | grep(5))
  [5]
  >>> list(range(10) | grep([5]))
  [5]
  >>> list(['cat', 'cabbage', 'conundrum', 'cathedral'] | grep('cat'))
  ['cat', 'cathedral']
  >>> list(['cat', 'cabbage', 'conundrum', 'cathedral'] | grep('^c.*e'))
  ['cabbage', 'cathedral']
  """
  try:
    # is pattern_src a regular expression?
    re.compile(pattern)
  except:
    # NO: use built-in comparison operators
    gen = grep_in
  else:
    # YES: use the re module
    gen = grep_e

  # use the good generator
  for line in gen(stdin, pattern):
    yield line


@pipe
def cut(stdin, fields=None, delimiter=None):
  """
  Yields the fields-th items of the strings splited as a list according
  to the delimiter.
  If delimiter is None, any whitespace-like character is used to split.
  If fields is None, every field are returned.

  >>> list(iter(["You don't NEED to follow ME",
  ...            "You don't NEED to follow ANYBODY!"]) | cut(1,"NEED to"))
  [' follow ME', ' follow ANYBODY!']
  >>> list(iter(["I say you are Lord",
  ...            "and I should know !",
  ...            "I've followed a few !"]) | cut([4]))
  [['Lord'], ['!'], ['!']]
  >>> list(iter(["You don't NEED to follow ME",
  ...            "You don't NEED to follow ANYBODY!"]) |
  ...      cut([0,1],"NEED to"))
  [["You don't ", ' follow ME'], ["You don't ", ' follow ANYBODY!']]
  >>> list(iter(["I say you are Lord",
  ...            "and I should know !",
  ...            "I've followed a few !"]) | cut([4,1]))
  [['Lord', 'say'], ['!', 'I'], ['!', 'followed']]
  """
  for string in stdin:
    if fields is None:
      yield string.split(delimiter)[:]
    elif isinstance(fields, collections.Iterable):
      data = string.split(delimiter)
      yield [data[i] for i in fields]
    else:
      yield string.split(delimiter)[fields]


@pipe
def join(stdin, delimiter=" "):
  """
  Join every list items in the input lines with the given delimiter.
  The default delimiter is a space.

  >>> list(iter(["- Yes, we are all different!\t- I'm not!"]) |
  ...      cut() | join())
  ["- Yes, we are all different! - I'm not!"]
  >>> list(iter(["- Yes, we are all different!\t- I'm not!"]) |
  ...      cut(delimiter="all") | join("NOT"))
  ["- Yes, we are NOT different!        - I'm not!"]
  """
  for lst in stdin:
    yield delimiter.join(lst)


@pipe
def glue(stdin, delimiter=" "):
  """
  Join every lines in the stream, using the given delimiter.
  The default delimiter is a space.

  >>> list([[[1], [2]], [[3], [4]], [[5], [6]]] |
  ...      traverse() | map(str) | glue(" "))
  ['1 2 3 4 5 6']
  """
  data = list(stdin)
  return iter([delimiter.join(data)])


@pipe
def append(stdin, val):
  """
  Yield the given item + val

  >>> list(range(5) | append(1) | map(str) | append(" ") |
  ...      map(list) | append([1]))
  [['1', ' ', 1], ['2', ' ', 1], ['3', ' ', 1], ['4', ' ', 1], ['5', ' ', 1]]
  """
  for i in stdin:
    yield i + val


@pipe
def prepend(stdin, val):
  """
  Yield the given val + item

  >>> list(range(5) | prepend(1) | map(str) | prepend(" ") |
  ...      map(list) | prepend([1]))
  [[1, ' ', '1'], [1, ' ', '2'], [1, ' ', '3'], [1, ' ', '4'], [1, ' ', '5']]
  """
  for i in stdin:
    yield val + i


@pipe
def dos2unix(stdin):
  """
  Replace DOS-like newline characters by UNIX-like ones.

  >>> list(iter(["dos\\r\\n","unix\\n"]) | dos2unix())
  ['dos\\n', 'unix\\n']
  """
  for line in stdin:
    yield line.replace("\r\n", "\n")


@pipe
def unix2dos(stdin):
  """
  Replace UNIX-like newline characters by DOS-like ones.

  >>> list(iter(["dos\\r\\n", "unix\\n"]) | unix2dos())
  ['dos\\r\\n', 'unix\\r\\n']
  """
  for line in stdin:
    yield line.replace("\r\n", "\n").replace("\n", "\r\n")


@pipe
def dir_file(paths):
  """
  Yields the file name and its absolute path in a tuple,
  expand home and vars if necessary.
  """
  for path in paths:
    p = os.path.abspath(path)
    yield (os.path.dirname(p), os.path.basename(p))


@pipe
def expand(filepatterns):
  """
  Yelds file names matching each 'filepatterns'.
  """
  if len(filepatterns) == 0:
    yield (i for i in [])

  for base_dir, filepattern in dir_file(filepatterns):
    for dirname, dirs, files in os.walk(base_dir):
      for filename in fnmatch.filter(files, filepattern):
        yield os.path.join(dirname, filename)


@pipe
def sed(stdin, pattern_src, replacement, exclusive=False):
  """
  Apply :func:`re.sub` to each line on stdin with the given pattern/repl.

  >>> list(iter(['cat', 'cabbage']) | sed(r'^ca', 'fu'))
  ['fut', 'fubbage']

  Upon encountering a non-matching line of input, :func:`sed` will pass it
  through as-is. If you want to change this behaviour to only yield lines
  which match the given pattern, pass `exclusive=True`::

  >>> list(iter(['cat', 'nomatch']) | sed(r'^ca', 'fu'))
  ['fut', 'nomatch']
  >>> list(iter(['cat', 'nomatch']) | sed(r'^ca', 'fu', exclusive=True))
  ['fut']
  """
  pattern = re.compile(pattern_src)
  for line in stdin:
    match = pattern.search(line)
    if match:
      yield (line[:match.start()] +
             match.expand(replacement) +
             line[match.end():])
    elif not exclusive:
      yield line


@pipe
def sort(stdin):
  data = list(stdin)
  return iter(sorted(data))


@pipe
def uniq(stdin):
  seen = set()
  for item in (x for x in stdin if x not in seen and not seen.add(x)):
    yield item


@pipe
def pretty_printer(stdin, **kwargs):
  """
  Pretty print each item on stdin and pass it straight through.

  >>> for item in iter([{'a': 1}, ['b', 'c', 3]]) | pretty_printer():
  ...     pass
  {'a': 1}
  ['b', 'c', 3]
  """
  import pprint
  for item in stdin:
    pprint.pprint(item, **kwargs)
    yield item


@pipe
def map(stdin, func):
  """
  Map each item on stdin through the given function.

  >>> list(range(5) | map(lambda x: x + 2))
  [2, 3, 4, 5, 6]
  """
  for item in stdin:
    yield func(item)


@pipe
def filter(stdin, predicate):
  """
  Only pass through items for which `predicate(item)` is truthy.

  >>> list(range(5) | filter(lambda x: x % 2 == 0))
  [0, 2, 4]
  """
  for item in stdin:
    if predicate(item):
      yield item


@pipe
def pairwise(iterable):
  """
  Iter over an iterable, two items by two items

  >>> list(range(10)|pairwise())
  [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9)]
  """
  a = iter(iterable)
  return zip(a, a)


@pipe
def sh(stdin, command=None, check_success=False):
  r"""
  Run a shell command, send it input, and produce its output.

  >>> print(''.join(echo("h\ne\nl\nl\no") | sh('sort -u')).strip())
  e
  h
  l
  o
  >>> for line in sh('echo Hello World'):
  ...     print(line.strip())
  Hello World
  >>> try:
  ...     for line in sh('false', check_success=True):
  ...         print(line.strip())  # doctest: +ELLIPSIS
  ... except Exception as error:
  ...     print(error.__class__.__name__.strip())
  <BLANKLINE>
  CalledProcessError
  """
  import subprocess
  import shlex

  if command is None:
    stdin, command = (), stdin

  if isinstance(command, basestring):
    command = shlex.split(command)

  pipe = subprocess.Popen(command,
                          stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE)

  pipe_stdin = " ".join(stdin)
  if sys.version[0] == '3':
    # FIXME: pipe.communicate() expects bytes string
    pipe_stdin = bytes(pipe_stdin, "utf-8")

  stdout, stderr = pipe.communicate(pipe_stdin)
  yield stdout.decode("utf-8")

  result = pipe.returncode
  if check_success and result != 0:
    raise subprocess.CalledProcessError(result, command)
