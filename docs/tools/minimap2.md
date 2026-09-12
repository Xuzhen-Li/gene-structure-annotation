# minimap2 — Iso-seq / long RNA

**Role:** S3 — align full-length transcripts.

## Get it
- bioconda `minimap2` + `samtools`

## Iso-seq style
```bash
minimap2 -t "$THREADS" -ax splice:hq -uf "$GENOME_FA" flnc.fastq.gz \
  | samtools sort -@ "$THREADS" -o "$WORK_DIR/rna/isoseq.bam"
samtools index "$WORK_DIR/rna/isoseq.bam"
export ISOSEQ_BAM="$WORK_DIR/rna/isoseq.bam"
```

## Flags
| Flag | Why |
|------|-----|
| `-ax splice:hq` | High-quality spliced (PacBio Iso-seq) |
| `-uf` | Transcript strand helpers for Iso-seq |

## Pitfalls
- Using genomic ONT presets on Iso-seq.  
- Skipping sort/index before EviAnn / GSAman.
