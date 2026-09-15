#!/usr/bin/env python3
"""Print recommended structure QC commands (print-first; does not run tools).

Maps to docs/EVALUATION_CHECKLIST.md / docs/QUALITY_SOURCES.md.

Usage:
  set -a && source config/local.env && set +a
  python3 pipeline/print_qc_commands.py
  python3 pipeline/print_qc_commands.py --env config/example.env
  python3 pipeline/print_qc_commands.py --grade L2   # include OMArk block as required
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
        # expand $VAR from already-seen keys / environ
        def repl(m: re.Match[str]) -> str:
            name = m.group(1) or m.group(2)
            return env.get(name, os.environ.get(name, m.group(0)))

        v = re.sub(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}|\$([A-Za-z_][A-Za-z0-9_]*)", repl, v)
        env[k] = v
    return env


def g(env: dict[str, str], key: str, default: str = "/path/to/…") -> str:
    v = env.get(key, "").strip()
    return v if v else default


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--env", type=Path, default=None, help="optional .env to read (else use shell env)")
    ap.add_argument("--grade", choices=["L0", "L1", "L2"], default="L1")
    args = ap.parse_args()

    env = load_env(args.env)
    work = g(env, "WORK_DIR", "$WORK_DIR")
    proteins = g(env, "PROTEINS_FA", "$PROTEINS_FA")
    gff = g(env, "CURATED_GFF", "") or g(env, "MERGED_GFF", "") or g(env, "DRAFT_GFF", "$MERGED_GFF")
    lineage = g(env, "BUSCO_LINEAGE", "viridiplantae_odb12")
    busco_out = g(env, "BUSCO_OUT", f"{work}/busco_prot")
    psauron = g(env, "PSAURON_TSV", f"{work}/psauron.tsv")
    agat = g(env, "AGAT_OUT", f"{work}/agat")
    omark = g(env, "OMARK_OUT", f"{work}/qc/omark")
    omamer = g(env, "OMAMER_DB", "$OMAMER_DB")
    compleasm_l = g(env, "COMPLEASM_LINEAGE", "eudicots")
    threads = g(env, "THREADS", "16")
    tag = g(env, "RELEASE_TAG", "release_tag")
    release = f"{work}/release/{tag}"
    rna = g(env, "RNA_BAM", "")
    ref_gff = g(env, "REF_GFF", "")

    print("# Structure QC — print-first (commands are suggestions)")
    print(f"# Target grade: {args.grade}  ·  checklist: docs/EVALUATION_CHECKLIST.md")
    print(f"# Sources: docs/QUALITY_SOURCES.md")
    print("# Does NOT install tools or run BRAKER. Review then paste on your cluster.")
    print()

    print("## 0) Pack smoke (files present?)")
    print(f"python3 pipeline/check_release_pack.py {release}")
    print()

    print("## G4 — AGAT / counts  (hard)")
    print(f"# uses pipeline/A5_agat_stats.sh")
    print(f'export WORK_DIR="{work}" AGAT_OUT="{agat}" MERGED_GFF="{gff}"')
    print("bash pipeline/A5_agat_stats.sh")
    print()

    print("## G5 — proteins from this GFF  (hard; regenerate if stale)")
    print("# see pipeline/A3_proteins_from_gff.sh")
    print(f'export WORK_DIR="{work}" PROTEINS_FA="{proteins}"')
    print(f"# gffread {gff} -g $GENOME_FA -y {proteins}")
    print()

    print("## G6 + G7 — BUSCO + PSAURON  (hard)")
    print(f'export WORK_DIR="{work}" PROTEINS_FA="{proteins}" \\')
    print(f'  BUSCO_LINEAGE="{lineage}" BUSCO_OUT="{busco_out}" \\')
    print(f'  PSAURON_TSV="{psauron}" THREADS="{threads}"')
    print("bash pipeline/01_qc_busco_psauron.sh")
    print("# then build / refresh PRIORITY_TSV — pipeline/02_priority_loci.py")
    print()

    print("## OMArk + Compleasm  (OMArk required at L2; Compleasm soft)")
    if args.grade == "L2":
        print("# L2: OMArk is required before claiming S5/L2")
    else:
        print("# L1: OMArk optional-but-recommended for plant/T2T; Compleasm soft cross-check")
    print(f'export WORK_DIR="{work}" PROTEINS_FA="{proteins}" \\')
    print(f'  OMARK_OUT="{omark}" OMAMER_DB="{omamer}" \\')
    print(f'  COMPLEASM_LINEAGE="{compleasm_l}" THREADS="{threads}" RUN=0')
    print("bash pipeline/A5b_omark_compleasm.sh   # print-first; RUN=1 to execute")
    print()

    print("## Soft — gffcompare (if you have a second draft or REF_GFF)")
    if ref_gff and not ref_gff.startswith("/path/"):
        print(f"gffcompare -r {ref_gff} -o {work}/qc/gffcompare {gff}")
    else:
        print(f"# gffcompare -r $REF_GFF -o {work}/qc/gffcompare {gff}")
        print("# or: gffcompare -r $DRAFT_GFF_B -o ... $MERGED_GFF")
    print()

    print("## Soft — RNA support (if RNA_BAM set; AnnoAudit-style idea)")
    if rna and not rna.startswith("/path/"):
        print(f"# You have RNA_BAM={rna}")
        print("# Option A: run ERGA AnnoAudit (Nextflow) with --genome_bam")
        print("#   https://github.com/ERGA-consortium/AnnoAudit")
        print("# Option B: featureCounts / custom exon coverage → METHODS %")
    else:
        print("# No RNA_BAM in env — skip or set RNA_BAM / use AnnoAudit with reads")
    print()

    print("## Soft — optional one-stop wrappers (still tick EVALUATION_CHECKLIST)")
    print("# GAQET2:  https://github.com/victorgcb1987/GAQET2")
    print("# AnnoAudit: https://github.com/ERGA-consortium/AnnoAudit")
    print("# atol-qc-annotation: https://github.com/TomHarrop/atol-qc-annotation")
    print("# Do not treat wrapper exit 0 as L1 — tick gates G1–G8 yourself.")
    print()

    print("## Finish")
    print("# Tick docs/zh/验收勾选表.md or docs/EVALUATION_CHECKLIST.md")
    print(f"# METHODS: status={args.grade}; BUSCO lineage={lineage}; TE trusted lib + sha256; stop rule…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
