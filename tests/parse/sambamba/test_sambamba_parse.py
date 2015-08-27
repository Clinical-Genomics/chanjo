# -*- coding: utf-8 -*-
from chanjo.parse import sambamba

BASE_HEADERS = ['chrom', 'chromStart', 'chromEnd']
THRESHOLDS = ['percentage10', 'percentage20', 'percentage100']
EXTRA_HEADERS = ['F3', 'F4', 'F5']
SAMBAMBA_HEADERS = ['readCount', 'meanCoverage']

BASE_COLS = ['1', '69089', '70007']
EXTRA_COLS = ['1-69090-70007', '0', '+', 'CCDS30547.1', 'OR4F5']
SAMBAMBA_COLS = ['232', '25.4946']
THRESHOLD_COLS = ['57.9521', '36.0566', '5.55556']
SAMBAMBA_END_COLS = ['ADM992A10', '']


def test_expand_header_no_thresholds():
    header_row = BASE_HEADERS + SAMBAMBA_HEADERS + ['sampleName']
    header = sambamba.expand_header(header_row)
    assert header['readCount'] == 3
    assert header['thresholds'] == {}
    assert header['extraFields'] == slice(3, 3)
    assert header['sampleName'] == 5


def test_expand_header_single_threshold():
    header_row = (BASE_HEADERS + SAMBAMBA_HEADERS + THRESHOLDS[:1]
                  + ['sampleName'])
    header = sambamba.expand_header(header_row)
    assert header['readCount'] == 3
    assert header['thresholds'] == {10: 5}
    assert header['sampleName'] == 6


def test_expand_header_multi_thresholds():
    header_row = (BASE_HEADERS + SAMBAMBA_HEADERS + THRESHOLDS
                  + ['sampleName'])
    header = sambamba.expand_header(header_row)
    assert header['readCount'] == 3
    assert header['thresholds'] == {10: 5, 20: 6, 100: 7}
    assert header['sampleName'] == 8


def test_expand_header_extra_cols():
    header_row = (BASE_HEADERS + EXTRA_HEADERS + SAMBAMBA_HEADERS
                  + ['sampleName'])
    header = sambamba.expand_header(header_row)
    assert header['readCount'] == 6
    assert header['extraFields'] == slice(3, 6)
    assert header['sampleName'] == 8


def test_expand_row_basic():
    header = {'extraFields': slice(3, 3), 'readCount': 3, 'meanCoverage': 4,
              'thresholds': {}, 'sampleName': 5}
    row = BASE_COLS + SAMBAMBA_COLS + SAMBAMBA_END_COLS
    row_data = sambamba.expand_row(header, row)
    assert row_data['chrom'] == '1'
    assert row_data['chromStart'] == 69089
    assert row_data['chromEnd'] == 70007
    assert row_data['extraFields'] == []
    assert row_data['readCount'] == 232
    assert row_data['meanCoverage'] == 25.4946
    assert row_data['thresholds'] == {}
    assert row_data['sampleName'] == 'ADM992A10'


def test_expand_row_with_threshold():
    header = {'extraFields': slice(3, 3), 'readCount': 3, 'meanCoverage': 4,
              'thresholds': {10: 5, 20: 6, 100: 7}, 'sampleName': 8}
    row = BASE_COLS + SAMBAMBA_COLS + THRESHOLD_COLS + SAMBAMBA_END_COLS
    row_data = sambamba.expand_row(header, row)
    assert row_data['thresholds'][10] == 57.9521
    assert row_data['thresholds'][20] == 36.0566
    assert row_data['thresholds'][100] == 5.55556
    assert row_data['sampleName'] == 'ADM992A10'


def test_expand_row_with_extra_fields():
    header = {'extraFields': slice(3, 8), 'readCount': 8, 'meanCoverage': 9,
              'thresholds': {}, 'sampleName': 10}
    row = BASE_COLS + EXTRA_COLS + SAMBAMBA_COLS + SAMBAMBA_END_COLS
    row_data = sambamba.expand_row(header, row)
    assert row_data['extraFields'] == EXTRA_COLS
    assert row_data['readCount'] == 232
    assert row_data['meanCoverage'] == 25.4946
    assert row_data['sampleName'] == 'ADM992A10'


def test_depth_output_exon():
    bed_lines = ["# chrom\tchromStart\tchromEnd\tF3\tF4\tF5\tF6\tF7\t"
                    "readCount\tmeanCoverage\tpercentage10\tpercentage20"
                    "\tpercentage100\tsampleName",
                 "1\t69089\t70007\t1-69090-70007\t0\t+\tCCDS30547.1\tOR4F5\t"
                    "232\t25.4946\t57.9521\t36.0566\t5.55556\tADM992A10\t"]

    row_data = sambamba.depth_output(bed_lines)
    results = [data for data in row_data]
    assert len(results) == 1
    assert results[0]['sampleName'] == 'ADM992A10'
    assert results[0]['chromStart'] == 69089


def test_depth_output_gene():
    bed_lines = ["# chrom\tchromStart\tchromEnd\tF3\treadCount\tmeanCoverage\t"
                    "percentage10\tpercentage20\tpercentage100\tsampleName",
                 "1\t69089\t70007\tOR4F5\t232\t25.4946\t57.9521\t36.0566\t"
                    "5.55556\tADM992A10\t"]

    row_data = sambamba.depth_output(bed_lines)
    results = [data for data in row_data]
    assert len(results) == 1
    assert results[0]['chrom'] == '1'
    assert results[0]['chromStart'] == 69089
    assert results[0]['chromEnd'] == 70007
    assert results[0]['extraFields'] == ['OR4F5']
    assert results[0]['readCount'] == 232
    assert results[0]['meanCoverage'] == 25.4946
    assert results[0]['thresholds'][20] == 36.0566
    assert results[0]['sampleName'] == 'ADM992A10'
