# Case: *Vitis* T2T assembly → publication-grade structure (S1 engine + S5 bar)

**Status:** delivery template (fill bracketed metrics with *your* run).  
**Audience:** someone who must ship a non-provisional GFF + proteins for a grapevine (or close *Vitis*) **T2T / near-T2T** genome.  
**Not this case:** liftoff-only cultivar draft (that is **S11**, provisional) · FA/GO tables (sibling [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation)).

| Layer | What you use |
|-------|----------------|
| Engine path | **S1** — RNA-seq + proteins → BRAKER ± GeMoMa/Liftoff → EVM → last mile |
| Quality bar | **S5** — stricter Asm1, mandatory OMArk, expanded priority, second GSAman, full PLAYBOOK checklist |
| Command depth | [`../DETAILED_GUIDE.md`](../DETAILED_GUIDE.md) Steps 1–13 |
| Scenario stubs | [`../SCENARIOS.md`](../SCENARIOS.md) S1 + S5 |
| Stage meanings | [`../STAGE_IO.md`](../STAGE_IO.md) |
| Error tags | [`../ERROR_CLASSES.md`](../ERROR_CLASSES.md) |

---

## 0. Deliverables (definition of done)

A run is **deliverable** only when all of the following exist under `$WORK_DIR/release/$RELEASE_TAG/` (or equivalent) and METHODS tells the truth:

| File / artifact | Role |
|-----------------|------|
| `${RELEASE_TAG}.gff3` | Qualified gene structure (gene / mRNA / CDS; validated) |
| `${RELEASE_TAG}.faa` | Representative proteins matching the GFF policy |
| `METHODS.md` | Tools, versions, databases, thresholds, open issues |
| `qc/` snapshot | Genome Asm1, protein BUSCO, PSAURON, OMArk/Compleasm, AGAT counts |
| `priority_rounds/` | Round-1 and round-2 priority lists + curation log (TSV or notes) |
| Optional | EGAPx side-by-side table (S8), SynGAP if dual-hap (S4) |

**Hard rule:** no `status=provisional` on a S5 delivery. If evidence is thin, stop and downgrade to S1 provisional or S11 — do not relabel.

---

## 1. Preconditions (before any gene finder)

### 1.1 Biology / data you must have

| Item | Requirement for this case |
|------|---------------------------|
| Assembly | Chromosome-scale *Vitis* T2T or near-T2T (`GENOME_FA`); ~19 chr preferred for *V. vinifera*-like claims |
| RNA | Illumina RNA-seq from **same or very close** genotype → will become `RNA_BAM` |
| Proteins | OrthoDB eudicots / Viridiplantae **or** high-quality grape proteins → `PROTEIN_DB` |
| Reference transfer | PN40024 (or best grape) `REF_FA` + `REF_GFF` for Liftoff / GeMoMa second track |
| TE lib | Curated grape TE lib (e.g. [vitis-te](https://github.com/Xuzhen-Li/vitis-te)) or EDTA + ProtExcluder clean |
| Compute | BRAKER/GALBA stack, HISAT2 or STAR, AGAT, BUSCO, gffread, EVM or TSEBRA; OMArk + Compleasm for S5 |

### 1.2 `config/local.env` skeleton (fill paths)

```bash
cp config/example.env config/local.env
# then edit — minimum for this case:
```

```bash
REPO_ROOT="/abs/path/gene-structure-annotation"
WORK_DIR="/abs/path/work/vitis_t2t_ann"
THREADS=32
MAX_INTRON=25000                         # grape-safe starting point; raise if needed

GENOME_FA="$WORK_DIR/genome/Vitis_T2T.fa"
GENOME_SOFT="$WORK_DIR/genome/Vitis_T2T.softmasked.fa"
GENOME_PREFIX="VitisT2T_v1"
ASSEMBLY_OK="no"                         # flip only after §2

RNA_BAM="$WORK_DIR/rna/aligned.rna.bam"
PROTEIN_DB="/path/to/OrthoDB_eudicots.faa"
REF_FA="/path/to/PN40024.fa"
REF_GFF="/path/to/PN40024.genes.gff3"

DRAFT_ENGINE="braker3"                   # prefer BRAKER4 if available
DRAFT_ENGINE_B="liftoff"                 # or gemoma
DRAFT_GFF="$WORK_DIR/draft/primary.gff3"
DRAFT_GFF_B="$WORK_DIR/draft/secondary.gff3"
MERGE_MODE="evm"
MERGED_GFF="$WORK_DIR/draft/merged.gff3"
EVM_WEIGHTS="$REPO_ROOT/config/evm_weights_s1_braker.txt"

PROTEINS_FA="$WORK_DIR/proteins.faa"
BUSCO_LINEAGE="viridiplantae_odb12"      # report this name in METHODS — do not leave eukaryota by accident
BUSCO_OUT="$WORK_DIR/qc/busco_prot"
PSAURON_TSV="$WORK_DIR/qc/psauron.tsv"
PRIORITY_TSV="$WORK_DIR/qc/priority_r1.tsv"
AGAT_OUT="$WORK_DIR/agat"
OMARK_OUT="$WORK_DIR/qc/omark"
CURATED_GFF="$WORK_DIR/curated/curated.gff3"
RELEASE_TAG="VitisT2T.structure.v1"
```

```bash
set -a && source config/local.env && set +a
mkdir -p "$WORK_DIR"/{genome,rna,draft,agat,qc,curated,release,priority_rounds,methods_scratch}
```

### 1.3 Write Asm1 pass bar **before** annotating (S5)

Put numbers in `methods_scratch/asm1_bar.md` (example — **replace** with your paper bar):

```text
Genome BUSCO lineage: viridiplantae_odb12
Pass if: BUSCO-C ≥ [YOUR_%] ; BUSCO-D interpreted via S9 if high
Chromosomes: expect ~19 for V. vinifera-like; record actual
N50 / gap summary: record seqkit stats
Fail → fix assembly (Asm0), do not annotate
```

---

## 2. Phase A — Assembly gate + mask + RNA (Steps 1–4)

Follow [`../DETAILED_GUIDE.md`](../DETAILED_GUIDE.md) Steps 1–4. Condensed checklist:

| Step | Action | Must produce | Accept when |
|------|--------|--------------|-------------|
| Asm0 | Already done for T2T case (or document how `GENOME_FA` was built) | `GENOME_FA` | FASTA headers stable for release |
| Asm1 | `busco -m genome` + `seqkit stats` | `WORK_DIR/asm/` | Meets §1.3 bar → set `ASSEMBLY_OK=yes` |
| A0 | TE lib → ProtExcluder → RepeatMasker `-xsmall` | `GENOME_SOFT` | Softmask only; NLR exons not stripped into TE lib |
| A1b | HISAT2 or STAR | `RNA_BAM` + index | Align rate recorded; BAM used by BRAKER + StringTie |

**Stop if:** `ASSEMBLY_OK` still `no`, or RNA is distant genotype (then reconsider S2 / provisional — not S5).

---

## 3. Phase B — S1 drafts + merge (Steps 5–7)

### 3.1 Primary draft (BRAKER4/3)

```bash
# Prefer BRAKER4 ETP — docs/tools/braker4.md
# Fallback prints classic command:
DRAFT_ENGINE=braker3 bash pipeline/A2_run_draft.sh
# Point DRAFT_GFF at the BRAKER GFF/GTF you keep as primary
```

| Produce | Check |
|---------|--------|
| `DRAFT_GFF` | `bash pipeline/A5_agat_stats.sh "$DRAFT_GFF"` → genes/mRNA/CDS > 0 |
| Copetti habit | `bash pipeline/A5d_stage_counts.sh` if you keep stage GFFs — mono:multi not absurd |

### 3.2 StringTie compare (required in this delivery template)

```bash
# Example — adjust to your modules
stringtie "$RNA_BAM" -o "$WORK_DIR/draft/stringtie.gtf" -p "$THREADS"
# TransDecoder / ORF call per your lab SOP → keep as COMPARE track only
```

Record in METHODS: StringTie(+TD) was **compare**, not silent replace of BRAKER (Freedman & Sackton 2025; [`../REVIEWS.md`](../REVIEWS.md)).

### 3.3 Second draft (GeMoMa **or** Liftoff from PN40024)

```bash
# Liftoff example — see pipeline/A2c_liftoff.md
# GeMoMa — see pipeline/A2b_second_predictor.md
# Result must be DRAFT_GFF_B
bash pipeline/A5_agat_stats.sh "$DRAFT_GFF_B"
```

### 3.4 Merge

```bash
MERGE_MODE=evm bash pipeline/A4_merge_sets.sh
bash pipeline/A5_agat_stats.sh "$MERGED_GFF"
```

| Produce | Check |
|---------|--------|
| `MERGED_GFF` | Counts between/near better parent; `EVM_WEIGHTS` path copied into METHODS |
| Weights file | `config/evm_weights_s1_braker.txt` (or documented fork) |

---

## 4. Phase C — Proteins + QC (Steps 8–9) + **S5 OMArk**

```bash
DRAFT_GFF="$MERGED_GFF" bash pipeline/A3_proteins_from_gff.sh
bash pipeline/01_qc_busco_psauron.sh
bash pipeline/A5b_omark_compleasm.sh          # S5 mandatory
```

| Artifact | Where | METHODS must say |
|----------|--------|------------------|
| Proteins | `PROTEINS_FA` | One-protein-per-gene rule (or longest CDS policy) |
| BUSCO proteins | `BUSCO_OUT` | **C/D/F/M + `BUSCO_LINEAGE` name** |
| PSAURON | `PSAURON_TSV` | Threshold used later for priority |
| OMArk / Compleasm | `OMARK_OUT` / compleasm dir | Tables kept under `qc/` for release |

**S5 gate:** do not enter “almost done” curation without OMArk (or written waiver — waiver ≠ S5 delivery).

---

## 5. Phase D — Priority + GSAman round 1 (Steps 10–11)

### 5.1 Round-1 priority (PSAURON-led)

```bash
python3 pipeline/02_priority_loci.py \
  -i "$PSAURON_TSV" \
  -o "$WORK_DIR/priority_rounds/priority_r1.tsv" \
  --threshold 90
# Optional: boost NLR / stilbene / QTL windows via extra TSV if you maintain one
cp "$WORK_DIR/priority_rounds/priority_r1.tsv" "$PRIORITY_TSV"
```

### 5.2 Evidence pack + GSAman

Load per [`../pipeline/03_evidence_checklist.md`](../pipeline/03_evidence_checklist.md):

- genome + merged/curated GFF  
- `RNA_BAM`  
- homolog / PN40024 proteins or GFF  
- priority list  

Curate in order ([`../pipeline/04_gsaman_curation.md`](../pipeline/04_gsaman_curation.md)):

1. Fragmentation  
2. Adjacent fusion  
3. Exon / splice / start-stop  
4. Tandem collapse (NLR, stilbene, RGA)  

Tag every edit with [`../ERROR_CLASSES.md`](../ERROR_CLASSES.md). Export → update working GFF (still pre-final).

**Round-1 log (required for delivery):**  
`priority_rounds/round1_notes.md` — gene IDs fixed / deferred / open, with error class.

---

## 6. Phase E — S5 expansion + GSAman round 2

### 6.1 Expand priority (not only PSAURON &lt; 90)

Build `priority_rounds/priority_r2.tsv` as the **union** of:

1. Remaining round-1 opens  
2. All **fragmented** BUSCO orthologs from protein BUSCO  
3. Genome-wide **tandem array** neighborhoods (NLR / stilbene / known clusters)  
4. OMArk inconsistent / missing family signals you trust  

### 6.2 Second GSAman pass

Only the expanded list — not aimless genome-wide clicking.

**Round-2 log:** `priority_rounds/round2_notes.md`.

### 6.3 Stop rules (S12)

Freeze genome-wide curation when:

| Observation | Action |
|-------------|--------|
| Priority empty at your threshold | Freeze → release path |
| Protein BUSCO-C unchanged after round 2 | Stop genome-wide GSAman |
| Leftovers are TE-like only | List in METHODS `Open issues`; freeze |
| Chasing &lt;0.1% BUSCO | Stop — not a delivery task |

Set `CURATED_GFF` to the frozen file.

---

## 7. Phase F — Qualify + package (Step 13)

```bash
export DRAFT_GFF="$CURATED_GFF"
bash pipeline/A3_proteins_from_gff.sh
bash pipeline/01_qc_busco_psauron.sh
bash pipeline/A5_agat_stats.sh "$CURATED_GFF"

REL="$WORK_DIR/release/$RELEASE_TAG"
mkdir -p "$REL/qc" "$REL/priority_rounds"
cp "$CURATED_GFF" "$REL/${RELEASE_TAG}.gff3"
cp "$PROTEINS_FA" "$REL/${RELEASE_TAG}.faa"
cp -r "$WORK_DIR/qc/." "$REL/qc/" 2>/dev/null || true
cp -r "$WORK_DIR/priority_rounds/." "$REL/priority_rounds/"
```

### 7.1 Qualification checklist (all required)

Copy into `REL/METHODS.md` and tick:

- [ ] `ASSEMBLY_OK=yes` + Asm1 metrics table  
- [ ] Soft-masked genome used for ab initio  
- [ ] Branch: **S1 engine + S5 bar**; BRAKER/GeMoMa/Liftoff/EVM versions  
- [ ] StringTie compare noted  
- [ ] AGAT gene/mRNA/CDS counts  
- [ ] Protein BUSCO-C/D/F/M + **lineage name**  
- [ ] OMArk (+ Compleasm if run) tables in `qc/`  
- [ ] Priority rounds 1–2 logged; opens listed  
- [ ] NLR/stilbene/QTL: no silent tandem-collapse (or listed open)  
- [ ] GFF validates (`gffread` / AGAT); proteins regenerated from final GFF  
- [ ] No private BAM/FASTQ in the release folder  
- [ ] **Not** marked provisional  

### 7.2 METHODS skeleton (paste and fill)

```markdown
# Structural annotation METHODS — RELEASE_TAG

## Assembly
- Genome: [file / accession], T2T or near-T2T claim: [yes/no]
- Asm1: genome BUSCO [lineage] C[ ]% D[ ]% F[ ]% M[ ]%; seqkit N50 [ ]; chr count [ ]

## Evidence
- RNA-seq: [samples], aligner [HISAT2/STAR] → RNA_BAM
- Proteins: [OrthoDB release / grape set]
- Reference transfer: PN40024 [GFF version] via [Liftoff/GeMoMa]

## Pipeline
- Soft-mask: [TE lib] + ProtExcluder [yes/no]; RepeatMasker -xsmall
- Primary: BRAKER[3/4] [version]; AUGUSTUS species [ ]
- Compare: StringTie [version] (+ TransDecoder [yes/no]) — compare only
- Secondary: [Liftoff/GeMoMa] [version]
- Merge: EVM [version]; weights file [path/hash]
- QC: AGAT; BUSCO proteins [lineage] C[ ]%; PSAURON; OMArk [ ]; Compleasm [ ]
- Curation: GSAman rounds 1–2; error classes per ERROR_CLASSES.md
- Stop rule: S12 [describe]

## Products
- GFF3: [filename]
- Proteins: [filename]; representative rule: [ ]
- Open issues: [list or none]

## Not done in this release
- Functional annotation (GO/KEGG/domains) → gene-function-annotation F1
```

---

## 8. Optional add-ons (same delivery, extra tables)

| Need | Branch / tool | Where it plugs in |
|------|---------------|-------------------|
| Dual haplotype T2T | **S4** after one hap is S5-qualified | Liftoff curated GFF → hap2; SynGAP; limited GSAman |
| NCBI compare | **S8** EGAPx | Side-by-side gene-count / BUSCO table in METHODS |
| GPU ab initio curiosity | **S13** | Compare track only — never replaces S5 primary without new evidence |

---

## 9. Hand-off to function (after structure delivery)

```text
PROTEINS_FA = release/${RELEASE_TAG}.faa
→ clone gene-function-annotation
→ docs/QUICKSTART.md (F1)
→ functional_master.tsv is a separate product
```

Do not claim GO in the structure GFF unless you explicitly built write-back (not default).

---

## 10. Reviewer / PI freeze questions (use as gate)

1. Can a stranger regenerate `proteins.faa` from the released GFF + genome alone?  
2. Is every BUSCO number paired with a **lineage name**?  
3. Are tandem NLR/stilbene windows either fixed or listed open — not silent?  
4. Is StringTie documented as compare, not hidden primary?  
5. Is `provisional` absent from METHODS?  

If any answer is no → **not deliverable** under this case.
