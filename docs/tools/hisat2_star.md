# HISAT2 / STAR — short-read RNA alignment

**Role:** A1b — BAM for BRAKER3 and GSAman tracks.

## Get them
- bioconda: `hisat2`, `star`, `samtools`

## HISAT2 (good default)
```bash
hisat2-build -p "$THREADS" "$GENOME_SOFT" "$WORK_DIR/rna/hisat_index"
hisat2 -p "$THREADS" -x "$WORK_DIR/rna/hisat_index" \
  -1 R1.fq.gz -2 R2.fq.gz \
  | samtools sort -@ "$THREADS" -o "$WORK_DIR/rna/aligned.bam"
samtools index "$WORK_DIR/rna/aligned.bam"
export RNA_BAM="$WORK_DIR/rna/aligned.bam"
```

## STAR (deep multi-sample panels)
```bash
STAR --runThreadN "$THREADS" --runMode genomeGenerate \
  --genomeDir "$WORK_DIR/rna/star_index" --genomeFastaFiles "$GENOME_SOFT"
STAR --runThreadN "$THREADS" --genomeDir "$WORK_DIR/rna/star_index" \
  --readFilesIn R1.fq.gz R2.fq.gz --readFilesCommand zcat \
  --outSAMtype BAM SortedByCoordinate --outFileNamePrefix "$WORK_DIR/rna/star_"
```

## Check before BRAKER
```bash
samtools flagstat "$RNA_BAM"
# Mapping rate very low → wrong genome or distant RNA → prefer S2
```

## Pitfalls
- Unsorted BAM.  
- Mixing many genotypes into one BAM without thinking about splices.  
- Using hard-masked genome for index (prefer soft-masked or raw consistently).
