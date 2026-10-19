#!/usr/bin/env python3
"""Run all structure QA steps (qa01-qa10) in order and write qc_summary.tsv.

Required: --gff (consensus GFF3 from the merge step), --genome, --out
Optional: --proteins, --evidence NAME=PATH (repeatable), --bam or --junctions,
          --te, --config, --strict
External tools (busco, omamer/omark, gffcompare) run only with RUN=1;
results already present under --out are reused.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import qa01_longest_isoform as s01  # noqa: E402
import qa02_busco as s02  # noqa: E402
import qa03_omark as s03  # noqa: E402
import qa04_evidence_aed as s04  # noqa: E402
import qa05_rnaseq_junctions as s05  # noqa: E402
import qa06_gene_stats as s06  # noqa: E402
import qa07_internal_stops as s07  # noqa: E402
import qa08_te_overlap as s08  # noqa: E402
import qa09_splice_sites as s09  # noqa: E402
import qa10_summary as s10  # noqa: E402


def check_path(label, value, required=False):
    if value is None:
        if required:
            sys.exit(f"[ERR] {label} is required")
        return
    if "/path/to" in value:
        sys.exit(f"[ERR] {label} is still a /path/to placeholder: {value}")
    if not Path(value).is_file():
        sys.exit(f"[ERR] {label} not found: {value}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--gff", required=True)
    ap.add_argument("--genome", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--proteins")
    ap.add_argument("--evidence", action="append", metavar="NAME=PATH")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--bam")
    g.add_argument("--junctions")
    ap.add_argument("--te")
    ap.add_argument("--config")
    ap.add_argument("--strict", action="store_true", help="exit 1 when any metric is WARN")
    a = ap.parse_args(argv)
    evidence = s04.parse_evidence(a.evidence)
    for label, val, req in (("--gff", a.gff, True), ("--genome", a.genome, True),
                            ("--proteins", a.proteins, False), ("--bam", a.bam, False),
                            ("--junctions", a.junctions, False), ("--te", a.te, False),
                            ("--config", a.config, False)):
        check_path(label, val, req)
    for name, path in evidence.items():
        check_path(f"--evidence {name}", path, True)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    metrics_dir = out / "metrics"
    if metrics_dir.is_dir():
        for old in metrics_dir.glob("qa*.tsv"):
            old.unlink()
    print("[qa01] longest isoform per gene")
    faa = s01.run(a.gff, out, a.proteins, a.genome)
    print("[qa02] BUSCO")
    s02.run(out, faa, a.genome, a.config)
    print("[qa03] OMArk")
    s03.run(out, faa, a.config)
    print("[qa04] evidence agreement and AED")
    s04.run(a.gff, out, evidence, a.config)
    print("[qa05] RNA-seq junctions")
    s05.run(a.gff, out, a.bam, a.junctions, a.config)
    print("[qa06] gene statistics")
    s06.run(a.gff, out, a.config)
    print("[qa07] internal stop codons")
    s07.run(a.gff, out, a.genome, a.proteins, a.config)
    print("[qa08] TE overlap")
    s08.run(a.gff, out, a.te, a.config)
    print("[qa09] splice sites")
    s09.run(a.gff, out, a.genome, a.config)
    print("[qa10] summary")
    return s10.run(out, a.config, a.strict)


if __name__ == "__main__":
    sys.exit(main())
