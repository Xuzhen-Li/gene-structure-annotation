# PSAURON — protein coding-likelihood scores

**Role:** Rank loci for GSAman (Chen et al. 2026 last-mile workflow).

## Get it
- Follow the PSAURON repository / paper cited in GSAman Methods (install path varies).  
- [[TODO-TEXT]]

## Typical use
```bash
# After PROTEINS_FA exists:
# psauron <args> → $PSAURON_TSV
bash pipeline/01_qc_busco_psauron.sh   # prints/runs if PSAURON on PATH
python3 pipeline/02_priority_loci.py -i "$PSAURON_TSV" -o curate/priority.tsv --threshold 0.5
```

## How to use scores
- Low score → inspect first in GSAman.  
- Boost known families via `--families` (**S7**).  
- Threshold is a dial, not magic — start 0.5, adjust.

## Pitfalls
- Matching IDs: PSAURON rows must match GFF gene/transcript ids (normalize before priority).  
- Dropping NLR just because score is odd — always check domains + soft-mask.
