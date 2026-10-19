#!/usr/bin/env python3
"""List low-PSAURON and boosted-family loci for manual curation (S5 round 1).

Input (-i): PSAURON output CSV (preamble lines, then columns description, psauron_is_protein, in-frame_score /
in_frame_score, …).
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


def _split(line: str) -> list[str]:
    delim = "," if line.count(",") >= line.count("\t") else "\t"
    return [c.strip() for c in next(csv.reader([line], delimiter=delim))]


def read_scores(path: Path) -> list[tuple[str, float]]:
    """Return (id, score) pairs from a PSAURON CSV or a legacy two-column TSV.

    PSAURON (v1.1.x) writes a preamble before the CSV header: the command line, "psauron score: X",
    and in CDS mode a "NOTE: …" line. Lines are skipped until a header row naming an ID column and a
    score column; files without such a header are read as two columns (id, score).
    """
    lines = [l for l in path.read_text().splitlines() if l.strip() and not l.startswith("#")]
    header_at = None
    for n, line in enumerate(lines):
        low = [c.lower() for c in _split(line)]
        if any(c in low for c in ID_COLUMNS) and any(c in low for c in SCORE_COLUMNS):
            header_at = n
            break
    if header_at is not None:
        low = [c.lower() for c in _split(lines[header_at])]
        id_i = next(low.index(c) for c in ID_COLUMNS if c in low)
        sc_i = next(low.index(c) for c in SCORE_COLUMNS if c in low)
        body = lines[header_at + 1:]
    else:
        id_i, sc_i, body = 0, 1, lines
    out = []
    for line in body:
        r = _split(line)
        if len(r) <= max(id_i, sc_i):
            continue
        try:
            score = float(r[sc_i])
        except ValueError:
            continue
        gid = r[id_i].split()[0] if r[id_i] else ""
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
    if not scores and args.psauron.read_text().strip():
        print(f"[ERR] {args.psauron} is not empty but no (id, score) rows were parsed — expected a PSAURON CSV "
              f"with a header naming one of {', '.join(ID_COLUMNS)} and one of {', '.join(SCORE_COLUMNS)}",
              file=sys.stderr)
        return 3
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
