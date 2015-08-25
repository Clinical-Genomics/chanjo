# -*- coding: utf-8 -*-
"""
Parse the sambamba "depth region" output.
"""
from chanjo._compat import iteritems


def parse(handle):
    """Parse the output."""
    lines = (line.strip() for line in handle)
    rows = (line.split('\t') for line in lines)
    # expect only a single header row
    header_row = next(rows)
    header_data = parse_header(header_row)
    # parse rows
    for row in rows:
        yield parse_row(header_data, row)


def parse_header(row):
    """Parse the header information."""
    # figure out where the sambamba output begins
    sambamba_start = row.index('readCount')
    sambamba_end = row.index('sampleName')
    coverage_columns = row[sambamba_start + 2:sambamba_end]
    thresholds = {int(column.replace('percentage', '')): row.index(column)
                  for column in coverage_columns}
    keys = {
        'readCount': sambamba_start,
        'meanCoverage': sambamba_start + 1,
        'thresholds': thresholds,
        'sampleName': sambamba_end,
        'extraFields': slice(3, sambamba_start)
    }
    return keys


def parse_row(header, row):
    """Parse information in row to dict."""
    thresholds = {threshold: float(row[key])
                  for threshold, key in iteritems(header['thresholds'])}
    data = {
        'chrom': row[0],
        'chromStart': int(row[1]),
        'chromEnd': int(row[2]),
        'sampleName': row[header['sampleName']],
        'readCount': int(row[header['readCount']]),
        'meanCoverage': float(row[header['meanCoverage']]),
        'thresholds': thresholds,
        'extraFields': row[header['extraFields']]
    }
    return data
