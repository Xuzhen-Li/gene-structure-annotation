# Chapter 18. Choosing tools

The repository chooses one primary route per genome from the data at hand (README, Default route and Branches; `docs/SCENARIOS.md`). The table below restates that choice and adds the evidence behind each first tool.

| Data situation | Route | First tools | Why (source) | Main check |
|---|---|---|---|---|
| RNA-seq and proteins, no close curated reference | S1 (default) | HISAT2 or STAR, StringTie, BRAKER3/4 | BRAKER3 outperformed BRAKER1, BRAKER2, MAKER2, Funannotate and FINDER on 11 genomes ([doi:10.1101/gr.278090.123](https://doi.org/10.1101/gr.278090.123)) | Mono-exonic to multi-exonic ratio after TSEBRA (README, Cross-cutting pitfalls) |
| Trusted curated annotation of the same species or cultivar | S11 lift-over first | Liftoff, LiftOn | Liftoff maps genes between assemblies of the same or closely related species ([doi:10.1093/bioinformatics/btaa1016](https://doi.org/10.1093/bioinformatics/btaa1016)); LiftOn adds protein alignments for more distant species ([doi:10.1101/gr.279620.124](https://doi.org/10.1101/gr.279620.124)) | Do not call a lift-only S11-lite set an L1 release (README, Data needed) |
| Proteins only | S2 | GALBA, GeMoMa, miniprot | GALBA combines miniprot with AUGUSTUS; its authors report it is strongest on large vertebrate genomes and show a land plant use case ([doi:10.1186/s12859-023-05449-z](https://doi.org/10.1186/s12859-023-05449-z)) | Do not claim complete UTRs from protein evidence alone (README, Data needed) |
| Deep long-read RNA (Iso-Seq or ONT) | S3 | minimap2, IsoQuant, SQANTI3 | IsoQuant authors report a fivefold lower false-positive rate for novel ONT transcripts in reference-based mode ([doi:10.1038/s41587-022-01565-y](https://doi.org/10.1038/s41587-022-01565-y)); LRGASP found longer, more accurate reads give more accurate transcripts than extra depth ([doi:10.1038/s41592-024-02298-3](https://doi.org/10.1038/s41592-024-02298-3)) | Run SQANTI-style filters ([doi:10.1038/s41592-024-02229-2](https://doi.org/10.1038/s41592-024-02229-2)) |
| GPU available, want an ab initio comparison | S13 | Helixer, Tiberius, ANNEVO | Helixer has pretrained plant models and needs no RNA-seq ([doi:10.1038/s41592-025-02939-1](https://doi.org/10.1038/s41592-025-02939-1)); Tiberius was trained on mammals ([doi:10.1093/bioinformatics/btae685](https://doi.org/10.1093/bioinformatics/btae685)) | Keep it beside the evidence draft; do not silently replace S1 (README, Data needed) |
| Classic multi-evidence stack | S14 | PASA, AUGUSTUS or GeneMark, EVidenceModeler | EVM weighted consensus approached manual curation on rice and human ([doi:10.1186/gb-2008-9-1-r7](https://doi.org/10.1186/gb-2008-9-1-r7)) | Document EVM weights; EVM is not required on every genome (README, Data needed) |
| Second haplotype | S4 | Liftoff, SynGAP | SynGAP polishes gene structures with synteny ([doi:10.1186/s13059-024-03359-8](https://doi.org/10.1186/s13059-024-03359-8)) | Do not purge haplotypes only to lower BUSCO duplication (README, Cross-cutting pitfalls) |

## How to read the tiers

The tier in every table (standard 500 or more citations, established 100 to 499, newer under 100 and published 2023 or later, niche under 100 and older) measures how widely a paper is cited. It says nothing about accuracy on your genome. General-purpose tools such as aligners and browsers collect citations from every field. Before switching a default, read the benchmark notes at the end of each step chapter and run the comparison on your own data, as the README asks (README, Data needed: notes do not change the default until a change is tested).

## Questions to ask before adding a tool

1. Which stage does it replace or add, and does the README already name a tool for that stage?
2. Is there an independent benchmark, or only the authors claim? Independent examples: G3PO for ab initio prediction ([doi:10.1186/s12864-020-6707-9](https://doi.org/10.1186/s12864-020-6707-9)), the plant benchmark of BRAKER and MAKER ([doi:10.1002/aps3.11533](https://doi.org/10.1002/aps3.11533)), RGASP and LRGASP for transcripts.
3. Was it tested on plants? Tiberius, for example, was trained for mammals ([doi:10.1093/bioinformatics/btae685](https://doi.org/10.1093/bioinformatics/btae685)).
4. Is the code maintained? The GitHub last-push date in the tables is a quick check.
