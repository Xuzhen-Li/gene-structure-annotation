# GALBA2

- https://github.com/Gaius-Augustus/GALBA2  
- Snakemake + Singularity rewrite of GALBA; shares BRAKER4-style orchestration.  
- Logic: miniprot protein alignments → miniprothint → AUGUSTUS train/predict (protein-only).  
- Prefer **closely related** proteins; for distant OrthoDB-scale evidence prefer BRAKER4 EP.  
- Authors highlight better scaling than BRAKER2-EP on large (≥~1 Gb) repeat-rich genomes.

**Adopt:** document as S2 alternative runner; keep classic GALBA notes for `galba.pl` sites.
