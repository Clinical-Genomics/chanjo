#!/usr/bin/env python
# -*- coding: utf-8 -*-
from invoke import run, task
from invoke.util import log


@task
def test(context, track=False):
    """Run the test runner."""
    command = ('py.test --cov-report html --cov "$(basename "$PWD")" tests/ '
               '--verbose --color=yes -s')
    command += ' --ipdb' if track else ' --looponfail'
    run(command, pty=True)


@task
def clean(context):
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
def publish(context):
    """Publish to the cheeseshop."""
    run('python setup.py sdist upload', pty=True)
    run('python setup.py bdist_wheel upload', pty=True)
    log.info('published new release')


@task
def coverage(context):
    """Run test coverage check and open HTML report."""
    run('coverage run --source chanjo setup.py test')
    run('coverage report -m')
    run('coverage html')
    run('open htmlcov/index.html')
    log.info('collected test coverage stats')
