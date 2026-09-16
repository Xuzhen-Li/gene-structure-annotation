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
# shellcheck source=pipeline/_env_guards.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_env_guards.sh"
_gsa_reject_placeholder_path WORK_DIR "$WORK_DIR" || exit 1
_gsa_reject_placeholder_path PROTEINS_FA "$PROTEINS_FA" || exit 1
BUSCO_LINEAGE="${BUSCO_LINEAGE:?set BUSCO_LINEAGE in local.env (no silent plant default)}"
_gsa_reject_busco_lineage "$BUSCO_LINEAGE" || exit 1
BUSCO_OUT="${BUSCO_OUT:-$WORK_DIR/busco_prot}"
PSAURON_TSV="${PSAURON_TSV:-$WORK_DIR/psauron.tsv}"
THREADS="${THREADS:-16}"
mkdir -p "$WORK_DIR" "$BUSCO_OUT"

busco_rc=0
psauron_rc=0

if command -v busco >/dev/null; then
  if ! busco -i "$PROTEINS_FA" -l "$BUSCO_LINEAGE" -o "$(basename "$BUSCO_OUT")" \
    --out_path "$(dirname "$BUSCO_OUT")" -m proteins -c "$THREADS"; then
    echo "[WARN] busco failed — check lineage download" >&2
    busco_rc=1
  fi
else
  echo "[WARN] busco not on PATH" >&2
  busco_rc=1
fi

if command -v psauron >/dev/null; then
  # CLI flags vary by PSAURON version — confirm with psauron --help
  if ! psauron -i "$PROTEINS_FA" -o "$PSAURON_TSV"; then
    echo "[WARN] psauron invocation failed — adjust flags for your install" >&2
    psauron_rc=1
  fi
else
  echo "[WARN] psauron not on PATH — install from upstream (see GSAman paper Methods)" >&2
  echo "gene_id	psauron_score" > "$PSAURON_TSV"
  echo "# placeholder — fill after install" >> "$PSAURON_TSV"
  psauron_rc=1
fi

if [[ "$busco_rc" -eq 0 && "$psauron_rc" -eq 0 ]]; then
  echo "[OK] review $BUSCO_OUT and $PSAURON_TSV"
  exit 0
fi
echo "[FAIL] QC incomplete (busco_rc=$busco_rc psauron_rc=$psauron_rc) — do not treat as passed" >&2
exit 1
