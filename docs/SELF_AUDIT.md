# Self-audit — gene-structure-annotation

**Date:** 2026-09-14 (UTC+8 / Asia/Shanghai)  
**Scope:** Lit + public peer pipelines vs this playbook’s chooser / ROADMAP / PEER list.  
**Hauls:** [`REVIEWS.md`](REVIEWS.md) § Haul 2026-09-14 · [`PEER_PIPELINES.md`](PEER_PIPELINES.md) § Haul 2026-09-14.  
**Sibling FA audit:** [gene-function-annotation `docs/SELF_AUDIT.md`](https://github.com/Xuzhen-Li/gene-function-annotation/blob/main/docs/SELF_AUDIT.md).

Honest rule: if we already cover something, say so. Prefer chooser honesty over tool spam.

## Gap table

| Gap | Evidence from lit / peer | Action taken or deferred |
|-----|--------------------------|---------------------------|
| Missing plant best-practice essay beyond Freedman | Vuruputoor et al. *Appl Plant Sci* 2023 doi:10.1002/aps3.11533 | **Taken:** Tier A haul in REVIEWS; **no** ROADMAP rewrite — soft-mask + combined evidence + filters already trunk. |
| Protist / divergent-eukaryote stacks under-documented | Eukan *NAR Genom Bioinform* 2026 doi:10.1093/nargab/lqag003 · github.com/BFL-lab/eukan | **Taken:** PEER entry (S14-class); **deferred:** no new S-ID (rare for our plant/animal default). |
| Pan-genome / phased Nextflow peer missing | GenePAL (Plant & Food Research) Zenodo doi:10.5281/zenodo.14195006 | **Taken:** PEER entry → maps S1+S11+FA hand-off; **deferred:** no pan-genome S-branch (out of spine). |
| Helixer+Mikado combiner not listed | RAGNAROK bioRxiv doi:10.1101/2025.10.03.680343 | **Taken:** PEER + REVIEWS Tier B; **deferred:** preprint — not METHODS default. |
| Foundation-model gene segmentation | SegmentNT *Nat Methods* 2025 doi:10.1038/s41592-025-02881-2 | **Taken:** S13 watchlist in PEER/REVIEWS; ROADMAP one-line under S13. |
| nf-core/genomeannotator & nf-annotate only name-dropped | nf-co.re/genomeannotator · github.com/nschan/nf-annotate | **Taken:** fleshed PEER entries (S14 / plant EVM). |
| MAKER exotic multi-genome Nextflow | EXOGAP github.com/dorinemerlat/exogap | **Taken:** PEER (MAKER alternate); out of default spine. |
| Helixer+EGAPx unified QC pack | AnnoCheck github.com/adlnosk/AnnoCheck | **Taken:** PEER (S13+S8+A5b). |
| DToL / Ensembl genebuild SOP | Ensembl DToL pages; sanger-tol/ensemblgenedownload | **Taken:** institutional PEER note — **consume** refs (S11), do not claim DIY Ensembl. |
| MoGAAAP paper DOI not in REVIEWS | *NAR Genom Bioinform* 2026 doi:10.1093/nargab/lqag008 | **Taken:** Tier A haul; PEER already had tool note. |
| Palm Nature review | PubMed Review filter still empty | **Closed as N/A** — already stated; crop Methods only. |
| StringTie compare when RNA exists | Freedman *GR* 2025; Ji *NRG* 2026 | **Already covered** — S1 + chooser. |
| TOGA monocot caveat | Freedman 2025 | **Already covered** — S11/TOGA2 notes. |
| AI ab initio ≠ silent S1 replace | Helixer/ANNEVO/EviAnn + Hiller commentary | **Already covered** — S13 rule; commentary added. |
| BUSCO-only QC insufficient | OMArk / PSAURON / MoGAAAP | **Already covered** — A5b / PLAYBOOK. |

## Chooser honesty (unchanged defaults)

```text
Close curated ref → S11
RNA + proteins    → S1 (+ StringTie compare)
Proteins only     → S2
Heavy Iso-seq     → S3
GPU / thin evid.  → S13 compare (incl. SegmentNT watchlist)
EVM/PASA classic  → S14 (± Eukan for divergent taxa)
```

## What we deliberately did **not** do

- Add a new draft S-ID for GenePAL, RAGNAROK, SegmentNT, or Eukan.
- Promote bioRxiv-only RAGNAROK to default METHODS.
- Mirror Ensembl genebuild as a local runnable spine.
- Stuff FA tools into this repo (still sibling).

## Follow-ups (deferred)

| Item | Why wait |
|------|----------|
| RAGNAROK peer-reviewed version | Update PEER weight when published. |
| SegmentNT plant gene-model bake-off | Needs lab GPU time; keep watchlist. |
| Palm-specific review | None exists in Nature family. |
