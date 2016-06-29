# Chanjo

_Coverage analysis for clinical sequencing_

**Current release**: Radical Red Panda (3.2.0)

The goals of Chanjo are quite simple:

1. Integrate seamlessly with `sambamba depth region` output
2. Break down coverage to intuitive levels of abstraction: exons, transcripts, and genes
3. Enable explorative coverage investigations across samples and genomic regions

## Simple [Sambamba][sambamba] integration

There’s a new kid on the BAM processing block: [Sambamba][sambamba]! You can easily load output into a Chanjo database for further coverage exploration:

```bash
$ sambamba depth region -L exons.bed -t 10 -t 20 alignment.bam > exons.coverage.bed
$ chanjo load exons.coverage.bed
$ chanjo calculate region 1 861321 871275 --sample ADM980A2
{"completeness_10": 100, "completeness_20": 87.123, "mean_coverage": 47.24234}
```

To learn more about Chanjo and how you can use it to gain a better understanding of sequencing coverage you can do no better than to:

[**Check out the demo!**][demo]


[demo]: topics/demo.md
[sambamba]: http://lomereiter.github.io/sambamba/index.html
