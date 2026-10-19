#!/usr/bin/env python3
"""Keep one protein per gene: the longest isoform, grouped by the GFF Parent (or GTF gene_id).

Isoforms with an internal stop codon are chosen only when a gene has no other isoform.
Usage: longest_isoform.py --gff genes.gff3 --proteins all_transcripts.faa --out proteins.faa
Output headers: >GENE_ID transcript=TRANSCRIPT_ID length=N (stop codons are not counted).
Transcripts that are missing from the GFF are reported and kept under their own ID.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TX_FEATURES = {"mRNA", "transcript"}
GTF_ATTR = re.compile(r'(\S+)\s+"([^"]*)"')


def parse_attrs(col9: str) -> dict[str, str]:
    col9 = col9.strip()
    if "=" in col9.split(";", 1)[0]:
        out = {}
        for part in col9.rstrip(";").split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                out[k.strip()] = v.strip()
        return out
    return {k: v for k, v in GTF_ATTR.findall(col9)}


def transcript_to_gene(gff: Path) -> dict[str, str]:
    tx_gene: dict[str, str] = {}
    with gff.open() as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            p = line.rstrip("\n").split("\t")
            if len(p) < 9:
                continue
            a = parse_attrs(p[8])
            if p[2] in TX_FEATURES:
                tid = a.get("ID") or a.get("transcript_id")
                gid = a.get("Parent") or a.get("gene_id")
                if tid and gid:
                    tx_gene[tid] = gid.split(",")[0]
            elif "transcript_id" in a and "gene_id" in a:
                tx_gene.setdefault(a["transcript_id"], a["gene_id"])
    return tx_gene


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


def has_internal_stop(seq: str) -> bool:
    core = seq.rstrip("*.")
    return "*" in core or "." in core


def pick_longest(tx_gene: dict[str, str], proteins) -> tuple[dict[str, tuple[int, str, str]], list[str]]:
    """Per gene, keep the longest isoform among those without an internal stop codon
    (isoforms with internal stops are used only when a gene has nothing else)."""
    best: dict[str, tuple[int, str, str]] = {}
    rank: dict[str, tuple] = {}
    unmapped: list[str] = []
    for tid, seq in proteins:
        gid = tx_gene.get(tid)
        if gid is None:
            unmapped.append(tid)
            gid = tid
        length = len(seq.rstrip("*."))
        # higher (clean ORF, length) wins; on a tie the lexicographically smaller transcript ID wins
        key = (not has_internal_stop(seq), length)
        if gid not in rank or key > rank[gid] or (key == rank[gid] and tid < best[gid][1]):
            rank[gid] = key
            best[gid] = (length, tid, seq)
    return best, unmapped


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--gff", type=Path, required=True)
    ap.add_argument("--proteins", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args(argv)

    tx_gene = transcript_to_gene(args.gff)
    best, unmapped = pick_longest(tx_gene, read_fasta(args.proteins))
    if unmapped:
        print(f"[WARN] {len(unmapped)} transcripts not found in {args.gff}; kept under their own ID "
              f"(first: {unmapped[0]})", file=sys.stderr)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w") as out:
        for gid in sorted(best):
            length, tid, seq = best[gid]
            out.write(f">{gid} transcript={tid} length={length}\n")
            for i in range(0, len(seq), 80):
                out.write(seq[i:i + 80] + "\n")
    print(f"wrote {len(best)} representative proteins (longest isoform per gene) -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
