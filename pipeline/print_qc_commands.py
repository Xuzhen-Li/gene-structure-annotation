#!/usr/bin/env python3
"""Print recommended structure QC commands (print-first; does not run tools).

Maps to docs/EVALUATION_CHECKLIST.md / docs/QUALITY_SOURCES.md.

Usage:
  set -a && source config/local.env && set +a
  python3 pipeline/print_qc_commands.py
  python3 pipeline/print_qc_commands.py --env config/example.env
  python3 pipeline/print_qc_commands.py --grade L2
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


def load_env(path: Path | None) -> dict[str, str]:
    env = dict(os.environ)
    if path is None:
        return env
    if not path.is_file():
        print(f"[WARN] env file not found: {path}", file=sys.stderr)
        return env
    for line in path.read_text().splitlines():
        s = line.split("#", 1)[0].strip()
        if not s or "=" not in s:
            continue
        k, v = s.split("=", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")

        def repl(m: re.Match[str]) -> str:
            name = m.group(1) or m.group(2)
            return env.get(name, os.environ.get(name, m.group(0)))

        v = re.sub(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)", repl, v)
        env[k] = v
    return env


def g(env: dict[str, str], key: str, default: str = "") -> str:
    v = env.get(key, "").strip()
    return v if v else default


def is_placeholder(v: str) -> bool:
    if not v:
        return True
    low = v.lower()
    if "/path/to" in low or v.startswith("/path/"):
        return True
    if "your_" in low or "YOUR_" in v:
        return True
    if "…" in v or "..." == v:
        return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--env", type=Path, default=None)
    ap.add_argument("--grade", choices=["L0", "L1", "L2"], default="L1")
    args = ap.parse_args()

    env = load_env(args.env)
    work = g(env, "WORK_DIR", "$WORK_DIR")
    proteins = g(env, "PROTEINS_FA", "$PROTEINS_FA")
    gff = g(env, "CURATED_GFF", "") or g(env, "MERGED_GFF", "") or g(env, "DRAFT_GFF", "$MERGED_GFF")
    lineage = g(env, "BUSCO_LINEAGE", "")
    busco_out = g(env, "BUSCO_OUT", f"{work}/busco_prot" if work else "$BUSCO_OUT")
    psauron = g(env, "PSAURON_TSV", f"{work}/psauron.tsv" if work else "$PSAURON_TSV")
    agat = g(env, "AGAT_OUT", f"{work}/agat" if work else "$AGAT_OUT")
    omark = g(env, "OMARK_OUT", f"{work}/qc/omark" if work else "$OMARK_OUT")
    omamer = g(env, "OMAMER_DB", "$OMAMER_DB")
    compleasm_l = g(env, "COMPLEASM_LINEAGE", "")
    threads = g(env, "THREADS", "16")
    tag = g(env, "RELEASE_TAG", "release_tag")
    release = f"{work}/release/{tag}" if work and not work.startswith("$") else f"$WORK_DIR/release/{tag}"
    rna = g(env, "RNA_BAM", "")
    ref_gff = g(env, "REF_GFF", "")

    bad = []
    for label, val in [
        ("WORK_DIR", work),
        ("PROTEINS_FA", proteins),
        ("BUSCO_LINEAGE", lineage),
        ("GFF", gff),
    ]:
        if is_placeholder(val) or val.startswith("$"):
            bad.append(f"{label}={val or '(empty)'}")
    if lineage and re.search(r"(?i)eukaryota", lineage) and "YOUR_" not in lineage:
        # bare eukaryota_* is too broad for pasteable G6 — treat as STOP
        bad.append(f"BUSCO_LINEAGE={lineage} (too broad — set a clade lineage, e.g. viridiplantae_odb12)")
    # Compleasm: STOP on YOUR_*/bare eukaryota/BUSCO-style *_odb* names
    if compleasm_l:
        if is_placeholder(compleasm_l) or compleasm_l.startswith("$"):
            bad.append(f"COMPLEASM_LINEAGE={compleasm_l or '(empty)'}")
        elif re.search(r"(?i)eukaryota", compleasm_l):
            bad.append(
                f"COMPLEASM_LINEAGE={compleasm_l} (too broad — Compleasm clade pack, e.g. eudicots|poales)"
            )
        elif re.search(r"(?i)_odb\d*$", compleasm_l) or "_odb" in compleasm_l.lower():
            bad.append(
                f"COMPLEASM_LINEAGE={compleasm_l} (BUSCO *_odb* name — use Compleasm pack, e.g. eudicots|poales)"
            )

    print("# Structure QC — print-first (commands are suggestions)")
    print(f"# Target grade: {args.grade}  ·  checklist: docs/EVALUATION_CHECKLIST.md")
    print("# Does NOT install tools or run BRAKER. Review then paste on your cluster.")
    print("# Bare `bash pipeline/01_…` without RUN=1 only prints [DRY] — it does NOT run BUSCO.")
    print()

    if bad:
        print("# [STOP] Placeholders / unset keys — do NOT paste RUN=1 blocks yet:")
        for b in bad:
            print(f"#   - {b}")
        print("# Edit config/local.env (real paths + clade lineages), then re-run this printer.")
        print("# BUSCO_LINEAGE examples: viridiplantae_odb12 | poales_odb10 | metazoa_odb10 (always *_odb*)")
        print("# COMPLEASM_LINEAGE examples: eudicots | poales | viridiplantae — not BUSCO *_odb* names")
        print("# Never leave YOUR_* / bare eukaryota for either.")
        print()
        print("## Reminders only (no executable G4–G6 until env is real)")
        print("# G1 ASSEMBLY_OK=yes after Asm1; G2 trusted TE soft-mask; G3 named draft + versions")
        print(f"# Would-be release smoke: python3 pipeline/check_release_pack.py {release}")
        print("# exit 1: fix local.env and re-run print_qc (not a RUN=1 plan)")
        return 1

    print("## Reminders G1–G3 (tick before trusting later QC)")
    print("# G1 ASSEMBLY_OK=yes only after Asm1; document source if genome was handed to you.")
    print("# G2 Soft-mask honesty: GENOME_SOFT is -xsmall; TRUSTED_TE_LIB + sha256 in METHODS")
    print("# G3 Named draft path + tool versions in METHODS")
    print()

    print("## 0) Pack smoke (files present?)")
    print(f"python3 pipeline/check_release_pack.py {release}")
    print()

    print("## G4 — AGAT / counts  (hard)")
    print(f'export WORK_DIR="{work}" AGAT_OUT="{agat}" MERGED_GFF="{gff}"')
    print("RUN=1 bash pipeline/A5_agat_stats.sh  # without RUN=1 = DRY only")
    print()

    print("## G5 — proteins from this GFF  (hard)")
    print(f'export WORK_DIR="{work}" PROTEINS_FA="{proteins}" MERGED_GFF="{gff}" DRAFT_GFF="{gff}"')
    print("RUN=1 bash pipeline/A3_proteins_from_gff.sh")
    print()

    print("## G6 + G7 — BUSCO + PSAURON  (hard)")
    print(f'export WORK_DIR="{work}" PROTEINS_FA="{proteins}" \\')
    print(f'  BUSCO_LINEAGE="{lineage}" BUSCO_OUT="{busco_out}" \\')
    print(f'  PSAURON_TSV="{psauron}" THREADS="{threads}"')
    print("RUN=1 bash pipeline/01_qc_busco_psauron.sh")
    print()

    print("## OMArk + Compleasm  (OMArk required at L2; Compleasm soft)")
    compleasm_bad = (
        (not compleasm_l)
        or is_placeholder(compleasm_l)
        or compleasm_l.startswith("$")
        or bool(re.search(r"(?i)eukaryota", compleasm_l))
        or ("_odb" in compleasm_l.lower())
    )
    if is_placeholder(omamer) or compleasm_bad:
        print("# [STOP OMArk block] set OMAMER_DB + COMPLEASM_LINEAGE (clade pack e.g. eudicots|poales — not YOUR_*/bare eukaryota/BUSCO *_odb*) before RUN=1")
        print(f"# export … COMPLEASM_LINEAGE=… OMAMER_DB=…")
        print("# RUN=1 bash pipeline/A5b_omark_compleasm.sh")
    else:
        print(f'export WORK_DIR="{work}" PROTEINS_FA="{proteins}" \\')
        print(f'  OMARK_OUT="{omark}" OMAMER_DB="{omamer}" \\')
        print(f'  COMPLEASM_LINEAGE="{compleasm_l}" THREADS="{threads}"')
        print("RUN=1 bash pipeline/A5b_omark_compleasm.sh")
    print()

    print("## Soft — gffcompare / RNA (optional)")
    if ref_gff and not is_placeholder(ref_gff):
        print(f"gffcompare -r {ref_gff} -o {work}/qc/gffcompare {gff}")
    else:
        print("# gffcompare -r $REF_GFF -o $WORK_DIR/qc/gffcompare $MERGED_GFF")
    if rna and not is_placeholder(rna):
        print(f"# RNA_BAM={rna} — AnnoAudit or featureCounts → METHODS")
    else:
        print("# No real RNA_BAM — skip soft RNA support")
    print()
    print("## Finish — tick EVALUATION_CHECKLIST; bare bash without RUN=1 ≠ QC done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
