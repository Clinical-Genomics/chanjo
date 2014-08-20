# -*- coding: utf-8 -*-
from chanjo.builder import (
  aggregate, build_block, build_interval, build_superblock
)
from chanjo.utils import BaseInterval
from chanjo.store import Store, Interval as StoreInterval


def test_aggregate():
  payloads = [
    ('block1', BaseInterval('X', 10, 100)),
    ('block1', BaseInterval('X', 50, 130)),
    ('block2', BaseInterval('Y', 111, 222))
  ]

  groups = [
    [('block1', BaseInterval('X', 10, 100)),
     ('block1', BaseInterval('X', 50, 130))],
    [('block2', BaseInterval('Y', 111, 222))]
  ]

  assert groups == list(aggregate(payloads))


class TestBuildElement(object):
  def setup(self):
    self.store = Store(':memory:')
    self.store.set_up()

    self.interval = BaseInterval(
      '1', 10, 100,
      name='int1',
      block_ids=['block1', 'block2'],
      superblock_ids=['sblock1', 'sblock1']
    )

    self.db_interval = StoreInterval(
      interval_id=self.interval.name,
      contig=self.interval.contig,
      start=self.interval.start,
      end=self.interval.end,
      strand=self.interval.strand
    )
    self.interval_group = [('block2', self.db_interval, 'sblock1')]

  def test_build_interval(self):
    intervals = list(build_interval(self.store, self.interval))
    self.store.save()
    new_interval = self.store.get('interval', self.interval.name)

    assert new_interval.id == self.interval.name
    assert new_interval.start == self.interval.start

    assert len(intervals) == 2

  def test_build_block(self):
    superblock_id, new_block = build_block(self.store, self.interval_group)
    self.store.save()
    db_block = self.store.get('block', self.interval_group[0][0])

    assert superblock_id == 'sblock1'
    assert new_block.id == db_block.id == self.interval_group[0][0]
    assert new_block.start == db_block.start == self.interval_group[0][1].start
