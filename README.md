# gene-structure-annotation
[中文](README.zh.md)

This repository provides pipelines for structural genome annotation.
Chinese teaching is in [`docs/zh/`](docs/zh/).
Runnable documents stay English in [`docs/BILINGUAL.md`](docs/BILINGUAL.md).
Plant simulations are in [`examples/plant_sim/`](examples/plant_sim/).

## Overview

Structural annotation is the primary layer. It finds genes on a genome and provides coordinates, GFF3, and proteins.

```text
genome FASTA  (+ RNA and/or proteins)
        ↓
 soft-mask (trusted TE lib) → predict gene models → QC → curate
        ↓
  qualified GFF3  +  proteins.faa  +  METHODS
```

TE soft-mask is a prerequisite. TE library construction is a separate job in [vitis-te](https://github.com/Xuzhen-Li/vitis-te) and [`docs/TE_LIBRARY.md`](docs/TE_LIBRARY.md).
GO, KEGG, and readable names are in the sibling repository [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation). This repository does not generate functional annotation tables.

Three layers:
1. Structure: This repository.
2. Function: [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation).
3. TE library build: [vitis-te](https://github.com/Xuzhen-Li/vitis-te) and [`TE_LIBRARY.md`](docs/TE_LIBRARY.md).

Boundary definitions are in [`docs/BOUNDARY.md`](docs/BOUNDARY.md).
![Structure overview](docs/figures/structure_overview.png)

Chinese shortest path is [`docs/zh/README.md`](docs/zh/README.md). English entry point is [`docs/START_HERE.md`](docs/START_HERE.md).
Quickstart is at [Wiki Start-tonight](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Start-tonight). Offline version is [`docs/CLASSROOM_TONIGHT.md`](docs/CLASSROOM_TONIGHT.md).
Track work at [Annotation board (Project #2)](https://github.com/users/Xuzhen-Li/projects/2).

## Usage

Chinese teaching entry is [`docs/zh/`](docs/zh/).
If already assembled, treat Asm0/Asm1 as a checklist and set `ASSEMBLY_OK=yes`. Edit every `/path/to` in `local.env` before any `mkdir`.
For a close curated reference GFF, set `close_curated_ref: true` in your answers (see `examples/plant_sim/03_solanum_s11`). Default `false` gives S1; a half-done Liftoff stays `false`.

Step 1: Provide evidence.
```bash
git clone https://github.com/Xuzhen-Li/gene-structure-annotation.git
cd gene-structure-annotation
cp pipeline/flow_tool/answers.example.yaml my_answers.yaml
# edit yes/no: RNA? proteins? close reference? paper bar?
python3 pipeline/flow_tool/flow.py --answers my_answers.yaml -o my_plan.md
```
Open `my_plan.md` to see the selected branch and stage explanations.

Step 2: Configure paths.
```bash
cp config/example.env config/local.env
# set GENOME_FA, BUSCO_LINEAGE, RNA_BAM / PROTEIN_DB, TE lib, WORK_DIR, THREADS
```

Step 3: Execution.
Finish `my_plan.md`. Read [Wiki Concepts](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Concepts) or [`docs/zh/05_softmask与A0.md`](docs/zh/05_softmask与A0.md). Write `grade=` and `status=` separately. Do not write `status=L1`.
Run on cluster only after [Done when](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Start-tonight#done-when) is ticked and `python3 pipeline/print_qc_commands.py` exits 0 with no `[STOP]`. Otherwise no `RUN=1`. Browsing with `--env config/example.env` will show `[STOP]`; this is expected.
Follow stages in `my_plan.md` and check [`docs/EVALUATION_CHECKLIST.md`](docs/EVALUATION_CHECKLIST.md). Read full rules in [`docs/EVALUATION.md`](docs/EVALUATION.md).
Provisional results are not L1. Read [`docs/EVALUATION.md`](docs/EVALUATION.md) for L0 vs L1.
The default branch is S1 for RNA and proteins with no close reference.
Handoff to function uses [`docs/HANDOFF_STRUCTURE_TO_FUNCTION.md`](docs/HANDOFF_STRUCTURE_TO_FUNCTION.md) with `RELEASE_TAG` and `PROTEINS_FA=…/release/<TAG>/proteins.faa`.

## Branches

Choose a branch based on evidence.
S11: Close curated reference GFF (Liftoff, LiftOn, CAT). Lift-only is S11-lite.
S1: RNA and proteins (BRAKER, StringTie).
S2: Proteins only (GALBA, GeMoMa).
S3: Heavy Iso-seq (IsoQuant, SQANTI).
S13: GPU ab initio comparison (Helixer, Tiberius, ANNEVO).
S14: Classic EVM/PASA (`docs/steps/dclab/`).

Overlays:
L2: Acceptance level L1 plus S5 overlay for Paper/T2T bar.
S7: Plant NLR or tandem windows overlay when `plant_tandem_focus: true`.

Full map is at [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Documentation

Chinese teaching and start is [`docs/zh/`](docs/zh/) and [`docs/START_HERE.md`](docs/START_HERE.md).

Narrated auto-plan: [`pipeline/flow_tool/`](pipeline/flow_tool/)
Stage I/O and evaluation: [`docs/STAGE_IO.md`](docs/STAGE_IO.md), [`docs/EVALUATION_CHECKLIST.md`](docs/EVALUATION_CHECKLIST.md), [`docs/EVALUATION.md`](docs/EVALUATION.md)
TE soft-mask: [`docs/TE_LIBRARY.md`](docs/TE_LIBRARY.md), [`docs/TRUSTED_TE_PATH.md`](docs/TRUSTED_TE_PATH.md)
Branch map and walkthrough: [`docs/ROADMAP.md`](docs/ROADMAP.md), [`docs/QUICKSTART.md`](docs/QUICKSTART.md)
Three-layer boundary: [`docs/BOUNDARY.md`](docs/BOUNDARY.md)
Post-assembly notes: [`docs/POST_ASSEMBLY.md`](docs/POST_ASSEMBLY.md)
QC sources: [`docs/QUALITY_SOURCES.md`](docs/QUALITY_SOURCES.md)
EDTA manual: [`docs/tools/edta.md`](docs/tools/edta.md)
BUSCO lineages: [`docs/LINEAGES.md`](docs/LINEAGES.md)
S11 gap-fill: [`pipeline/A2e_s11_gapfill.md`](pipeline/A2e_s11_gapfill.md), [`pipeline/A2c_liftoff.md`](pipeline/A2c_liftoff.md)
Golden pack checklist: [`examples/golden_pack/`](examples/golden_pack/)
Protein database: [`pipeline/A2_protein_db.md`](pipeline/A2_protein_db.md)
Helixer vs BRAKER: [`docs/COMPARE_HELIXER_BRAKER.md`](docs/COMPARE_HELIXER_BRAKER.md)
Merge and entry modes: [`docs/MERGE_AND_ENTRIES.md`](docs/MERGE_AND_ENTRIES.md)
Multi-source aggregation (EVM, optional TSEBRA / Mikado / PASA update): [`pipeline/A4_aggregation.md`](pipeline/A4_aggregation.md) [[TODO-TEXT]]
EGAPx compare: [`docs/EGAPX_COMPARE.md`](docs/EGAPX_COMPARE.md)
Scenarios and tools: [`docs/SCENARIOS.md`](docs/SCENARIOS.md), [`docs/TOOLS.md`](docs/TOOLS.md), [`docs/cases/vitis-t2t-s1-s5.md`](docs/cases/vitis-t2t-s1-s5.md), [`docs/TUTORIALS_AND_MEETINGS.md`](docs/TUTORIALS_AND_MEETINGS.md), [`docs/PLAYBOOK.md`](docs/PLAYBOOK.md)

## Scope

This is not functional annotation. Use [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation) for GO/KEGG.
This is not a standalone TE library build. Use [vitis-te](https://github.com/Xuzhen-Li/vitis-te) and `docs/TE_LIBRARY.md`.
This is not for pangenome graphs. Use [vitis-pangenome](https://github.com/Xuzhen-Li/vitis-pangenome).
Do not commit private FASTQ/BAM files.

Author: Xuzhen Li, [ORCID](https://orcid.org/0000-0003-3670-6657).