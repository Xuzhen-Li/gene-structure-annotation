# Four structural error classes (from GSAman)

Use these labels when tagging priority loci and release notes.

| Class | Symptom | Typical grape risk |
|-------|---------|-------------------|
| Fragmentation | One locus split into several gene IDs | Under-count of gene family size; broken domains |
| Adjacent fusion | Two loci merged into one | Inflated CDS; false chimeric transcripts |
| Exon / splice error | Missing exon, wrong GT-AG, bad start/stop | Wrong protein length; false “novel isoform” |
| Tandem collapse | Paralogs collapsed to one model | Severe under-annotation of NLR / stilbene / RGA clusters |

QC triage: low PSAURON + fragmented BUSCO orthologs + tandem-array neighborhoods first.
