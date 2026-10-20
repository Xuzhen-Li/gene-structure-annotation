"""Shared helpers for the test mocks (not a real tool). Standard library only."""
from __future__ import annotations

import os
import re
import sys

GTF_ATTR = re.compile(r'(\S+)\s+"([^"]*)"')


def log(tool: str, argv) -> None:
    path = os.environ.get("MOCK_LOG")
    if path:
        with open(path, "a") as fh:
            fh.write(tool + "\t" + "\t".join(argv) + "\n")


def attrs(col9: str) -> dict:
    if GTF_ATTR.search(col9) and "=" not in col9.split(";")[0]:
        return dict(GTF_ATTR.findall(col9))
    out = {}
    for p in col9.strip().strip(";").split(";"):
        if "=" in p:
            k, v = p.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def rows(path: str):
    with open(path) as fh:
        for line in fh:
            if line.strip() and not line.startswith("#"):
                f = line.rstrip("\n").split("\t")
                if len(f) == 9:
                    yield f


def opt(argv, *names, default=None):
    for i, a in enumerate(argv):
        if a in names and i + 1 < len(argv):
            return argv[i + 1]
    return default


def die(msg: str) -> None:
    sys.stderr.write(f"[mock] {msg}\n")
    sys.exit(1)


def clusters(models):
    """models: list of (seqid, strand, lo, hi, key). Group overlapping same-strand spans."""
    out = []
    for m in sorted(models, key=lambda x: (x[0], x[1], x[2])):
        if out and out[-1][-1][0] == m[0] and out[-1][-1][1] == m[1] and m[2] <= max(x[3] for x in out[-1]):
            out[-1].append(m)
        else:
            out.append([m])
    return out
