# Pipeline folder overview

Helpers for **gene structure** only — find exons/CDS, not GO labels.

**Primary products:** `GFF3` + `proteins.faa` (+ METHODS).

| Start | |
|-------|--|
| Confused? | [`../docs/START_HERE.md`](../docs/START_HERE.md) |
| Auto plan | [`flow_tool/`](flow_tool/) |
| Stage I/O | [`../docs/STAGE_IO.md`](../docs/STAGE_IO.md) |
| Branch map | [`../docs/ROADMAP.md`](../docs/ROADMAP.md) |
| PROTEIN_DB | [`A2_protein_db.md`](A2_protein_db.md) |
| S11 gap-fill | [`A2e_s11_gapfill.md`](A2e_s11_gapfill.md) · Liftoff [`A2c_liftoff.md`](A2c_liftoff.md) |

**Not here:** GO / KEGG / InterPro / eggNOG → [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation)  
(hand-off note only: [`A6_functional_optional.md`](A6_functional_optional.md)).

Typical order after Asm0–A0 and an evidence branch (default **S1**):

```text
A2 draft → A2b/A2c second set → A4 merge → A5 AGAT
  → A3 proteins → 01 BUSCO/PSAURON → 02 priority → 04 GSAman → 06 release
  → A6 hand-off to FA sibling (optional)
```
