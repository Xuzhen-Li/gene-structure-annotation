**Prefer [`braker4.md`](braker4.md) (Snakemake) when you can; this page is classic `braker.pl`.**

# BRAKER3 — primary gene prediction (RNA + proteins)

**Role:** Default draft engine in **S1** (and secondary in **S3**).

## Get it
- Official: https://github.com/Gaius-Augustus/BRAKER  
- Strongly prefer the published **Singularity/Docker** image (GeneMark license may apply — read BRAKER docs).

## What it needs
| Input | Variable |
|-------|----------|
| Soft-masked genome | `GENOME_SOFT` |
| Protein FASTA (OrthoDB eudicots/Viridiplantae) | `PROTEIN_DB` |
| Optional RNA BAM | `RNA_BAM` |
| Threads / species label | `THREADS`, `AUGUSTUS_SPECIES` |

## Command pattern
```bash
# Via singularity (image name is yours):
singularity exec braker3.sif braker.pl \
  --genome="$GENOME_SOFT" \
  --prot_seq="$PROTEIN_DB" \
  --bam="$RNA_BAM" \
  --softmasking \
  --threads="$THREADS" \
  --species="${AUGUSTUS_SPECIES:-Vitis_custom}" \
  --workingdir="$WORK_DIR/draft/braker3"
```
No RNA: omit `--bam` (protein + ab initio).

Helper that **prints** this for you: `pipeline/A2_run_draft.sh` (`DRAFT_ENGINE=braker3`).

## Outputs to keep
- `braker.gtf` / `braker.gff3` → copy to `DRAFT_GFF`  
- Augustus species parameters under the working dir (reuse later)

## How to use afterward
1. `bash pipeline/A5_agat_stats.sh "$DRAFT_GFF"`  
2. Second predictor (GeMoMa/Liftoff) → EVM/TSEBRA  
3. If gene count absurd → **S10** (TE), not more BRAKER rounds

## Common failures
| Symptom | Likely cause |
|---------|----------------|
| Dies on GeneMark | License / container not set |
| Very few genes | Hard mask or empty BAM |
| Huge tiny ORFs | TE lib / soft-mask failure |
| “Species already exists” | Change `--species` name or reuse carefully |


## Naming (genepal)

- **Workflow C** — proteins only (our S2 / no BAM).  
- **Workflow D** — RNA BAM + proteins (our S1).

After run, always compare GeneMark / Augustus / final with [`../../pipeline/A5d_stage_counts.sh`](../../pipeline/A5d_stage_counts.sh) (Copetti habit).
