#!/usr/bin/env bash
# Minimal Slurm sketches for S11 (Liftoff + gap-fill) — EDIT partition/account/qos for your site.
# Sibling of sbatch_s1_examples.sh. Does NOT submit until you uncomment/adapt.
#
# Required exports (fill via config/local.env, then):
#   set -a && source config/local.env && set +a
# Minimum for S11 / S11-lite:
#   WORK_DIR  GENOME_FA  GENOME_SOFT  TRUSTED_TE_LIB/CLEAN_TE_LIB
#   REF_FA  REF_GFF  THREADS  RELEASE_TAG  DRAFT_GFF
# For full S11 gap-fill also: PROTEIN_DB  (RNA_BAM optional)  BUSCO_LINEAGE
#   DRAFT_GFF_B  MERGE_MODE  MERGED_GFF  PROTEINS_FA
# Docs: pipeline/A2c_liftoff.md · pipeline/A2e_s11_gapfill.md · docs/LINEAGES.md

# Soft-mask (A0) — same as S1; trusted TE only
# #SBATCH --job-name=str_a0 --cpus-per-task=16 --mem=32G --time=12:00:00
# # follow pipeline/A0_softmask.md → GENOME_SOFT

# Liftoff (S11-lite stop possible after this + AGAT)
# #SBATCH --job-name=str_lift --cpus-per-task=16 --mem=64G --time=24:00:00
# # paste CLI from pipeline/A2c_liftoff.md; export DRAFT_GFF=liftoff.gff3
# # bash pipeline/A5_agat_stats.sh "$DRAFT_GFF"
# # STOP here only if claiming S11-lite (L0 provisional) — see A2c

# Gap-fill orphan draft (full S11) — BRAKER/GALBA on soft-masked genome or windows
# #SBATCH --job-name=str_orphan --cpus-per-task=32 --mem=128G --time=48:00:00
# # DRAFT_ENGINE=braker3|galba; write orphan GFF → DRAFT_GFF_B (pipeline/A2e_s11_gapfill.md)
# bash pipeline/A2_run_draft.sh

# Merge lift + orphans
# #SBATCH --job-name=str_merge --cpus-per-task=16 --mem=64G --time=24:00:00
# bash pipeline/A4_merge_sets.sh

# Proteins + QC (rejoin trunk)
# #SBATCH --job-name=str_qc --cpus-per-task=16 --mem=32G --time=12:00:00
# bash pipeline/A3_proteins_from_gff.sh
# bash pipeline/01_qc_busco_psauron.sh

echo "This file is documentation-in-shell for S11 lift+gapfill. Adapt SBATCH lines; do not blind-submit."
