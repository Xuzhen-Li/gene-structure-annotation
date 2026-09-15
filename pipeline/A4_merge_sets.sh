#!/usr/bin/env bash
# Merge prediction sets. S1 weights vs S14 EVM weights.
# See docs/steps/dclab/07_evm_polish.md and docs/DETAILED_GUIDE.md Step 7.
set -euo pipefail
: "${WORK_DIR:?}"
: "${DRAFT_GFF:?primary GFF/GTF}"
MERGE_MODE="${MERGE_MODE:-evm}"
MERGED_GFF="${MERGED_GFF:-$WORK_DIR/draft/merged.gff3}"
EVM_WEIGHTS="${EVM_WEIGHTS:-}"
REPO_ROOT="${REPO_ROOT:-}"
mkdir -p "$(dirname "$MERGED_GFF")" "$WORK_DIR/draft"

# Dual-track only. StringTie compare ≠ second gene set for EVM — skip A4 if no real B.
if [[ -z "${DRAFT_GFF_B:-}" || "$DRAFT_GFF_B" == "$DRAFT_GFF" ]]; then
  cat <<'SKIP'
[A4 skip] DRAFT_GFF_B unset or identical to DRAFT_GFF — merge not applicable.
  Pure S1 + StringTie compare does not need EVM/TSEBRA.
  Export MERGED_GFF=$DRAFT_GFF and continue to AGAT/proteins, OR set a true second
  predictor/Liftoff GFF as DRAFT_GFF_B (A2b/A2c) before re-running.
SKIP
  exit 0
fi
if [[ ! -f "$DRAFT_GFF_B" ]]; then
  echo "[A4 error] DRAFT_GFF_B=$DRAFT_GFF_B not found — skip A4 or fix path." >&2
  exit 1
fi

case "$MERGE_MODE" in
  evm)
    W="${EVM_WEIGHTS}"
    if [[ -z "$W" && -n "$REPO_ROOT" ]]; then
      W="$REPO_ROOT/config/evm_weights_s1_braker.txt"
    fi
    cat <<MSG
[EVM] Inputs:
  A=$DRAFT_GFF
  B=$DRAFT_GFF_B
  weights=${W:-config/evm_weights_*.txt}
S1 template:  config/evm_weights_s1_braker.txt
S14 weights: config/evm_weights_cantulab.txt  (needs transcript_alignments + repeats.gff3)

S14-style run (after predictions.gff3 + transcript_alignments.gff3 + repeats.gff3):
  \${EVM_TOOLS}/EvmUtils/partition_EVM_inputs.pl --partition_dir ./partition_dir \\
    --genome GENOME.fa --gene_predictions predictions.gff3 \\
    --transcript_alignments transcript_alignments.gff3 --repeats repeats.gff3 \\
    --segmentSize 300000 --overlapSize 100000 --partition_listing partitions_list.out
  \${EVM_TOOLS}/EvmUtils/write_EVM_commands.pl ... > commands.list && parallel -j \$THREADS :::: commands.list
  recombine_EVM_partial_outputs.pl → convert_EVM_outputs_to_GFF3.pl → EVM.all.gff3
Full S14: docs/steps/dclab/07_evm_polish.md
MSG
    echo "[STOP] Run EVM with your install; copy final GFF to $MERGED_GFF"
    ;;
  tsebra)
    echo "tsebra.py -g $DRAFT_GFF,$DRAFT_GFF_B -c default.cfg -o $WORK_DIR/draft/tsebra.gtf"
    echo "gffread $WORK_DIR/draft/tsebra.gtf -o $MERGED_GFF"
    echo "[STOP] Install TSEBRA and run"
    ;;
  evi_backbone)
    echo "[EviAnn backbone] keep $DRAFT_GFF_B; add non-overlapping from $DRAFT_GFF → $MERGED_GFF"
    echo "[STOP] Implement overlap filter"
    ;;
  mikado)
    echo "[Mikado] configure/prepare/serialise/pick — see docs/tools/mikado.md and S13"
    echo "[STOP] Wire Mikado or run RAGNAROK upstream"
    ;;
  *)
    echo "MERGE_MODE must be evm|tsebra|evi_backbone|mikado"; exit 1
    ;;
esac
