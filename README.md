![Chanjo Avatar](https://raw.github.com/robinandeer/chanjo2/master/assets/chanjo_logo.png)

Current release: v0.0.2-beta

Chanjo is a coverage analysis tool for clinical sequencing.

*BEDtools* and *PicardTools* are both powerful and universally used in DNA sequencing analysis. However, they were built for doing research, not clinic analysis. This means that simple tasks like finding out coverage for a gene are obscrured behind abstract BED intervals.

```python
>>> gene = hub.get("gene", "GIT1")
>>> hub.annotate(gene)
>>> gene.coverage  # Average coverage across the gene
9.2131342342
>>> gene.completeness  # Percent of bases covered at x read depth
0.8234234234
>>> hub.commit()  # Persists annotation(s) to data store
```

Chanjo sets out be part of a new breed of tools aimed at solving problems more or less specific to *clinical* sequencing. Chanjo follows a few general guidelines:

One concrete new feature you will get for free using Chanjo is to set a lower limit for what you consider acceptable coverage and determine what percentage of each element (gene, transcript, exon) is covered to that degree. This is a new way of looking at coverage and is a more fair assessment of the success of sequencing than average coverage.

| Feature            | Description   |
| ------------------ | ------------- |
| BAM support        | Generate coverage directly from BAM alignments. Fit's right into your genomics pipeline. |
| Just what you need | Limit calculations to a list of genes of interest. |
| % coverage         | The bredth of coverage at sufficient coverage is treated as important as depth of coverage. |
| Test report export | Simple output that can be parsed to generate a genetic test report. |

### Contribute
If you feel like learning more about the project and contributing you should check out the [extended documentation](https://chanjo.readthedocs.org/en/latest/).

### Contributor list
Robin Andeer

### License
MIT
