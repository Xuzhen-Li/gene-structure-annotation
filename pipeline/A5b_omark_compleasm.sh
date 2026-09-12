#!/usr/bin/env bash
# Extra proteome QC beyond BUSCO: OMArk (DessimozLab) and/or Compleasm.
set -euo pipefail

: "${WORK_DIR:?}"
: "${PROTEINS_FA:?}"
OUT="${OMARK_OUT:-$WORK_DIR/omark}"
mkdir -p "$OUT"

if command -v omark >/dev/null || command -v OMArk >/dev/null; then
  echo "[INFO] OMArk — https://github.com/DessimozLab/OMArk"
  echo "  Typical: omamer search --db <LUCA/clade>.h5 --query $PROTEINS_FA --out $OUT/omamer.tsv"
  echo "           omark -f $OUT/omamer.tsv -o $OUT -d <OMAmer DB dir> ..."
  echo "[STOP] Wire OMAmer DB path for Viridiplantae / eudicots on your cluster"
else
  echo "[WARN] OMArk/OMAmer not on PATH"
fi

if command -v compleasm >/dev/null; then
  echo "[INFO] Compleasm (miniprot BUSCO-like) — https://github.com/huangnengCSU/compleasm"
  compleasm protein -p "$PROTEINS_FA" -l "${COMPLEASM_LINEAGE:-eudicots}" \
    -o "$OUT/compleasm" -t "${THREADS:-16}" \
    || echo "[WARN] compleasm failed — check lineage pack"
else
  echo "[WARN] compleasm not on PATH (optional)"
fi

echo "[OK] review $OUT — flag missing / duplicated / inconsistent placements for priority.tsv"
