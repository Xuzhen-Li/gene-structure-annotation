# gene-structure-annotation

**Main product: structural gene annotation** — genome → qualified GFF + proteins.

Biology-general teaching / METHODS playbook (not grape-only, not plant-only). Plant engines (BRAKER / GALBA / GeMoMa) are the richest worked examples; set BUSCO lineage, OrthoDB partition, and soft-mask libraries for your clade. Formerly `plant-gene-annotation`.

Functional annotation (GO / KEGG / domains) lives in sibling [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation).

| Doc | |
|-----|--|
| **[`docs/PLAYBOOK.md`](docs/PLAYBOOK.md)** | End-to-end spine + qualification checklist |
| **[`docs/steps/MAIN.md`](docs/steps/MAIN.md)** | Branch pick S1–S14 |
| **[`docs/SCENARIOS.md`](docs/SCENARIOS.md)** | Scenario recipes |
| **[`docs/DETAILED_GUIDE.md`](docs/DETAILED_GUIDE.md)** | Copy-paste steps |
| [`docs/steps/dclab/`](docs/steps/dclab/) | S14 EVM / PASA path |
| [`docs/AI_ASSIST.md`](docs/AI_ASSIST.md)| Co-pilot prompts / checks |
| [`docs/TOOLS.md`](docs/TOOLS.md) | Tool index |
| [`config/example.env`](config/example.env) | Paths / threads / lineages |
| [`docs/PEER_PIPELINES.md`](docs/PEER_PIPELINES.md) | Biology-wide peer stacks (GALBA2 / TOGA2 / funannotate2) |

## Inputs → outputs

| | What |
|--|------|
| **In** | Genome FASTA (+ RNA BAM and/or proteins; TE lib) |
| **Out (primary)** | Curated / qualified GFF + `proteins.faa` + METHODS |
| **Next** | Hand proteins to [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation) for F1 FA |

## Default line

```text
Asm0 → Asm1 → A0 soft-mask
  → pick ONE branch (default S1 if RNA+proteins)
  → merge / AGAT → proteins → BUSCO (+ PSAURON)
  → GSAman depth by scenario → qualify → release
```

Unsure? **S1** (RNA + proteins → BRAKER4/3 ± GeMoMa/Liftoff → EVM).  
No usable RNA? **S2**. Deep Iso-seq? **S3**. Classic PASA→EVM? **S14** (`docs/steps/dclab/`).

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
