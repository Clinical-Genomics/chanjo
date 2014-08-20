# -*- coding: utf-8 -*-
from codecs import open

from chanjo.builder import init_db
from chanjo.store import Store


def test_builder_pipeline():
  """Test the entire builder pipeline."""
  chanjo_db = Store(':memory:')
  chanjo_db.set_up()

  # test with minimal BED "file"
  bed_stream = open('tests/fixtures/CCDS.mini.bed', 'r', encoding='utf-8')
  init_db(chanjo_db, bed_stream)

  block = chanjo_db.get('block', 'CCDS2.2')
  assert block.start == 12
  assert block.end == 35

  superblock = chanjo_db.get('superblock', 'RFPL2')
  assert superblock.start == 32586759
  assert superblock.end == 32589260

  block_ids = [block_.id for block_ in superblock.blocks]
  assert set(block_ids) == set(['CCDS46694.1', 'CCDS54521.1'])

  assert len(chanjo_db.find('block')) == 5
  assert len(chanjo_db.find('superblock')) == 4
