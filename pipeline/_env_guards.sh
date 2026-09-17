# shellcheck shell=bash
# Source from pipeline scripts after WORK_DIR / lineage are set.
# Reject example placeholders and overly broad lineages.
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
# Shared odb-style lineage gate (BUSCO / Compleasm): reject empty, YOUR_*, bare eukaryota.
_gsa_reject_odb_lineage() {
  local label="$1" val="${2:-}"
  if [[ -z "$val" ]]; then
    echo "[ERR] $label unset" >&2
    return 1
  fi
  case "$val" in
    YOUR_*|*YOUR_*)
      echo "[ERR] $label still placeholder ($val) — use a clade package / lineage, not YOUR_* / bare eukaryota" >&2
      return 1
      ;;
  esac
  if [[ "$val" == eukaryota* || "$val" == *eukaryota_odb* ]]; then
    echo "[ERR] $label=$val is too broad — set a clade lineage/pack (not bare eukaryota_*)" >&2
    return 1
  fi
  return 0
}
_gsa_reject_busco_lineage() {
  _gsa_reject_odb_lineage BUSCO_LINEAGE "${1:-}"
}
_gsa_reject_compleasm_lineage() {
  _gsa_reject_odb_lineage COMPLEASM_LINEAGE "${1:-}"
}
