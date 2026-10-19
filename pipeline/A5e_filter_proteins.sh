#!/usr/bin/env bash
# Filter GFF by protein stop + min length (S14 protein filter).
# Requires: gffread, GENOME_FA, input GFF → writes *.checked.gff3
# Also writes *.internal_stop.txt, *.no_terminal_stop.txt, *.short.txt and *.ids_to_remove.txt.
set -euo pipefail
: "${GENOME_FA:?}"
IN_GFF="${1:?usage: A5e_filter_proteins.sh genes.gff3 [min_aa]}"
MIN_AA="${2:-50}"
STEM="${IN_GFF%.gff3}"
STEM="${STEM%.gff}"
PROT="${STEM}.protein.faa"
DROP="${STEM}.ids_to_remove.txt"
OUT="${STEM}.checked.gff3"

# GFF3 only: the removal step reads ID=/Parent= attributes, so a GTF would pass through unfiltered.
if [[ "$IN_GFF" == *.gtf || "$IN_GFF" == *.gtf.gz ]] || \
   awk -F'\t' '!/^#/ && NF>=9 {gtf = ($9 !~ /=/ && $9 ~ /"/); found = 1; exit} END {exit !(found && gtf)}' "$IN_GFF"; then
  echo "[ERR] $IN_GFF looks like GTF; A5e needs GFF3 (e.g. gffread \"$IN_GFF\" --keep-genes -o genes.gff3)" >&2
  exit 2
fi
CDS="${STEM}.cds.fa"
# Spliced CDS, translated by the checker: gffread -y drops the final stop codon from its output,
# so "has a terminal stop" can only be judged on the CDS. Internal stops are reported separately.
gffread "$IN_GFF" -g "$GENOME_FA" -x "$CDS"
# Terminal vs internal stops are reported separately; KEEP_PARTIAL=1 keeps models that only lack a terminal stop.
KEEP_ARGS=()
[[ "${KEEP_PARTIAL:-0}" == "1" ]] && KEEP_ARGS=(--keep-partial)
python3 "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/protein_stop_check.py" --cds "$CDS" --protein-out "$PROT" \
  --out-prefix "$STEM" --min-aa "$MIN_AA" ${KEEP_ARGS[@]+"${KEEP_ARGS[@]}"}

python3 - "$IN_GFF" "$DROP" "$OUT" <<'PY'
import sys
from collections import defaultdict

gff, drop_path, out = sys.argv[1:4]
drop = {x.strip() for x in open(drop_path) if x.strip()}


def attrs(col9):
    d = {}
    for part in col9.strip().rstrip(";").split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            d[k.strip()] = v.strip()
    return d


rows = []
gene_tx = defaultdict(set)   # gene ID -> transcript IDs
tx_gene = {}
for line in open(gff):
    p = line.rstrip("\n").split("\t")
    rows.append((line, p))
    if line.startswith("#") or len(p) < 9:
        continue
    a = attrs(p[8])
    if a.get("ID") and a.get("Parent") and p[2] not in ("exon", "CDS", "five_prime_UTR", "three_prime_UTR",
                                                       "start_codon", "stop_codon", "intron"):
        for par in a["Parent"].split(","):
            gene_tx[par].add(a["ID"])
            tx_gene[a["ID"]] = par

# Only the transcripts flagged by the protein check are removed; a gene goes only when all of its
# transcripts are removed (one bad isoform must not take the good ones with it).
kill_tx = {t for t in drop if t in tx_gene} | {t for t in drop if t not in gene_tx}
kill_gene = {g for g, txs in gene_tx.items() if txs and txs <= kill_tx}
kill = kill_tx | kill_gene
with open(out, "w") as o:
    for line, p in rows:
        if line.startswith("#"):
            o.write(line)
            continue
        if not line.strip():
            continue
        if len(p) < 9:
            o.write(line)
            continue
        a = attrs(p[8])
        if a.get("ID") in kill:
            continue
        parents = [x for x in a.get("Parent", "").split(",") if x]
        if parents:
            remaining = [x for x in parents if x not in kill]
            if not remaining:
                continue          # every parent removed → remove the feature
            if len(remaining) < len(parents):
                # shared feature (e.g. exon of several isoforms): drop only the removed parents
                parts = []
                for part in p[8].strip().rstrip(";").split(";"):
                    if part.strip().startswith("Parent="):
                        part = "Parent=" + ",".join(remaining)
                    parts.append(part)
                p[8] = ";".join(parts)
                line = "\t".join(p) + "\n"
        o.write(line if line.endswith("\n") else line + "\n")
print(f"[OK] removed transcripts={len(kill_tx & set(tx_gene))} genes={len(kill_gene)} -> {out}")
PY
echo "[OK] $OUT (min_aa=$MIN_AA); review $DROP"
