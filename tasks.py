#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

from invoke import run, task
from invoke.util import log


@task
def test():
  """Run the test runner."""
  run('python setup.py test', pty=True)


@task
def clean():
  """Clean up temporary files."""
  run('rm -r build/')
  run('rm -rf dist/')
  run('rm -rf chanjo.egg-info')
  run('find . -name __pycache__ -delete')
  log.info('Cleaned up')


@task(clean)
def publish(test=False):
  """Publish to the cheeseshop."""
  if test:
    run('python setup.py register -r test sdist upload -r test')
  else:
    run('python setup.py register bdist_wheel upload')
    run('python setup.py register sdist upload')
  log.info('Published new release')
