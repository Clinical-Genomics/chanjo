# -*- coding: utf-8 -*-
from chanjo.importer import convert_old_interval_id


def test_convert_old_interval_id():
  # test simple case, chromosome 1, position 10 -> 15
  assert convert_old_interval_id('1-10-15') == '1-11-16'

  # test with 'chr' prefix on chromosome id
  assert convert_old_interval_id('chrX-588234-588847') == 'chrX-588235-588848'

  # test edge case with 0
  assert convert_old_interval_id('Y-0-1201') == 'Y-1-1202'
