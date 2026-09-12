#!/usr/bin/env bash
# Structural QC with AGAT (NBISweden/AGAT) — before and after merge/curation.
set -euo pipefail

: "${WORK_DIR:?}"
GFF="${1:-${MERGED_GFF:-${DRAFT_GFF:?}}}"
OUT="${AGAT_OUT:-$WORK_DIR/agat}"
mkdir -p "$OUT"
base=$(basename "$GFF")
base=${base%.gz}

if ! command -v agat_sp_statistics.pl >/dev/null && ! command -v agat >/dev/null; then
  echo "Install AGAT (bioconda agat). Placeholder stats via gffread/awk only."
fi

if command -v agat_sp_statistics.pl >/dev/null; then
  agat_sp_statistics.pl --gff "$GFF" -o "$OUT/${base}.agat_stats.txt"
elif command -v agat >/dev/null; then
  agat statistics --gff "$GFF" -o "$OUT/${base}.agat_stats.txt"
fi

# Lightweight always-on counts
awk '
  $3=="gene"{g++}
  $3=="mRNA"||$3=="transcript"{t++}
  $3=="CDS"{c++}
  END{print "genes",g+0,"\nmRNA/transcript",t+0,"\nCDS",c+0}
' "$GFF" | tee "$OUT/${base}.counts.txt"

echo "[OK] $OUT — compare gene count vs near relative × ploidy; check mono-exon fraction"
