# Helixer ↔ BRAKER — classroom compare (not default production)

**Purpose:** a short **compare scaffold** inspired by the Galaxy GTN *Helixer vs BRAKER3* tutorial.  
**Not** a default production path. Do **not** treat “run Helixer and stop” as L1.

---

## When to use this page

| Use | Do not use |
|-----|------------|
| **S13 overlay** — GPU / AI ab initio **compare** beside an evidence primary (usually **S1**) | Silent replace of S1 when RNA + proteins exist |
| Classroom / methods literacy — see how Helixer and BRAKER disagree | Claiming publication-final from Helixer-only |
| Thin-evidence exploration where S13 is already on the plan | Skipping EVALUATION gates because BUSCO looked fine |

Branch map: [`ROADMAP.md`](ROADMAP.md) (S1 vs S13). Grades: [`EVALUATION.md`](EVALUATION.md) (L0 vs L1).

---

## What each side needs

| Lane | Evidence / compute | Role here |
|------|--------------------|-----------|
| **BRAKER** (S1 spine) | Soft-masked genome + RNA and/or proteins; container/HPC time | Evidence-trained gene models — usual **primary** when RNA exists |
| **Helixer** (S13 compare) | Soft-masked genome + **GPU**; lineage model choice | Fast ab initio draft for **side-by-side** compare — not a silent primary |

Honest stop for class: generate plans / print commands only (`flow.py`, `print_qc_commands.py`). Do not claim L1 from a print-only night.

---

## Compare metrics (keep multi-metric)

Use the same QC pack you would for a real draft — **not** BUSCO alone:

- **BUSCO** (protein mode on each set’s peptides) and/or **Compleasm**
- **OMArk** (consistency / completeness of gene families)
- Optional: AGAT gene/mRNA counts, PSAURON-style priority lists

Rising gene counts after Helixer are **not** automatically “more complete” (JOBIM 2026 Helixer pitfalls). Write both tool versions and the lineage dataset in NOTES.

---

## Mapping to this playbook

```text
Evidence primary (RNA+proteins)  →  S1 (BRAKER) as primary
GPU ab initio compare            →  S13 (Helixer / Tiberius / ANNEVO) alongside
Helixer-only / no evidence primary →  provisional L0 — not L1
```

Provisional vs qualified: [`EVALUATION.md`](EVALUATION.md). Tutorials index: [`TUTORIALS_AND_MEETINGS.md`](TUTORIALS_AND_MEETINGS.md).

---

## External practice (GTN)

Hands-on buttons on a **tiny public** demo (often fungal — numbers will not match your plant T2T):

- [Galaxy GTN — Comparison of Helixer and BRAKER3](https://training.galaxyproject.org/training-material/topics/genome-annotation/tutorials/comparison-braker-helixer-annotation/tutorial.html)

Use GTN to learn the flow; use this repo to **choose the branch** and **grade a release**.
