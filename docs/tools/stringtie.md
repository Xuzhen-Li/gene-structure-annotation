# StringTie — transcript assembly (sanity track)

**Role:** External RNA models to compare with BRAKER (Copetti #949). Not always fed into BRAKER; used in IGV/GSAman and Mikado.

```bash
stringtie "$RNA_BAM" -o "$WORK_DIR/rna/stringtie.gtf" -p "$THREADS"
```

Compare gene counts / mono:multi to BRAKER via [`../../pipeline/A5d_stage_counts.sh`](../../pipeline/A5d_stage_counts.sh).
