# Upstream structural spine (optional)

Biology-general (any species with a genome + evidence). **This repo’s primary deliverable is structural annotation** (GFF + proteins). Functional FA → [gene-function-annotation](https://github.com/Xuzhen-Li/gene-function-annotation).

One-page map (trunk / pick-one / overlays): [`../ROADMAP.md`](../ROADMAP.md).

This is the **main** annotation process. S1–S14 are not side docs; they are named exits from the same spine. The EVM consensus path is **S14** and is fully specified under [`dclab/`](dclab/).

```text
Raw reads
  → Asm0 assemble / phase / scaffold
  → Asm1 QC gate (fail → Asm0)
  → A0 repeat soft-mask (+ ProtExcluder / EDTA)
  → BRANCH PICK (S1–S14)     ← AI: docs/AI_ASSIST.md §3.1
  → draft + merge (branch-specific)
  → A5 AGAT → A3 proteins → BUSCO + PSAURON (+ A5d stage counts)
  → optional S8/S9/S10 repairs (loop)
  → priority → GSAman (S5/S7 depth; S12 stop)
  → qualify → release
```


## Evidence chooser (before you pick an ID)

Same logic as Ji *NRG* 2026 + Freedman *GR* 2025 — full notes in [`../REVIEWS.md`](../REVIEWS.md):

1. **Close curated reference?** → start at **S11** (Liftoff / LiftOn / CAT; vertebrates + WGA: TOGA2). Fill gaps with S1/S2, do not ignore liftover.
2. **RNA + proteins, no close ref?** → **S1** (BRAKER4/3). Always keep a **StringTie→TransDecoder** compare set when RNA exists.
3. **Proteins only?** → **S2** (GALBA/GALBA2).
4. **Deep Iso-seq / evidence-only CDS?** → **S3** (± EviAnn).
5. **GPU ab initio compare / thin evidence?** → **S13** (never a silent replace of S1 when evidence exists).
6. **Function (GO/KEGG/names)?** → stop structure release, then sibling FA repo — not an S-branch.

## Branch pick (main flowchart node)

| ID | When | Draft / merge core |
|----|------|--------------------|
| **S1** | RNA + proteins (no close curated ref) | **BRAKER4 ETP** (or BRAKER3) + GeMoMa → EVM; **StringTie→TransDecoder** compare |
| **S2** | No usable RNA | GALBA/**GALBA2**/GeMoMa + Liftoff → EVM |
| **S3** | Deep Iso-seq / evidence-first | IsoQuant→SQANTI3 (± EviAnn) backbone + BRAKER orphans |
| **S4** | Multi-hap | After S1/S3: Liftoff + SynGAP |
| **S5** | Paper / T2T | S1/S14 + OMArk + deeper GSAman |
| **S6** | Thin evidence | Homology-first provisional |
| **S7** | Family / QTL | Genome draft + HRP/NLR windows + GSAman |
| **S8** | NCBI compare | Parallel EGAPx |
| **S9** | High BUSCO-D | Annotate haps / don’t purge blind |
| **S10** | TE gene inflation | Remask → re-enter draft |
| **S11** | Close curated reference (Ji: prefer liftover first) | **Liftoff / LiftOn / CAT** (± TOGA2 if WGA); provisional until QC |
| **S12** | Stop rules | Freeze when stable |
| **S13** | GPU / AI ab initio | Helixer / Tiberius / ANNEVO / OrionGeno (± Mikado); compare to S1 when evidence exists |
| **S14** | EVM consensus (PASA→EVM→polish) | PASA → Augustus/GeneMark → EVM → PASA polish → filter → rename |

Recipes: [`../SCENARIOS.md`](../SCENARIOS.md).  
S14 detail: [`dclab/README.md`](dclab/README.md).  
Commands spine: [`../DETAILED_GUIDE.md`](../DETAILED_GUIDE.md).  
AI co-pilot: [`../AI_ASSIST.md`](../AI_ASSIST.md).

Peer stacks (GALBA2 / TOGA2 / funannotate2): [`../PEER_PIPELINES.md`](../PEER_PIPELINES.md).

Reviews / decision tree: [`../REVIEWS.md`](../REVIEWS.md) (Ji *NRG* 2026 + Freedman *GR* 2025).

AI ab initio notes: [`../notes/helixer.md`](../notes/helixer.md), [`../notes/tiberius.md`](../notes/tiberius.md), [`../notes/annevo.md`](../notes/annevo.md) (Kai Ye / 叶凯).

Evidence/transfer notes: [`../notes/eviann.md`](../notes/eviann.md), [`../notes/finder.md`](../notes/finder.md), [`../notes/cat.md`](../notes/cat.md), [`../notes/lifton.md`](../notes/lifton.md).

Long-read notes: [`../notes/isoquant.md`](../notes/isoquant.md), [`../notes/sqanti3.md`](../notes/sqanti3.md).
