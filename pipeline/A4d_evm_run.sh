#!/usr/bin/env bash
# A4d: run EVidenceModeler 2.x on the A4c inputs (single EVidenceModeler command:
# partitions, runs in parallel with --CPU, recombines; EVM wiki "Running EVM").
# Inputs:  $EVM_INPUT_DIR/{gene_predictions,transcript_alignments,protein_alignments}.gff3 + weights.txt
# Output:  $EVM_DIR/$EVM_SAMPLE_ID.EVM.gff3, copied to $EVM_GFF  ->  A4e PASA update or A5 AGAT
# Print-first: default DRY. Export RUN=1 to execute.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=pipeline/_env_guards.sh
source "$HERE/_env_guards.sh"

: "${WORK_DIR:?}"
_gsa_reject_placeholder_path WORK_DIR "$WORK_DIR" || exit 1
EVM_GENOME="${EVM_GENOME:-${GENOME_FA:?set GENOME_FA or EVM_GENOME}}"
_gsa_reject_placeholder_path EVM_GENOME "$EVM_GENOME" || exit 1
AGG_DIR="${AGG_DIR:-$WORK_DIR/aggregate}"
EVM_INPUT_DIR="${EVM_INPUT_DIR:-$AGG_DIR/evm_inputs}"
EVM_DIR="${EVM_DIR:-$AGG_DIR/evm}"
EVM_SAMPLE_ID="${EVM_SAMPLE_ID:-evm}"
EVM_GFF="${EVM_GFF:-$EVM_DIR/$EVM_SAMPLE_ID.EVM.gff3}"
# --segmentSize < 1 Mb; --overlapSize >= one or two expected gene lengths (EVM wiki).
EVM_SEGMENT_SIZE="${EVM_SEGMENT_SIZE:-100000}"
EVM_OVERLAP_SIZE="${EVM_OVERLAP_SIZE:-10000}"
THREADS="${THREADS:-4}"
EVM_BIN="${EVM_HOME:+$EVM_HOME/}EVidenceModeler"

abspath() { (cd "$(dirname "$1")" && echo "$(pwd)/$(basename "$1")"); }

GP="$EVM_INPUT_DIR/gene_predictions.gff3"
PA="$EVM_INPUT_DIR/protein_alignments.gff3"
TA="$EVM_INPUT_DIR/transcript_alignments.gff3"
W="$EVM_INPUT_DIR/weights.txt"
REPEATS_GFF="${REPEATS_GFF:-}"
build_cmd() {
  cmd=("$EVM_BIN" --sample_id "$EVM_SAMPLE_ID" --genome "$EVM_GENOME" --weights "$W"
       --gene_predictions "$GP")
  if [[ -s "$PA" ]]; then cmd+=(--protein_alignments "$PA"); fi
  if [[ -s "$TA" ]]; then cmd+=(--transcript_alignments "$TA"); fi
  if [[ -n "$REPEATS_GFF" ]]; then cmd+=(--repeats "$REPEATS_GFF"); fi
  cmd+=(--segmentSize "$EVM_SEGMENT_SIZE" --overlapSize "$EVM_OVERLAP_SIZE" --CPU "$THREADS")
}
build_cmd

echo "[A4d] cd $EVM_DIR"
echo "[A4d] ${cmd[*]}"
if [[ "${RUN:-0}" != "1" ]]; then
  echo "[DRY] A4d_evm_run.sh: not executing. Review, then: RUN=1 bash pipeline/A4d_evm_run.sh"
  exit 0
fi

for f in "$EVM_GENOME" "$GP" "$W"; do
  [[ -s "$f" ]] || { echo "[A4d error] missing input: $f (run A4c first)" >&2; exit 1; }
done
command -v "$EVM_BIN" >/dev/null || { echo "[A4d error] $EVM_BIN not found (set EVM_HOME or PATH)" >&2; exit 2; }
# Re-validate the inputs before spending cluster time.
python3 "$HERE/A4c_evm_inputs.py" --validate "$GP" --kind gene
for a in "$PA" "$TA"; do
  if [[ -s "$a" ]]; then python3 "$HERE/A4c_evm_inputs.py" --validate "$a" --kind alignment; fi
done
# EVM writes relative to its cwd: absolute paths for every input.
EVM_GENOME="$(abspath "$EVM_GENOME")"; GP="$(abspath "$GP")"; W="$(abspath "$W")"
PA="$(abspath "$PA")"; TA="$(abspath "$TA")"
if [[ -n "$REPEATS_GFF" ]]; then REPEATS_GFF="$(abspath "$REPEATS_GFF")"; fi
build_cmd
mkdir -p "$EVM_DIR"
(cd "$EVM_DIR" && "${cmd[@]}")
OUT="$EVM_DIR/$EVM_SAMPLE_ID.EVM.gff3"
[[ -s "$OUT" ]] || { echo "[A4d error] EVM wrote no $OUT" >&2; exit 1; }
[[ "$(abspath "$OUT")" == "$(abspath "$EVM_GFF")" ]] || { mkdir -p "$(dirname "$EVM_GFF")"; cp "$OUT" "$EVM_GFF"; }
cp "$W" "$EVM_DIR/weights.used.txt"
echo "[A4d] genes: $(awk -F'\t' '$3=="gene"' "$EVM_GFF" | wc -l)  ($EVM_GFF; weights logged in $EVM_DIR/weights.used.txt)"
echo "[A4d] next: A4e_pasa_update.sh (optional UTR/isoform rounds) or MERGED_GFF=$EVM_GFF -> A5 AGAT"
