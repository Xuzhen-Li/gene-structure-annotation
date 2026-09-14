# gene-structure-annotation

> **中文教学：** [`docs/zh/`](docs/zh/)（是什么 / TE与基因 / 怎么跑 / 怎么选支）  
> **English ops:** runnable docs stay in English — [`docs/BILINGUAL.md`](docs/BILINGUAL.md)

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

---

## Three steps (start here)

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

### 3. Follow the plan → release GFF + proteins

Walk the stages in `my_plan.md` (helpers under `pipeline/`).  
When done, tick [`docs/EVALUATION.md`](docs/EVALUATION.md) (L1 default; L2 = paper/T2T).

**Default if you have RNA + proteins and no close ref:** branch **S1** (BRAKER + StringTie compare).

---

## Plain map (one glance)

| You have | Branch | Engine (short) |
|----------|--------|----------------|
| Close curated reference GFF | **S11** | Liftoff / LiftOn / CAT |
| RNA + proteins | **S1** | BRAKER4/3 + StringTie compare |
| Proteins only | **S2** | GALBA / GeMoMa |
| Heavy Iso-seq | **S3** | IsoQuant / SQANTI (± EviAnn) |
| Want GPU ab initio **compare** | **S13** | Helixer / Tiberius / ANNEVO |
| Classic EVM/PASA | **S14** | `docs/steps/dclab/` |

Full map: [`docs/ROADMAP.md`](docs/ROADMAP.md).

---

## Docs (only when you need them)

| Need | Open |
|------|------|
| Narrated auto-plan | [`pipeline/flow_tool/`](pipeline/flow_tool/) · [`docs/FLOW_TOOL.md`](docs/FLOW_TOOL.md) |
| Human walkthrough | [`docs/QUICKSTART.md`](docs/QUICKSTART.md) |
| What each folder means | [`docs/STAGE_IO.md`](docs/STAGE_IO.md) |
| Done? (L0/L1/L2) | [`docs/EVALUATION.md`](docs/EVALUATION.md) |
| TE → soft-mask | [`docs/TE_LIBRARY.md`](docs/TE_LIBRARY.md) |
| *Vitis* T2T example | [`docs/cases/vitis-t2t-s1-s5.md`](docs/cases/vitis-t2t-s1-s5.md) |
| Tool how-tos | [`docs/TOOLS.md`](docs/TOOLS.md) |
| Recipes S1–S14 | [`docs/SCENARIOS.md`](docs/SCENARIOS.md) |
| Audit 2026-09-14 | [`docs/AUDIT_2026-09-14.md`](docs/AUDIT_2026-09-14.md) |
| Reviews / peers | [`docs/REVIEWS.md`](docs/REVIEWS.md) · [`docs/PEER_PIPELINES.md`](docs/PEER_PIPELINES.md) |

More: [`docs/PLAYBOOK.md`](docs/PLAYBOOK.md) · [`docs/steps/MAIN.md`](docs/steps/MAIN.md) · [`docs/DETAILED_GUIDE.md`](docs/DETAILED_GUIDE.md) · [`docs/SELF_AUDIT.md`](docs/SELF_AUDIT.md).

---

## This is not

- **Not** functional annotation (GO/KEGG) → [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation)
- **Not** TE library build alone → [vitis-te](https://github.com/Xuzhen-Li/vitis-te) + `docs/TE_LIBRARY.md`
- **Not** pangenome graphs → [vitis-pangenome](https://github.com/Xuzhen-Li/vitis-pangenome)

No private FASTQ/BAM in git.

**Author:** Xuzhen Li · [ORCID](https://orcid.org/0000-0003-3670-6657)
