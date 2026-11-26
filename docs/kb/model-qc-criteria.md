# Is the gene set good enough? (criteria)

[中文](model-qc-criteria.zh.md) · [Knowledge units](README.md)

This is a criteria unit. The grades, gates and fail rules are written once, in [`docs/EVALUATION.md`](../EVALUATION.md). This page explains what the checks measure and points to them; it copies no thresholds.

## 1. What it is

A gene set is judged on three things: **completeness** (are the expected genes there), **consistency** (does the gene repertoire look like that of related species, without many fragments, extra genes or contamination) and **validity** (do the GFF3 and the proteins agree and pass format checks). This repository turns these checks into three finish grades, L0 (provisional), L1 (qualified) and L2 (paper or T2T bar).

## 2. How the evidence is structured

| Question | Typical measure | Where the rule is |
|---|---|---|
| Are conserved genes present? | BUSCO on the proteins, with the lineage named | [G6](../EVALUATION.md#g6--protein-busco-reported) |
| Are there many bad or extra models? | per-model scores and a list of the worst loci; OMArk consistency | [G7](../EVALUATION.md#g7--beyond-busco-triage); [soft metrics](../EVALUATION.md#soft-metrics-interpret-do-not-fake-universal-cutoffs) |
| Do the files agree? | GFF3 validation; proteins translated from the same GFF3 | [G4, G5](../EVALUATION.md#g4--models-validate) |
| Which grade can be claimed? | all hard gates for L1; extra checks for L2 | [Three finish grades](../EVALUATION.md#three-finish-grades) |

## 3. How to recognise a sound QC report (field card)

- BUSCO is given with the lineage data set name.
- BUSCO is not the only check.
- `grade=` and `status=` are written separately.
- A provisional draft is not called final.

## 4. Repository default and branches

The checklist that follows the rules is [`docs/EVALUATION_CHECKLIST.md`](../EVALUATION_CHECKLIST.md). QC tools are listed in [catalogue section 10](../../catalog/METHODS_CATALOG.md#section-10). The last-mile steps that act on the worst models (priority loci, manual curation, release) are folders LM01 to LM06 in [`catalog/`](../../catalog/README.md).

## 5. What is known in plants and in *Vitis*

- BUSCO counts only conserved single-copy genes; lineage-specific, tandem and TE-overlapping genes are under-sampled ([G7 background](../EVALUATION.md#g7--beyond-busco-triage)).
- The grapevine T2T case shows one way to reach L2 ([`docs/cases/vitis-t2t-s1-s5.md`](../cases/vitis-t2t-s1-s5.md)). For another clade the evaluation page asks for its own lineage and curation story.
- A plant-wide reference value for OMArk consistency is not given here: **[待确认]**.

## 6. Claims and sources

| Claim | Source | Quoted sentence or figure | What was read |
|---|---|---|---|
| BUSCO measures completeness and redundancy from universal single-copy orthologs. | Manni et al. 2021, *Mol Biol Evol* 38:4647, [doi:10.1093/molbev/msab199](https://doi.org/10.1093/molbev/msab199) | “BUSCO estimates the completeness and redundancy of processed genomic data based on universal single-copy orthologs.” | Abstract (PubMed 34320186) |
| Completeness tools miss overprediction and contamination. | Nevers et al. 2025, *Nat Biotechnol* 43:124, [doi:10.1038/s41587-024-02147-w](https://doi.org/10.1038/s41587-024-02147-w) | “State-of-the-art tools to assess genome annotations measure the completeness of a gene repertoire but are blind to other errors, such as gene overprediction or contamination.” | Abstract (PubMed 38383603) |
| OMArk adds consistency with related species and flags contamination. | Nevers et al. 2025, as above | “OMArk assesses not only the completeness but also the consistency of the gene repertoire as a whole relative to closely related species and reports likely contamination events.” | Abstract (PubMed 38383603) |
| A BUSCO score without the lineage name cannot be read. | [`docs/EVALUATION.md`](../EVALUATION.md#g6--protein-busco-reported), G6 background (this repository) | “Reporting C without the odb name is not interpretable.” | The file at the current main branch |
| The grapevine L2 path is an example, not a checklist for other clades. | [`docs/EVALUATION.md`](../EVALUATION.md) (this repository) | “do not copy grape OMArk/window depth as a checkbox” | The file at the current main branch, section on non-grape L2 |

## 7. See also

- Book: [chapter 11, Gene-model QC](../../book/chapters/11-gene-model-qc.md); [chapter 19, Pitfalls and quality control](../../book/chapters/19-pitfalls-and-qc.md)
- Knowledge units: [Gene models and the evidence behind them](gene-model-concepts.md); [Soft-masking with a trusted TE library](trusted-softmask.md)
- Next layer: function checks in [gene-function-annotation `docs/EVALUATION.md`](https://github.com/Xuzhen-Li/gene-function-annotation/blob/main/docs/EVALUATION.md)
