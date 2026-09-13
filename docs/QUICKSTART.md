# Quickstart — run once, understand the project

**Audience:** first time through eukaryotic **gene structure** annotation with this playbook.  
**Goal:** finish a **default S1-shaped** draft → proteins → QC, and know **what each file means**.  
**Not covered here:** full FA (GO/KEGG) — that is the sibling repo after proteins exist.

| If you need… | Open |
|--------------|------|
| Evidence → which S-branch | [README “Evidence → branch”](../README.md#evidence--branch-chooser) |
| Every stage’s inputs/outputs | [`STAGE_IO.md`](STAGE_IO.md) |
| Full qualification checklist | [`PLAYBOOK.md`](PLAYBOOK.md) |
| Copy-paste depth | [`DETAILED_GUIDE.md`](DETAILED_GUIDE.md) |
| Reviews behind the chooser | [`REVIEWS.md`](REVIEWS.md) |
| *Vitis* T2T publication delivery | [`cases/vitis-t2t-s1-s5.md`](cases/vitis-t2t-s1-s5.md) |
| TE library → soft-mask | [`TE_LIBRARY.md`](TE_LIBRARY.md) |

---

## 1. What this project is (2 minutes)

Genomes are DNA strings. **Structure annotation** answers: *where are the genes, exons, and CDS?*  
The durable products are:

1. a **GFF3** (coordinates + gene/mRNA/CDS features), and  
2. a **protein FASTA** (translations for QC and for functional annotation).

**Function** (what the protein *does*: GO, domains, pathways) is a **second layer** —  
[`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation) — run only after proteins are stable.

Mental model (Ji *Nat Rev Genet* 2026 + this repo):

```text
Evidence you have  →  pick ONE branch (S1, S2, S11, …)
                   →  draft gene models
                   →  merge + QC
                   →  curate hard loci
                   →  release GFF + proteins
                   →  (optional) functional tables next door
```

---

## 2. One-time setup

```bash
git clone https://github.com/Xuzhen-Li/gene-structure-annotation.git
cd gene-structure-annotation
cp config/example.env config/local.env
```

Edit `config/local.env`. **Minimum to attempt S1** (RNA + proteins):

| Variable | Meaning |
|----------|---------|
| `REPO_ROOT` | Absolute path to this clone |
| `WORK_DIR` | Scratch directory you own (create it) |
| `GENOME_FA` | Assembly FASTA |
| `GENOME_SOFT` | Soft-masked genome (after A0) |
| `PROTEIN_DB` | Protein evidence FASTA (e.g. OrthoDB clade) |
| `RNA_BAM` | Aligned RNA-seq BAM (or set workflow to S2 if none) |
| `BUSCO_LINEAGE` | Lineage name you will report (e.g. `viridiplantae_odb12`) |
| `THREADS` | Cores for your machine/cluster |
| `RELEASE_TAG` | Name for the output folder |

Load env in every shell:

```bash
set -a
source config/local.env
set +a
mkdir -p "$WORK_DIR"/{genome,rna,draft,agat,qc,curated,release}
```

Install tools on your cluster as needed (BRAKER/GALBA, HISAT2/STAR, AGAT, BUSCO, gffread, …).  
This repo is a **METHODS playbook + helpers**, not a single `conda install` black box — helpers often **print** commands first so you can adapt to your modules.

---

## 3. Choose your branch (do not skip)

Open the [Evidence → branch](../README.md#evidence--branch-chooser) section.

| You have | Branch | Why |
|----------|--------|-----|
| Close curated reference GFF | **S11** first | Liftover is faster/more accurate than inventing genes |
| RNA + proteins, no close ref | **S1** (this quickstart) | BRAKER-style evidence draft + StringTie compare |
| Proteins only | **S2** | GALBA / GeMoMa |
| Deep Iso-seq | **S3** | Long-read / EviAnn-style evidence |

**This page continues with S1.** Other IDs: [`SCENARIOS.md`](SCENARIOS.md).

---

## 4. Walkthrough — S1 with I/O at each step

After each step, glance at [`STAGE_IO.md`](STAGE_IO.md) for the same stage.

### Step A — Assembly gate

1. Put/link assembly → `$GENOME_FA`.  
2. Run assembly QC (see `pipeline/Asm1_assembly_qc.md`).  
3. Only then set `ASSEMBLY_OK=yes` in `local.env`.

**Produces:** confidence that annotating this FASTA is worth it.  
**Do not:** annotate a failed / wrong-ploidy assembly “to save time”.

### Step B — Soft-mask (A0)

Follow the lab TE scheme: [`TE_LIBRARY.md`](TE_LIBRARY.md) (EDTA → TEtrimmer → TEsorter → curate → ProtExcluder → RepeatMasker `-xsmall`). Short path: `pipeline/A0_softmask.md` + `A0b_protexcluder.md`.

**Produces:** `$GENOME_SOFT` + curated TE lib notes.  
**Why:** raw EDTA is not a gold lib; hard-mask or gene-contaminated libs break BRAKER / NLR loci.

### Step C — RNA align (A1b)

Align RNA → `$RNA_BAM` (+ `.bai`).

**Produces:** splice evidence for BRAKER / StringTie.  
**Check:** alignment rate; sample of junctions in a browser later.

### Step D — Primary draft (A2)

```bash
# Often prints the braker.pl line for you to run under your modules:
bash pipeline/A2_run_draft.sh
```

**Produces:** `$DRAFT_GFF` (primary gene models).  
**Check:**

```bash
bash pipeline/A5_agat_stats.sh "$DRAFT_GFF"
# look at $AGAT_OUT/*.counts.txt — genes / mRNAs / CDS
```

### Step E — Second draft + StringTie compare

- Second predictor or Liftoff → `$DRAFT_GFF_B` (`A2b` / `A2c`).  
- If you have RNA: run **StringTie → TransDecoder** as a **compare** track (Freedman & Sackton 2025; see [`REVIEWS.md`](REVIEWS.md)).

**Produces:** alternative gene set(s), not yet “the truth”.

### Step F — Merge (A4)

```bash
MERGE_MODE=evm bash pipeline/A4_merge_sets.sh
bash pipeline/A5_agat_stats.sh "$MERGED_GFF"
```

**Produces:** `$MERGED_GFF`.  
**Check:** counts sit between or near the better parent; record EVM weights path in METHODS.

### Step G — Proteins (A3)

```bash
bash pipeline/A3_proteins_from_gff.sh
```

**Produces:** `$PROTEINS_FA`.  
**Check:** sequence count ≈ gene or mRNA policy you chose; no empty file.

### Step H — Protein QC (01)

```bash
bash pipeline/01_qc_busco_psauron.sh
```

**Produces:** BUSCO summary under `$BUSCO_OUT`, scores in `$PSAURON_TSV`.  
**Check:** write **BUSCO-C + lineage** into your lab notes / METHODS draft.

### Step I — Priority list → curation → release

```bash
python3 pipeline/02_priority_loci.py   # → PRIORITY_TSV
# GSAman / browser: pipeline/04_gsaman_curation.md
# When stable: pipeline/06_release_gff.md + PLAYBOOK checklist
```

**Produces:** `$CURATED_GFF` / `release/$RELEASE_TAG/` with GFF + proteins + METHODS.  
**Check:** every box in [`PLAYBOOK.md`](PLAYBOOK.md) qualification list.

### Step J — Function (optional next repo)

Copy or point `PROTEINS_FA` into  
[`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation) and follow its [`docs/QUICKSTART.md`](https://github.com/Xuzhen-Li/gene-function-annotation/blob/main/docs/QUICKSTART.md).

**Produces:** `functional_master.tsv` (names/GO/domains) — **not** a replacement GFF.

---

## 5. How to “understand the project” while running

1. **Name the product** of the step before you start (use the tables above).  
2. **Write one line** in a lab notebook: path + gene count or BUSCO.  
3. **Do not skip** Asm1 / soft-mask / AGAT just to see BRAKER finish — those gates are the playbook.  
4. When stuck on *which* tool: [`REVIEWS.md`](REVIEWS.md) + README chooser, not random GitHub stars.

---

## 6. Common first-run failures

| Symptom | Likely cause |
|---------|----------------|
| BRAKER gene explosion in repeats | Hard-mask or weak TE lib; fix A0 |
| Empty proteins | GFF has no CDS; wrong genome for `gffread` |
| BUSCO very low | Wrong lineage, fragmented assembly, or draft failed |
| “I annotated function in the GFF” | Wrong layer — use FA repo / master TSV |

---

## 7. Next reading (in order)

1. This file + [`STAGE_IO.md`](STAGE_IO.md)  
2. [`steps/MAIN.md`](steps/MAIN.md) (all branches)  
3. [`SCENARIOS.md`](SCENARIOS.md) **S1** full recipe  
4. [`PLAYBOOK.md`](PLAYBOOK.md) release checklist  
5. Sibling FA quickstart when proteins are ready  
