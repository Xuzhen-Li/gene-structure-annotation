# RepeatMasker — soft-mask TE

**Role:** A0 — lowercase TE so ab initio predictors skip them without deleting sequence.

## Get it
- http://www.repeatmasker.org / bioconda `repeatmasker`  
- Needs a **TE library** (prefer curated [vitis-te](https://github.com/Xuzhen-Li/vitis-te); else EDTA/RepeatModeler then clean).

## Minimal run
```bash
# ALWAYS soft-mask for annotation:
RepeatMasker -lib cleaned_te.lib -xsmall -pa "$THREADS" \
  -dir "$WORK_DIR/mask" "$GENOME_FA"
# Use the *.masked file as GENOME_SOFT
```

## Flags that matter
| Flag | Meaning |
|------|---------|
| `-xsmall` | Soft-mask (lowercase) — **required** for BRAKER |
| `-lib` | Your TE fasta |
| default hard mask | Writes `N` — **do not** feed to BRAKER |

## Afterward
Run ProtExcluder-style cleaning **before** this if the lib may contain NLR exons — [`protexcluder.md`](protexcluder.md).

## Pitfalls
- Hard-masked genome → missing genes.  
- Dirty TE lib → NLR exons masked → broken disease-resistance annotation (**S10**).
