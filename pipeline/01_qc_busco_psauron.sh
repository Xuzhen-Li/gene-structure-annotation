#!/usr/bin/env bash
# Protein-set completeness (BUSCO) + coding-likelihood scores (PSAURON).
# Pattern from GSAman Methods (Chen et al. 2026 The Innovation).
# Produces: BUSCO_OUT summary + PSAURON_TSV.
# See: docs/STAGE_IO.md · docs/QUICKSTART.md
set -euo pipefail

# Print-first: default DRY. Export RUN=1 to execute on the cluster.
if [[ "${RUN:-0}" != "1" ]]; then
  echo "[DRY] 01_qc_busco_psauron.sh: not executing. Review script, then: RUN=1 bash pipeline/01_qc_busco_psauron.sh"
  exit 0
fi


: "${WORK_DIR:?}"
: "${PROTEINS_FA:?}"
BUSCO_LINEAGE="${BUSCO_LINEAGE:?set BUSCO_LINEAGE in local.env (no silent plant default)}"
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
