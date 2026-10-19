#!/usr/bin/env bash
# Build a representative protein FASTA from draft (or curated) GFF for BUSCO/PSAURON.
# Produces: PROTEINS_FA (representative translations for BUSCO / FA).
# See: docs/STAGE_IO.md · docs/QUICKSTART.md
set -euo pipefail

# Print-first: default DRY. Export RUN=1 to execute on the cluster.
if [[ "${RUN:-0}" != "1" ]]; then
  echo "[DRY] A3_proteins_from_gff.sh: not executing. Review script, then: RUN=1 bash pipeline/A3_proteins_from_gff.sh"
  exit 0
fi

# Gene models: an existing MERGED_GFF (after A4) wins over DRAFT_GFF; pass a path as $1 to override.
: "${GENOME_FA:?unmasked or soft-masked genome OK for gffread CDS}"
: "${PROTEINS_FA:?}"
# shellcheck source=pipeline/_env_guards.sh
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_env_guards.sh"
IN_GFF="${1:-$(_gsa_pick_gff)}" || exit 1
_gsa_reject_placeholder_path GENOME_FA "$GENOME_FA" || exit 1
_gsa_reject_placeholder_path PROTEINS_FA "$PROTEINS_FA" || exit 1
_gsa_reject_placeholder_path GFF "$IN_GFF" || exit 1
WORK_DIR="${WORK_DIR:-$(dirname "$PROTEINS_FA")}"
_gsa_reject_placeholder_path WORK_DIR "$WORK_DIR" || exit 1
if [[ ! -f "$IN_GFF" ]]; then
  echo "[ERR] GFF not found: $IN_GFF" >&2
  exit 1
fi
mkdir -p "$(dirname "$PROTEINS_FA")"
echo "[INFO] A3 gene models: $IN_GFF"

if ! command -v gffread >/dev/null; then
  echo "need gffread (cufflinks / bioconda gffread)"; exit 1
fi

# CDS → protein for every transcript ('*' = stop); -J drops incomplete CDS if you want a stricter set
gffread "$IN_GFF" -g "$GENOME_FA" -y "$PROTEINS_FA.raw.faa" -S

# One protein per gene: longest isoform, grouped by the GFF Parent / GTF gene_id
python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/longest_isoform.py" \
  --gff "$IN_GFF" --proteins "$PROTEINS_FA.raw.faa" --out "$PROTEINS_FA"

echo "[OK] $PROTEINS_FA"
