#!/usr/bin/env bash
# Primary draft launcher. Fill in the real binary/container lines for your cluster.
# Full narrative: docs/DETAILED_GUIDE.md Step 5.
# Prefer BRAKER4 (docs/tools/braker4.md) when available; this script prints classic braker.pl.
set -euo pipefail

: "${WORK_DIR:?}"
: "${GENOME_SOFT:?soft-masked FASTA}"
: "${DRAFT_GFF:?output GFF3 path}"
DRAFT_ENGINE="${DRAFT_ENGINE:-braker3}"
THREADS="${THREADS:-32}"
mkdir -p "$WORK_DIR/draft" "$(dirname "$DRAFT_GFF")"

case "$DRAFT_ENGINE" in
  braker3)
    : "${PROTEIN_DB:?OrthoDB Viridiplantae/eudicots FASTA}"
    RNA_BAM="${RNA_BAM:-none}"
    WD="$WORK_DIR/draft/braker3"
    mkdir -p "$WD"
    echo "[INFO] BRAKER3 — softmasking on; species model AUGUSTUS_SPECIES=${AUGUSTUS_SPECIES:-generic}"
    if [[ "$RNA_BAM" == "none" || -z "$RNA_BAM" ]]; then
      cat <<CMD
# Protein + ab initio (no RNA):
braker.pl \\
  --genome=$GENOME_SOFT \\
  --prot_seq=$PROTEIN_DB \\
  --softmasking \\
  --threads=$THREADS \\
  --species=${AUGUSTUS_SPECIES:-generic} \\
  --workingdir=$WD
CMD
    else
      cat <<CMD
# RNA + proteins (recommended S1):
braker.pl \\
  --genome=$GENOME_SOFT \\
  --prot_seq=$PROTEIN_DB \\
  --bam=$RNA_BAM \\
  --softmasking \\
  --threads=$THREADS \\
  --species=${AUGUSTUS_SPECIES:-generic} \\
  --workingdir=$WD
CMD
    fi
    echo "# After success:"
    echo "#   cp $WD/braker.gff3 $DRAFT_GFF"
    echo "#   # or: gffread $WD/braker.gtf -o $DRAFT_GFF"
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
  *)
    echo "unknown DRAFT_ENGINE=$DRAFT_ENGINE (braker3|galba|gemoma|eviann)"; exit 1
    ;;
esac
