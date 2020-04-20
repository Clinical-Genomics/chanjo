
<center>
	<img src="assets/logo.png" width="400px" />
</center>

# Chanjo
## Coverage analysis for clinical sequencing

<br><br>

**Current release**: Optimistic Otter (4.0)

The goals of Chanjo are quite simple:

1. Integrate seamlessly with `sambamba depth region` output
2. Break down coverage to intuitive levels of abstraction: exons, transcripts, and genes
3. Enable exploratory coverage investigations across samples and genomic regions

```bash
$ sambamba depth region -L exons.bed -t 10 -t 20 alignment.bam > exons.coverage.bed
$ chanjo load exons.coverage.bed
$ chanjo calculate gene ADK
{"completeness_10": 100, "completeness_20": 87.123, "mean_coverage": 47.24234}
```

To learn more about Chanjo and how you can use it to gain a better understanding of sequencing coverage you can do no better than to:

[**Check out the demo!**][demo]


[demo]: topics/demo.md
