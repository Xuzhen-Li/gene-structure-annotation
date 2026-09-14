# gene-structure-annotation

> **New here?** Start with [`docs/QUICKSTART.md`](docs/QUICKSTART.md) (run + understand) and [`docs/STAGE_IO.md`](docs/STAGE_IO.md) (what each step produces).

**Main product: structural gene annotation** — genome → qualified GFF + proteins.

Biology-general teaching / METHODS playbook (not grape-only, not plant-only). Plant engines (BRAKER / GALBA / GeMoMa) are the richest worked examples; set BUSCO lineage, OrthoDB partition, and soft-mask libraries for your clade. Formerly `plant-gene-annotation`.

Functional annotation (GO / KEGG / domains) lives in sibling [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation).

| Doc | |
|-----|--|
| **[`docs/ROADMAP.md`](docs/ROADMAP.md)** | **Branch map** — trunk vs pick-one draft vs overlays |
| **[`docs/QUICKSTART.md`](docs/QUICKSTART.md)** | **Start here** — run default S1 and learn each product |
| [`docs/STAGE_IO.md`](docs/STAGE_IO.md) | Every stage: inputs → outputs → how to check |
| [`docs/TE_LIBRARY.md`](docs/TE_LIBRARY.md) | **TE scheme** → soft-mask (EDTA→curate→A0; docks [vitis-te](https://github.com/Xuzhen-Li/vitis-te)) |
| [`docs/cases/vitis-t2t-s1-s5.md`](docs/cases/vitis-t2t-s1-s5.md) | **Delivery case:** *Vitis* T2T × S1 engine + S5 bar |
| **[`docs/PLAYBOOK.md`](docs/PLAYBOOK.md)** | End-to-end spine + qualification checklist |
| **[`docs/steps/MAIN.md`](docs/steps/MAIN.md)** | Branch pick S1–S14 |
| **[`docs/SCENARIOS.md`](docs/SCENARIOS.md)** | Scenario recipes |
| **[`docs/DETAILED_GUIDE.md`](docs/DETAILED_GUIDE.md)** | Copy-paste steps |
| [`docs/steps/dclab/`](docs/steps/dclab/) | S14 EVM / PASA path |
| [`docs/AI_ASSIST.md`](docs/AI_ASSIST.md)| Co-pilot prompts / checks |
| [`docs/TOOLS.md`](docs/TOOLS.md) | Tool index |
| [`config/example.env`](config/example.env) | Paths / threads / lineages |
| [`docs/PEER_PIPELINES.md`](docs/PEER_PIPELINES.md) | Biology-wide peer stacks (GALBA2 / TOGA2 / funannotate2; Haul 2026-09-14) |
| [`docs/REVIEWS.md`](docs/REVIEWS.md) | Reviews & chooser (Ji *NRG* 2026 + Freedman *GR* 2025; Haul 2026-09-14) |
| [`docs/SELF_AUDIT.md`](docs/SELF_AUDIT.md) | 2026-09-14 self-audit gap table (lit + peers) |

## Inputs → outputs

| | What |
|--|------|
| **In** | Genome FASTA (+ RNA BAM and/or proteins; TE lib) |
| **Out (primary)** | Curated / qualified GFF + `proteins.faa` + METHODS |
| **Next** | Hand proteins to [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation) for F1 FA |


## Evidence → branch (chooser)

Framed like Ji, Pertea & Salzberg (*Nat Rev Genet* 2026 Fig. 2): **what evidence you have** decides the draft path. Details and citations: [`docs/REVIEWS.md`](docs/REVIEWS.md).

```text
Asm0 → Asm1 → A0 soft-mask
        │
        ▼
   What do you have?
        │
        ├─ Close, curated reference annotation
        │     → S11 first: Liftoff / LiftOn / CAT (± TOGA2 if WGA)
        │       then qualify; de novo only to fill gaps
        │
        ├─ RNA-seq + proteins (no close ref)
        │     → S1: BRAKER4/3 (± GeMoMa) + StringTie→TransDecoder compare
        │
        ├─ Proteins only
        │     → S2: GALBA / GALBA2 / GeMoMa
        │
        ├─ Deep Iso-seq / want traceable evidence CDS
        │     → S3: IsoQuant→SQANTI3 (± EviAnn)
        │
        ├─ GPU / thin evidence ab initio compare
        │     → S13: Helixer / Tiberius / ANNEVO (not a silent S1 replace)
        │
        └─ NCBI / GenBank package compare
              → S8: EGAPx / Gnomon
        │
        ▼
   Merge / AGAT → proteins → BUSCO + PSAURON → GSAman → qualify → release
        │
        ▼
   Hand proteins to gene-function-annotation (F1)  ← function is a second layer
```

| Evidence | Prefer | Avoid as sole draft |
|----------|--------|---------------------|
| Near-identical / same-species curated GFF | **S11** liftover | Starting BRAKER from scratch |
| Illumina RNA + OrthoDB/proteins | **S1** + StringTie compare | Ab initio-only (no UTRs / multi-isoform) |
| Proteins, little/no RNA | **S2** | Claiming complete UTRs |
| Long-read / Iso-seq heavy | **S3** (± EviAnn) | Ignoring SQANTI filters |
| WGA to close clade | TOGA2 / LiftOn (with S11 or S1) | Blind TOGA on tough monocots without BUSCO check |

Unsure with RNA+proteins? **S1**. Full map (draft vs overlay): [`docs/ROADMAP.md`](docs/ROADMAP.md). Recipes: [`docs/SCENARIOS.md`](docs/SCENARIOS.md).


```bash
git clone https://github.com/Xuzhen-Li/gene-structure-annotation.git
cd gene-structure-annotation
cp config/example.env config/local.env   # set GENOME_FA, BUSCO_LINEAGE, evidence paths
# docs/PLAYBOOK.md → docs/SCENARIOS.md (one branch) → release checklist
```

## This is not

- Not functional annotation — [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation)
- Not TE-only — species TE lib (grape example: [vitis-te](https://github.com/Xuzhen-Li/vitis-te))
- Not graphs / synteny — [vitis-pangenome](https://github.com/Xuzhen-Li/vitis-pangenome), [vitis-synteny](https://github.com/Xuzhen-Li/vitis-synteny)

No private FASTQ/BAM in git.

**Agent skill:** `skills/gene-structure-annotation/` (optional Cursor skill install).

**Author:** Xuzhen Li · [ORCID](https://orcid.org/0000-0003-3670-6657)
