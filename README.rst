
.. raw:: html

  <p align="center">
    <a href="http://chanjo.co">
      <img height="235"
           width="244"
           src="https://raw.githubusercontent.com/robinandeer/chanjo/master/assets/chanjo-logo.png"/>
    </a>
  </p>


.. image:: https://badge.fury.io/py/chanjo.png
  :target: http://badge.fury.io/py/chanjo
  :alt: PyPI version

.. image:: https://travis-ci.org/robinandeer/chanjo.png?branch=develop
  :target: https://travis-ci.org/robinandeer/chanjo
  :alt: Build Status

Chanjo
=======
Coverage analysis for clincal sequencing and beyond.

.. code-block:: console

  $ cat intervals.bed
  1  10 15 interval-1
  2  45 55 interval-2
  $ cat intervals.bed | chanjo annotate alignment.bam
  #{"sample_id": "bavewira", ...}
  1  10 15 interval-1  9.92231     0.97231
  2  45 55 interval-2  14.23123 1.0


Documentation
---------------
The redesigned documentation has all the information you want; getting started guide, foolproof installation instructions, and in-depth overviews.

I can specifically recommend the fully `interactive demo`_ with sample data to get you started right away.


Installation
-------------
Complete instructions are available in the documentation_ but installation (*can be*) as simple as running:

.. code-block:: console

  $ pip install chanjo


Contributors
-------------
Robin Andeer

Luca Beltrame (lbeltrame_)


License
--------
MIT


.. _documentation: https://chanjo.co/en/latest/
.. _interactive demo: http://www.chanjo.co/en/latest/introduction.html#demo
.. _lbeltrame: https://github.com/lbeltrame
