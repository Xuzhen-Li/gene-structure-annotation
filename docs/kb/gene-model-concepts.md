# Gene models and the evidence behind them

[中文](gene-model-concepts.zh.md) · [Knowledge units](README.md)

## 1. What it is

A gene model is the description of one gene on an assembled genome: the gene, one or more transcripts (mRNA), and for each transcript its exons, coding sequence (CDS) and untranslated regions (UTR). Structural annotation writes these models as GFF3 rows, together with the predicted proteins. Names, GO terms and pathways are a separate layer, handled in [gene-function-annotation](https://github.com/Xuzhen-Li/gene-function-annotation).

## 2. How the evidence is structured

A model is built from up to four kinds of evidence, then checked:

| Evidence | What it gives | Book |
|---|---|---|
| Transcripts (short-read RNA-seq, long reads) | exon and intron positions; full isoforms from long reads | [chapter 4](../../book/chapters/04-rna-and-iso-seq-evidence.md) |
| Proteins from related species | spliced alignments that mark coding exons | [chapter 5](../../book/chapters/05-protein-evidence.md) |
| Ab initio and language-model predictors | statistical or learned gene structure, also where no evidence aligns | [chapters 6](../../book/chapters/06-ab-initio-gene-finders.md) and [7](../../book/chapters/07-dna-language-model-predictors.md) |
| A close curated reference annotation | models lifted over from a related genome | [chapter 8](../../book/chapters/08-lift-over-and-annotation-transfer.md) |

Combiners and pipelines merge these lines into one gene set ([chapter 9](../../book/chapters/09-combiners-and-annotation-pipelines.md)). All of them expect a genome whose repeats are soft-masked first ([Soft-masking with a trusted TE library](trusted-softmask.md)).

## 3. How to recognise a usable gene model (field card)

- Each CDS row has a `Parent` that is an mRNA, and each mRNA has a `Parent` that is a gene.
- The phase column is filled for every CDS row.
- The protein file is translated from the same GFF3 and has the same IDs.
- The METHODS text names one primary draft route and the tool versions.

The release checks behind the last two points are G3 and G5 in [`docs/EVALUATION.md`](../EVALUATION.md); this page does not restate them.

## 4. Repository default and branches

The default route and the branches (S1, S11, S2, S3, S13, S14) are described in the [README, Branches](../../README.md#branches), in [`docs/ROADMAP.md`](../ROADMAP.md) and in [`catalog/_branches.md`](../../catalog/_branches.md). The workflow index is [`docs/workflow/README.md`](../workflow/README.md).

## 5. What is known in plants and in *Vitis*

- Plant genomes are large, rich in transposable elements and often polyploid; chapter 1 of the book gives the sources ([section 1.2](../../book/chapters/01-concepts.md#12-why-plant-genomes-are-hard)).
- Fused (chimeric) gene models are a known error type in recently annotated plant and invertebrate genomes ([section 1.2](../../book/chapters/01-concepts.md#12-why-plant-genomes-are-hard)).
- The grapevine worked example is in [`docs/cases/vitis-t2t-s1-s5.md`](../cases/vitis-t2t-s1-s5.md). A general number for how many grapevine models are fused or split is not given on this page: **[待确认]**.

## 6. Claims and sources

| Claim | Source | Quoted sentence or figure | What was read |
|---|---|---|---|
| In GFF3, the `Parent` attribute links exons to transcripts and transcripts to genes. | GFF3 specification, Sequence Ontology ([gff3.md](https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md)) | “A parent ID can be used to group exons into transcripts, transcripts into genes, an so forth.” (spelling as in the source) | The specification text, definition of the `Parent` attribute |
| Every CDS row must carry a phase. | GFF3 specification, as above | “The phase is REQUIRED for all CDS features.” | The specification text, column 8 |
| Annotating a eukaryotic genome is feasible for a small group but still hard. | Yandell and Ence 2012, *Nat Rev Genet* 13:329, [doi:10.1038/nrg3174](https://doi.org/10.1038/nrg3174) | “Although annotating a eukaryotic genome assembly is now within the reach of non-experts, it remains a challenging task.” | Abstract (PubMed 22510764) |
| Predicting genes on an unmasked genome produces false gene structures in repeats. | BRAKER README ([Gaius-Augustus/BRAKER](https://github.com/Gaius-Augustus/BRAKER)) | “This will avoid the prediction of false positive gene structures in repetitive and low complexitiy regions.” (spelling as in the source) | README, section on the genome file |
| Plant genomes are hard to annotate because of size, transposable elements and polyploidy. | Book chapter 1, section 1.2, which cites [doi:10.1002/aps3.11533](https://doi.org/10.1002/aps3.11533) | “Plant genomes are large, rich in transposable elements and often polyploid” | The chapter text; the cited paper was not reopened for this page |

## 7. See also

- Book: [chapter 1, Concepts and principles](../../book/chapters/01-concepts.md); [chapter 13, GFF3 cleanup and release](../../book/chapters/13-gff3-cleanup-and-release.md)
- Knowledge units: [Soft-masking with a trusted TE library](trusted-softmask.md); [Is the gene set good enough?](model-qc-criteria.md)
- Software by step: [`catalog/README.by-type.md`](../../catalog/README.by-type.md)
- Boundary between structure, function and TE work: [`docs/BOUNDARY.md`](../BOUNDARY.md)
