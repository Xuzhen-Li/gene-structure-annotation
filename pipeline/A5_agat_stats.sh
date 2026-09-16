#!/usr/bin/env bash
# Structural QC with AGAT (NBISweden/AGAT) — before and after merge/curation.
# Produces: AGAT_OUT counts/stats for a GFF (genes / mRNA / CDS).
# See: docs/STAGE_IO.md
set -euo pipefail

# Print-first: default DRY. Export RUN=1 to execute on the cluster.
if [[ "${RUN:-0}" != "1" ]]; then
  echo "[DRY] A5_agat_stats.sh: not executing. Review script, then: RUN=1 bash pipeline/A5_agat_stats.sh"
  exit 0
fi


: "${WORK_DIR:?}"
# shellcheck source=pipeline/_env_guards.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_env_guards.sh"
_gsa_reject_placeholder_path WORK_DIR "$WORK_DIR" || exit 1

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
