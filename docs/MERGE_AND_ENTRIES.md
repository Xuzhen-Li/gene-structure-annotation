# Entry modes + merge QC (process guide)

**Purpose:** one page for *how you enter this repo* and *what “merge” means before L1* — inspired by multi-entry teaching peers (e.g. GenAnT), **not** their animal tool stack.

**Not in scope here:** shipping a full Snakemake DAG, animal ncRNA defaults, or Mikado as a silent production combiner. External automation examples only — do **not** add Snakemake to this repo because of this page.

---

## Three entry modes (this repo)

| Mode | What you do | Honest stop |
|------|-------------|-------------|
| **1. Classroom / print-first** | Edit answers → `flow.py` → open **`my_plan.md`** (± list paths in `local.env`) | Stop. No BRAKER / Liftoff / `RUN=1` required tonight. |
| **2. Stage walk** | Follow stages in `my_plan.md`; when Ready, use `print_qc_commands.py` / helpers; only then `RUN=1` on cluster | No green `print_qc` / unchecked Done-when ⇒ **no** `RUN=1` |
| **3. Full automation (out of scope)** | Not provided here | See external peers below — **do not** treat them as this repo’s default |

Doors: [`START_HERE.md`](START_HERE.md) · [`../README.md`](../README.md) · wiki [Start-tonight](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Start-tonight) · [Choose-branch](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Choose-branch).

**External Snakemake / automation examples only** (read, do not fork into spine):

- [GenAnT](https://github.com/BaderLab/GenAnT) — **animal teaching peer** (mammalian tutorial + optional GAT_Snakemake); multi-entry pedagogy, not our plant defaults
- [MoGAAAP](https://github.com/dirkjanvw/MoGAAAP) — Liftoff+Helixer **provisional** + QC pack (maps to S11/S13 language; still provisional ≠ L1)

---

## What “merge” means in our ROADMAP

Trunk: pick **one primary** draft branch → optional second track → **A4/A5** (merge + AGAT) → proteins → QC → release ([`ROADMAP.md`](ROADMAP.md)).

| Situation | Merge meaning here | Pointers (existing — no new scripts) |
|-----------|--------------------|--------------------------------------|
| Single draft | **A4skip** — `MERGED_GFF=$DRAFT_GFF`; still run AGAT | [`SCENARIOS.md`](SCENARIOS.md) · [`DETAILED_GUIDE.md`](DETAILED_GUIDE.md) Step 7 |
| Two BRAKER-family GTFs | **TSEBRA** (`MERGE_MODE=tsebra`) | [`tools/tsebra.md`](tools/tsebra.md) |
| Heterogeneous tracks (e.g. BRAKER + GeMoMa, lift + de novo) | **EVM** (or documented combiner) + weights; then AGAT cleanup | `pipeline/A4_merge_sets.sh` · A5 AGAT |
| BRAKER primary + Helixer compare | Keep **S1 as primary**; Helixer = **S13** side-by-side — not a silent replace | [`COMPARE_HELIXER_BRAKER.md`](COMPARE_HELIXER_BRAKER.md) |
| Liftoff + gap-fill | Full **S11** = lift **+** gap-fill **+** trunk QC; lift-only = **S11-lite** | [`../pipeline/A2e_s11_gapfill.md`](../pipeline/A2e_s11_gapfill.md) |

Priority loci / GSAman sit **after** a named merged (or single) GFF — they do not invent a second primary ([`PLAYBOOK.md`](PLAYBOOK.md)).

---

## QC before calling L1

Multi-draft work is still **provisional** until you declare a **primary draft ID** and pass gates.

**Before `grade=L1`:**

1. **METHODS names one primary** — `primary=S1|S11|S11-lite|…` + tool versions (EVALUATION G3).
2. **Valid GFF + counts** — AGAT / gffread after merge (G4).
3. **Multi-metric QC** — protein **BUSCO** and/or **Compleasm**; **gffcompare** when a reference or second draft exists; **OMArk** required for **L2** / S5 (recommended for careful L1).
4. **Provisional honesty** — Liftoff-only, Helixer-only, or multi-draft **without** a declared primary ⇒ stay **`grade=L0`**, `status=provisional`. MoGAAAP-style Liftoff+Helixer merge is useful and still provisional until evidence primary + gates.

Full rules: [`EVALUATION.md`](EVALUATION.md) · checklist: [`EVALUATION_CHECKLIST.md`](EVALUATION_CHECKLIST.md) · Chinese: [`zh/PROVISIONAL_NOT_L1.md`](zh/PROVISIONAL_NOT_L1.md).

---

## Explicit non-goals

| We do **not** | Instead |
|---------------|---------|
| Ship animal **ncRNA** / Infernal defaults as spine | Optional notes only; plant coding GFF is the product |
| Ship **Mikado** as default combiner | Peer / S13 notes ([`PEER_PIPELINES.md`](PEER_PIPELINES.md)); primary stays evidence branch |
| Add GenAnT / MoGAAAP Snakemake into this repo | Link as external examples; keep stage helpers + `flow.py` |

GenAnT URL = **animal teaching peer** for multi-entry / automation literacy — not a template to copy tool defaults.

---

## Quick links

| Doc | Why |
|-----|-----|
| [`EVALUATION.md`](EVALUATION.md) | L0 / L1 / L2 + provisional wording |
| [`ROADMAP.md`](ROADMAP.md) | Trunk + primary draft pick |
| [`COMPARE_HELIXER_BRAKER.md`](COMPARE_HELIXER_BRAKER.md) | Classroom Helixer ↔ BRAKER (S13) |
| [`zh/PROVISIONAL_NOT_L1.md`](zh/PROVISIONAL_NOT_L1.md) | 临时稿 ≠ L1 |
| Wiki [Choose-branch](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Choose-branch) | Evidence → engine |
