#!/usr/bin/env bash
# Extra proteome QC beyond BUSCO: OMArk (DessimozLab) and/or Compleasm.
# Docs: docs/tools/omark_compleasm.md
# Wire OMAMER_DB to the .h5 path; set RUN=1 to execute (otherwise print).
set -euo pipefail

: "${WORK_DIR:?}"
: "${PROTEINS_FA:?}"
# shellcheck source=pipeline/_env_guards.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_env_guards.sh"
# YOUR_* / bare eukaryota in COMPLEASM_LINEAGE → [ERR] and exit 1 (not print-only / DRY).
# Reject bad Compleasm lineage early (even if compleasm binary is absent).
if [[ -n "${COMPLEASM_LINEAGE:-}" ]]; then
  _gsa_reject_compleasm_lineage "$COMPLEASM_LINEAGE" || exit 1
fi
OUT="${OMARK_OUT:-$WORK_DIR/qc/omark}"
OMAMER_DB="${OMAMER_DB:-}"
THREADS="${THREADS:-16}"
RUN="${RUN:-0}"
mkdir -p "$OUT"

run_or_print() {
  printf '[CMD]'; printf '%q ' "$@"; echo
  if [[ "$RUN" == "1" ]]; then
    "$@"
  else
    echo "[DRY] export RUN=1 to execute"
  fi
}

if command -v omamer >/dev/null && command -v omark >/dev/null; then
  if [[ -z "$OMAMER_DB" || ! -f "$OMAMER_DB" ]]; then
    echo "[STOP] Set OMAMER_DB to an OMAmer .h5 (prefer LUCA.h5 for S5)."
    echo "       See docs/tools/omark_compleasm.md"
    echo "  Example download: curl -fL -O https://omabrowser.org/All/LUCA.h5"
  else
    echo "[INFO] OMArk via OMAmer DB: $OMAMER_DB"
    run_or_print omamer search --db "$OMAMER_DB" --query "$PROTEINS_FA" --out "$OUT/proteins.omamer"
    mkdir -p "$OUT/omark_output"
    OMARK_ARGS=(omark -f "$OUT/proteins.omamer" -d "$OMAMER_DB" -o "$OUT/omark_output")
    if [[ -n "${OMARK_TAXID:-}" ]]; then
      OMARK_ARGS+=(-t "$OMARK_TAXID")
    fi
    run_or_print "${OMARK_ARGS[@]}"
  fi
else
  echo "[WARN] omamer/omark not both on PATH — install or load modules"
  echo "       https://github.com/DessimozLab/OMArk"
fi

if command -v compleasm >/dev/null; then
  : "${COMPLEASM_LINEAGE:?set COMPLEASM_LINEAGE in local.env (no silent eudicots default)}"
  _gsa_reject_compleasm_lineage "$COMPLEASM_LINEAGE" || exit 1
  echo "[INFO] Compleasm protein mode — lineage=$COMPLEASM_LINEAGE"
  run_or_print compleasm protein -p "$PROTEINS_FA" -l "$COMPLEASM_LINEAGE" \
    -o "$OUT/compleasm" -t "$THREADS"
else
  echo "[WARN] compleasm not on PATH (optional)"
fi

echo "[OK] review $OUT — export missing/inconsistent IDs into priority_r2 (02b_merge_priority_r2.py)"
