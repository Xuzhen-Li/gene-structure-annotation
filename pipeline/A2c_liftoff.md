# A2c — Liftoff (detailed)

Used in S1 (second set), S2, S4, S6, S11.

```bash
: "${REF_FA:?reference genome}"
: "${REF_GFF:?reference annotation}"
: "${GENOME_FA:?target genome}"
OUT="$WORK_DIR/draft/liftoff.gff3"
liftoff -g "$REF_GFF" \
  -o "$OUT" \
  -dir "$WORK_DIR/draft/liftoff_int" \
  -p "${THREADS:-16}" \
  -polish \
  -copies \
  "$GENOME_FA" "$REF_FA"
export DRAFT_GFF_B="$OUT"   # or primary DRAFT_GFF in S11
```

## After Liftoff
```bash
bash pipeline/A5_agat_stats.sh "$OUT"
# Inspect low-quality lifts (attribute names vary by Liftoff version):
grep -E 'valid_ORF=False|partial_mapping|low_identity' "$OUT" | head -n 50 || true
```

## Notes
- Prefer polished PN40024 (or your best curated grape) as reference.  
- `-copies` helps tandem arrays but can create extras — GSAman NLR windows.  
- Liftoff alone is **S11 provisional**, not qualified.
