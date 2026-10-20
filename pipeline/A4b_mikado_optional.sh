#!/usr/bin/env bash
# A4b (optional): Mikado — pick the best transcript per locus across several transcript
# assemblies (StringTie, Trinity-GG, Iso-Seq, ...). Mikado is a transcript selector, not an
# ab initio consensus: its loci go to EVM on the TRANSCRIPT side (A4c --mikado).
# Steps: mikado configure -> prepare -> serialise -> pick  (Mikado tutorial, mikado.readthedocs.io)
# Output: $AGG_DIR/mikado/mikado.loci.gff3
# Print-first: default DRY. Export RUN=1 to execute.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=pipeline/_env_guards.sh
source "$HERE/_env_guards.sh"

: "${WORK_DIR:?}"
_gsa_reject_placeholder_path WORK_DIR "$WORK_DIR" || exit 1
: "${GENOME_FA:?}"
_gsa_reject_placeholder_path GENOME_FA "$GENOME_FA" || exit 1
# Tab list, one assembly per row: file alias strand_specific [score reference exclude_redundant strip_cds skip_split]
: "${MIKADO_LIST:?tab-separated assembly list (see examples/aggregation_toy/mikado_list.tsv)}"
AGG_DIR="${AGG_DIR:-$WORK_DIR/aggregate}"
OUT_DIR="$AGG_DIR/mikado"
MIKADO_BIN="${MIKADO_BIN:-mikado}"
MIKADO_SCORING="${MIKADO_SCORING:-plant.yaml}"
MIKADO_MODE="${MIKADO_MODE:-permissive}"
CONF="$OUT_DIR/configuration.yaml"

configure=("$MIKADO_BIN" configure --list "$OUT_DIR/list.abs.tsv" --reference "$GENOME_FA"
           --mode "$MIKADO_MODE" --scoring "$MIKADO_SCORING")
serialise=("$MIKADO_BIN" serialise --json-conf "$CONF")
if [[ -n "${MIKADO_JUNCTIONS:-}" ]]; then
  configure+=(--junctions "$MIKADO_JUNCTIONS"); serialise+=(--junctions "$MIKADO_JUNCTIONS")
fi
if [[ -n "${MIKADO_BLAST_TARGETS:-}" ]]; then
  configure+=(-bt "$MIKADO_BLAST_TARGETS"); serialise+=(--blast_targets "$MIKADO_BLAST_TARGETS")
fi
if [[ -n "${MIKADO_BLAST_TSV:-}" ]]; then serialise+=(--xml "$MIKADO_BLAST_TSV"); fi
if [[ -n "${MIKADO_ORFS:-}" ]]; then serialise+=(--orfs "$MIKADO_ORFS"); fi
configure+=("$CONF")
prepare=("$MIKADO_BIN" prepare --json-conf "$CONF")
pick=("$MIKADO_BIN" pick --configuration "$CONF" --subloci_out mikado.subloci.gff3)

echo "[A4b] cd $OUT_DIR"
echo "[A4b] ${configure[*]}"
echo "[A4b] ${prepare[*]}"
echo "[A4b] ${serialise[*]}"
echo "[A4b] ${pick[*]}"
if [[ "${RUN:-0}" != "1" ]]; then
  echo "[DRY] A4b_mikado_optional.sh: not executing. Review, then: RUN=1 bash pipeline/A4b_mikado_optional.sh"
  exit 0
fi

[[ -s "$MIKADO_LIST" ]] || { echo "[A4b error] MIKADO_LIST=$MIKADO_LIST not found" >&2; exit 1; }
command -v "$MIKADO_BIN" >/dev/null || { echo "[A4b error] $MIKADO_BIN not found" >&2; exit 2; }
mkdir -p "$OUT_DIR"
# Mikado runs inside OUT_DIR: rewrite relative assembly paths against the list's directory.
LIST_DIR="$(cd "$(dirname "$MIKADO_LIST")" && pwd)"
awk -v d="$LIST_DIR" 'BEGIN{FS=OFS="\t"} /^#/||NF==0{print;next} $1!~/^\//{$1=d"/"$1} {print}' \
  "$MIKADO_LIST" > "$OUT_DIR/list.abs.tsv"
cut -f1 "$OUT_DIR/list.abs.tsv" | grep -v '^#' | while read -r f; do
  [[ -z "$f" || -s "$f" ]] || { echo "[A4b error] assembly in list not found: $f" >&2; exit 1; }
done
cd "$OUT_DIR"
"${configure[@]}"
"${prepare[@]}"
"${serialise[@]}"
"${pick[@]}"
[[ -s mikado.loci.gff3 ]] || { echo "[A4b error] mikado pick wrote no mikado.loci.gff3" >&2; exit 1; }
echo "[A4b] done: $OUT_DIR/mikado.loci.gff3  ->  A4c_evm_inputs.py --mikado $OUT_DIR/mikado.loci.gff3"
