# BRAKER4 (Gaius-Augustus) — Snakemake rewrite of BRAKER

- Repo: https://github.com/Gaius-Augustus/BRAKER4  
- Migrate from `braker.pl`: [MIGRATING_FROM_BRAKER3.md](https://github.com/Gaius-Augustus/BRAKER4/blob/main/MIGRATING_FROM_BRAKER3.md)

**Modes ↔ our branches**

| BRAKER4 mode | Evidence | Use as |
|--------------|----------|--------|
| ETP | RNA + proteins | **S1** preferred draft engine |
| EP | proteins only | **S2** |
| IsoSeq | Iso-seq + proteins | **S3** alternative to EviAnn |
| Dual | short RNA + Iso-seq + proteins | **S3** rich |
| ET | RNA only | thin-protein S1 variant |
| ES | genome only | last resort / compare |

**Ideas adopted**

- Prefer BRAKER4 Singularity+Snakemake over monolithic `braker.pl` when available ([`../tools/braker4.md`](../tools/braker4.md)).  
- Built-in RepeatModeler2/Red masking option; still prefer EDTA/vitis-te + ProtExcluder for grape.  
- Post-QC: AGAT + BUSCO/compleasm + OMArk (aligns with our spine).  
- Optional ncRNA / UTR decoration — record in METHODS if used.  
- `samples.csv` multi-genome — useful for **S4** panels.

Do not vendor their Snakefile; point users upstream.
