#!/usr/bin/env bash
# Minimal Slurm sketches for default S1 — EDIT partition/account/qos for your site.
# Does NOT submit jobs until you uncomment/adapt. Print-first helpers still print until you run them.
#
# Required exports (fill via config/local.env, then):
#   set -a && source config/local.env && set +a
# Minimum for S1:
#   WORK_DIR  GENOME_FA  GENOME_SOFT  TRUSTED_TE_LIB/CLEAN_TE_LIB
#   PROTEIN_DB  RNA_BAM  BUSCO_LINEAGE  THREADS  RELEASE_TAG
#   DRAFT_GFF  MERGED_GFF  PROTEINS_FA  DRAFT_ENGINE
# See config/example.env and docs/LINEAGES.md / docs/TRUSTED_TE_PATH.md.

# Soft-mask (A0) — often short; needs CLEAN_TE_LIB / TRUSTED_TE_LIB
# #SBATCH --job-name=str_a0 --cpus-per-task=16 --mem=32G --time=12:00:00
# # follow pipeline/A0_softmask.md (or your RM wrapper); then export GENOME_SOFT

# Draft (S1) — BRAKER-class; long walltime / high mem typical
# #SBATCH --job-name=str_s1 --cpus-per-task=32 --mem=128G --time=48:00:00
# bash pipeline/A2_run_draft.sh
# # review printed braker.pl → run via module/singularity; copy GFF to DRAFT_GFF

# Proteins from GFF
# #SBATCH --job-name=str_prot --cpus-per-task=8 --mem=16G --time=4:00:00
# bash pipeline/A3_proteins_from_gff.sh

# QC proteins (after GFF→proteins)
# #SBATCH --job-name=str_qc --cpus-per-task=16 --mem=32G --time=12:00:00
# bash pipeline/01_qc_busco_psauron.sh

echo "This file is documentation-in-shell. Adapt SBATCH lines for your cluster; do not blind-submit."
