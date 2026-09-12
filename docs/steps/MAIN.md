# Upstream structural spine (optional)

Biology-general (any species with a genome + evidence). **This repo’s primary deliverable is structural annotation** (GFF + proteins). Functional FA → [gene-function-annotation](https://github.com/Xuzhen-Li/gene-function-annotation).

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

## Branch pick (main flowchart node)

| ID | When | Draft / merge core |
|----|------|--------------------|
| **S1** | RNA + proteins | **BRAKER4 ETP** (or BRAKER3) + GeMoMa/Liftoff → EVM |
| **S2** | No usable RNA | GALBA/**GALBA2**/GeMoMa + Liftoff → EVM |
| **S3** | Deep Iso-seq | EviAnn backbone + BRAKER orphans |
| **S4** | Multi-hap | After S1/S3: Liftoff + SynGAP |
| **S5** | Paper / T2T | S1/S14 + OMArk + deeper GSAman |
| **S6** | Thin evidence | Homology-first provisional |
| **S7** | Family / QTL | Genome draft + HRP/NLR windows + GSAman |
| **S8** | NCBI compare | Parallel EGAPx |
| **S9** | High BUSCO-D | Annotate haps / don’t purge blind |
| **S10** | TE gene inflation | Remask → re-enter draft |
| **S11** | Quick IDs | Liftoff / LiftOn (vertebrates: consider TOGA2) provisional |
| **S12** | Stop rules | Freeze when stable |
| **S13** | GPU / AI ab initio | Helixer / Tiberius / ANNEVO (± Mikado); compare to S1 when evidence exists |
| **S14** | EVM consensus (PASA→EVM→polish) | PASA → Augustus/GeneMark → EVM → PASA polish → filter → rename |

Recipes: [`../SCENARIOS.md`](../SCENARIOS.md).  
S14 detail: [`dclab/README.md`](dclab/README.md).  
Commands spine: [`../DETAILED_GUIDE.md`](../DETAILED_GUIDE.md).  
AI co-pilot: [`../AI_ASSIST.md`](../AI_ASSIST.md).

Peer stacks (GALBA2 / TOGA2 / funannotate2): [`../PEER_PIPELINES.md`](../PEER_PIPELINES.md).

AI ab initio notes: [`../notes/helixer.md`](../notes/helixer.md), [`../notes/tiberius.md`](../notes/tiberius.md), [`../notes/annevo.md`](../notes/annevo.md) (Kai Ye / 叶凯).
