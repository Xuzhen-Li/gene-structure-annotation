# Liftoff — map annotation GFF to a new assembly

**Role:** S1 second set, S2, S4 haplotype transfer, S6, S11 quick provisional.

## Get it
- https://github.com/agshumate/Liftoff · `pip install liftoff` / bioconda

## Minimal run
```bash
liftoff -g "$REF_GFF" \
  -o "$WORK_DIR/draft/liftoff.gff3" \
  -dir "$WORK_DIR/draft/liftoff_int" \
  -p "$THREADS" \
  -polish \
  -copies \
  "$GENOME_FA" "$REF_FA"
```

## Useful options
| Option | Meaning |
|--------|---------|
| `-polish` | Try to repair CDS after lift |
| `-copies` | Extra copies (tandems) — check NLR by hand |
| `-exclude_partial` | Drop weak partials (optional) |

## After
```bash
bash pipeline/A5_agat_stats.sh "$WORK_DIR/draft/liftoff.gff3"
grep -E 'valid_ORF=False|partial' "$WORK_DIR/draft/liftoff.gff3" | head
```

## Pitfalls
- Claiming Liftoff-only as publication-qualified (**S11** is provisional).  
- Blind trust of `-copies` in resistance-gene clusters.
