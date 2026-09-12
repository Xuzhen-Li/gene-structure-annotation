# BRAKER4 — preferred modern BRAKER runner

**Role:** Drop-in upgrade for S1/S2/S3 drafts when Singularity+Snakemake are available.

## Get it
https://github.com/Gaius-Augustus/BRAKER4

## Minimal idea
1. Fill `samples.csv` (genome + BAM/FASTQ/SRA + protein FASTA).  
2. Copy `config.ini.example` → `config.ini`.  
3. `snakemake --cores N --use-singularity` (or SLURM executor).

| Want | Mode |
|------|------|
| S1 | ETP |
| S2 | EP |
| S3 Iso-seq | IsoSeq or Dual |

Migration table from `braker.pl`: upstream `MIGRATING_FROM_BRAKER3.md`.

## After
Still run our `A5d_stage_counts.sh` if intermediate GTFs exist; then GeMoMa/Liftoff second set + EVM **or** take BRAKER4 GFF as `DRAFT_GFF` and continue QC → GSAman.

## Pitfalls
- GeneMark commercial license.  
- Letting BRAKER4’s RepeatModeler replace a curated grape TE lib without ProtExcluder.
