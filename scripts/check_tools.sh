#!/usr/bin/env bash
# Print the version of every tool used by this repo, or "missing".
# Usage: bash scripts/check_tools.sh [--strict]
#   --strict  exit 1 when a required tool is missing (default: always exit 0)
# Required for the first run (scripts/first_run.sh): python3, bash, awk.
# BRAKER is checked through the container in BRAKER_SIF (apptainer or singularity).
set -uo pipefail
STRICT=0
[[ "${1:-}" == "--strict" ]] && STRICT=1

missing_required=0

ver() {  # ver <label> <required:0|1> <cmd...>
  local label="$1" req="$2"; shift 2
  if ! command -v "$1" >/dev/null 2>&1; then
    printf '%-14s %s\n' "$label" "missing$([[ $req == 1 ]] && echo ' (required)')"
    [[ $req == 1 ]] && missing_required=1
    return
  fi
  local out
  out="$("$@" 2>&1 | grep -m1 -E '[0-9]+\.[0-9]+' || true)"
  printf '%-14s %s\n' "$label" "${out:-found at $(command -v "$1") (version not printed)}"
}

echo "== required for scripts/first_run.sh"
ver python3      1 python3 --version
ver bash         1 bash --version
ver awk          1 awk --version
echo "== envs/structure.yml"
ver samtools     0 samtools --version
ver gffread      0 gffread --version
ver gffcompare   0 gffcompare --version
ver agat         0 agat --version
ver hisat2       0 hisat2 --version
ver stringtie    0 stringtie --version
ver miniprot     0 miniprot --version
ver liftoff      0 liftoff --version
ver busco        0 busco --version
ver psauron      0 psauron --version
echo "== envs/structure-proteome-qc.yml"
ver omamer       0 omamer --version
ver omark        0 omark --version
ver compleasm    0 compleasm --version
echo "== envs/structure-repeats.yml"
ver RepeatMasker 0 RepeatMasker -v
ver RepeatModeler 0 RepeatModeler -version
echo "== BRAKER (container)"
RUNNER="$(command -v apptainer || command -v singularity || true)"
if [[ -n "${BRAKER_SIF:-}" && -f "${BRAKER_SIF}" && -n "$RUNNER" ]]; then
  printf '%-14s %s\n' braker.pl "$("$RUNNER" exec "$BRAKER_SIF" braker.pl --version 2>&1 | grep -m1 -E '[0-9]+\.[0-9]+' || echo 'version not printed')"
else
  printf '%-14s %s\n' braker.pl "not checked: set BRAKER_SIF and install apptainer/singularity"
fi

if [[ $STRICT == 1 && $missing_required == 1 ]]; then
  exit 1
fi
exit 0
