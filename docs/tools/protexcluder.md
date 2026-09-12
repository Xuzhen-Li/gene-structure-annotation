# ProtExcluder (pattern) — clean host genes out of TE libraries

**Role:** A0b — keep real genes (especially NLR) out of the repeat library.

## Get it
- Search GitHub / papers for ProtExcluder (plant TE pipelines).  
- Equivalent DIY: BLAST TE consensi vs UniProt plant / grape proteins; drop strong gene hits.

## What to do
1. BLAST or Diamond: `te.lib` vs plant proteins.  
2. Remove consensi that hit NLR, LRR, kinase, etc. at high coverage.  
3. Save `cleaned_te.lib` → RepeatMasker.

## Pitfalls
- Skipping this once → TE-inflated gene calls or masked NLR (**S10**).  
- Over-cleaning every weak hit → under-masking; balance with AGAT gene counts after BRAKER.
