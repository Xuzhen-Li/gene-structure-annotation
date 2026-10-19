#!/usr/bin/env bash
# Stage-wise gene counts + mono:multi (Copetti / BRAKER#949 habit).
# Usage: bash pipeline/A5d_stage_counts.sh label1.gtf [label2.gff3 ...]
# Reads GTF (key "value") and GFF3 (key=value). Writes STAGE_QC_TSV
# (default: $WORK_DIR/qc/stage_qc.tsv, or ./stage_qc.tsv when WORK_DIR is unset).
set -euo pipefail
if [[ -n "${STAGE_QC_TSV:-}" ]]; then
  OUT="$STAGE_QC_TSV"
elif [[ -n "${WORK_DIR:-}" ]]; then
  OUT="$WORK_DIR/qc/stage_qc.tsv"
else
  OUT="stage_qc.tsv"
fi
mkdir -p "$(dirname "$OUT")"
echo -e "label\tgenes\tmono\tmulti\tmono_multi_ratio" > "$OUT"

count_one() {
  python3 - "$1" <<'PY'
import os
import re
import sys
from collections import Counter, defaultdict

path = sys.argv[1]
GTF_ATTR = re.compile(r'(\S+)\s+"([^"]*)"')
TX = {"transcript", "mRNA"}


def parse_attrs(col9):
    col9 = col9.strip()
    first = col9.split(";", 1)[0]
    if "=" in first and '"' not in first:
        d = {}
        for part in col9.rstrip(";").split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                d[k.strip()] = v.strip()
        return d
    return dict(GTF_ATTR.findall(col9))


genes = set()
tx_gene = {}
exons = Counter()
rows = []
for line in open(path):
    if not line.strip() or line.startswith("#"):
        continue
    p = line.rstrip("\n").split("\t")
    if len(p) < 9:
        continue
    rows.append((p[2], parse_attrs(p[8])))
for feat, a in rows:
    if feat == "gene":
        gid = a.get("ID") or a.get("gene_id")
        if gid:
            genes.add(gid)
exon_rows = []
for feat, a in rows:
    if feat == "gene":
        continue
    if feat == "exon":
        exon_rows.append(a)
        continue
    par = (a.get("Parent") or "").split(",")[0]
    # transcripts: mRNA/transcript lines, or any child with an ID whose Parent is a gene (tRNA, ncRNA, …)
    if feat in TX or (a.get("ID") and par in genes):
        tid = a.get("ID") or a.get("transcript_id")
        gid = par or a.get("gene_id")
        if tid:
            gid = gid or tid
            tx_gene[tid] = gid
            genes.add(gid)

for a in exon_rows:
    parents = (a.get("Parent") or a.get("transcript_id") or "").split(",")
    for tid in parents:
        if not tid:
            continue
        exons[tid] += 1
        if tid not in tx_gene and a.get("gene_id"):
            # GTF without transcript lines
            tx_gene[tid] = a["gene_id"]
            genes.add(a["gene_id"])

# Per gene: transcript with most exons
g_ex = defaultdict(int)
for tid, n in exons.items():
    g = tx_gene.get(tid, tid)
    g_ex[g] = max(g_ex[g], n)
for g in genes:
    g_ex.setdefault(g, 1)  # no exon lines → counted as mono-exonic
mono = sum(1 for n in g_ex.values() if n <= 1)
multi = sum(1 for n in g_ex.values() if n > 1)
ratio = f"{mono / multi:.3f}" if multi else "NA"
print(f"{os.path.basename(path)}\t{len(g_ex)}\t{mono}\t{multi}\t{ratio}")
PY
}

for f in "$@"; do
  [[ -f "$f" ]] || { echo "missing $f" >&2; exit 1; }
  count_one "$f" | tee -a "$OUT"
done
echo "[OK] wrote $OUT — compare BRAKER vs GeneMark vs Augustus vs StringTie (Copetti table)"
