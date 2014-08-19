# -*- coding: utf-8 -*-
"""
chanjo.read_depth.core
~~~~~~~~~~~~~~~~~~~~~~~
Closure for interfacing directly with BAM alignment files. Uses
:class:`Samfile` from pysam. It's used by Chanjo to read, read depths
across various genomics intervals.

Depends on the Pysam_ package and requires Samtools_ to be installed in
your ``$PATH`` to work. N.B. by installing *Pysam* through *pip*,
*Samtools* will by installed alongside.

.. _Pysam: http://www.cgat.org/~andreas/documentation/pysam/contents.html
.. _Samtools: http://samtools.sourceforge.net/
"""
from __future__ import absolute_import, unicode_literals
import errno
import os

from pysam import Samfile
from toolz import partial

try:
  import numpy as np
  # numpy dtype to use for read depths
  prealloc_func = partial(np.zeros, dtype=np.int_)

except ImportError:
  def prealloc_func(size, default=0):
    """Preallocate a list of "default"."""
    return [default] * size


def BamFile(bam_path):
  """Return enclosed function to read, read depths from the "bam_path".

  .. code-block:: python

    >>> from chanjo.read_depth import BamFile
    >>> read_depths = BamFile('./alignment.bam')

  Args:
    bam_path (path): path to alignment BAM-file

  Returns:
    function: function to read from the BAM-file
  """
  # raise an error if the file doesn't exist
  if not os.path.exists(bam_path):
    raise OSError(errno.ENOENT, bam_path)

  bam = Samfile(bam_path)
  try:
    bam.pileup()
  except ValueError:
    # catch error when BAM-file isn't indexed (+ ".bai" file)
    raise OSError(
      errno.ENOENT,
      "BAM-file (%s) must be indexed." % os.path.basename(bam_path)
    )

  def reader(contig, start, end):
    """Generate a list of read depths for each position (start, end).

    The `numpy` array is used to optimize performance when building and
    slicing the list.

    This function depends on `Pysam` >=0.7.5 since the ``truncate``
    option wasn't available in previous versions.

    .. code-block:: python

      >>> bamfile.read('17', 1, 5)
      array([3., 4., 4., 5., 4.])

    .. note::

      Positions are expected to be 1:1-based. In other words; if
      start=1, end=9 you should expect read depths for base pair
      positions 1-9 to be returned.

    Args:
      contig (str): contig/chromosome id (str) of interest
      start (int): first position of the interval (1-based)
      end (int): last position of the interval (1-based)

    Returns:
      list or numpy.array: array of read depths for *each* position in
        the interval
    """
    # convert start to 0-based since this is what pysam expects!
    pysam_start = start - 1

    # pysam expects contig as bytes in Python 2
    pysam_contig = str(contig)

    # check that we don't have a negative start position
    if pysam_start < 0:
      raise ValueError("Start position must be > 0, not %d" % start)

    # preallocate an array of 0 read depth for each position
    # pysam excludes positions with 0 read depth
    read_depths = prealloc_func(end - pysam_start)

    try:
      # overwrite read-covered positions (>0 read depth)
      # ``truncate`` ensures it starts and ends on the gives positions
      # note: ``col.pos`` is 0-based, as is ``pysam_start``
      for col in bam.pileup(pysam_contig, pysam_start, end, truncate=True):
        read_depths[col.pos - pysam_start] = col.n

    except ValueError as ve:
      # catch errors where the contig doesn't exist in the BAM-file
      raise ValueError(
        "Must use contig that exist in the Bam-file. Error: %s" % ve)

    return read_depths

  return reader
