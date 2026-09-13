# Pipeline folder overview

This folder holds **runnable helpers and stage notes** for **gene structure** annotation  
(genome → qualified GFF + proteins).

| Start here | |
|------------|--|
| New to the project? | [`../docs/QUICKSTART.md`](../docs/QUICKSTART.md) |
| What each stage produces | [`../docs/STAGE_IO.md`](../docs/STAGE_IO.md) |
| Branch pick (S1–S14) | [`../docs/steps/MAIN.md`](../docs/steps/MAIN.md) |
| Full checklist | [`../docs/PLAYBOOK.md`](../docs/PLAYBOOK.md) |
| One scenario recipe | [`../docs/SCENARIOS.md`](../docs/SCENARIOS.md) |

**Functional annotation (GO / KEGG / names)** is **not** done here — use sibling  
[`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation) after you have `proteins.faa`.

Typical order after Asm0–A0 and an evidence branch (default **S1**):

```text
A2 draft → A2b/A2c second set → A4 merge → A5 AGAT
  → A3 proteins → 01 BUSCO/PSAURON → 02 priority → 04 GSAman → 06 release
```
