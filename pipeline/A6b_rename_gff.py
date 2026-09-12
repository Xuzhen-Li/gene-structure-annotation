#!/usr/bin/env python3
"""Rename genes to PREFIX_chrNNgXXXXXX.tXX style (S14 rename helper).
Usage: A6b_rename_gff.py PREFIX VERSION CHR_STRIP_PREFIX in.gff3 > out.gff3
Example: A6b_rename_gff.py VitisVinifera 1 chr genome.gff3 > renamed.gff3
"""
from __future__ import annotations
import sys
from collections import defaultdict

if len(sys.argv) != 5:
    sys.exit(__doc__)

prefix, version, chr_strip, path = sys.argv[1:5]
gene_digits, mrna_digits = 6, 2

# Collect genes ordered by seq + start
genes: dict[str, dict] = {}
order = []
for line in open(path):
    if not line.strip() or line.startswith("#"):
        continue
    seq, src, feat, start, end, score, strand, frame, attrs = line.rstrip().split("\t")
    ad = dict(p.split("=", 1) for p in attrs.rstrip(";").split(";") if "=" in p)
    if feat == "gene":
        gid = ad["ID"]
        genes[gid] = {"line": line.rstrip(), "seq": seq, "start": int(start), "mrna": {}}
        order.append(gid)
    elif feat == "mRNA":
        gid = ad["Parent"]
        genes.setdefault(gid, {"line": "", "seq": seq, "start": int(start), "mrna": {}})
        genes[gid]["mrna"][ad["ID"]] = {"line": line.rstrip(), "start": int(start), "kids": []}
    else:
        parent = ad.get("Parent", "")
        # attach to mRNA
        for g in genes.values():
            if parent in g["mrna"]:
                g["mrna"][parent]["kids"].append(line.rstrip())
                break

order.sort(key=lambda g: (genes[g]["seq"], genes[g]["start"]))
print("##gff-version 3")
print(f"# renamed with A6b_rename_gff.py prefix={prefix} version={version}", file=sys.stderr)

seq_counts: dict[str, int] = defaultdict(int)
for gid in order:
    g = genes[gid]
    seq = g["seq"]
    seq_counts[seq] += 1
    n = seq_counts[seq]
    chrom = seq
    if chrom.startswith(chr_strip):
        chrom = chrom[len(chr_strip) :]
    # keep numeric-ish chrom labels padded when possible
    try:
        chrom_lab = f"{int(chrom):02d}"
    except ValueError:
        chrom_lab = chrom.replace(" ", "_")
    new_gene = f"{prefix}_chr{chrom_lab}g{n:0{gene_digits}d}"
    # rewrite gene line
    parts = g["line"].split("\t")
    if len(parts) == 9:
        parts[8] = f"ID={new_gene};Name={new_gene};version={version}"
        print("\t".join(parts))
    mr_sorted = sorted(g["mrna"].items(), key=lambda x: x[1]["start"])
    for i, (mid, md) in enumerate(mr_sorted, 1):
        new_mrna = f"{new_gene}.t{i:0{mrna_digits}d}"
        mp = md["line"].split("\t")
        if len(mp) == 9:
            mp[8] = f"ID={new_mrna};Parent={new_gene};Name={new_mrna}"
            print("\t".join(mp))
        for kid in md["kids"]:
            kp = kid.split("\t")
            if len(kp) != 9:
                continue
            ad = dict(p.split("=", 1) for p in kp[8].rstrip(";").split(";") if "=" in p)
            feat = kp[2]
            kid_id = f"{new_mrna}:{feat}"
            kp[8] = f"ID={kid_id};Parent={new_mrna}"
            print("\t".join(kp))
        print(f"{mid}\t{new_mrna}", file=sys.stderr)
