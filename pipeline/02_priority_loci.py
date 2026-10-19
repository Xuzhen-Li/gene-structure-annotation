#!/usr/bin/env python3
"""List low-PSAURON and boosted-family loci for manual curation (S5 round 1).

Input (-i): PSAURON output CSV (columns: description, psauron_is_protein, in-frame_score, …).
A two-column TSV (gene_id<TAB>score) is also accepted. Per-sequence scores are probabilities in [0, 1];
--threshold uses the same scale (default 0.5, PSAURON's own in-frame cutoff).
Output (-o): TSV gene_id, psauron, family, reason — lowest scores first.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

SCORE_COLUMNS = ("in-frame_score", "in_frame_score", "psauron_score", "score")
ID_COLUMNS = ("description", "gene_id", "id", "transcript_id")


def read_scores(path: Path) -> list[tuple[str, float]]:
    """Return (id, score) pairs from a PSAURON CSV or a legacy two-column TSV."""
    lines = [l for l in path.read_text().splitlines() if l.strip() and not l.startswith("#")]
    if not lines:
        return []
    delim = "," if lines[0].count(",") >= lines[0].count("\t") else "\t"
    rows = list(csv.reader(lines, delimiter=delim))
    header = [h.strip() for h in rows[0]]
    low = [h.lower() for h in header]
    has_header = any(h in low for h in SCORE_COLUMNS + ID_COLUMNS)
    if has_header:
        id_i = next((low.index(c) for c in ID_COLUMNS if c in low), 0)
        sc_i = next((low.index(c) for c in SCORE_COLUMNS if c in low), None)
        if sc_i is None:
            raise SystemExit(f"[ERR] no score column in {path} (expected one of {', '.join(SCORE_COLUMNS)})")
        body = rows[1:]
    else:
        id_i, sc_i, body = 0, 1, rows
    out = []
    for r in body:
        if len(r) <= max(id_i, sc_i):
            continue
        try:
            score = float(r[sc_i])
        except ValueError:
            continue
        gid = r[id_i].strip().split()[0] if r[id_i].strip() else ""
        if gid:
            out.append((gid, score))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-i", "--psauron", type=Path, required=True, help="PSAURON CSV")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--threshold", type=float, default=0.5,
                    help="flag in-frame score < this; scale 0-1 (default 0.5)")
    ap.add_argument("--families", type=Path, help="optional gene_id\\tfamily TSV")
    ap.add_argument("--boost-families", default="NLR,stilbene,RGA,NBS",
                    help="comma families always listed")
    args = ap.parse_args(argv)

    if not 0.0 <= args.threshold <= 1.0:
        ap.error(f"--threshold {args.threshold} is outside 0-1; PSAURON per-sequence scores are probabilities")

    boost = {x.strip() for x in args.boost_families.split(",") if x.strip()}
    fam_of: dict[str, str] = {}
    if args.families and args.families.exists():
        for line in args.families.read_text().splitlines():
            if not line.strip() or line.startswith("#"):
                continue
            gid, fam = line.split("\t", 1)
            fam_of[gid.strip()] = fam.strip()

    scores = read_scores(args.psauron)
    if scores and max(s for _, s in scores) > 1.0:
        print(f"[ERR] scores above 1 in {args.psauron}: expected per-sequence probabilities (0-1)", file=sys.stderr)
        return 2

    rows: list[tuple[float, str, str, str]] = []
    for gid, score in scores:
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
    print(f"wrote {len(rows)} priority loci (of {len(scores)} scored) -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
