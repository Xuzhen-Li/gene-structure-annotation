# Stage reference (assembly → release)

**Main process index:** [`steps/MAIN.md`](steps/MAIN.md) · AI: [`AI_ASSIST.md`](AI_ASSIST.md) · S14: [`steps/dclab/`](steps/dclab/).

Human guides: [`PLAYBOOK.md`](PLAYBOOK.md) · [`SCENARIOS.md`](SCENARIOS.md).  
**Branch diagram:** repository README.

| Stage | Path |
|-------|------|
| Asm0 Assembly | [`../pipeline/Asm0_assembly.md`](../pipeline/Asm0_assembly.md) |
| Asm1 Assembly QC | [`../pipeline/Asm1_assembly_qc.md`](../pipeline/Asm1_assembly_qc.md) |
| A0 / A0b Soft-mask | `A0_softmask.md` · `A0b_protexcluder.md` |
| A1 / A1b | engine · RNA |
| A2 / A2b / A2c / A2d | drafts · Liftoff · EGAPx |
| A4 Merge | `A4_merge_sets.sh` |
| A5 / A5b / A5c | AGAT · OMArk · expression filter |
| A3 Proteins | `A3_proteins_from_gff.sh` |
| 01–06 Last mile | QC → GSAman → SynGAP → release |
| A6 Function | optional |

Default branch: **S1** after Asm0–A0.
