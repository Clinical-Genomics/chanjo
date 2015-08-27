#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
chanjo.__main__
~~~~~~~~~~~~~~~~

The main entry point for the command line interface.

Invoke as ``chanjo`` (if installed) or ``python -m chanjo`` (no install
required).
"""
import sys

from .cli import cli


if __name__ == '__main__':
    # exit using whatever exit code the main returned
    sys.exit(cli())
