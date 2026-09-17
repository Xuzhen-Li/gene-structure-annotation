# gene-structure-annotation

> **中文教学：** [`docs/zh/`](docs/zh/)（是什么 / TE与基因 / 怎么跑 / 怎么选支）  
> **English ops:** runnable docs stay English — [`docs/BILINGUAL.md`](docs/BILINGUAL.md)  
> **Plant sims (3):** [`examples/plant_sim/`](examples/plant_sim/) — Vitis S1+S7 / Oryza S1 / Solanum S11 (print-first plans).


---

## What this repo is

**Find genes on a genome** — where are the exons / CDS?

```text
genome FASTA  (+ RNA and/or proteins)
        ↓
 soft-mask → predict gene models → QC → curate
        ↓
  qualified GFF3  +  proteins.faa  +  METHODS
```

That is **structural** annotation.  
**Not** GO / KEGG / domain tables — those are the sibling  
[`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation) **after** proteins exist.

![Structure overview](docs/figures/structure_overview.png)

**中文最短路径：** [`docs/zh/README.md`](docs/zh/README.md) · English door: [`docs/START_HERE.md`](docs/START_HERE.md)

**One-glance tonight:** [Wiki Start-tonight](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Start-tonight) (GitHub Wiki — **not** in the clone tree).

---

## Three steps (start here)

Chinese teaching door: [`docs/zh/`](docs/zh/)（今天最短路径）.

**Already assembled?** Treat Asm0/Asm1 as a checklist; set `ASSEMBLY_OK=yes` — do not reassemble. Edit every `/path/to` in `local.env` before any `mkdir`.

**Close curated reference GFF?** Set `close_curated_ref: true` in answers (see `examples/plant_sim/03_solanum_s11`). Default `false` → S1; half-done Liftoff stays `false`.

### 1. Tell the tool what evidence you have

```bash
git clone https://github.com/Xuzhen-Li/gene-structure-annotation.git
cd gene-structure-annotation
cp pipeline/flow_tool/answers.example.yaml my_answers.yaml
# edit yes/no: RNA? proteins? close reference? paper bar?
python3 pipeline/flow_tool/flow.py --answers my_answers.yaml -o my_plan.md
```

Open `my_plan.md`: it picks an **S-branch** and explains every stage  
(**input → software purpose → process → output**).

### 2. Fill paths once

```bash
cp config/example.env config/local.env
# set GENOME_FA, BUSCO_LINEAGE, RNA_BAM / PROTEIN_DB, TE lib, WORK_DIR, THREADS
```

### 3. Plan tonight; run when you have cluster + data

| | |
|--|--|
| **Tonight (classroom)** | Finish `my_plan.md` (± list paths in `local.env`). No BRAKER/Liftoff required. Oral check: [Wiki Concepts](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Concepts) (or zh `05_softmask与A0` three sentences). Write `grade=` and `status=` separately — do **not** write `status=L1`. |
| **Later (cluster)** | Only after [Done when](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Start-tonight#done-when) is ticked **and** `python3 pipeline/print_qc_commands.py` exits 0 with **no** `[STOP]`. Otherwise **no** `RUN=1`. Browsing with `--env config/example.env` **will** show `[STOP]` — **expected**. Also tick Soft-mask Done when / Concepts oral checks before A0 ([Wiki Start-tonight](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Start-tonight)). |

Then walk stages in `my_plan.md` → tick [`docs/EVALUATION_CHECKLIST.md`](docs/EVALUATION_CHECKLIST.md) (full rules: [`docs/EVALUATION.md`](docs/EVALUATION.md)). Default bar **L1**; paper/T2T = **L2**.

**Provisional ≠ L1:** Liftoff-only (**S11-lite**), Helixer-only, or MoGAAAP-style provisional merge ≠ evidence-based L1 — see [`docs/EVALUATION.md`](docs/EVALUATION.md) L0 vs L1.

**Default (RNA + proteins, no close ref):** branch **S1** (BRAKER + StringTie compare).

---

## Plain map (one glance)

| You have | Branch | Engine (short) |
|----------|--------|----------------|
| Close curated reference GFF | **S11** (lift+gap-fill; lift-only = **S11-lite**) | Liftoff / LiftOn / CAT |
| RNA + proteins | **S1** | BRAKER4/3 + StringTie compare |
| Proteins only | **S2** | GALBA / GeMoMa |
| Heavy Iso-seq | **S3** | IsoQuant / SQANTI (± EviAnn) |
| Want GPU ab initio **compare** | **S13** | Helixer / Tiberius / ANNEVO |
| Classic EVM/PASA | **S14** | `docs/steps/dclab/` |

| Goal / overlay (not a primary draft) | What it means |
|--------------------------------------|---------------|
| Paper / T2T bar **L2** | Acceptance level = L1 **plus** overlay **S5** (OMArk, deeper curation). Say “L2 with S5 overlay”, **not** “take the S5 branch”. |
| Plant NLR / tandem windows | Overlay **S7** when `plant_tandem_focus: true` |

Full map: [`docs/ROADMAP.md`](docs/ROADMAP.md).

---

## Docs (open only when needed)

| Need | Open |
|------|------|
| Chinese teaching (short path first) | [`docs/zh/`](docs/zh/) · [`docs/START_HERE.md`](docs/START_HERE.md) |
| Narrated auto-plan | [`pipeline/flow_tool/`](pipeline/flow_tool/) |
| Stage I/O · **Done?** | [`docs/STAGE_IO.md`](docs/STAGE_IO.md) · [`docs/EVALUATION_CHECKLIST.md`](docs/EVALUATION_CHECKLIST.md) · [`docs/EVALUATION.md`](docs/EVALUATION.md) |
| TE → soft-mask (trusted only) | [`docs/TE_LIBRARY.md`](docs/TE_LIBRARY.md) · checklist [`docs/TRUSTED_TE_PATH.md`](docs/TRUSTED_TE_PATH.md) |
| Branch map · walkthrough | [`docs/ROADMAP.md`](docs/ROADMAP.md) · [`docs/QUICKSTART.md`](docs/QUICKSTART.md) |
| **Post-assembly one-pager** | [`docs/POST_ASSEMBLY.md`](docs/POST_ASSEMBLY.md) |

<details>
<summary>More docs</summary>

| Need | Open |
|------|------|
| QC methods / papers / repos | [`docs/QUALITY_SOURCES.md`](docs/QUALITY_SOURCES.md) |
| EDTA how-to | [`docs/tools/edta.md`](docs/tools/edta.md) |
| BUSCO / Compleasm lineages | [`docs/LINEAGES.md`](docs/LINEAGES.md) |
| S11 gap-fill (after lift) | [`pipeline/A2e_s11_gapfill.md`](pipeline/A2e_s11_gapfill.md) · Liftoff [`pipeline/A2c_liftoff.md`](pipeline/A2c_liftoff.md) |
| Golden pack checklist (EXAMPLE) | [`examples/golden_pack/`](examples/golden_pack/) |
| PROTEIN_DB (BRAKER/GALBA) | [`pipeline/A2_protein_db.md`](pipeline/A2_protein_db.md) |
| Helixer ↔ BRAKER compare (classroom) | [`docs/COMPARE_HELIXER_BRAKER.md`](docs/COMPARE_HELIXER_BRAKER.md) |
| Entry modes + merge QC | [`docs/MERGE_AND_ENTRIES.md`](docs/MERGE_AND_ENTRIES.md) |
| EGAPx / S8 compare door | [`docs/EGAPX_COMPARE.md`](docs/EGAPX_COMPARE.md) |
| Recipes · tools · case · tutorials | [`docs/SCENARIOS.md`](docs/SCENARIOS.md) · [`docs/TOOLS.md`](docs/TOOLS.md) · [`docs/cases/vitis-t2t-s1-s5.md`](docs/cases/vitis-t2t-s1-s5.md) · [`docs/TUTORIALS_AND_MEETINGS.md`](docs/TUTORIALS_AND_MEETINGS.md) · [`docs/PLAYBOOK.md`](docs/PLAYBOOK.md) |

</details>

---

## This is not

- **Not** functional annotation (GO/KEGG) → [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation)
- **Not** TE library build alone → [vitis-te](https://github.com/Xuzhen-Li/vitis-te) + `docs/TE_LIBRARY.md`
- **Not** pangenome graphs → [vitis-pangenome](https://github.com/Xuzhen-Li/vitis-pangenome)

No private FASTQ/BAM in git.

**Author:** Xuzhen Li · [ORCID](https://orcid.org/0000-0003-3670-6657)
