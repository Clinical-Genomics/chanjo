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

from .cli import root_command


if __name__ == '__main__':
    # exit using whatever exit code the main returned
    sys.exit(root_command())
