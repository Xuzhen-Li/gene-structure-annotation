#!/usr/bin/env bash
# A4a (optional): TSEBRA — combine BRAKER1 (RNA-seq) and BRAKER2 (protein) gene sets.
# Only for separate BRAKER1 + BRAKER2 runs. BRAKER3 already runs TSEBRA internally:
# with BRAKER_VERSION=3 this step skips and braker.gtf goes straight to A4c --braker.
# Output: $AGG_DIR/tsebra/tsebra.gtf  ->  A4c_evm_inputs.py --tsebra (not together with --braker).
# Print-first: default DRY. Export RUN=1 to execute.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=pipeline/_env_guards.sh
source "$HERE/_env_guards.sh"

BRAKER_VERSION="${BRAKER_VERSION:-}"
case "$BRAKER_VERSION" in
  3|braker3|BRAKER3)
    echo "[A4a skip] BRAKER_VERSION=$BRAKER_VERSION: TSEBRA is built into BRAKER3. Use braker.gtf with A4c --braker."
    exit 0
    ;;
  1+2|braker1+2|BRAKER1+2) ;;
  *)
    echo "[A4a error] set BRAKER_VERSION=3 (skip) or BRAKER_VERSION=1+2 (run TSEBRA on BRAKER1 + BRAKER2)" >&2
    exit 1
    ;;
esac

: "${WORK_DIR:?}"
_gsa_reject_placeholder_path WORK_DIR "$WORK_DIR" || exit 1
AGG_DIR="${AGG_DIR:-$WORK_DIR/aggregate}"
OUT_DIR="$AGG_DIR/tsebra"
TSEBRA_OUT="${TSEBRA_OUT:-$OUT_DIR/tsebra.gtf}"
: "${BRAKER1_DIR:?BRAKER1 (RNA-seq) working directory}"
: "${BRAKER2_DIR:?BRAKER2 (protein) working directory}"
TSEBRA_GTFS="${TSEBRA_GTFS:-$BRAKER1_DIR/augustus.hints.gtf,$BRAKER2_DIR/augustus.hints.gtf}"
TSEBRA_HINTS="${TSEBRA_HINTS:-$BRAKER1_DIR/hintsfile.gff,$BRAKER2_DIR/hintsfile.gff}"
TSEBRA_BIN="${TSEBRA_HOME:+$TSEBRA_HOME/bin/}tsebra.py"
TSEBRA_CFG="${TSEBRA_CFG:-${TSEBRA_HOME:+$TSEBRA_HOME/config/default.cfg}}"
: "${TSEBRA_CFG:?set TSEBRA_CFG (e.g. TSEBRA/config/default.cfg) or TSEBRA_HOME}"

cmd=("$TSEBRA_BIN" -g "$TSEBRA_GTFS" -e "$TSEBRA_HINTS" -c "$TSEBRA_CFG" -o "$TSEBRA_OUT")
# Extra flags, e.g. TSEBRA_EXTRA="--filter_single_exon_genes" or "-k braker2.gtf"
if [[ -n "${TSEBRA_EXTRA:-}" ]]; then
  read -r -a extra <<<"$TSEBRA_EXTRA"
  cmd+=("${extra[@]}")
fi

echo "[A4a] ${cmd[*]}"
if [[ "${RUN:-0}" != "1" ]]; then
  echo "[DRY] A4a_tsebra_optional.sh: not executing. Review, then: RUN=1 bash pipeline/A4a_tsebra_optional.sh"
  exit 0
fi

IFS=, read -r -a files <<<"$TSEBRA_GTFS,$TSEBRA_HINTS,$TSEBRA_CFG"
for f in "${files[@]}"; do
  [[ -s "$f" ]] || { echo "[A4a error] missing input: $f" >&2; exit 1; }
done
command -v "$TSEBRA_BIN" >/dev/null || { echo "[A4a error] $TSEBRA_BIN not found (set TSEBRA_HOME or PATH)" >&2; exit 2; }
mkdir -p "$(dirname "$TSEBRA_OUT")"
"${cmd[@]}"
[[ -s "$TSEBRA_OUT" ]] || { echo "[A4a error] TSEBRA wrote no $TSEBRA_OUT" >&2; exit 1; }
echo "[A4a] done: $TSEBRA_OUT  ->  A4c_evm_inputs.py --tsebra $TSEBRA_OUT"
