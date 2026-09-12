#!/usr/bin/env python3
"""Build a triage list for GSAman: low PSAURON first.

Optional: merge a gene-family table (TSV: gene_id\\tfamily) to boost
NLR / pathway / QTL targets for your species even when scores look OK.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-i", "--psauron", type=Path, required=True, help="PSAURON TSV")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--threshold", type=float, default=90.0, help="flag score < this")
    ap.add_argument("--families", type=Path, help="optional gene_id\\tfamily TSV")
    ap.add_argument("--boost-families", default="NLR,stilbene,RGA,NBS",
                    help="comma families always listed")
    args = ap.parse_args()

    boost = {x.strip() for x in args.boost_families.split(",") if x.strip()}
    fam_of: dict[str, str] = {}
    if args.families and args.families.exists():
        for line in args.families.read_text().splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            gid, fam = line.split("\t", 1)
            fam_of[gid.strip()] = fam.strip()

    rows: list[tuple[float, str, str, str]] = []
    for line in args.psauron.read_text().splitlines():
        if not line.strip() or line.startswith("#") or line.lower().startswith("gene"):
            continue
        parts = line.split("\t")
        if len(parts) < 2:
            continue
        gid, score_s = parts[0].strip(), parts[1].strip()
        try:
            score = float(score_s)
        except ValueError:
            continue
        fam = fam_of.get(gid, "")
        reason = []
        if score < args.threshold:
            reason.append(f"psauron<{args.threshold}")
        if fam and any(b.lower() in fam.lower() for b in boost):
            reason.append(f"family:{fam}")
        if reason:
            rows.append((score, gid, fam, ";".join(reason)))

    rows.sort(key=lambda x: x[0])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as fh:
        fh.write("gene_id\tpsauron\tfamily\treason\n")
        for score, gid, fam, reason in rows:
            fh.write(f"{gid}\t{score}\t{fam}\t{reason}\n")
    print(f"wrote {len(rows)} priority loci -> {args.out}")


if __name__ == "__main__":
    main()
