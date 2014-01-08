..  _development:

Development
======================

Git Branch Structure
---------------------
I attempt to follow the branch model laid out in a `Successful Git Branching Model`_ .

``develop``
  Main development branch. Consider unstable.
``master``
  Production branch. `develop` folds into `master` for every new release.
``feature/<feture_name>``
  Experimental new features that might be merged into ``develop``.

Each release is tagged via GitHub on ``master`` following `Semantic Versioning 2`_.

Testing Chanjo
---------------
Coming soon. Right after the documentation is fleshed out.

Building Docs
---------------
Chanjo uses the slightly wierd `reStructuredText` markup language. The docs are then built using `Sphinx`. If you haven't already, install Sphinx:

.. code-block:: console
 
  $ pip install sphinx

Now you can simply do the following to build the documentation as HTML:

.. code-block:: console

  $ cd docs/
  $ make html
  $ open docs/_build/html/index.html

Or double-click ``docs/_build/html/index.html`` to open the documentation in your default web browser.

.. _`Successful Git Branching Model`: http://nvie.com/posts/a-successful-git-branching-model/

.. _`Semantic Versioning 2`: http://semver.org/
