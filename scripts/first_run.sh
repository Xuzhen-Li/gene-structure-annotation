#!/usr/bin/env bash
# First run on the tiny toy in testdata/structure/ (about 1 second, no heavy tools).
# Usage: bash scripts/first_run.sh [OUT_DIR]      (default: ./first_run_out)
#
# Steps (one output each):
#   1 plan            -> OUT/plan.md                     (pipeline/flow_tool/flow.py)
#   2 tool check      -> OUT/tools.txt                   (scripts/check_tools.sh)
#   3 draft           -> OUT/work/draft/primary.gff3     (toy stands in for BRAKER; A2 printed only)
#   4 gene counts     -> OUT/work/agat/primary.gff3.counts.txt   (RUN=1 A5_agat_stats.sh)
#   5 proteins        -> OUT/work/proteins.faa           (longest isoform per gene, built-in translator)
#   6 quality check   -> OUT/work/qc/structure_qa/qc_summary.tsv (pipeline/structure_qa)
#   7 release pack    -> OUT/work/release/toy.v0.1/      (pipeline/check_release_pack.py)
#   8 compare         -> OUT/first_run_files.txt vs testdata/structure/expected/
# Exit 0 when every step worked and the outputs match the expected listing.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOY="$REPO/testdata/structure"
OUT="${1:-$PWD/first_run_out}"
mkdir -p "$OUT"
OUT="$(cd "$OUT" && pwd)"
WORK="$OUT/work"
TAG="toy.v0.1"
rm -rf "$WORK"
mkdir -p "$WORK/draft"

# Env for the scripts below; only toy paths, nothing private.
cat > "$OUT/toy.env" <<ENV
WORK_DIR="$WORK"
GENOME_FA="$TOY/genome.fa"
GENOME_SOFT="$TOY/genome.fa"
PROTEIN_DB="$TOY/protein_db.faa"
RNA_BAM="$TOY/rnaseq.bam"
TRUSTED_TE_LIB="$TOY/te_lib.fa"
DRAFT_GFF="$WORK/draft/primary.gff3"
MERGED_GFF="$WORK/draft/primary.gff3"
PROTEINS_FA="$WORK/proteins.faa"
AGAT_OUT="$WORK/agat"
RELEASE_TAG="$TAG"
THREADS=1
ENV
set -a
# shellcheck disable=SC1091
source "$OUT/toy.env"
set +a

echo "== 1 plan"
python3 "$REPO/pipeline/flow_tool/flow.py" \
  --answers "$REPO/examples/plant_sim/01_vitis_s1_s7/answers.sim.yaml" -o "$OUT/plan.md" >/dev/null 2>&1
echo "[OK] $OUT/plan.md"

echo "== 2 tool check"
bash "$REPO/scripts/check_tools.sh" > "$OUT/tools.txt"
echo "[OK] $OUT/tools.txt"

echo "== 3 draft (toy stands in for BRAKER)"
env -u RUN bash "$REPO/pipeline/A2_run_draft.sh" > "$OUT/draft_command.txt" 2>&1 || true
cp "$TOY/draft.gff3" "$DRAFT_GFF"
echo "[OK] $DRAFT_GFF  (the BRAKER command it replaces: $OUT/draft_command.txt)"

echo "== 4 gene counts"
RUN=1 bash "$REPO/pipeline/A5_agat_stats.sh" "$DRAFT_GFF" > /dev/null
echo "[OK] $AGAT_OUT/primary.gff3.counts.txt"

echo "== 5 proteins (longest isoform per gene)"
python3 "$REPO/pipeline/structure_qa/qa01_longest_isoform.py" \
  --gff "$DRAFT_GFF" --genome "$GENOME_FA" --out "$WORK/qc/proteins_tmp" > /dev/null
cp "$WORK/qc/proteins_tmp/longest_isoform.proteins.faa" "$PROTEINS_FA"
rm -rf "$WORK/qc/proteins_tmp"
echo "[OK] $PROTEINS_FA"

echo "== 6 quality check"
env -u RUN python3 "$REPO/pipeline/structure_qa/run_structure_qa.py" \
  --gff "$DRAFT_GFF" --genome "$GENOME_FA" --proteins "$PROTEINS_FA" \
  --evidence transcripts="$TOY/transcripts.gtf" \
  --bam "$RNA_BAM" --te "$TOY/te.gff3" \
  --out "$WORK/qc/structure_qa" > "$OUT/structure_qa.log" 2>&1
echo "[OK] $WORK/qc/structure_qa/qc_summary.tsv"

echo "== 7 release pack"
REL="$WORK/release/$TAG"
mkdir -p "$REL"
cp "$DRAFT_GFF" "$REL/$TAG.gff3"
cp "$PROTEINS_FA" "$REL/proteins.faa"
cp "$WORK/qc/structure_qa/qc_summary.tsv" "$REL/qc_summary.tsv"
cp "$REPO/examples/golden_pack/METHODS.stub.md" "$REL/METHODS.md"
python3 "$REPO/pipeline/check_release_pack.py" "$REL" > "$OUT/release_check.txt"
echo "[OK] $REL"

echo "== 8 compare with testdata/structure/expected/"
cut -f1-4 "$WORK/qc/structure_qa/qc_summary.tsv" > "$OUT/qc_summary.key.tsv"
(cd "$OUT" && find . -type f ! -name first_run_files.txt | LC_ALL=C sort) > "$OUT/first_run_files.txt"
status=0
for f in first_run_files.txt qc_summary.key.tsv; do
  [[ -f "$TOY/expected/$f" ]] || { echo "[ERR] missing testdata/structure/expected/$f"; exit 1; }
done
# files that must exist (extra files from optional tools, e.g. AGAT, are allowed)
missing="$(LC_ALL=C comm -23 "$TOY/expected/first_run_files.txt" "$OUT/first_run_files.txt")"
if [[ -n "$missing" ]]; then
  echo "[DIFF] missing outputs:"; echo "$missing"; status=1
fi
if ! diff -q "$TOY/expected/qc_summary.key.tsv" "$OUT/qc_summary.key.tsv" >/dev/null; then
  echo "[DIFF] qc_summary differs from testdata/structure/expected/qc_summary.key.tsv:"
  diff "$TOY/expected/qc_summary.key.tsv" "$OUT/qc_summary.key.tsv" | head -20 || true
  status=1
fi
if [[ $status == 0 ]]; then
  echo "[OK] first run finished; outputs match the expected listing. Summary: $WORK/qc/structure_qa/qc_summary.tsv"
fi
exit $status
