..  _development:

Development
======================

Git Branch Structure
---------------------

I attempt to follow the branch model laid out in `Successful Git Branching Model`_ .

``develop``
    Main development branch. Consider unstable.
``master``
    Production branch. `develop` folds into `master` for every new release.

Each release is tagged via GitHub on `master`.

.. _`Successful Git Branching Model`: http://nvie.com/posts/a-successful-git-branching-model/

Testing Chanjo
---------------
Coming soon.

Building Docs
---------------
Chanjo uses the slightly wierd `reStructuredText` markup language. The docs are then built using `Sphinx`. If you haven't already, install Sphinx::
  
  $ pip install sphinx

Now you can simply do the following to build the documentation as HTML::

  $ cd docs/
  $ make html

To open the docs, double-click ``docs/_build/html/index.html`` to open them in your default web browser.