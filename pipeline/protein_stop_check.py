#!/usr/bin/env python3
"""Classify translated proteins by stop codons and length (used by A5e_filter_proteins.sh).

Input: spliced CDS FASTA from `gffread -x` (--cds, translated here with the standard code), or a
protein FASTA (--protein). `gffread -y` drops the final stop codon from its output, so terminal stops
can only be judged from the CDS; in protein input '*' and '.' both count as stops.
Writes one ID list per reason under --out-prefix:
  <prefix>.internal_stop.txt     stop codon before the last residue
  <prefix>.no_terminal_stop.txt  last residue is not a stop (partial / truncated CDS)
  <prefix>.short.txt             fewer than --min-aa residues (stops excluded)
  <prefix>.ids_to_remove.txt     union of the lists selected for removal
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

STOPS = "*."
_BASES = "TCAG"
_AA = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
CODON = {a + b + c: _AA[16 * i + 4 * j + k]
         for i, a in enumerate(_BASES) for j, b in enumerate(_BASES) for k, c in enumerate(_BASES)}


def translate(cds: str) -> str:
    """Standard-code translation; codons with N or other ambiguity become X, a trailing partial codon is dropped."""
    cds = cds.upper().replace("U", "T")
    return "".join(CODON.get(cds[i:i + 3], "X") for i in range(0, len(cds) - len(cds) % 3, 3))


def read_fasta(path: Path):
    name, chunks = None, []
    with path.open() as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith(">"):
                if name is not None:
                    yield name, "".join(chunks)
                name, chunks = line[1:].split()[0], []
            elif line:
                chunks.append(line.strip())
    if name is not None:
        yield name, "".join(chunks)


def classify(seq: str, min_aa: int) -> set[str]:
    """Return the set of problems for one protein sequence."""
    problems: set[str] = set()
    if not seq:
        return {"no_terminal_stop", "short"}
    body, last = seq[:-1], seq[-1]
    if any(c in STOPS for c in body):
        problems.add("internal_stop")
    if last not in STOPS:
        problems.add("no_terminal_stop")
    core = "".join(c for c in seq if c not in STOPS)
    if len(core) < min_aa:
        problems.add("short")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--cds", type=Path, help="spliced CDS FASTA (gffread -x)")
    src.add_argument("--protein", type=Path, help="protein FASTA with stops kept as '*' or '.'")
    ap.add_argument("--protein-out", type=Path, help="with --cds: also write the translated proteins here")
    ap.add_argument("--out-prefix", required=True)
    ap.add_argument("--min-aa", type=int, default=50)
    ap.add_argument("--keep-partial", action="store_true",
                    help="do not remove proteins that only lack a terminal stop")
    args = ap.parse_args(argv)

    reasons = ("internal_stop", "no_terminal_stop", "short")
    lists: dict[str, list[str]] = {r: [] for r in reasons}
    n = 0
    pout = args.protein_out.open("w") if (args.cds and args.protein_out) else None
    records = read_fasta(args.cds or args.protein)
    for name, seq in records:
        n += 1
        if args.cds:
            seq = translate(seq)
            if pout:
                pout.write(f">{name}\n{seq}\n")
        for r in classify(seq, args.min_aa):
            lists[r].append(name)
    if pout:
        pout.close()
    remove_reasons = [r for r in reasons if not (args.keep_partial and r == "no_terminal_stop")]
    remove = sorted({i for r in remove_reasons for i in lists[r]})
    for r in reasons:
        Path(f"{args.out_prefix}.{r}.txt").write_text("".join(f"{i}\n" for i in sorted(set(lists[r]))))
    Path(f"{args.out_prefix}.ids_to_remove.txt").write_text("".join(f"{i}\n" for i in remove))
    summary = " ".join(f"{r}={len(set(lists[r]))}" for r in reasons)
    print(f"[stop-check] proteins={n} {summary} remove={len(remove)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
