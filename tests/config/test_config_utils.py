# -*- coding: utf-8 -*-
from chanjo.config import remove_ansi


def test_remove_ansi():
  # Test a general case
  ansi_string = '[\x1b[32m?\x1b[0m] name: '
  assert remove_ansi(ansi_string) == '[?] name: '
