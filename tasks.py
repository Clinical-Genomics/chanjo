#!/usr/bin/env python
# -*- coding: utf-8 -*-
from invoke import run, task
from invoke.util import log


@task
def test():
    """Run the test runner."""
    run('python setup.py test', pty=True)


@task
def clean():
    """clean - remove build artifacts."""
    run('rm -rf build/')
    run('rm -rf dist/')
    run('rm -rf chanjo.egg-info')
    run("find . -name '*.pyc' -delete")
    run("find . -name '*.pyo' -delete")
    run("find . -name '*~' -delete")
    run('find . -name __pycache__ -delete')
    log.info('cleaned up')


@task(clean)
def publish():
    """Publish to the cheeseshop."""
    run('python setup.py sdist upload', pty=True)
    run('python setup.py bdist_wheel upload', pty=True)
    log.info('published new release')


@task
def coverage():
    """Run test coverage check and open HTML report."""
    run('coverage run --source chanjo setup.py test')
    run('coverage report -m')
    run('coverage html')
    run('open htmlcov/index.html')
    log.info('collected test coverage stats')


@task
def docs():
    """Build Sphinx documentation and display in browser."""
    run('make -C docs html')
    run('open docs/_build/html/index.html')
    log.info('built and displayed documentation')
