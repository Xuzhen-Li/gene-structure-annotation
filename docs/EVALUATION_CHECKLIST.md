# Structure release checklist (pass / fail)

Full rules: [`EVALUATION.md`](EVALUATION.md). Chinese tick sheet: [`zh/验收勾选表.md`](zh/验收勾选表.md).

**Target:** [ ] L0 provisional [ ] L1 qualified (default) [ ] L2 paper/T2T

## L1 hard gates (any fail ⇒ not L1)

- [ ] G1 Assembly OK (`ASSEMBLY_OK` + Asm1)
- [ ] G2 Soft-mask + **trusted** TE lib
- [ ] G3 Named draft path + tool versions
- [ ] G4 Valid GFF (AGAT/gffread) + counts
- [ ] G5 Proteins from **this** release GFF
- [ ] G6 Protein BUSCO Completeness **+ lineage**
- [ ] G7 Beyond-BUSCO triage (PSAURON + priority list)
- [ ] G8 `release/<TAG>/` = GFF + proteins + METHODS
- [ ] G9 Tandem/disease/QTL windows if relevant

## Soft / optional (report; strengthen METHODS)

- [ ] Compleasm cross-check (same lineage family as BUSCO)
- [ ] gffcompare vs ref or second draft (if available)
- [ ] RNA support % and/or BRH (if RNA / proteome available)
- [ ] Optional wrapper: none / GAQET2 / AnnoAudit / atol-qc…
- [ ] OMArk tables (required if claiming L2)

Shelf: [`QUALITY_SOURCES.md`](QUALITY_SOURCES.md).

## Auto-fail (any grade)

- [ ] No hard-mask for BRAKER/GALBA
- [ ] No raw EDTA / whole working lib as curatedlib
- [ ] No silent S13 replacing S1 when RNA+proteins exist
- [ ] No GO/KEGG claimed in this repo
- [ ] No private reads in git/release

**Verdict:** status=________ TAG=________

## Pack smoke (optional)

```bash
python3 pipeline/check_release_pack.py path/to/release/TAG
```

Checks files exist; does **not** replace the gates above.

## Print commands

```bash
python3 pipeline/print_qc_commands.py
```
