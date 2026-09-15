#!/usr/bin/env bash
# Minimal Slurm sketches for default S1 — EDIT partition/account/qos for your site.
# After: set -a && source config/local.env && set +a
# Does NOT submit jobs until you uncomment/adapt. Print-first helpers still print until you run them.

# Soft-mask (A0) — often short; needs CLEAN_TE_LIB / TRUSTED_TE_LIB
# #SBATCH --job-name=str_a0 --cpus-per-task=16 --mem=32G --time=12:00:00
# bash pipeline/A0_softmask.md  # follow doc; or your RM wrapper

# Draft (S1) — BRAKER-class; long walltime / high mem typical
# #SBATCH --job-name=str_s1 --cpus-per-task=32 --mem=128G --time=48:00:00
# bash pipeline/A2_run_draft.sh

# QC proteins (after GFF→proteins)
# #SBATCH --job-name=str_qc --cpus-per-task=16 --mem=32G --time=12:00:00
# bash pipeline/01_qc_busco_psauron.sh

echo "This file is documentation-in-shell. Adapt SBATCH lines for your cluster; do not blind-submit."
