# GALBA — protein-only gene prediction

**Role:** Primary draft in **S2** (no usable RNA).

## Get it
- https://github.com/Gaius-Augustus/GALBA (BRAKER sibling; container recommended)

## Pattern
```bash
galba.pl \
  --genome="$GENOME_SOFT" \
  --prot_seq="$PROTEIN_DB" \
  --softmasking \
  --threads="$THREADS" \
  --workingdir="$WORK_DIR/draft/galba"
# → galba.gff3 → DRAFT_GFF
```

## Tips
- Use **close** proteins (grape + related eudicots), not only distant OrthoDB, when possible.  
- Always pair with Liftoff PN40024 as second set before EVM.  
- Expect more splice fixes in GSAman than S1.

## Pitfalls
Same soft-mask / TE issues as BRAKER. Do not call GALBA “RNA-supported.”
