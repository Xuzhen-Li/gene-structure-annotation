# Start here — gene **structure**

**中文请从这里进：** [`zh/README.md`](zh/README.md)

You want **gene models** (GFF), not GO tables.

1. Run the flow tool → [`../pipeline/flow_tool/README.md`](../pipeline/flow_tool/README.md)  
2. Fill `config/local.env`  
3. Follow the printed plan; finish by ticking [`EVALUATION_CHECKLIST.md`](EVALUATION_CHECKLIST.md)  
   (Chinese: [`zh/验收勾选表.md`](zh/验收勾选表.md); full rules: [`EVALUATION.md`](EVALUATION.md))  
4. Optional: `python3 pipeline/print_qc_commands.py` after sourcing `local.env`  
5. Lineages / trusted TE / S11 gap-fill: [`LINEAGES.md`](LINEAGES.md) · [`TRUSTED_TE_PATH.md`](TRUSTED_TE_PATH.md) · [`../pipeline/A2e_s11_gapfill.md`](../pipeline/A2e_s11_gapfill.md) · proteins DB [`../pipeline/A2_protein_db.md`](../pipeline/A2_protein_db.md)
6. One-page path + EXAMPLE pack: [`POST_ASSEMBLY.md`](POST_ASSEMBLY.md) · [`../examples/golden_pack/`](../examples/golden_pack/)

**Classroom minimum ≠ finish BRAKER tonight.** Honest stop: understand `my_plan.md` + list real paths in `local.env` + know what L1 ticks mean. Write `grade=` and `status=` separately — never `status=L1`.

**When ready for `RUN=1`:** tick [Done when](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Start-tonight#done-when) **and** `python3 pipeline/print_qc_commands.py` exits 0 with **no** `[STOP]`. Otherwise no cluster run. Need HPC/containers before BRAKER/Liftoff.

**Provisional ≠ L1:** Liftoff-only / Helixer-only drafts stay **L0** until gap-fill + gates — [`EVALUATION.md`](EVALUATION.md). Optional classroom compare: [`COMPARE_HELIXER_BRAKER.md`](COMPARE_HELIXER_BRAKER.md).

Entry modes + merge QC (print-first / stage walk / no Snakemake here): [`MERGE_AND_ENTRIES.md`](MERGE_AND_ENTRIES.md).


One-sentence test: *Does this step change exon coordinates or only protein labels?*  
Coordinates → this repo. Labels (GO/KEGG/names) → [gene-function-annotation](https://github.com/Xuzhen-Li/gene-function-annotation).

Back to [`../README.md`](../README.md).
