#!/usr/bin/env bash
# Filter GFF by protein stop + min length (S14 protein filter).
# Requires: gffread, GENOME_FA, input GFF → writes *.checked.gff3
set -euo pipefail
: "${GENOME_FA:?}"
IN_GFF="${1:?usage: A5e_filter_proteins.sh genes.gff3 [min_aa]}"
MIN_AA="${2:-50}"
STEM="${IN_GFF%.gff3}"
STEM="${STEM%.gff}"
PROT="${STEM}.protein.faa"
TAB="${STEM}.protein.tab"
DROP="${STEM}.ids_to_remove.txt"
OUT="${STEM}.checked.gff3"

gffread "$IN_GFF" -g "$GENOME_FA" -y "$PROT"
# one line per protein; keep stop as *
awk '/^>/{if(NR>1)printf("\n%s\t", substr($0,2)); else printf("%s\t", substr($0,2)); next}
     {printf "%s",$0} END{print ""}' "$PROT" > "$TAB"

: > "$DROP"
# no stop codon
awk -F'\t' '($2 !~ /\*/){print $1}' "$TAB" >> "$DROP"
# short proteins (count AA excluding *)
awk -F'\t' -v m="$MIN_AA" '{
  seq=$2; gsub(/\*/,"",seq); if(length(seq)<m) print $1
}' "$TAB" >> "$DROP"
sort -u "$DROP" -o "$DROP"

python3 - "$IN_GFF" "$DROP" "$OUT" <<'PY'
import sys
gff, drop_path, out = sys.argv[1:4]
drop = set(x.strip() for x in open(drop_path) if x.strip())
# Also drop if ID/Parent intersects drop (gene or mRNA names from gffread often = mRNA id)
keep_lines = []
# First pass: map which gene/mRNA ids to kill
kill = set(drop)
for line in open(gff):
    if line.startswith("#") or not line.strip():
        continue
    p = line.rstrip().split("\t")
    if len(p) < 9:
        continue
    attrs = p[8]
    def ids():
        for part in attrs.split(";"):
            part = part.strip()
            if part.startswith("ID=") or part.startswith("Parent="):
                yield part.split("=",1)[1]
    if p[2] in ("gene","mRNA","transcript") and any(i in kill for i in ids()):
        for i in ids():
            kill.add(i)

with open(out,"w") as o:
    for line in open(gff):
        if line.startswith("#") or not line.strip():
            o.write(line if line.startswith("#") else "")
            continue
        p = line.rstrip().split("\t")
        if len(p) < 9:
            o.write(line); continue
        attrs = p[8]
        ids = []
        for part in attrs.split(";"):
            part = part.strip()
            if part.startswith("ID=") or part.startswith("Parent="):
                ids.append(part.split("=",1)[1])
        if any(i in kill for i in ids):
            continue
        o.write(line if line.endswith("\n") else line+"\n")
print(f"[OK] removed up to {len(kill)} ids → {out}")
PY
echo "[OK] $OUT (min_aa=$MIN_AA); review $DROP"
