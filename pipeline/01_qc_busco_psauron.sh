#!/usr/bin/env bash
# Protein-set completeness (BUSCO) + coding-likelihood scores (PSAURON).
# Pattern from GSAman Methods (Chen et al. 2026 The Innovation).
set -euo pipefail

: "${WORK_DIR:?}"
: "${PROTEINS_FA:?}"
BUSCO_LINEAGE="${BUSCO_LINEAGE:-viridiplantae_odb12}"
BUSCO_OUT="${BUSCO_OUT:-$WORK_DIR/busco_prot}"
PSAURON_TSV="${PSAURON_TSV:-$WORK_DIR/psauron.tsv}"
THREADS="${THREADS:-16}"
mkdir -p "$WORK_DIR" "$BUSCO_OUT"

if command -v busco >/dev/null; then
  busco -i "$PROTEINS_FA" -l "$BUSCO_LINEAGE" -o "$(basename "$BUSCO_OUT")" \
    --out_path "$(dirname "$BUSCO_OUT")" -m proteins -c "$THREADS" \
    || echo "[WARN] busco failed — check lineage download"
else
  echo "[WARN] busco not on PATH"
fi

if command -v psauron >/dev/null; then
  # CLI flags vary by PSAURON version — confirm with psauron --help
  psauron -i "$PROTEINS_FA" -o "$PSAURON_TSV" \
    || echo "[WARN] psauron invocation failed — adjust flags for your install"
else
  echo "[WARN] psauron not on PATH — install from upstream (see GSAman paper Methods)"
  echo "gene_id	psauron_score" > "$PSAURON_TSV"
  echo "# placeholder — fill after install" >> "$PSAURON_TSV"
fi

echo "[OK] review $BUSCO_OUT and $PSAURON_TSV"
