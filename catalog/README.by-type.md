# Catalogue by type

[中文](README.by-type.zh.md) · [Full catalogue](METHODS_CATALOG.md) · [Counts](COUNTS.md) · [Index by stage](README.md)

One row per type section of the methods catalogue. Entry counts come from [`SOFTWARE_AUTHORITY.tsv`](SOFTWARE_AUTHORITY.tsv) (207 entries, 2026-11-26). The type-class key is the label used in the 2026-11 survey file [`docs/CATALOG_BY_TYPE_2026-11.md`](../docs/CATALOG_BY_TYPE_2026-11.md), which is kept as a legacy record. The folders in this directory sort the first-pass cards by stage; that index ([`README.md`](README.md)) is kept unchanged as a second view.

| # | Type section | Type-class key (legacy) | Entries | Default and branch tools | Book chapter | Knowledge unit |
|---|---|---|---|---|---|---|
| 1 | [1. Assembly and assembly QC](METHODS_CATALOG.md#section-1) | `assembly-qc` | 22 | hifiasm | [ch. 2](../book/chapters/02-assembly-and-assembly-qc.md) | — |
| 2 | [2. Soft-mask with a trusted library](METHODS_CATALOG.md#section-2) | `soft-mask` | 11 | RepeatMasker | [ch. 3](../book/chapters/03-soft-mask-with-a-trusted-library.md) | [trusted-softmask](../docs/kb/trusted-softmask.md) |
| 3 | [3. RNA and Iso-Seq evidence](METHODS_CATALOG.md#section-3) | `rna-evidence` | 31 | HISAT2, STAR, minimap2, PASA, IsoQuant, SQANTI3, StringTie (v3 line) | [ch. 4](../book/chapters/04-rna-and-iso-seq-evidence.md) | [gene-model-concepts](../docs/kb/gene-model-concepts.md) |
| 4 | [4. Protein evidence](METHODS_CATALOG.md#section-4) | `protein-evidence` | 8 | miniprot | [ch. 5](../book/chapters/05-protein-evidence.md) | [gene-model-concepts](../docs/kb/gene-model-concepts.md) |
| 5 | [5. Ab initio gene finders](METHODS_CATALOG.md#section-5) | `ab-initio` | 12 | BRAKER4, GALBA2, Tiberius, ANNEVO, Helixer | [ch. 6](../book/chapters/06-ab-initio-gene-finders.md) | [gene-model-concepts](../docs/kb/gene-model-concepts.md) |
| 6 | [6. DNA language-model predictors](METHODS_CATALOG.md#section-6) | `language-model` | 11 | — | [ch. 7](../book/chapters/07-dna-language-model-predictors.md) | [gene-model-concepts](../docs/kb/gene-model-concepts.md) |
| 7 | [7. Lift-over and annotation transfer](METHODS_CATALOG.md#section-7) | `lift-over` | 10 | GeMoMa, Liftoff, LiftOn, Comparative Annotation Toolkit (CAT) | [ch. 8](../book/chapters/08-lift-over-and-annotation-transfer.md) | [gene-model-concepts](../docs/kb/gene-model-concepts.md) |
| 8 | [8. Combiners and annotation pipelines](METHODS_CATALOG.md#section-8) | `combiner-pipeline` | 15 | EVidenceModeler (EVM) | [ch. 9](../book/chapters/09-combiners-and-annotation-pipelines.md) | [gene-model-concepts](../docs/kb/gene-model-concepts.md) |
| 9 | [9. Non-coding RNA and pseudogene loci](METHODS_CATALOG.md#section-9) | `ncrna-pseudogene` | 17 | — | [ch. 10](../book/chapters/10-non-coding-rna-and-pseudogene-loci.md) | — |
| 10 | [10. Gene-model QC](METHODS_CATALOG.md#section-10) | `model-qc` | 7 | — | [ch. 11](../book/chapters/11-gene-model-qc.md) | [model-qc-criteria](../docs/kb/model-qc-criteria.md) |
| 11 | [11. Curation and browsers](METHODS_CATALOG.md#section-11) | `curation-browser` | 8 | — | [ch. 12](../book/chapters/12-curation-and-browsers.md) | — |
| 12 | [12. GFF3 cleanup and release](METHODS_CATALOG.md#section-12) | `gff-release` | 11 | — | [ch. 13](../book/chapters/13-gff3-cleanup-and-release.md) | [gene-model-concepts](../docs/kb/gene-model-concepts.md) |
| 13 | [13. Reference databases](METHODS_CATALOG.md#section-13) | `database` | 11 | — | [ch. 14](../book/chapters/14-reference-databases.md) | — |
| 14 | [14. Standards and reviews](METHODS_CATALOG.md#section-14) | `standard-review` | 13 | — | [ch. 15](../book/chapters/15-standards-and-overview-papers.md) | — |
| 15 | [15. Ideas not yet tied to one tool](METHODS_CATALOG.md#section-15) | `idea` | 8 | — | [ch. 16](../book/chapters/16-ideas-not-yet-tied-to-one-tool.md) | — |
| viz | [Visualization tools](METHODS_CATALOG.md#visualization) | — | 12 | — | [ch. 17](../book/chapters/17-visualization-tools.md) | — |

**Total: 207**

## Stage folders with no cards

These stage folders hold no first-pass card. They are kept so that stage links still resolve; the tools for these steps are in the type sections above.

- Asm0 — assembly: [`Asm0_assembly/`](Asm0_assembly/README.md)
- A4 — aggregation (A4a TSEBRA, A4b Mikado, A4c–A4d EVM, A4e PASA update): [`A4_aggregation/`](A4_aggregation/README.md)
- A3 — proteins from GFF: [`A3_proteins/`](A3_proteins/README.md)
- Last mile 01 — BUSCO / PSAURON QC: [`LM01_qc_busco_psauron/`](LM01_qc_busco_psauron/README.md)
- Last mile 02 — priority loci (02, 02b): [`LM02_priority_loci/`](LM02_priority_loci/README.md)
- Last mile 03 — evidence pack: [`LM03_evidence_pack/`](LM03_evidence_pack/README.md)
- A6 / A6b — hand-off to function: [`A6_handoff_to_function/`](A6_handoff_to_function/README.md)
