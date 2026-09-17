# Post-assembly path (one page)

English ops checklist after you have a genome FASTA. **No real sequences in this repo** — fill paths on your cluster.

Sibling after proteins: [gene-function-annotation](https://github.com/Xuzhen-Li/gene-function-annotation).

```text
Asm1 OK → trusted TE → evidence → draft → QC → golden pack → handoff FA
```

| Step | Done when | Open |
|------|-----------|------|
| **1. Asm1 OK** | `ASSEMBLY_OK=yes` (or finished-genome note + source/version); lineage name set | [`../pipeline/Asm1_assembly_qc.md`](../pipeline/Asm1_assembly_qc.md) · [`LINEAGES.md`](LINEAGES.md) |
| **2. Trusted TE → soft-mask** | Trusted curatedlib path + **real sha256** → `GENOME_SOFT`; Soft-mask Done when ticked | [`TRUSTED_TE_PATH.md`](TRUSTED_TE_PATH.md) · [`TE_LIBRARY.md`](TE_LIBRARY.md) · [`../pipeline/A0_softmask.md`](../pipeline/A0_softmask.md) |
| **3. Evidence** | RNA BAM and/or `PROTEIN_DB` paths real (or honest S11 ref GFF) | [`../pipeline/A2_protein_db.md`](../pipeline/A2_protein_db.md) · [`../pipeline/A1b_rna_align.md`](../pipeline/A1b_rna_align.md) |
| **4. Draft (one primary)** | S1 / S11 / … plan from `flow.py`; S11 needs gap-fill for L1 | [`ROADMAP.md`](ROADMAP.md) · [`../pipeline/A2c_liftoff.md`](../pipeline/A2c_liftoff.md) · [`../pipeline/A2e_s11_gapfill.md`](../pipeline/A2e_s11_gapfill.md) · [`../pipeline/A2_run_draft.sh`](../pipeline/A2_run_draft.sh) |
| **5. QC + curation** | AGAT → proteins → BUSCO/PSAURON → priority → GSAman as needed | [`STAGE_IO.md`](STAGE_IO.md) · [`EVALUATION.md`](EVALUATION.md) · [`EVALUATION_CHECKLIST.md`](EVALUATION_CHECKLIST.md) |
| **6. Golden pack** | `release/<TAG>/` has GFF + proteins + METHODS + qc (EXAMPLE layout only in git) | [`../examples/golden_pack/`](../examples/golden_pack/) · [`../pipeline/check_release_pack.py`](../pipeline/check_release_pack.py) |
| **7. Handoff FA** | Point FA `PROTEINS_FA` at **this** release proteins + `RELEASE_TAG` | [`HANDOFF_STRUCTURE_TO_FUNCTION.md`](HANDOFF_STRUCTURE_TO_FUNCTION.md) · [`../pipeline/A6_functional_optional.md`](../pipeline/A6_functional_optional.md) · [gene-function-annotation](https://github.com/Xuzhen-Li/gene-function-annotation) |

**Classroom / print-first:** `flow.py` → `my_plan.md` is enough tonight. Soft-mask Done when + real sha256 before any A0 `RUN=1`.

**Hard stops:** `YOUR_SHA256` / empty TE checksum → no A0. Lift-only → **S11-lite** / L0, not S11/L1. Placeholders in `local.env` → `print_qc` `[STOP]` → no cluster.

Start door: [`START_HERE.md`](START_HERE.md) · Branch map: [`ROADMAP.md`](ROADMAP.md) · Wiki: [Evaluate-release](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Evaluate-release)
