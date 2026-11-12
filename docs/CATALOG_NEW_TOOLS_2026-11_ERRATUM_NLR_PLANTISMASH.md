# Erratum to gene-function-annotation catalog v4 (NLR-Annotator, NLRSeek, plantiSMASH 2.0)

- Date: 2026-11-13 00:12 CST (Asia/Shanghai)
- Author: auto-paper-写作
- Purpose: record required and suggested wording and placement fixes for function-catalog v4. This file is new. It does not change `CATALOG_NEW_TOOLS_2026-11_v4.md`, the two locked `directory_structure_v1.md` files, `catalog_v1.md`, `catalog_v1_erratum.md`, or `docs/PANGENOME_CATALOG.md` in [PR #1](https://github.com/Xuzhen-Li/vitis-pangenome/pull/1).
- Catalog checked (read-only): `/workspace/github-maintain-20261112/gene-function-annotation/CATALOG_NEW_TOOLS_2026-11_v4.md` (sha256 `6d4bf891f9c2f90c5aa7b3409708ec11002511f060952016a8c03d641d750d96`)
- Review: `/workspace/github-maintain-20261112/reviews/geneticist_ruling_nlr_plantismash_v1.md` (sha256 `4cce8002a464eae1ec9e5522f759c2a21e739d81e65594bf6ea2291976c41cb9`), 2026-11-13 00:08:37 CST. Verdict: FAIL on ①-1 and ①-2 (F8 placement of NLR-Annotator and NLRSeek).
- Style follows `/workspace/github-maintain-20261112/vitis-pangenome/catalog_v1_erratum.md` and `catalog_supplement_v3_erratum.md`.
- Scope: close ①-1 and ①-2 as written in the ruling, and absorb ②-1 to ②-3, each with a paste-ready English replacement. Do not reopen plan A for main-catalog ①-3 (V093 stays in section 7). Do not edit PR #1 tonight. Resistify, NLRtracker, NLRexpress and HRP stay in F8.

Replacement sentences below are English, ready to paste into a later new file. They are not applied here.

---

## ①-1 (must fix) — NLR-Annotator must leave the F8 body table

v4 L162 currently says:

| Field | v4 text |
|---|---|
| What it does | Annotation-independent NLR locus finder on genomic sequence. |
| Plant / eukaryote relevance | Window list can be handed to structure scenario S7 for model review. |

That placement is wrong for this catalog. The concept is the same as closed main-catalog ①-3 plan A: NLR-Annotator is structure-layer locus finding (motifs, including partial genes and pseudogenes); it does not make or transfer gene models; gene models stay in gene-structure-annotation; other catalogs only borrow the locus list. The placement is not the same. Main-catalog section 7 may keep V093, because that section’s job is presence and copy-number counts. Frame F8’s job is protein-level NLR classification. A stronger boundary sentence cannot turn a genomic locus scanner into an F8 protein classifier, so the body entry cannot stay in F8.

**Adopted placement.** Move the body entry to gene-structure-annotation as a window source for scenario S7, to be reviewed in LM04. NLR-Annotator itself is not an LM04 editor and does not write the release GFF. In the function catalog, keep a pointer only. Do not change main-catalog V093.

**Proposed function-catalog F8 replacement** (pointer row only; not a body entry):

> Pointer only (the body entry belongs in gene-structure-annotation). NLR-Annotator is a structure-layer locus finder on genomic sequence (motifs, including partial genes and pseudogenes); it does not make or transfer gene models. This catalog does not keep it as an F8 classifier. Use the locus list as a window source for structure scenario S7 (for LM04 review); gene models stay in the structure repository. Protein-level NLR classification in this repository remains Resistify, NLRtracker, NLRexpress and HRP. Cross-link: main-catalog V093 (presence and copy-number counts only; unchanged) and the structure-catalog body entry.

**Proposed structure-catalog body text** (S7 window source, not an LM04 editor):

What it does:

> Annotation-independent NLR locus finder on genomic sequence (motifs, including partial genes and pseudogenes). This is structure-layer locus finding; it does not make or transfer gene models.

Plant / eukaryote relevance, or equivalent Why cell:

> Use its locus list as a window source for scenario S7, to be reviewed in LM04. NLR-Annotator itself is not an LM04 editor and does not write the release GFF. Gene models stay in this repository’s curation path. Other catalogs only borrow the locus list: the vitis-pangenome main catalog (V093) for presence and copy-number counts; the function catalog keeps a pointer only and classifies proteins with Resistify, NLRtracker, NLRexpress and HRP.

The locked structure and function `directory_structure_v1.md` files are not edited here. For a later new framework draft only: close structure L81 by stating that S7 windows have two sources — (a) F8 protein-classification results (HRP and peers, already locked) and (b) this repository’s locus scanner (NLR-Annotator); close function L75 and L106 by replacing the open [待确认] with “gene-model-independent NLR locus scanning belongs in the structure repository; this catalog keeps a pointer only.”

---

## ①-2 (must fix) — NLRSeek must leave the F8 body table

v4 L164 currently says:

| Field | v4 text |
|---|---|
| What it does | Combines NLR-Annotator loci, targeted re-annotation and NLRtracker to recover NLRs missing from proteomes. |
| Plant / eukaryote relevance | Its re-annotation output is a structure-side hint: send recovered loci to S7, do not merge them into the release GFF from here. |

NLRSeek is not the same class as V093. NLR-Annotator does not make gene models; NLRSeek’s core is targeted re-annotation to recover missing NLR gene models. The v4 boundary sentence is correct and must be kept, but it is not enough to leave the whole pipeline in F8. Do not apply plan A to keep this row in the function catalog.

**Adopted placement.** Move the body entry to gene-structure-annotation as directed re-annotation / model hints on S7 windows, for LM04 review. The function catalog may keep a pointer at most, and must say that the NLRtracker classification step remains an F8 method. Keep this exact v4 sentence: “do not merge them into the release GFF from here.” Do not read “recover NLRs missing from proteomes” as this function catalog releasing a protein set.

**Proposed function-catalog F8 replacement** (pointer row only; not a body entry):

> Pointer only (the body entry belongs in gene-structure-annotation). NLRSeek’s core is targeted re-annotation to recover missing NLR gene models; it is not an F8 protein classifier and is not the same class as NLR-Annotator or main-catalog V093. The NLRtracker classification step inside the pipeline remains an F8 method (see the NLRtracker row). Its re-annotation output is a structure-side hint: send recovered loci to S7, do not merge them into the release GFF from here.

**Proposed structure-catalog body text:**

What it does:

> Combines NLR-Annotator loci, targeted re-annotation and NLRtracker to recover NLR gene models missing from proteomes. This is directed re-annotation on S7 windows, not protein-level classification.

Plant / eukaryote relevance, or equivalent Why cell:

> Place this body entry here as directed re-annotation / model hints on S7 windows, for LM04 review. Its re-annotation output is a structure-side hint: send recovered loci to S7, do not merge them into the release GFF from here. The NLRtracker classification step remains in gene-function-annotation (frame F8).

---

## ②-1 — plantiSMASH 2.0 stays in the function-catalog pathway add-ons; do not move it to S7

v4 L123 (section “Pathways and enzymes”) currently says:

| Field | v4 text |
|---|---|
| What it does | Plant biosynthetic gene cluster detection, substrate prediction for some enzyme families, promoter TF sites; DB of ~30k BGCs over 430 genomes. |
| Plant / eukaryote relevance | Grapevine terpene/stilbene clusters. |

**Adopted placement.** Keep the entry in the function catalog, in its current Pathways and enzymes section. Do not move it to structure scenario S7. S7 in these repositories is the NLR window path.

**Proposed addition to the plantiSMASH 2.0 “Plant / eukaryote relevance” cell**, after the v4 sentence:

> This tool labels existing gene models with cluster type, substrate and neighbourhood tags; it does not make gene models and does not change the release GFF from this repository. Cluster coordinates may optionally be handed to gene-structure-annotation as priority curation windows (for example LM02 priority loci; tandem terpene or stilbene synthase models are easily merged). That hand-off does not move this entry to S7.

[待确认] only here, and not raised to ①: whether plantiSMASH 2.0 can also find genes on an unannotated genome. If that is confirmed later, add a structure-catalog pointer then; do not move this entry tonight.

---

## ②-2 — keep the F8 section intro, but do not use it to justify NLR-Annotator or NLRSeek

v4 L156 currently says:

> Family classifiers. Window lists from here can be handed to structure scenario S7 for gene-model review; the classifiers stay in this repo.

That sentence is correct for the protein-level classifiers that remain in F8 (Resistify, NLRtracker, NLRexpress, HRP). After ①-1 and ①-2, the intro need not be rewritten at length.

**Optional clarifying addition after the v4 sentence:**

> This applies to the protein-level classifiers that remain in F8 (Resistify, NLRtracker, NLRexpress, HRP). It does not mean that every tool that can emit an NLR window belongs in F8.

---

## ②-3 — V089–V091 are not out of scope; do not edit PR #1 tonight

Main-catalog section 7 already carries a boundary sentence for miniprot, Liftoff and LiftOn (V089–V091): this catalog only checks presence and copy number; making gene models stays in gene-structure-annotation (structure stage A2 already lists those tools). That placement is the same class as plan A. This erratum does not reopen it and does not write a main-catalog change. Do not edit PR #1 tonight.

---

## Already checked, not raised

- Resistify, NLRtracker, NLRexpress and HRP start from proteins and stay in F8.
- Main-catalog V093 plan A is unchanged.

---

## What this file does not do

- It does not edit function-catalog v4, the structure catalog, either locked `directory_structure_v1.md`, `catalog_v1.md`, `catalog_v1_erratum.md`, or the PR copy of `docs/PANGENOME_CATALOG.md`.
- It does not open, update, or merge a pull request, and it does not change PR #1.
- It does not change plan A for main-catalog ①-3 (V093 stays in section 7 with a locus-list boundary sentence).
