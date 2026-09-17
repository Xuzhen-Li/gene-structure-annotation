# EGAPx / S8 — optional 对照 & GenBank door (not default)

**Purpose:** when and why to look at NCBI **EGAPx** as a **parallel compare** or **submission-oriented** path.  
**Not** a replacement for evidence-first **S1 / S11** drafts or [`EVALUATION.md`](EVALUATION.md) L grades.

Upstream: [ncbi/egapx](https://github.com/ncbi/egapx) · Our branch: **S8** in [`ROADMAP.md`](ROADMAP.md) · Recipe: [`SCENARIOS.md`](SCENARIOS.md) (S8) · Ops note: [`tools/egapx.md`](tools/egapx.md) · [`../pipeline/A2d_egapx_optional.md`](../pipeline/A2d_egapx_optional.md)

---

## What EGAPx is

NCBI’s **public** eukaryotic genebuild package (EGAP-style): RNA + protein evidence → **Gnomon** chaining (± ab initio / ncRNA). Oriented toward **institutional / GenBank-ready** packages (ASN path where applicable). Internal RefSeq EGAP remains NCBI-side — public EGAPx ≠ “your genome is RefSeq.”

---

## How it maps to **our** branches

| Ours | Role vs EGAPx |
|------|----------------|
| **S1 / S11** (+ evidence) | Usual **primary** draft for classroom & lab papers |
| **S8** | Overlay: run/compare EGAPx **beside** primary — table diffs; do not silent-replace |
| Trunk QC · L0/L1/L2 | Still required — EGAPx GFF does not skip [`EVALUATION.md`](EVALUATION.md) |
| Merge / entry modes | Keep one named primary; see [`MERGE_AND_ENTRIES.md`](MERGE_AND_ENTRIES.md) |

Primary release stays the **lab branch** unless EGAPx clearly wins **documented** metrics — then say so in METHODS.

---

## When to open EGAPx docs vs stay on our path

| Open EGAPx / S8 | Stay classroom / print-first (this repo) |
|-----------------|------------------------------------------|
| GenBank / NCBI-style package as a goal | Tonight: answers → `flow.py` → plan (± `local.env`) |
| External NCBI-style **对照** table for METHODS | Default RNA+proteins → **S1**; close curated GFF → **S11** |
| You can supply correct **taxid** + RNA YAML and run their stack | Teaching playbook, Done-when / `print_qc` gates, GSAman curation |

Do **not** add EGAPx runners to this repo — docs and optional external install only.

---

## Honest limits

- **Plant / taxid-driven:** support and evidence packs depend on taxonomy + RNA; wrong taxid/YAML → empty or generic models.
- **Not a teaching playbook:** no classroom “print-first” path inside EGAPx; our S1/S11 + EVALUATION remain the learning spine.
- **EGAPx ≠ RefSeq** and is RNA-library sensitive (community notes, e.g. JOBIM 2026) — splice disagreements with BRAKER/Helixer are expected.
- Still soft-mask + local QC; do not let EGAPx silently overwrite curated NLR / priority loci without a diff table.

---

## Related

- Grades: [`EVALUATION.md`](EVALUATION.md) · Checklist: [`EVALUATION_CHECKLIST.md`](EVALUATION_CHECKLIST.md)
- Peer context: [`PEER_PIPELINES.md`](PEER_PIPELINES.md) · Notes: [`notes/egapx_gnomon.md`](notes/egapx_gnomon.md)
- Classroom Helixer↔BRAKER (different overlay, **S13**): [`COMPARE_HELIXER_BRAKER.md`](COMPARE_HELIXER_BRAKER.md)
