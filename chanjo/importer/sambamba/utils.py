# -*- coding: utf-8 -*-

def parse_sambamba(line):
    pass


class SambambaEntry(object):

    """Sambamba entry object."""

    def __init__(self, chromosome, start, end, id, sample, read_count,
                 coverage, completeness_levels=None):
        self.chromosome = chromosome
        self.start = start
        self.end = end
        self.id = id
        self.sample = sample
        self.read_count = read_count
        self.coverage = coverage
        self.completeness_levels = completeness_levels
