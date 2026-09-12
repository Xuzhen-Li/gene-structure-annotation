# Detailed guide — every step from assembly to qualified annotation

**Tool how-tos:** [`TOOLS.md`](TOOLS.md).  
**Main spine:** [`steps/MAIN.md`](steps/MAIN.md). **AI:** [`AI_ASSIST.md`](AI_ASSIST.md). **S14:** [`steps/dclab/`](steps/dclab/).


Work directory layout assumed:

```text
$WORK_DIR/
  asm/           # assembly + reports
  mask/          # TE lib + soft-masked fasta
  rna/           # fastq lists, BAM
  draft/         # BRAKER / GeMoMa / Liftoff / merged GFF
  qc/            # AGAT, BUSCO, PSAURON, OMArk
  curate/        # priority.tsv, changelog, GSAman exports
  release/       # versioned GFF + proteins + METHODS.md
```

```bash
cp config/example.env config/local.env
# edit all paths; set THREADS
set -a && source config/local.env && set +a
mkdir -p "$WORK_DIR"/{asm,mask,rna,draft,qc,curate,release}
```

Homepage branches: [`../README.md`](../README.md).  
Qualification checklist: [`PLAYBOOK.md`](PLAYBOOK.md).

---

# Part A — Common spine (before any branch)

## Step 1 — Assemble (Asm0)

### Goal
Chromosome-scale (or accepted contig-scale) FASTA for one haplotype or primary.

### Inputs
- HiFi BAM/FASTQ; optional ONT; optional Hi-C FASTQ

### What to run (example HiFi diploid)

```bash
# Example only — use your site’s hifiasm module/container
hifiasm -o "$WORK_DIR/asm/vitis" -t "$THREADS" hi fi_reads.fastq.gz
# Dual assembly graphs → hap1/hap2 fasta via gfatools / hifiasm docs
# Hi-C scaffolding example (YaHS) after aligning Hi-C to contigs:
# yahs contigs.fa hi-c.bam -o "$WORK_DIR/asm/yahs"
```

Purge false duplications if needed (`purge_dups` / `purge_haplotigs`) **before** calling the annotation genome final.

### Outputs
| File | Variable |
|------|----------|
| Chromosome-scale FASTA | `GENOME_FA` |
| Optional hap2 | `GENOME_FA_HAP2` |
| Assembly stats note | `$WORK_DIR/asm/README.txt` |

### Done when
- You can point `GENOME_FA` at a stable file
- You decided: annotate **one** primary **or** dual haplotypes (affects S4/S9)

### Details
[`../pipeline/Asm0_assembly.md`](../pipeline/Asm0_assembly.md)

---

## Step 2 — Assembly QC gate (Asm1)

### Goal
Refuse to annotate broken assemblies.

### Commands

```bash
busco -i "$GENOME_FA" -l viridiplantae_odb12 \
  -o genome_busco --out_path "$WORK_DIR/asm" -m genome -c "$THREADS"
seqkit stats -a "$GENOME_FA" | tee "$WORK_DIR/asm/seqkit_stats.txt"
# Optional:
# compleasm run -a "$GENOME_FA" -l eudicots -t "$THREADS" -o "$WORK_DIR/asm/compleasm"
# merqury.sh best.meryl "$GENOME_FA" "$WORK_DIR/asm/merqury"
```

### Record
| Metric | Where |
|--------|--------|
| BUSCO-C / D / F / M (genome) | `asm/genome_busco/` |
| N50, #scaffolds, gaps | `seqkit_stats.txt` |

### Pass rule (edit for your paper bar)
- Genome BUSCO-C acceptable for clade
- For *V. vinifera*-like claims: ~19 chromosomes preferred
- Extreme BUSCO-D → read S9 before continuing

```bash
# when satisfied:
# ASSEMBLY_OK=yes  in config/local.env
```

### Details
[`../pipeline/Asm1_assembly_qc.md`](../pipeline/Asm1_assembly_qc.md)

---

## Step 3 — Soft-mask repeats (A0 + A0b)

### Goal
Soft-mask TE without wiping NLR exons.

### Steps

1. Build / update TE library ([vitis-te](https://github.com/Xuzhen-Li/vitis-te) or EDTA + curated lib).  
2. **ProtExcluder-style clean**: BLAST lib vs plant proteins; remove host-gene hits (NLR, kinases, etc.).  
3. Soft-mask (lowercase), **never** hard-mask to `N` before BRAKER.

```bash
# RepeatMasker example (after cleaned lib)
RepeatMasker -lib cleaned_te.lib -xsmall -pa "$THREADS" \
  -dir "$WORK_DIR/mask" "$GENOME_FA"
# Result soft-masked fasta → GENOME_SOFT
cp "$WORK_DIR/mask/"*.masked "$GENOME_SOFT"
```

### Outputs
- `GENOME_SOFT` — soft-masked genome  
- Log of excluded TE consensi (NLR-safe)

### Fail if
- You hard-masked
- NLR peptides were inside the TE lib

### Details
[`../pipeline/A0_softmask.md`](../pipeline/A0_softmask.md) · [`../pipeline/A0b_protexcluder.md`](../pipeline/A0b_protexcluder.md)

---

# Part B — Default branch S1 (RNA + proteins)

Do Steps 1–3 first. Then:

## Step 4 — Align RNA-seq (A1b)

### Inputs
- Paired FASTQ; `GENOME_SOFT` or `GENOME_FA` for index

### HISAT2 example

```bash
hisat2-build -p "$THREADS" "$GENOME_SOFT" "$WORK_DIR/rna/hisat_index"
hisat2 -p "$THREADS" -x "$WORK_DIR/rna/hisat_index" \
  -1 reads_R1.fq.gz -2 reads_R2.fq.gz \
  | samtools sort -@ "$THREADS" -o "$WORK_DIR/rna/aligned.bam"
samtools index "$WORK_DIR/rna/aligned.bam"
export RNA_BAM="$WORK_DIR/rna/aligned.bam"
```

### STAR alternative (high depth)

```bash
STAR --runThreadN "$THREADS" --runMode genomeGenerate \
  --genomeDir "$WORK_DIR/rna/star_index" --genomeFastaFiles "$GENOME_SOFT"
STAR --runThreadN "$THREADS" --genomeDir "$WORK_DIR/rna/star_index" \
  --readFilesIn reads_R1.fq.gz reads_R2.fq.gz --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate --outFileNamePrefix "$WORK_DIR/rna/star_"
export RNA_BAM="$WORK_DIR/rna/star_Aligned.sortedByCoord.out.bam"
```

### Done when
- BAM indexes; mapping rate sane; path in `RNA_BAM`

---

## Step 5 — Primary draft BRAKER4 / BRAKER3 (A2)

Prefer **BRAKER4** ETP ([`tools/braker4.md`](tools/braker4.md), [`notes/braker4.md`](notes/braker4.md)). Classic `braker.pl` below remains valid.

### Inputs
- `GENOME_SOFT`, `RNA_BAM`, `PROTEIN_DB` (OrthoDB eudicots or Viridiplantae proteins)

### Example (Singularity — adjust tag/path)

```bash
# Official-style container; Exact flags: braker.pl --help on your install
singularity exec braker3.sif braker.pl \
  --genome="$GENOME_SOFT" \
  --prot_seq="$PROTEIN_DB" \
  --bam="$RNA_BAM" \
  --softmasking \
  --threads="$THREADS" \
  --species="${AUGUSTUS_SPECIES:-Vitis_custom}" \
  --workingdir="$WORK_DIR/draft/braker3"
# Copy / convert:
cp "$WORK_DIR/draft/braker3/braker.gff3" "$DRAFT_GFF" \
  || gffread "$WORK_DIR/draft/braker3/braker.gtf" -o "$DRAFT_GFF"
```

Protein-only (no BAM): omit `--bam` (BRAKER uses proteins + ab initio).

### Outputs
- `DRAFT_GFF` primary structure

### Checks
```bash
bash pipeline/A5_agat_stats.sh "$DRAFT_GFF"
```
Gene count vs near relative × ploidy — if crazy high → jump to **S10**.

### Copetti check (do not skip)
Compare GeneMark / Augustus / BRAKER / StringTie counts and mono:multi — [`notes/copetti.md`](notes/copetti.md):
```bash
bash pipeline/A5d_stage_counts.sh genemark.gtf augustus.hints.gtf braker.gtf stringtie.gtf
```
If BRAKER collapsed → TSEBRA rescue before merge ([`tools/tsebra.md`](tools/tsebra.md)).

---

## Step 6 — Second draft GeMoMa or Liftoff (A2b / A2c)

### Option A — GeMoMa (homology from annotated ref)

```bash
# GeMoMa CLI varies by version — typical pattern:
# GeMoMa ... t="$REF_GFF" a="$REF_FA" g="$GENOME_SOFT" ...
# Write result to DRAFT_GFF_B
export DRAFT_GFF_B="$WORK_DIR/draft/gemoma.gff3"
```

### Option B — Liftoff

```bash
liftoff -g "$REF_GFF" \
  -o "$WORK_DIR/draft/liftoff.gff3" \
  -dir "$WORK_DIR/draft/liftoff_int" \
  -p "$THREADS" -polish \
  "$GENOME_FA" "$REF_FA"
export DRAFT_GFF_B="$WORK_DIR/draft/liftoff.gff3"
# Flag low-quality lifts for later GSAman:
grep 'valid_ORF=False\|coverage=0\.' "$DRAFT_GFF_B" | head
```

Use PN40024 (or your best curated grape) as `REF_FA` / `REF_GFF`.

---

## Step 7 — Merge prediction sets (A4)

### EVM (BRAKER + GeMoMa) — default for S1

1. Convert both GFFs to EVM-compatible gene predictions.  
2. Write `weights.txt` (example idea: BRAKER 5–8, GeMoMa 7–10, transcripts higher if PASA).  
3. Run EVidenceModeler → `MERGED_GFF`.

```bash
export MERGE_MODE=evm
export DRAFT_GFF=...      # braker
export DRAFT_GFF_B=...    # gemoma
bash pipeline/A4_merge_sets.sh
# Then paste your real EVM commands from Krabbenhoft-style run_EVM.sh into the STOP section
export MERGED_GFF="$WORK_DIR/draft/merged.gff3"
```

### TSEBRA — two BRAKER-family GTFs

```bash
export MERGE_MODE=tsebra
bash pipeline/A4_merge_sets.sh
# tsebra.py -g set1.gtf,set2.gtf -c default.cfg -o merged.gtf
```

### Done when
- Single `MERGED_GFF` exists and AGAT runs clean

```bash
bash pipeline/A5_agat_stats.sh "$MERGED_GFF" | tee "$WORK_DIR/qc/agat_merged.txt"
```

---

## Step 8 — Proteins from GFF (A3)

```bash
export DRAFT_GFF="$MERGED_GFF"
export PROTEINS_FA="$WORK_DIR/qc/proteins.faa"
# GENOME_FA for CDS extraction
bash pipeline/A3_proteins_from_gff.sh
```

### Output
- One representative protein per gene → `PROTEINS_FA`

---

## Step 9 — Structural QC (01 + optional A5b)

```bash
export BUSCO_OUT="$WORK_DIR/qc/busco_prot"
export PSAURON_TSV="$WORK_DIR/qc/psauron.tsv"
bash pipeline/01_qc_busco_psauron.sh
bash pipeline/A5b_omark_compleasm.sh   # if installed
```

### Interpret
| Signal | Action |
|--------|--------|
| Low BUSCO-C | More evidence / fix merges / curation |
| Tiny protein spike | TE fragments → S10 |
| Many low PSAURON | Feed step 10 |

---

## Step 10 — Priority list (02)

```bash
# optional families.tsv: gene_id<TAB>NLR
python3 pipeline/02_priority_loci.py \
  -i "$PSAURON_TSV" \
  -o "$WORK_DIR/curate/priority.tsv" \
  --threshold 90 \
  --families "$WORK_DIR/curate/families.tsv"
```

---

## Step 11 — Evidence pack + GSAman (03–04)

### Load in GSAman
- Soft-masked genome  
- `MERGED_GFF` (or current curated)  
- RNA / Iso-seq BAM  
- Miniprot / protein hits  
- Homolog GFF from PN40024  

### Curate in order
1. Rows in `priority.tsv` top-down  
2. Tag each fix with error class ([`ERROR_CLASSES.md`](ERROR_CLASSES.md))  
3. Export GFF often → `CURATED_GFF`  
4. Changelog: `curate/changelog.tsv` (`gene_id`, `class`, `note`)

### Details
[`../pipeline/03_evidence_checklist.md`](../pipeline/03_evidence_checklist.md) · [`../pipeline/04_gsaman_curation.md`](../pipeline/04_gsaman_curation.md)

---

## Step 12 — Optional SynGAP (05)

Only if ≥2 haplotype annotations exist — see **S4**.

---

## Step 13 — Qualify and release (06)

```bash
# Regenerate proteins from CURATED_GFF; re-run BUSCO+PSAURON
export DRAFT_GFF="$CURATED_GFF"
bash pipeline/A3_proteins_from_gff.sh
bash pipeline/01_qc_busco_psauron.sh
bash pipeline/A5_agat_stats.sh "$CURATED_GFF"
```

### Qualification checklist (all must pass for non-provisional)

- [ ] Asm1 documented (`ASSEMBLY_OK=yes`)  
- [ ] Soft-mask used for ab initio  
- [ ] Branch named (S1) + tool versions  
- [ ] AGAT counts saved  
- [ ] Protein BUSCO lineage + scores saved  
- [ ] Priority curated or explicitly deferred in METHODS  
- [ ] NLR/stilbene/QTL: no silent tandem-collapse (or listed open)  
- [ ] GFF validates; proteins match GFF  
- [ ] `RELEASE_TAG` set; public files only  

```bash
cp "$CURATED_GFF" "$WORK_DIR/release/${RELEASE_TAG}.gff3"
cp "$PROTEINS_FA" "$WORK_DIR/release/${RELEASE_TAG}.faa"
# write release/METHODS.md — then freeze
```

Optional **A6** eggNOG after freeze.

---

# Part C — Other branches (detailed deltas)

## S2 — Proteins only

After Steps 1–3:

| Step | Do this instead of S1 |
|------|------------------------|
| 4 | Skip RNA or set `RNA_BAM=none` |
| 5 | `DRAFT_ENGINE=galba` **or** GeMoMa primary |
| 6 | Liftoff PN40024 as second |
| 7 | EVM with **higher weight on homology** |
| 11 | Expect more splice fixes in GSAman |
| 13 | Label `provisional` if no RNA |

```bash
DRAFT_ENGINE=galba bash pipeline/A2_run_draft.sh
# Liftoff → DRAFT_GFF_B
MERGE_MODE=evm bash pipeline/A4_merge_sets.sh
# continue Part B from Step 8
```

---

## S3 — Deep Iso-seq

After Steps 1–3:

1. Map Iso-seq:  
   `minimap2 -ax splice:hq -uf "$GENOME_FA" flnc.fq.gz | samtools sort -o isoseq.bam`  
2. EviAnn primary (`DRAFT_ENGINE=eviann`) using Iso-seq + proteins.  
3. BRAKER3 secondary.  
4. `MERGE_MODE=evi_backbone` — keep EviAnn genes; add BRAKER orphans only.  
5. Continue Step 8–13; GSAman focuses on backbone/orphan conflicts.

```bash
DRAFT_ENGINE=eviann bash pipeline/A2_run_draft.sh   # → put evidence GFF as DRAFT_GFF_B
# BRAKER → DRAFT_GFF
MERGE_MODE=evi_backbone bash pipeline/A4_merge_sets.sh
# finish orphans into MERGED_GFF then Step 8+
```

---

## S4 — Haplotype panel

1. Complete **S1 (or S3) through Step 13** on **reference haplotype**.  
2. For each other hap: Liftoff curated ref GFF (`A2c`).  
3. SynGAP ref vs hap → conflict list.  
4. GSAman only conflicts + priority families on each hap.  
5. Release set: `ref.${RELEASE_TAG}.gff3`, `hap2.${RELEASE_TAG}.gff3`, SynGAP reports.

---

## S5 — T2T / publication

1. Stricter Asm1 (document thresholds in METHODS).  
2. Full S1 through first GSAman.  
3. Mandatory `A5b` OMArk/Compleasm.  
4. Expand priority: all fragmented BUSCOs + genome-wide tandem arrays.  
5. Second GSAman round; apply S12 stop rules.  
6. Optional S8 EGAPx comparison table.  
7. Checklist 100% — no `provisional`.

---

## S6 — Thin evidence

1. Steps 1–3.  
2. Liftoff/GeMoMa = only serious draft.  
3. Optional weak BRAKER protein-only orphans.  
4. Light merge → Steps 8–10.  
5. GSAman **families only**.  
6. Release `provisional`; schedule Iso-seq → S3.

---

## S7 — Family / QTL first

1. Run S1 Steps 4–10 genome-wide (auto).  
2. Build `families.tsv` for genes in windows / Orthogroups of interest.  
3. Priority with `--families`.  
4. GSAman **only** those windows (±100 kb tandems).  
5. Release dual tracks or tagged merge (`curated=yes`).

---

## S8 — EGAPx parallel

1. Keep S1 as primary through merge.  
2. Install/run [ncbi/egapx](https://github.com/ncbi/egapx) with *Vitis* taxid + RNA YAML (`A2d`).  
3. AGAT+BUSCO both; GSAman NLR spot-check.  
4. Primary release = lab S1 unless EGAPx wins documented QC.

---

## S9 — High BUSCO-D / polyploid

1. At Asm1: do **not** purge until ploidy known.  
2. Prefer S4 (hap1+hap2) over collapsed primary.  
3. If collapsed: more GSAman for fusion/split; report BUSCO-D.

---

## S10 — TE inflation

1. Stop at inflated AGAT gene count / short-protein spike.  
2. Rebuild TE lib + ProtExcluder; re-soft-mask.  
3. Re-enter S1 from Step 5.  
4. Optional A5c: delete only loci failing RNA **and** Pfam **and** homolog.  
5. Never FPKM-kill NLR.

---

## S11 — Lift only

1. Asm1 minimal; A0 recommended.  
2. Liftoff only (Step 6 option B).  
3. AGAT + optional protein BUSCO.  
4. METHODS `status=provisional`.  
5. No qualification claim.

---

## S12 — Stop rules

| Observation | Action |
|-------------|--------|
| Priority empty at threshold | Freeze GFF → Step 13 |
| BUSCO-C unchanged after round 2 | Stop genome-wide GSAman |
| Only TE-like leftovers | Document in METHODS |
| New Iso-seq | Re-enter S3 on touched chromosomes |

---

# Part D — Quick command index

| Step | Command / doc |
|------|----------------|
| Soft-mask | RepeatMasker `-xsmall` + A0b |
| RNA | HISAT2/STAR → `RNA_BAM` |
| BRAKER3 | `pipeline/A2_run_draft.sh` |
| Liftoff | `pipeline/A2c_liftoff.md` |
| Merge | `pipeline/A4_merge_sets.sh` |
| AGAT | `pipeline/A5_agat_stats.sh` |
| Proteins | `pipeline/A3_proteins_from_gff.sh` |
| BUSCO/PSAURON | `pipeline/01_qc_busco_psauron.sh` |
| Priority | `pipeline/02_priority_loci.py` |
| Release | `pipeline/06_release_gff.md` |

Peers: [`RELATED_SOFTWARE.md`](RELATED_SOFTWARE.md).


## S14 — EVM consensus (part of the main process)

Follow [`steps/dclab/`](steps/dclab/) 00→09, then return here at Step 8 (proteins/QC) through release.  
Notes: [`notes/cantulab_evm.md`](notes/cantulab_evm.md). Upstream: https://github.com/CantuLab/AnnotationPipeline2-EVM_based-DClab
