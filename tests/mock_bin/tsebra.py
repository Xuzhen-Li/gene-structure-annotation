#!/usr/bin/env python3
"""MOCK tsebra.py for tests: union of the -g gene sets, transcripts with an identical
CDS chain kept once (no hint scoring). Checks -g/-e/-c inputs exist; writes -o GTF."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _mocklib import attrs, die, log, opt  # noqa: E402

argv = sys.argv[1:]
log("tsebra.py", argv)
gtfs, hints, cfg, out = (opt(argv, "-g", "--gtf"), opt(argv, "-e", "--hintfiles"),
                         opt(argv, "-c", "--cfg"), opt(argv, "-o", "--out"))
if not (gtfs and hints and cfg and out):
    die("usage: tsebra.py -g a.gtf,b.gtf -e h1.gff,h2.gff -c default.cfg -o out.gtf")
for p in gtfs.split(",") + hints.split(",") + [cfg]:
    if not os.path.isfile(p):
        die(f"{p}: not found")

seen, keep = set(), []
for p in gtfs.split(","):
    tx = {}
    for line in open(p):
        if line.startswith("#") or not line.strip():
            continue
        f = line.rstrip("\n").split("\t")
        tid = attrs(f[8]).get("transcript_id")
        if tid:
            tx.setdefault(tid, []).append(f)
    for tid, fs in tx.items():
        chain = tuple(sorted((f[0], f[6], f[3], f[4]) for f in fs if f[2] == "CDS"))
        if chain in seen:
            continue
        seen.add(chain)
        keep.extend("\t".join(f) for f in fs)
with open(out, "w") as fh:
    fh.write("# MOCK TSEBRA output (tests only)\n" + "\n".join(keep) + "\n")
