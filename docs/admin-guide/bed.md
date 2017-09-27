# Bed files

The bed files describe how exons, transcripts and genes are linked. The idea is that chanjo could be used with any defenition of the transcriptome regardless of species etc.
Chanjo is distributed with a defenition of the human transcriptome which is used by defult. The exome coordinates are collected from [ensemble][ensemble], build GRCh37, and the gene names/ids are from [hgnc][hgnc].

The file is produced so that hgnc defines the gene symbols and ids, then all exons that belongs to these genes are collected from ensembl. Feel free to produce your own defenition.

[ensemble]: http://www.ensembl.org/index.html
[hgnc]: http://www.genenames.org