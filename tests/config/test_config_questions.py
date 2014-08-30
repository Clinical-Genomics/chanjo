# -*- coding: utf-8 -*-
from chanjo.config import remove_ansi
from chanjo.config.questions import build_prompt


def test_build_prompt():
  # Test simple prompt
  prompt = '[?] name: (Heisenberg) '
  assert remove_ansi(build_prompt('name', '(Heisenberg)')) == prompt

  # Test custom prompt
  prompt = '[?] What is your name? (Heisenberg) '
  built_prompt = build_prompt('What is your name?', '(Heisenberg)')
  assert prompt == remove_ansi(built_prompt)

  # Test highly customized prompt (default not in the end)
  prompt = '[?] I [walk]ed to China '
  built_prompt = build_prompt('I %sed to China', '[walk]')
  assert prompt == remove_ansi(built_prompt)
