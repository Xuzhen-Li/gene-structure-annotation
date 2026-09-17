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
# Shared lineage gate: reject empty, YOUR_*, bare eukaryota. Compleasm adds *_odb* ban below.
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
  # Compleasm wants short clade packs (eudicots|poales|…), not BUSCO *_odb* names.
  local val="${1:-}"
  _gsa_reject_odb_lineage COMPLEASM_LINEAGE "$val" || return 1
  if [[ "$val" == *_odb* || "$val" == *_odb ]]; then
    echo "[ERR] COMPLEASM_LINEAGE=$val looks like a BUSCO *_odb* name — use a Compleasm clade pack (e.g. eudicots|poales), not BUSCO lineage strings" >&2
    return 1
  fi
  return 0
}
