# A1b — RNA align (detailed)

Full examples: [`../docs/DETAILED_GUIDE.md`](../docs/DETAILED_GUIDE.md) Step 4.

## Checklist
- [ ] FASTQ from target species (multi-tissue better)
- [ ] Index on soft-masked or raw genome (be consistent)
- [ ] Sorted BAM + `.bai`
- [ ] `RNA_BAM` exported in `config/local.env`

## HISAT2
```bash
hisat2-build -p "$THREADS" "$GENOME_SOFT" "$WORK_DIR/rna/hisat_index"
hisat2 -p "$THREADS" -x "$WORK_DIR/rna/hisat_index" \
  -1 R1.fq.gz -2 R2.fq.gz \
  | samtools sort -@ "$THREADS" -o "$WORK_DIR/rna/aligned.bam"
samtools index "$WORK_DIR/rna/aligned.bam"
```

## Iso-seq (S3)
```bash
minimap2 -t "$THREADS" -ax splice:hq -uf "$GENOME_FA" flnc.fastq.gz \
  | samtools sort -@ "$THREADS" -o "$WORK_DIR/rna/isoseq.bam"
samtools index "$WORK_DIR/rna/isoseq.bam"
```
