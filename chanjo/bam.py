# -*- coding: utf-8 -*-
"""
chanjo.bam
~~~~~~~~~~~

Adapter for interfacing directly with BAM alignment files. Inherits from
:class:`Samfile` which requires a second init parameter that tells it to
expect a *binary* BAM-file rather than the plain text cousin SAM-file format.

.. code-block:: python

  >>> from chanjo.bam import CoverageAdapter
  >>> bam_path = "/path/to/bam/file.bam"
  >>> adapter = CoverageAdapter(bam_path)

Args:
  bam_path (str): Path to a BAM alignment file

The default :class:`CoverageAdapter` that ships with Chanjo. Talks directly
to a BAM alignment file to extract read depth data.

Depends on the Pysam_ package and requires Samtools_ to be installed in your
``$PATH`` to work. N.B. by installing *Pysam* through *pip*, *Samtools* will
by installed alongside.

:copyright: (c) 2013 by Robin Andeer
:license: MIT, see LICENSE for more details

.. _Pysam: http://www.cgat.org/~andreas/documentation/pysam/contents.html
.. _Samtools: http://samtools.sourceforge.net/
"""
import errno

import numpy as np
from path import path
from pysam import Samfile


def BamFile(bam_path):
  """Generates a list of read depths for each position between (start, end).
  The `numpy` array is used to optimize performance when building and
  slicing the list.

  This method depends on `Pysam` >=0.7.5 since the `truncate` option wasn't
  available in previous versions.

  .. code-block:: python

    >>> adapter.read('17', 1, 5)
    array([3., 4., 4., 5., 4.])

  .. note::

    Positions are expected to be 1:1-based. In other words; if start=1,
    end=9 you should expect read depths for base pair positions 1-9 to
    be returned.

  Args:
    contig_id (str): The contig/chromosome Id (str) of interest
    start (int): The first position of the interval (1-based)
    end (int): The last position of the interval (1-based)

  Returns:
    numpy.array: Array of read depths for *each* position in the interval
  """
  # Raise an error if the file doesn't exist
  if not path(bam_path).exists():
    raise OSError(errno.ENOENT, bam_path)

  bam = Samfile(bam_path)

  def reader(contig_id, start, end):
    # Convert start to 0-based since this is what pysam expects!
    pysam_start = start - 1

    # Check that we don't have a negative start position
    if pysam_start < 0:
      raise ValueError('Start position must be >0, not %d' % start)

    # Generate a list of 0 read depth for each position (as defaults)
    positions = np.zeros(end - pysam_start)

    # Start Pileup iterator and walk through each position in the interval
    # `truncate` will make sure it starts and ends on the given positions!
    # Pysam already expects 'end' to be 1-based - how convenient!
    try:
      for col in bam.pileup(str(contig_id), pysam_start, end, truncate=True):
        # Overwrite the read depth in the correct position
        # This will allow simple slicing to get at the positions of interest
        # Note: ``col.pos`` is 0-based, as is ``pysam_start``
        positions[col.pos - pysam_start] = col.n
    except ValueError:
      # Catch errors where the contig didn't exist in the BAM-file
      raise ValueError('Must use contig ids that exist in the Bam-file')

    return positions

  return reader
