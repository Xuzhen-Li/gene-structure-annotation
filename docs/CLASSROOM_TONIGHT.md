# Classroom tonight (structure) — offline mirror

GitHub Wiki [Start-tonight](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Start-tonight) is **not** in the clone. Short checklist only — not a full Wiki copy.

## Done when

- [ ] You generated and **read** `my_plan.md` (stages make sense). How to scan: [`zh/读plan.md`](zh/读plan.md).
- [ ] Paths in `local.env` are listed **or** honestly left empty for tonight.
- [ ] You can say one line: write `grade=` and `status=` separately (never `status=L1`).

## Submit tonight

**Deliverable:** `my_plan.md` only (± path list in `local.env`).  
Do **not** claim L1 / finished BRAKER / soft-mask done.

## `print_qc` `[STOP]` — expected on example.env

```bash
python3 pipeline/print_qc_commands.py --env config/example.env
```

`[STOP]` / exit 1 with placeholders is **expected**, not a broken printer.  
Before any `RUN=1`: real `local.env` + exit 0 with **no** `[STOP]` + Wiki Done when (or this page) ticked.

## Concepts oral (pick one)

- Wiki: [Concepts](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Concepts)
- Offline: [`zh/05_softmask与A0.md`](zh/05_softmask与A0.md) — soft≠hard; `softmasked_fraction`≠genome TE%; trusted lib only

Before A0 later: [`TRUSTED_TE_PATH.md`](TRUSTED_TE_PATH.md) · Soft-mask Done when.
