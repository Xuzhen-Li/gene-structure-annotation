# TE library scheme → soft-mask (A0)

**Canonical TE home:** [`vitis-te`](https://github.com/Xuzhen-Li/vitis-te) (EDTA / curation / LAI).  
**This doc:** how that scheme plugs into **gene structure** annotation. Soft-mask is not a one-liner — a raw EDTA dump is **not** a gold library.

Sibling stages: [`../pipeline/A0_softmask.md`](../pipeline/A0_softmask.md) · [`../pipeline/A0b_protexcluder.md`](../pipeline/A0b_protexcluder.md) · [`tools/edta.md`](tools/edta.md) · [`tools/protexcluder.md`](tools/protexcluder.md) · [`tools/repeatmasker.md`](tools/repeatmasker.md).

---

## Why structure annotation cares

Ab initio / evidence engines (BRAKER, GALBA, …) over-predict inside repeats if you:

- skip masking,  
- **hard**-mask to `N`, or  
- soft-mask with a library full of **host genes** (NLR, kinases, …) → real exons get masked → **S10** gene inflation / missing disease loci later.

So A0 is: **curate TE lib → ProtExcluder-clean → soft-mask (`-xsmall`) → `GENOME_SOFT`**.

---

## The lab TE order (from `vitis-te`)

Do **not** hook a classifier-only tool as a genome-wide scanner. Classifiers **name**; they do not replace trim or replace EDTA.

| Step | Tool / action | Product | Done when |
|------|---------------|---------|-----------|
| **1** | **EDTA** de novo on *this* assembly | Raw TE lib + optional raw anno | EDTA finished; **not** yet “gold” |
| **2** | **TEtrimmer** | Boundary-improved consensi | Ends look like real TEs, not gene chunks |
| **3** | **TEsorter** | Lineage / classification labels | Names for curation tables |
| **4** | Manual spot-check | Curator notes | LTR FPs, LINE/SINE misses, **CDS contamination** flagged |
| **5** | Curate lib | Drop CDS → CD-HIT ~**85%** → **80-80** collapse | Deduped, gene-clean consensi FASTA |
| **6** | Re-annotate | EDTA `--curatedlib` and/or **RepeatMasker `-lib`** | Soft-masked genome + TE GFF/out |
| **7** | LTR age + **LAI** | Age / LAI tables | **Only after** curated lib (never on raw EDTA alone) |

Then hand soft-masked FASTA to structure as `GENOME_SOFT`.

---

## Step-by-step commands (structure hand-off)

Paths assume `WORK_DIR` from `config/local.env`. Adjust module names to your cluster.

### 1 — EDTA (starter)

```bash
# --species others unless rice/maize
EDTA.pl --genome "$GENOME_FA" --species others --sensitive 1 --anno 1 --threads "$THREADS"
# Optional: pass gene CDS to reduce gene fragments in the lib
# EDTA.pl ... --cds genes.cds.fa
```

**Outputs (names vary by EDTA version):** under `*.mod.EDTA*` — raw lib + raw TE annotation.  
**Red line:** do not set `GENOME_SOFT` from raw EDTA hard-mask / MAKER.masked.

See [`tools/edta.md`](tools/edta.md).

### 2–3 — TEtrimmer + TEsorter

```bash
# TEtrimmer — follow upstream CLI for your install; input = EDTA consensi
# TEsorter  — classify trimmed consensi (lineage labels for the curation table)
```

Record versions in METHODS. Classifier output is for **naming**, not a substitute for genome-wide scanning.

### 4 — Manual spot-check (required for delivery)

Checklist (write into `WORK_DIR/mask/te_curation_notes.md`):

- [ ] Obvious LTR false positives removed or demoted  
- [ ] LINE/SINE under-calls noted if relevant to your clade  
- [ ] Consensi with strong BLAST to plant proteins / NLR / kinase held out → A0b  
- [ ] No unpublished genotype dumps committed to git  

### 5 — Curated library

```bash
# Conceptual recipe — keep exact scripts in vitis-te as they land:
# 1) drop consensi that hit CDS / UniProt plant genes (see A0b / ProtExcluder)
# 2) cd-hit -c 0.85 ...          # ~85% identity collapse
# 3) 80-80 length/identity collapse of remaining fragmented copies
# → CLEAN_TE_LIB="$WORK_DIR/mask/te_curated.fasta"
```

### 6a — ProtExcluder / host-gene purge (A0b) — mandatory before BRAKER

```bash
# BLAST cleaned consensi vs UniProt plant / grape proteins; remove hits
# See pipeline/A0b_protexcluder.md
# Never leave NLR / R-gene peptides inside the RepeatMasker library
```

### 6b — Soft-mask for gene annotation

```bash
RepeatMasker -lib "$CLEAN_TE_LIB" -xsmall -pa "$THREADS" \
  -dir "$WORK_DIR/mask" "$GENOME_FA"
# Soft-masked = lowercase; NEVER hard-mask to N for BRAKER/GALBA
cp "$WORK_DIR/mask/"*.masked "$GENOME_SOFT"
```

Optional: re-run EDTA with `--curatedlib "$CLEAN_TE_LIB"` for a TE annotation track (useful for METHODS / S10), still soft-mask for predictors.

### 7 — LAI / LTR age (after curation only)

Run only on the curated lib + curated annotation. Numbers on raw EDTA are not delivery-grade.

---

## Products structure annotation must see

| Artifact | Env / path | Used by |
|----------|------------|---------|
| Soft-masked genome | `GENOME_SOFT` | BRAKER / GALBA / Helixer / … |
| Curated TE lib | `WORK_DIR/mask/te_curated.fasta` | METHODS + remask (S10) |
| Curation notes | `mask/te_curation_notes.md` | Delivery / S5 METHODS |
| Optional TE GFF/out | `mask/` | S10 TE-gene inflation triage |

Verify soft-mask fraction (see `pipeline/A0_softmask.md`). Extreme ~0% or absurdly high → recheck lib.

---

## Failure modes → structure branches

| Symptom | Likely TE problem | Branch / fix |
|---------|-------------------|--------------|
| Gene explosion in repeats | Weak / raw lib or hard-mask | Remask with curated lib → **S10** |
| NLR / stilbene exons missing | Host genes were in TE lib | A0b redo; unmask loci; GSAman |
| “EDTA finished so A0 done” | Skipped trim/curate/LAI order | Restart from step 2–5 |

---

## METHODS bullets (copy)

```text
TE library: EDTA [version] (--species others); TEtrimmer [v]; TEsorter [v];
curation: CDS drop + CD-HIT ~85% + 80-80 collapse; ProtExcluder/host-gene purge;
soft-mask: RepeatMasker -xsmall with curated lib → GENOME_SOFT;
LAI/LTR age: [yes/no, only post-curation].
Raw EDTA was not used as the gold library for gene prediction.
```

---

## Red lines (same as `vitis-te` skill)

1. Do not treat EDTA raw output as a gold-standard TE library.  
2. Classifier-only tools are for naming, not for replacing trim or genome-wide scanning.  
3. Do not publish another group’s raw TE calls as yours.  
4. Do not hard-mask for BRAKER/GALBA.  
5. Do not put NLR/R-gene proteins into the TE lib.
