# -*- coding: utf-8 -*-
"""Python 2.7.x, 3.2+ compatability module."""
import operator
import sys

is_py2 = sys.version_info[0] == 2


if not is_py2:  # pragma: no cover
    # Python 3
    from urllib.request import urlretrieve

    # strings and ints
    text_type = str
    string_types = (str,)
    integer_types = (int,)

    # lazy iterators
    zip = zip
    range = range
    iteritems = operator.methodcaller('items')
    iterkeys = operator.methodcaller('keys')
    itervalues = operator.methodcaller('values')

else:
    # Python 2
    from urllib import urlretrieve

    # strings and ints
    text_type = unicode
    string_types = (str, unicode)
    integer_types = (int, long)

    # lazy iterators
    range = xrange
    from itertools import izip as zip
    iteritems = operator.methodcaller('iteritems')
    iterkeys = operator.methodcaller('iterkeys')
    itervalues = operator.methodcaller('itervalues')
