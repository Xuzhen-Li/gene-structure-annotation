#!/usr/bin/env python3
"""Rename genes to PREFIX_chrNNgXXXXXX.tXX style (S14 rename helper).

Usage: A6b_rename_gff.py PREFIX VERSION CHR_STRIP_PREFIX in.gff3 [--map ids.tsv] [--keep-unparented] > out.gff3
Example: A6b_rename_gff.py VitisVinifera 1 chr genome.gff3 --map rename_map.tsv > renamed.gff3

IDs written:
  gene        PREFIX_chrNNgXXXXXX
  transcript  <gene>.tNN       (mRNA and any other child with an ID, e.g. tRNA / ncRNA; feature type kept)
  exon        <transcript>.exonN   (numbered 5'->3')
  CDS         <transcript>.cds     (one multi-line CDS feature, as GFF3 allows)
  other       <transcript>.<type>N (UTRs, codons, …)
--map writes old_id<TAB>new_id<TAB>type for genes and transcripts (without --map the pairs go to stderr).
Features whose Parent is not in the file stop the run (exit 2) unless --keep-unparented passes them through.
"""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict

GENE_TYPES = {"gene", "ncRNA_gene", "pseudogene"}
GENE_DIGITS, TX_DIGITS = 6, 2


def parse_attrs(col9: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for part in col9.strip().rstrip(";").split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("prefix")
    ap.add_argument("version")
    ap.add_argument("chr_strip")
    ap.add_argument("gff")
    ap.add_argument("--map", help="write old_id/new_id/type TSV here")
    ap.add_argument("--keep-unparented", action="store_true",
                    help="pass through features whose Parent is missing instead of failing")
    args = ap.parse_args(argv)

    rows = []            # (cols, attrs)
    genes: dict[str, dict] = {}
    passthrough: list[str] = []
    for line in open(args.gff):
        if not line.strip() or line.startswith("#"):
            continue
        cols = line.rstrip("\n").split("\t")
        if len(cols) != 9:
            continue
        a = parse_attrs(cols[8])
        rows.append((cols, a))
        if cols[2] in GENE_TYPES and "ID" in a and "Parent" not in a:
            genes[a["ID"]] = {"cols": cols, "seq": cols[0], "start": int(cols[3]), "tx": {}}

    tx_of: dict[str, tuple[str, str]] = {}   # transcript ID -> (gene ID, transcript ID)
    for cols, a in rows:
        par = a.get("Parent")
        if par and "ID" in a and par.split(",")[0] in genes and cols[2] not in GENE_TYPES:
            gid = par.split(",")[0]
            genes[gid]["tx"][a["ID"]] = {"cols": cols, "start": int(cols[3]), "kids": []}
            tx_of[a["ID"]] = (gid, a["ID"])

    orphans: list[str] = []
    for cols, a in rows:
        if cols[2] in GENE_TYPES and "Parent" not in a:
            continue
        if "ID" in a and a.get("ID") in tx_of:
            continue
        par = a.get("Parent")
        if not par:
            passthrough.append("\t".join(cols))     # top-level non-gene feature (region, repeat, …)
            continue
        attached = False
        for p in par.split(","):
            if p in tx_of:
                gid, tid = tx_of[p]
                genes[gid]["tx"][tid]["kids"].append(cols)
                attached = True
        if not attached:
            orphans.append("\t".join(cols))

    if orphans and not args.keep_unparented:
        print(f"[ERR] {len(orphans)} features have a Parent that is not a gene/transcript in {args.gff} "
              f"(first: {orphans[0][:120]}). Fix the GFF or re-run with --keep-unparented.", file=sys.stderr)
        return 2

    mapping: list[tuple[str, str, str]] = []
    out = sys.stdout
    out.write("##gff-version 3\n")
    for line in passthrough:
        out.write(line + "\n")

    order = sorted(genes, key=lambda g: (genes[g]["seq"], genes[g]["start"]))
    seq_counts: dict[str, int] = defaultdict(int)
    for gid in order:
        g = genes[gid]
        seq = g["seq"]
        seq_counts[seq] += 1
        chrom = seq[len(args.chr_strip):] if args.chr_strip and seq.startswith(args.chr_strip) else seq
        try:
            chrom_lab = f"{int(chrom):02d}"
        except ValueError:
            chrom_lab = chrom.replace(" ", "_")
        new_gene = f"{args.prefix}_chr{chrom_lab}g{seq_counts[seq]:0{GENE_DIGITS}d}"
        gc = list(g["cols"])
        gc[8] = f"ID={new_gene};Name={new_gene};version={args.version}"
        out.write("\t".join(gc) + "\n")
        mapping.append((gid, new_gene, gc[2]))
        for i, (tid, td) in enumerate(sorted(g["tx"].items(), key=lambda x: x[1]["start"]), 1):
            new_tx = f"{new_gene}.t{i:0{TX_DIGITS}d}"
            tc = list(td["cols"])
            tc[8] = f"ID={new_tx};Parent={new_gene};Name={new_tx}"
            out.write("\t".join(tc) + "\n")
            mapping.append((tid, new_tx, tc[2]))
            minus = tc[6] == "-"
            kids = sorted(td["kids"], key=lambda c: (int(c[3]), int(c[4])), reverse=minus)
            counters: dict[str, int] = defaultdict(int)
            for kc in kids:
                kc = list(kc)
                feat = kc[2]
                if feat == "CDS":
                    kid_id = f"{new_tx}.cds"
                else:
                    counters[feat] += 1
                    kid_id = f"{new_tx}.{feat.lower()}{counters[feat]}"
                kc[8] = f"ID={kid_id};Parent={new_tx}"
                out.write("\t".join(kc) + "\n")

    if args.keep_unparented:
        for line in orphans:
            out.write(line + "\n")
        if orphans:
            print(f"[WARN] passed through {len(orphans)} unparented features unchanged", file=sys.stderr)

    print(f"# renamed with A6b_rename_gff.py prefix={args.prefix} version={args.version}", file=sys.stderr)
    if args.map:
        with open(args.map, "w") as fh:
            fh.write("old_id\tnew_id\ttype\n")
            for old, new, typ in mapping:
                fh.write(f"{old}\t{new}\t{typ}\n")
    else:
        for old, new, typ in mapping:
            if typ not in GENE_TYPES:
                print(f"{old}\t{new}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
