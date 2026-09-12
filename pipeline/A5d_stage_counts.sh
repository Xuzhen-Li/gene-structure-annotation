#!/usr/bin/env bash
# Stage-wise gene counts + mono:multi (Copetti / BRAKER#949 habit).
# Usage: bash pipeline/A5d_stage_counts.sh label1.gtf [label2.gtf ...]
# GTF/GFF with gene or transcript features; best-effort exon counting.
set -euo pipefail
OUT="${STAGE_QC_TSV:-stage_qc.tsv}"
echo -e "label\tgenes\tmono\tmulti\tmono_multi_ratio" > "$OUT"

count_one() {
  local f="$1" lab
  lab=$(basename "$f")
  python3 - "$f" <<'PY'
import sys, collections
path = sys.argv[1]
# Map transcript -> exon count; gene -> set of transcripts
exons = collections.Counter()
tx_gene = {}
genes = set()
for line in open(path):
    if not line.strip() or line.startswith("#"):
        continue
    p = line.rstrip("\n").split("\t")
    if len(p) < 9:
        continue
    feat, attrs = p[2], p[8]
    def grab(key):
        for part in attrs.split(";"):
            part = part.strip()
            if part.startswith(key):
                return part.split(None,1)[-1].strip().strip('"').strip("'")
            if part.startswith(key + "="):
                return part.split("=",1)[1].strip().strip('"')
        return None
    gid = grab("gene_id") or grab("ID") if feat == "gene" else grab("gene_id") or grab("Parent")
    tid = grab("transcript_id") or grab("ID") if feat in ("transcript","mRNA") else grab("transcript_id")
    if feat == "gene" and gid:
        genes.add(gid.split(",")[0])
    if feat in ("transcript","mRNA") and tid:
        tid = tid.split(",")[0]
        g = (grab("gene_id") or grab("Parent") or tid)
        if g:
            g = g.split(",")[0]
            genes.add(g)
            tx_gene[tid] = g
    if feat == "exon":
        tid = grab("transcript_id") or grab("Parent")
        if tid:
            exons[tid.split(",")[0]] += 1
# Fall back: count gene features only
if not genes:
    for line in open(path):
        if line.startswith("#"): continue
        p = line.split("\t")
        if len(p) > 2 and p[2] == "gene":
            genes.add(p[8][:40])
# Per gene: pick transcript with most exons
from collections import defaultdict
g_ex = defaultdict(int)
for tid, n in exons.items():
    g = tx_gene.get(tid, tid)
    if n > g_ex[g]:
        g_ex[g] = n
for g in genes:
    g_ex.setdefault(g, 1)  # unknown structure → count as mono-ish placeholder
mono = sum(1 for g,n in g_ex.items() if n <= 1)
multi = sum(1 for g,n in g_ex.items() if n > 1)
ratio = (mono / multi) if multi else float("inf")
print(f"{path}\t{len(g_ex)}\t{mono}\t{multi}\t{ratio:.3f}")
PY
}

for f in "$@"; do
  [[ -f "$f" ]] || { echo "missing $f" >&2; exit 1; }
  count_one "$f" | tee -a "$OUT"
done
echo "[OK] wrote $OUT — compare BRAKER vs GeneMark vs Augustus vs StringTie (Copetti table)"
