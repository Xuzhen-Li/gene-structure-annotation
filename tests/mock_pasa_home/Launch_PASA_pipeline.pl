#!/usr/bin/env python3
"""MOCK Launch_PASA_pipeline.pl -A (tests only). Writes
<db>.gene_structures_post_PASA_updates.<pid>.gff3: the loaded models, each gene's first
mRNA with its terminal exons extended by 30 bp (a stand-in for added UTRs)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _mockpasa import STATE, db_name, die, log, opt  # noqa: E402

argv = sys.argv[1:]
log("Launch_PASA_pipeline.pl", argv)
if "-A" not in argv:
    die("mock supports only the annotation-compare mode (-A)")
for k in ("-c", "-g", "-t"):
    v = opt(argv, k)
    if not v or not os.path.isfile(v):
        die(f"{k} missing or not a file")
if not os.path.isfile(STATE):
    die("no annotations loaded (run Load_Current_Gene_Annotations.dbi first)")
src = open(STATE).read().strip()
lines = [l.rstrip("\n").split("\t") for l in open(src) if l.strip() and not l.startswith("#")]
exons = {}
for f in lines:
    if f[2] == "exon":
        par = dict(p.split("=", 1) for p in f[8].split(";") if "=" in p)["Parent"]
        exons.setdefault(par, []).append(f)
for par, ex in exons.items():
    ex.sort(key=lambda f: int(f[3]))
    ex[0][3] = str(max(1, int(ex[0][3]) - 30))
    ex[-1][4] = str(int(ex[-1][4]) + 30)
span = {}
for par, ex in exons.items():
    span[par] = (ex[0][3], ex[-1][4])
for f in lines:
    a = dict(p.split("=", 1) for p in f[8].split(";") if "=" in p)
    if f[2] == "mRNA" and a.get("ID") in span:
        f[3], f[4] = span[a["ID"]]
gspan = {}
for f in lines:
    a = dict(p.split("=", 1) for p in f[8].split(";") if "=" in p)
    if f[2] == "mRNA":
        lo, hi = gspan.get(a["Parent"], (f[3], f[4]))
        gspan[a["Parent"]] = (str(min(int(lo), int(f[3]))), str(max(int(hi), int(f[4]))))
for f in lines:
    a = dict(p.split("=", 1) for p in f[8].split(";") if "=" in p)
    if f[2] == "gene" and a.get("ID") in gspan:
        f[3], f[4] = gspan[a["ID"]]
out = f"{db_name(opt(argv, '-c'))}.gene_structures_post_PASA_updates.{os.getpid()}.gff3"
with open(out, "w") as fh:
    fh.write(f"##gff-version 3\n# MOCK PASA annotation update of {os.path.basename(src)}\n")
    fh.write("\n".join("\t".join(f) for f in lines) + "\n")
