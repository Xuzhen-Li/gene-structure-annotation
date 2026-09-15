# Annotation quality — methods, papers, repos

Short map of **how peers judge “is this annotation OK?”**  
Our grades stay in [`EVALUATION.md`](EVALUATION.md) / [`EVALUATION_CHECKLIST.md`](EVALUATION_CHECKLIST.md).  
This page is the **source shelf** (cite / optional run), not a second checklist.

Chinese: [`zh/15_为什么质控是这些指标.md`](zh/15_为什么质控是这些指标.md) · [`zh/验收勾选表.md`](zh/验收勾选表.md)

---

## Spine we already require (do not replace)

| Need | Tool / idea | Role here |
|------|-------------|-----------|
| Conserved completeness | **BUSCO** (protein mode for gene set) | Hard gate **G6** — Completeness **+ lineage** |
| Model “looks coding” triage | **PSAURON** | Hard gate **G7** (+ priority list) |
| Family completeness + consistency + contamination | **OMArk** | Soft at L1; **required for L2/S5** |
| GFF hygiene + counts | **AGAT** / gffread | Hard gate **G4** |
| Multi-metric pack (peer) | **MoGAAAP** QC | Reinforces provisional Liftoff+Helixer + BUSCO/OMArk — not a new default draft |

Key papers (already in [`REVIEWS.md`](REVIEWS.md)):

- OMArk — Nevers et al. *Nat Biotechnol* 2025, doi:[10.1038/s41587-024-02147-w](https://doi.org/10.1038/s41587-024-02147-w) · https://omark.omabrowser.org/
- PSAURON — *NAR Genom Bioinform*, doi:[10.1093/nargab/lqae189](https://doi.org/10.1093/nargab/lqae189) · https://github.com/salzberg-lab/PSAURON
- MoGAAAP — van Workum et al. *NAR Genom Bioinform* 2026, doi:[10.1093/nargab/lqag008](https://doi.org/10.1093/nargab/lqag008) · https://github.com/dirkjanvw/MoGAAAP
- Evidence→method — Ji/Pertea/Salzberg *NRG* 2026; Freedman/Sackton *Genome Res* 2025

---

## High-value add-ons (soft / optional wrappers)

Use these to **strengthen METHODS**, not to invent new universal %-cutoffs.

| Method | What it adds | How we use it | Link |
|--------|--------------|---------------|------|
| **Compleasm** | Fast BUSCO-ortholog completeness via miniprot; good cross-check vs BUSCO | Soft metric: report beside G6; same lineage family; do **not** drop named BUSCO lineage | doi:[10.1093/bioinformatics/btad595](https://doi.org/10.1093/bioinformatics/btad595) · https://github.com/huangnengCSU/compleasm |
| **gffcompare** | Overlap / missing / novel loci vs a reference or second draft | Soft when you have RNA draft or close ref (S1 StringTie compare / S11) | https://github.com/gpertea/gffcompare |
| **RNA support + BRH** | Fraction of models with RNA coverage; reciprocal hits to a trusted proteome | Soft at L1 if RNA exists; **recommended for L2** narrative | Pattern from **AnnoAudit** (ERGA) |
| **GAQET2** | One-stop: AGAT + BUSCO + PSAURON + OMArk (+ DeTEnGA TE flags, optional DIAMOND) | Optional **wrapper** around our gates — still tick our checklist | https://github.com/victorgcb1987/GAQET2 · protocol doi:[10.17504/protocols.io.8epv5k5rnv1b/v1](https://doi.org/10.17504/protocols.io.8epv5k5rnv1b/v1) |
| **AnnoAudit** | Nextflow: GFF stats + RNA support + BUSCO/OMArk + BRH | Optional community audit pack (esp. if you already have BAM) | https://github.com/ERGA-consortium/AnnoAudit · WorkflowHub [1330](https://workflowhub.eu/workflows/1330) |
| **atol-qc-annotation** | AGAT extract → BUSCO + OMArk for AToL-style reports | Optional thin QC | https://github.com/TomHarrop/atol-qc-annotation |
| **AnnoOddities** (EI) | Standardise / flag GFF oddities before QC | Optional pre-clean before AGAT counts | https://github.com/EI-CoreBioinformatics/annooddities |
| **DeTEnGA** (via GAQET2) | TE-like content inside gene models | Soft plant metric — complements trusted soft-mask honesty (G2) | Bundled with GAQET2 |

Internal notes: [`notes/omark_compleasm.md`](notes/omark_compleasm.md) · [`notes/psauron_gaqet_annoaudit.md`](notes/psauron_gaqet_annoaudit.md) · [`PEER_PIPELINES.md`](PEER_PIPELINES.md)

---

## What we deliberately do **not** add as hard gates

| Idea | Why not a hard gate here |
|------|---------------------------|
| Universal BUSCO-C ≥ X% | Clade/assembly dependent (Freedman); set bar in Asm1/S5 |
| CAFA / DL-GO accuracy | Function layer; research benchmark ≠ production FA ([FA EVALUATION](https://github.com/Xuzhen-Li/gene-function-annotation/blob/main/docs/EVALUATION.md)) |
| Requiring GAQET2/AnnoAudit to ship | Nice wrappers; cluster/deps vary — keep optional |
| Compleasm **instead of** BUSCO | Different aligner/behaviour; keep BUSCO lineage as the common language |
| MoGAAAP Liftoff+Helixer as default L1 | Provisional only — our auto-fail still blocks silent S13 replace of S1 |

---

## Minimal METHODS snippet (optional extras)

```text
QC spine: BUSCO protein (<lineage>) ; PSAURON ; AGAT counts ; [OMArk if L2].
Optional: Compleasm (<same lineage family>) ; gffcompare vs <ref/draft> ;
RNA exon support % ; BRH vs <proteome> ; [GAQET2|AnnoAudit run id].
```

## Print recommended commands

```bash
set -a && source config/local.env && set +a
python3 pipeline/print_qc_commands.py          # default L1
python3 pipeline/print_qc_commands.py --grade L2
```
Print-first only — see also `pipeline/01_qc_busco_psauron.sh`, `A5_agat_stats.sh`, `A5b_omark_compleasm.sh`.
