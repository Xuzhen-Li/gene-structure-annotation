# A1b — RNA align (detailed)

Produce sorted `RNA_BAM` (+ `.bai`) for BRAKER / GSAman.  
Full narrative: [`../docs/DETAILED_GUIDE.md`](../docs/DETAILED_GUIDE.md) Step 4 · tool cards: [`../docs/tools/hisat2_star.md`](../docs/tools/hisat2_star.md) · [`../docs/tools/minimap2.md`](../docs/tools/minimap2.md).

**Print-first:** helpers and these blocks are for review. Set `RUN=1` (or paste into an interactive job) only after paths and modules look right. Do not blind-submit.

## Checklist

- [ ] FASTQ from **target** species (multi-tissue better)
- [ ] Index on soft-masked **or** raw genome — be consistent across samples
- [ ] Sorted BAM + `.bai`
- [ ] `RNA_BAM` exported in `config/local.env`

## Env (source local.env first)

```bash
set -a && source config/local.env && set +a
: "${GENOME_FA:?}"
: "${WORK_DIR:?}"
: "${THREADS:?}"
mkdir -p "$WORK_DIR/rna"
# Prefer soft-masked for index when GENOME_SOFT exists:
GENOME_FOR_INDEX="${GENOME_SOFT:-$GENOME_FA}"
# Short-read inputs (edit names):
: "${RNA_FASTQ_R1:=$WORK_DIR/rna/R1.fq.gz}"
: "${RNA_FASTQ_R2:=$WORK_DIR/rna/R2.fq.gz}"
# Or single/long-read:
: "${RNA_FASTQ:=$WORK_DIR/rna/flnc.fastq.gz}"
RNA_BAM="${RNA_BAM:-$WORK_DIR/rna/aligned.bam}"
```

---

## HISAT2 (Illumina paired-end — default)

```bash
hisat2-build -p "$THREADS" "$GENOME_FOR_INDEX" "$WORK_DIR/rna/hisat_index"
hisat2 -p "$THREADS" -x "$WORK_DIR/rna/hisat_index" \
  -1 "$RNA_FASTQ_R1" -2 "$RNA_FASTQ_R2" \
  | samtools sort -@ "$THREADS" -o "$RNA_BAM"
samtools index "$RNA_BAM"
export RNA_BAM
samtools flagstat "$RNA_BAM" | tee "$WORK_DIR/rna/flagstat.txt"
```

## STAR (deep multi-sample panels)

```bash
STAR --runThreadN "$THREADS" --runMode genomeGenerate \
  --genomeDir "$WORK_DIR/rna/star_index" \
  --genomeFastaFiles "$GENOME_FOR_INDEX"
STAR --runThreadN "$THREADS" --genomeDir "$WORK_DIR/rna/star_index" \
  --readFilesIn "$RNA_FASTQ_R1" "$RNA_FASTQ_R2" --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate \
  --outFileNamePrefix "$WORK_DIR/rna/star_"
# STAR default sorted BAM name:
export RNA_BAM="$WORK_DIR/rna/star_Aligned.sortedByCoord.out.bam"
samtools index "$RNA_BAM"
```

## minimap2 (long-read / Iso-seq — S3)

```bash
# PacBio Iso-seq / HQ transcripts:
minimap2 -t "$THREADS" -ax splice:hq -uf "$GENOME_FA" "$RNA_FASTQ" \
  | samtools sort -@ "$THREADS" -o "${ISOSEQ_BAM:-$WORK_DIR/rna/isoseq.bam}"
samtools index "${ISOSEQ_BAM:-$WORK_DIR/rna/isoseq.bam}"
# ONT cDNA (adjust -ax splice as needed for your chemistry):
# minimap2 -t "$THREADS" -ax splice "$GENOME_FA" "$RNA_FASTQ" | samtools sort -@ "$THREADS" -o "$RNA_BAM"
```

For BRAKER short-read evidence, keep `RNA_BAM` as the Illumina BAM. Put Iso-seq in `ISOSEQ_BAM` for S3 / EviAnn paths.

---

## Before BRAKER

```bash
samtools flagstat "$RNA_BAM"
# Mapping rate very low → wrong genome or distant RNA → prefer S2 / fix FASTQ
```

## Pitfalls

- Unsorted BAM or missing `.bai`
- Mixing many genotypes into one BAM without thinking about splices
- Indexing a **hard**-masked genome (prefer soft-masked or raw consistently)
- Forgetting to `export RNA_BAM=...` into `local.env` before `A2_run_draft.sh`
