#!/usr/bin/env bash
# Primary draft launcher. Fill in the real binary/container lines for your cluster.
# Full narrative: docs/DETAILED_GUIDE.md Step 5.
# Prefer BRAKER4 (docs/tools/braker4.md) when available; this script prints classic braker.pl.
set -euo pipefail

: "${WORK_DIR:?set WORK_DIR in config/local.env}"
: "${DRAFT_GFF:?output GFF3 path}"
DRAFT_ENGINE="${DRAFT_ENGINE:-braker3}"
THREADS="${THREADS:-32}"
# shellcheck source=pipeline/_env_guards.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_env_guards.sh"
_gsa_reject_placeholder_path WORK_DIR "$WORK_DIR" || exit 1
_gsa_reject_placeholder_path DRAFT_GFF "$DRAFT_GFF" || exit 1
if [[ "$DRAFT_ENGINE" != "liftoff" ]]; then
  : "${GENOME_SOFT:?soft-masked FASTA}"
  _gsa_reject_placeholder_path GENOME_SOFT "$GENOME_SOFT" || exit 1
fi
mkdir -p "$WORK_DIR/draft" "$(dirname "$DRAFT_GFF")"

case "$DRAFT_ENGINE" in
  braker3)
    : "${PROTEIN_DB:?clade-matched protein DB FASTA (OrthoDB or equivalent for YOUR species)}"
    RNA_BAM="${RNA_BAM:-none}"
    # AUGUSTUS species name: fixed per genome (${GENOME_PREFIX}_braker), never a shared "generic".
    # braker.pl stops if that species directory already exists. To rerun on the same genome, add
    # --useexisting (BRAKER then trains again and overwrites the parameters in that directory); to start
    # training from scratch, delete the species directory first. Only --skipAllTraining reuses it unchanged.
    # The printed "# --useexisting" line sits above braker.pl: a comment inside the \ continuation would cut the command.
    case "${GENOME_PREFIX:-}" in
      ""|Species_v1.0|YOUR_*)
        echo "[STOP] set GENOME_PREFIX in config/local.env (now: '${GENOME_PREFIX:-}') — it names the AUGUSTUS species ${GENOME_PREFIX:-<GENOME_PREFIX>}_braker" >&2
        exit 1
        ;;
    esac
    AUGUSTUS_SPECIES="${AUGUSTUS_SPECIES:-${GENOME_PREFIX}_braker}"
    WD="$WORK_DIR/draft/braker3"
    mkdir -p "$WD"
    echo "[INFO] BRAKER3 — softmasking on; species model AUGUSTUS_SPECIES=$AUGUSTUS_SPECIES"
    if [[ "$RNA_BAM" == "none" || -z "$RNA_BAM" ]]; then
      cat <<CMD
# Protein + ab initio (no RNA):
# --useexisting
braker.pl \\
  --genome=$GENOME_SOFT \\
  --prot_seq=$PROTEIN_DB \\
  --softmasking \\
  --threads=$THREADS \\
  --species=$AUGUSTUS_SPECIES \\
  --gff3 \\
  --workingdir=$WD
CMD
    else
      cat <<CMD
# RNA + proteins (recommended S1):
# --useexisting
braker.pl \\
  --genome=$GENOME_SOFT \\
  --prot_seq=$PROTEIN_DB \\
  --bam=$RNA_BAM \\
  --softmasking \\
  --threads=$THREADS \\
  --species=$AUGUSTUS_SPECIES \\
  --gff3 \\
  --workingdir=$WD
CMD
    fi
    echo "# After success (--gff3 writes braker.gff3; the gffread fallback keeps gene lines):"
    echo "cp \"$WD/braker.gff3\" \"$DRAFT_GFF\""
    echo "# or, if only braker.gtf exists:"
    echo "gffread \"$WD/braker.gtf\" --keep-genes -o \"$DRAFT_GFF\""
    echo "[STOP] Run the printed braker.pl via your module/singularity, then copy GFF to DRAFT_GFF"
    ;;
  galba)
    : "${PROTEIN_DB:?close-relative proteins}"
    WD="$WORK_DIR/draft/galba"
    mkdir -p "$WD"
    cat <<CMD
galba.pl \\
  --genome=$GENOME_SOFT \\
  --prot_seq=$PROTEIN_DB \\
  --softmasking \\
  --threads=$THREADS \\
  --workingdir=$WD
# cp $WD/galba.gff3 $DRAFT_GFF
CMD
    echo "[STOP] Wire GALBA container/module"
    ;;
  gemoma)
    : "${REF_GFF:?}" ; : "${REF_FA:?}"
    echo "[INFO] GeMoMa — project $REF_GFF from $REF_FA onto $GENOME_SOFT"
    echo "# See GeMoMa manual for your version’s CLI; write $DRAFT_GFF"
    echo "[STOP] Wire GeMoMa"
    ;;
  eviann)
    : "${ISOSEQ_BAM:?}" ; : "${PROTEIN_DB:?}"
    echo "[INFO] EviAnn — Iso-seq/RNA evidence + proteins → $DRAFT_GFF"
    echo "# Follow https://github.com/alekseyzimin/EviAnn_release for current CLI"
    echo "[STOP] Wire EviAnn"
    ;;
  liftoff)
    # S11 / S11-lite primary draft: lift a close curated reference (details: pipeline/A2c_liftoff.md).
    : "${REF_FA:?reference genome FASTA}" ; : "${REF_GFF:?reference annotation GFF3}"
    : "${GENOME_FA:?target genome FASTA}"
    _gsa_reject_placeholder_path REF_FA "$REF_FA" || exit 1
    _gsa_reject_placeholder_path REF_GFF "$REF_GFF" || exit 1
    _gsa_reject_placeholder_path GENOME_FA "$GENOME_FA" || exit 1
    WD="$WORK_DIR/draft/liftoff_int"
    mkdir -p "$WD"
    echo "[INFO] Liftoff — $REF_GFF ($REF_FA) onto $GENOME_FA → $DRAFT_GFF"
    cat <<CMD
liftoff -g $REF_GFF \\
  -o $DRAFT_GFF \\
  -dir $WD \\
  -p $THREADS \\
  -polish \\
  -copies \\
  $GENOME_FA $REF_FA
CMD
    echo "# Then: RUN=1 bash pipeline/A5_agat_stats.sh \"$DRAFT_GFF\"  (S11 also needs pipeline/A2e_s11_gapfill.md)"
    echo "[STOP] Run the printed liftoff command (see pipeline/A2c_liftoff.md)"
    ;;
  *)
    echo "unknown DRAFT_ENGINE=$DRAFT_ENGINE (braker3|galba|gemoma|eviann|liftoff)"; exit 1
    ;;
esac
