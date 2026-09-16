# shellcheck shell=bash
# Source from pipeline scripts after WORK_DIR / lineage are set.
# Reject example placeholders and anti-pattern lineages.
_gsa_reject_placeholder_path() {
  local label="$1" val="${2:-}"
  case "$val" in
    /path/to*|*/path/to*|"")
      echo "[ERR] $label is missing or still /path/to — edit config/local.env" >&2
      return 1
      ;;
  esac
  return 0
}
_gsa_reject_busco_lineage() {
  local val="${1:-}"
  if [[ -z "$val" ]]; then
    echo "[ERR] BUSCO_LINEAGE unset" >&2
    return 1
  fi
  case "$val" in
    YOUR_*|*YOUR_*)
      echo "[ERR] BUSCO_LINEAGE still placeholder ($val) — set a real odb lineage" >&2
      return 1
      ;;
  esac
  if [[ "$val" == eukaryota* || "$val" == *eukaryota_odb* ]]; then
    echo "[ERR] BUSCO_LINEAGE=$val looks like bare eukaryota (EVALUATION anti-pattern for clade papers)" >&2
    return 1
  fi
  return 0
}
