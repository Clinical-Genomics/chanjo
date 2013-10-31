#!/usr/bin/env python
# coding: utf-8

def chromosomes(prepend="", extra=[]):
  # Stringify
  base = map(str, range(1,23))
  return [prepend + chrom for chrom in base + ["X", "Y"] + extra]
