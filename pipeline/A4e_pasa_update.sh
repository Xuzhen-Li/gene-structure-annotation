#!/usr/bin/env bash
# A4e (optional): PASA annotation update on the EVM models — adds UTRs and alternatively
# spliced isoforms from PASA alignment assemblies. Default 2 rounds: round 2 loads the
# round-1 output (PASA wiki, "Annotation Comparisons and Annotation Updates": at least two
# cycles of load -> compare -> update).
# Needs an existing PASA alignment-assembly DB (alignAssembly.config) for the same genome
# and transcripts. Output: $PASA_UPDATED_GFF  ->  A5 AGAT (MERGED_GFF).
# Print-first: default DRY. Export RUN=1 to execute.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=pipeline/_env_guards.sh
source "$HERE/_env_guards.sh"

: "${WORK_DIR:?}"
_gsa_reject_placeholder_path WORK_DIR "$WORK_DIR" || exit 1
: "${PASA_HOME:?PASApipeline install directory}"
_gsa_reject_placeholder_path PASA_HOME "$PASA_HOME" || exit 1
: "${GENOME_FA:?}"
: "${PASA_ALIGN_CONFIG:?alignAssembly.config used for the PASA assemblies}"
: "${PASA_ANNOT_CONFIG:?annotCompare.config (from pasa_conf/pasa.annotationCompare.Template.txt)}"
: "${PASA_TRANSCRIPTS:?transcripts FASTA given to PASA (e.g. transcripts.fasta.clean)}"
AGG_DIR="${AGG_DIR:-$WORK_DIR/aggregate}"
EVM_GFF="${EVM_GFF:-$AGG_DIR/evm/evm.EVM.gff3}"
PASA_ROUNDS="${PASA_ROUNDS:-2}"
OUT_DIR="${PASA_UPDATE_DIR:-$AGG_DIR/pasa_update}"
PASA_UPDATED_GFF="${PASA_UPDATED_GFF:-$OUT_DIR/pasa_updated.gff3}"
[[ "$PASA_ROUNDS" =~ ^[1-9][0-9]*$ ]] || { echo "[A4e error] PASA_ROUNDS must be >= 1" >&2; exit 1; }

VALIDATOR="$PASA_HOME/misc_utilities/pasa_gff3_validator.pl"
LOADER="$PASA_HOME/scripts/Load_Current_Gene_Annotations.dbi"
LAUNCH="$PASA_HOME/Launch_PASA_pipeline.pl"
for r in $(seq 1 "$PASA_ROUNDS"); do
  in_gff=$([[ "$r" -eq 1 ]] && echo "$EVM_GFF" || echo "$OUT_DIR/round$((r - 1)).gff3")
  echo "[A4e] round $r: $VALIDATOR $in_gff"
  echo "[A4e] round $r: $LOADER -c $PASA_ALIGN_CONFIG -g $GENOME_FA -P $in_gff"
  echo "[A4e] round $r: $LAUNCH -c $PASA_ANNOT_CONFIG -A -g $GENOME_FA -t $PASA_TRANSCRIPTS"
  echo "[A4e] round $r: -> <db>.gene_structures_post_PASA_updates.<pid>.gff3 -> $OUT_DIR/round$r.gff3"
done
if [[ "${RUN:-0}" != "1" ]]; then
  echo "[DRY] A4e_pasa_update.sh: not executing. Review, then: RUN=1 bash pipeline/A4e_pasa_update.sh"
  exit 0
fi

abspath() { (cd "$(dirname "$1")" && echo "$(pwd)/$(basename "$1")"); }
for f in "$EVM_GFF" "$GENOME_FA" "$PASA_ALIGN_CONFIG" "$PASA_ANNOT_CONFIG" "$PASA_TRANSCRIPTS"; do
  [[ -s "$f" ]] || { echo "[A4e error] missing input: $f" >&2; exit 1; }
done
for t in "$VALIDATOR" "$LOADER" "$LAUNCH"; do
  [[ -x "$t" ]] || { echo "[A4e error] not executable: $t (check PASA_HOME)" >&2; exit 2; }
done
G="$(abspath "$GENOME_FA")"; AC="$(abspath "$PASA_ALIGN_CONFIG")"
CC="$(abspath "$PASA_ANNOT_CONFIG")"; T="$(abspath "$PASA_TRANSCRIPTS")"
mkdir -p "$OUT_DIR"
OUT_DIR="$(cd "$OUT_DIR" && pwd)"
current="$(abspath "$EVM_GFF")"
cd "$OUT_DIR"
for r in $(seq 1 "$PASA_ROUNDS"); do
  echo "[A4e] round $r: loading $current"
  "$VALIDATOR" "$current"
  "$LOADER" -c "$AC" -g "$G" -P "$current"
  before="$(ls -1 ./*.gene_structures_post_PASA_updates.*.gff3 2>/dev/null || true)"
  "$LAUNCH" -c "$CC" -A -g "$G" -t "$T"
  new=""
  for f in $(ls -1t ./*.gene_structures_post_PASA_updates.*.gff3 2>/dev/null || true); do
    grep -qxF "$f" <<<"$before" || { new="$f"; break; }
  done
  [[ -n "$new" && -s "$new" ]] || { echo "[A4e error] round $r: no new *.gene_structures_post_PASA_updates.*.gff3" >&2; exit 1; }
  cp "$new" "round$r.gff3"
  echo "[A4e] round $r: $(basename "$new") -> round$r.gff3 (genes: $(awk -F'\t' '$3=="gene"' "round$r.gff3" | wc -l))"
  current="$OUT_DIR/round$r.gff3"
done
mkdir -p "$(dirname "$PASA_UPDATED_GFF")"
[[ "$(abspath "$PASA_UPDATED_GFF")" == "$current" ]] || cp "$current" "$PASA_UPDATED_GFF"
echo "[A4e] done: $PASA_UPDATED_GFF  ->  MERGED_GFF=$PASA_UPDATED_GFF, then A5 AGAT"
