# -*- coding: utf-8 -*-

def groupby_tx(exons, sambamba=False):
    """Group (unordered) exons per transcript.
    
    Args:
        exons(iterable(dict)): Parsed exon information
        sambamba(bool)
    
    Returns:
        transcripts(dict(list)): Exons grouped by transcript
    """
    transcripts = {}
    for exon in exons:
        if sambamba:
            ids = zip(exon['extraFields'][-3].split(','),
                      exon['extraFields'][-2].split(','),
                      exon['extraFields'][-1].split(','))
        else:
            ids = exon['elements']
        elements = {}
        for tx_id, gene_id, symbol in ids:
            elements[tx_id] = dict(symbol=symbol, gene_id=gene_id)
        exon['elements'] = elements

        for transcript_id in exon['elements']:
            if transcript_id not in transcripts:
                transcripts[transcript_id] = []
            transcripts[transcript_id].append(exon)
    return transcripts


