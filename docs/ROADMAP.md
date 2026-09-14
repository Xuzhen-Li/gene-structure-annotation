# Branch roadmap — gene structure

One page: **what is the trunk**, **which S-IDs pick a draft engine**, **which only overlay**.  
Recipes: [`SCENARIOS.md`](SCENARIOS.md) · chooser detail: [`steps/MAIN.md`](steps/MAIN.md) · reviews: [`REVIEWS.md`](REVIEWS.md).

Sibling function layer (after proteins): [gene-function-annotation `ROADMAP`](https://github.com/Xuzhen-Li/gene-function-annotation/blob/main/docs/ROADMAP.md).

---

## Big picture (two layers)

```text
genome + evidence
        │
        ▼
┌───────────────────────────────┐
│  gene-structure-annotation    │  ← this repo
│  trunk → ONE draft branch     │
│  → merge → QC → curated GFF   │
│  → proteins.faa + METHODS     │
└───────────────┬───────────────┘
                │ hand proteins
                ▼
┌───────────────────────────────┐
│  gene-function-annotation     │
│  F0 → F1 → optional add-ons   │
│  → functional_master.tsv      │
└───────────────────────────────┘
```

---

## Trunk (every successful run rejoins)

Do these in order. Branches only replace the **draft** middle.

```text
Asm0   assemble / phase / purge / scaffold
  │
Asm1   assembly QC gate  (fail → back to Asm0)
  │
A0     soft-mask with **trusted** TE lib   ← docs/TE_LIBRARY.md
  │
  ├──── DRAFT BRANCH (pick ONE primary) ────┐
  │         S11 / S1 / S2 / S3 / S13 / S14 / S6
  │                                         │
  ▼                                         ▼
A4/A5  merge + AGAT (if dual draft)   ◄─────┘
  │
A3     proteins from GFF
  │
01     BUSCO proteins + PSAURON (+ optional OMArk)
  │
02     priority loci list
  │
04     GSAman (depth depends on goal; see overlays)
  │
05     SynGAP if multi-haplotype
  │
06     re-QC → qualified release (PLAYBOOK checklist)
  │
       proteins → gene-function-annotation (F1)
```

Default when unsure and you have RNA+proteins: **S1**, then rejoin at A4/A5.

---

## A. Draft branches — pick **one** primary

These decide *how gene models are invented*. Start from evidence (Ji *NRG* 2026).

| Pick | Evidence you have | Engine (short) | Do not treat as |
|------|-------------------|----------------|-----------------|
| **S11** | Close, curated reference GFF | Liftoff / LiftOn / CAT (± TOGA2 if WGA) | Optional afterthought — prefer **before** de novo |
| **S1** | Illumina RNA + proteins, no close ref | BRAKER4/3 (± GeMoMa) + StringTie→TransDecoder compare | Ab initio-only story |
| **S2** | Proteins, little/no RNA | GALBA / GALBA2 / GeMoMa | Complete UTR claims |
| **S3** | Deep Iso-seq / evidence CDS | IsoQuant→SQANTI3 (± EviAnn) + BRAKER orphans | Ignoring SQANTI filters |
| **S13** | GPU / thin-evidence ab initio **compare** | Helixer / Tiberius / ANNEVO | Silent replace of S1 when RNA exists |
| **S14** | Classic EVM consensus stack | PASA → Augustus/GeneMark → EVM → polish ([`steps/dclab/`](steps/dclab/)) | Required for every genome |
| **S6** | Thin evidence, provisional OK | Homology-first draft | “Publication-final” without saying provisional |

**Chooser (one glance):**

```text
Close curated ref?     → S11 first
RNA + proteins?        → S1
Proteins only?         → S2
Heavy Iso-seq?         → S3
Want GPU compare?      → S13 (alongside, not instead of S1 if RNA exists)
Want full EVM/PASA?    → S14
Almost no evidence?    → S6 provisional
```

---

## B. Overlay branches — **not** a second draft pick

These modify QC depth, compare packs, or loop back. They sit **on top of** a draft branch (usually S1/S11/S14).

| ID | Role | Typical attach |
|----|------|----------------|
| **S4** | Multi-haplotype transfer + SynGAP | After S1 or S3 |
| **S5** | Paper / T2T bar (OMArk + deeper GSAman) | On S1 or S14 — see [`cases/vitis-t2t-s1-s5.md`](cases/vitis-t2t-s1-s5.md) |
| **S7** | Family / QTL / NLR window focus | Any draft + HRP windows |
| **S8** | Parallel NCBI EGAPx / Gnomon compare | Beside S1 (not instead) |
| **S9** | High BUSCO-D / don’t purge haplotypes blind | Asm1 / filter policy |
| **S10** | TE gene inflation → remask → re-enter draft | Loop to A0 then same draft ID |
| **S12** | Stop / freeze rules | End of curation |

```text
Example paper path:   Asm* → A0 → S1 → (+S5 bar) → trunk QC → release
Example liftover:     Asm* → A0 → S11 → fill gaps with S1/S2 → trunk
Example TE blow-up:   … → S10 remask → re-run same draft branch
```

---

## C. What is **not** an S-branch

| Need | Where |
|------|--------|
| GO / KEGG / domains / names | [gene-function-annotation](https://github.com/Xuzhen-Li/gene-function-annotation) F-line |
| TE library build / panEDTA | [`TE_LIBRARY.md`](TE_LIBRARY.md) · [vitis-te](https://github.com/Xuzhen-Li/vitis-te) |
| PAV / graphs | vitis-pangenome (sibling) |

---

## Quick links

| Doc | Use |
|-----|-----|
| [`QUICKSTART.md`](QUICKSTART.md) | Run default S1 once |
| [`STAGE_IO.md`](STAGE_IO.md) | Inputs → products per stage |
| [`PLAYBOOK.md`](PLAYBOOK.md) | Qualification checklist |
| [`SCENARIOS.md`](SCENARIOS.md) | Step recipes per S-ID |
| [`steps/MAIN.md`](steps/MAIN.md) | Same map, tool-oriented |
