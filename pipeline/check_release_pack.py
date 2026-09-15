#!/usr/bin/env python3
"""Smoke-check a structure release folder has the pack files (not a full L1 judge).

Usage:
  python3 pipeline/check_release_pack.py path/to/release/TAG
Exit 0 if GFF + proteins + METHODS-like file found; else 1.
Full pass/fail: docs/EVALUATION_CHECKLIST.md
"""
from __future__ import annotations
import sys
from pathlib import Path

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_release_pack.py release/<TAG>", file=sys.stderr)
        return 2
    root = Path(sys.argv[1])
    if not root.is_dir():
        print(f"FAIL: not a directory: {root}")
        return 1
    names = {p.name.lower() for p in root.iterdir() if p.is_file()}
    gff = any(n.endswith((".gff", ".gff3")) for n in names)
    faa = any(n.endswith(".faa") for n in names) or any(
        n.endswith((".fa", ".fasta")) and ("prot" in n or "pep" in n or "protein" in n) for n in names
    )
    methods = any("method" in n or n.endswith(".md") or "readme" in n for n in names)
    print(f"release_dir={root}")
    print(f"  gff/gff3: {'OK' if gff else 'MISSING'}")
    print(f"  proteins: {'OK' if faa else 'MISSING (need *.faa or *prot*)'}")
    print(f"  METHODS/README: {'OK' if methods else 'MISSING'}")
    print("Note: pack presence only. Tick docs/EVALUATION_CHECKLIST.md for L0/L1/L2.")
    return 0 if (gff and faa and methods) else 1

if __name__ == "__main__":
    raise SystemExit(main())
