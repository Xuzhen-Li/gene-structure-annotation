# Numbering schemes

[中文](NUMBERING.zh.md) · [Knowledge units](README.md)

Several numbering schemes are used in this repository. The current ones are used in new pages; the legacy ones are kept in older pages and are not renumbered. This page maps them.

| Scheme | Labels | Status | Defined in |
|---|---|---|---|
| Catalogue type sections | 1–15 and visualization | current | [`catalog/METHODS_CATALOG.md`](../../catalog/METHODS_CATALOG.md); `section` column of the TSV |
| Book chapters | 1–20 and appendix A; chapter *n* + 1 covers type section *n*, chapter 17 covers visualization | current | [`book/`](../../book/README.md) |
| Branch IDs | S1–S14: draft routes S1, S2, S3, S6, S11, S13, S14; overlays S4, S5, S7–S10, S12 | current | [`docs/ROADMAP.md`](../ROADMAP.md); [`catalog/_branches.md`](../../catalog/_branches.md) |
| Finish grades and gates | L0, L1, L2; G1–G9 | current | [`docs/EVALUATION.md`](../EVALUATION.md) |
| Stage IDs | Asm0, Asm1, A0–A6, last mile 01–06 | current for pipeline steps | [`docs/STAGE_IO.md`](../STAGE_IO.md) |
| Stage folders of first-pass cards | `Asm0_assembly/` … `LM06_release/`; folder `LMnn` = last mile *nn* | legacy view (2026-11 first pass) | [`catalog/README.md`](../../catalog/README.md) |
| Type-class keys | `assembly-qc` … `idea` | legacy (2026-11 survey) | [`docs/CATALOG_BY_TYPE_2026-11.md`](../CATALOG_BY_TYPE_2026-11.md) |

## Type sections, legacy keys and book chapters

| Type section (current) | Type-class key (legacy) | Book chapter |
|---|---|---|
| [1. Assembly and assembly QC](../../catalog/METHODS_CATALOG.md#section-1) | `assembly-qc` | [Chapter 2. Assembly and assembly QC](../../book/chapters/02-assembly-and-assembly-qc.md) |
| [2. Soft-mask with a trusted library](../../catalog/METHODS_CATALOG.md#section-2) | `soft-mask` | [Chapter 3. Soft-mask with a trusted library](../../book/chapters/03-soft-mask-with-a-trusted-library.md) |
| [3. RNA and Iso-Seq evidence](../../catalog/METHODS_CATALOG.md#section-3) | `rna-evidence` | [Chapter 4. RNA and Iso-Seq evidence](../../book/chapters/04-rna-and-iso-seq-evidence.md) |
| [4. Protein evidence](../../catalog/METHODS_CATALOG.md#section-4) | `protein-evidence` | [Chapter 5. Protein evidence](../../book/chapters/05-protein-evidence.md) |
| [5. Ab initio gene finders](../../catalog/METHODS_CATALOG.md#section-5) | `ab-initio` | [Chapter 6. Ab initio gene finders](../../book/chapters/06-ab-initio-gene-finders.md) |
| [6. DNA language-model predictors](../../catalog/METHODS_CATALOG.md#section-6) | `language-model` | [Chapter 7. DNA language-model predictors](../../book/chapters/07-dna-language-model-predictors.md) |
| [7. Lift-over and annotation transfer](../../catalog/METHODS_CATALOG.md#section-7) | `lift-over` | [Chapter 8. Lift-over and annotation transfer](../../book/chapters/08-lift-over-and-annotation-transfer.md) |
| [8. Combiners and annotation pipelines](../../catalog/METHODS_CATALOG.md#section-8) | `combiner-pipeline` | [Chapter 9. Combiners and annotation pipelines](../../book/chapters/09-combiners-and-annotation-pipelines.md) |
| [9. Non-coding RNA and pseudogene loci](../../catalog/METHODS_CATALOG.md#section-9) | `ncrna-pseudogene` | [Chapter 10. Non-coding RNA and pseudogene loci](../../book/chapters/10-non-coding-rna-and-pseudogene-loci.md) |
| [10. Gene-model QC](../../catalog/METHODS_CATALOG.md#section-10) | `model-qc` | [Chapter 11. Gene-model QC](../../book/chapters/11-gene-model-qc.md) |
| [11. Curation and browsers](../../catalog/METHODS_CATALOG.md#section-11) | `curation-browser` | [Chapter 12. Curation and browsers](../../book/chapters/12-curation-and-browsers.md) |
| [12. GFF3 cleanup and release](../../catalog/METHODS_CATALOG.md#section-12) | `gff-release` | [Chapter 13. GFF3 cleanup and release](../../book/chapters/13-gff3-cleanup-and-release.md) |
| [13. Reference databases](../../catalog/METHODS_CATALOG.md#section-13) | `database` | [Chapter 14. Reference databases](../../book/chapters/14-reference-databases.md) |
| [14. Standards and reviews](../../catalog/METHODS_CATALOG.md#section-14) | `standard-review` | [Chapter 15. Standards and overview papers](../../book/chapters/15-standards-and-overview-papers.md) |
| [15. Ideas not yet tied to one tool](../../catalog/METHODS_CATALOG.md#section-15) | `idea` | [Chapter 16. Ideas not yet tied to one tool](../../book/chapters/16-ideas-not-yet-tied-to-one-tool.md) |
