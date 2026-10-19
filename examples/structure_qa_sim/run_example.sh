#!/usr/bin/env bash
# Run the structure QA step on the simulated example.
# BUSCO / OMArk / gffcompare results are mock files copied from mock_tool_outputs/.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
OUT="${1:-$HERE/qa_out}"
mkdir -p "$OUT"
cp -R "$HERE/mock_tool_outputs/." "$OUT/"
python3 "$REPO/pipeline/structure_qa/run_structure_qa.py" \
  --gff "$HERE/consensus.gff3" \
  --genome "$HERE/genome.fa" \
  --proteins "$HERE/proteins.faa" \
  --evidence transcripts="$HERE/evidence_transcripts.gtf" \
  --evidence proteins="$HERE/evidence_proteins.gff3" \
  --bam "$HERE/rnaseq.bam" \
  --te "$HERE/te.gff3" \
  --out "$OUT"
echo "[OK] summary: $OUT/qc_summary.tsv"
