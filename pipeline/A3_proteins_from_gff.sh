#!/usr/bin/env bash
# Build a representative protein FASTA from draft (or curated) GFF for BUSCO/PSAURON.
set -euo pipefail

: "${GENOME_FA:?unmasked or soft-masked genome OK for gffread CDS}"
: "${DRAFT_GFF:?}"
: "${PROTEINS_FA:?}"
WORK_DIR="${WORK_DIR:-$(dirname "$PROTEINS_FA")}"
mkdir -p "$(dirname "$PROTEINS_FA")"

if ! command -v gffread >/dev/null; then
  echo "need gffread (cufflinks / bioconda gffread)"; exit 1
fi

# CDS → protein; -J drops incomplete CDS if you want stricter set
gffread "$DRAFT_GFF" -g "$GENOME_FA" -y "$PROTEINS_FA.raw.faa"

# Optional: keep one protein per gene_id (longest CDS)
python3 - "$PROTEINS_FA.raw.faa" "$PROTEINS_FA" <<'PY'
import sys
from pathlib import Path

inp, outp = Path(sys.argv[1]), Path(sys.argv[2])
best: dict[str, tuple[int, str, str]] = {}
name = seq = None

def flush():
    global name, seq
    if not name or not seq:
        return
    # gene id heuristics: strip transcript suffixes common in BRAKER/GeMoMa
    gid = name.split()[0]
    for sep in [".t", ".T", "-mRNA", "_t", ".1", ".2"]:
        # only strip trailing isoform markers carefully
        pass
    if ".t" in gid:
        gid = gid.rsplit(".t", 1)[0]
    elif gid.count(".") >= 2 and gid[-1].isdigit():
        # e.g. gene.1 → keep as-is if BRAKER style g123.t1 already handled
        pass
    if gid.endswith(".1") or gid.endswith(".2"):
        base = gid.rsplit(".", 1)[0]
        if base:
            gid = base
    L = len(seq.replace("\n", ""))
    prev = best.get(gid)
    if prev is None or L > prev[0]:
        best[gid] = (L, name.split()[0], seq)

with inp.open() as fh:
    for line in fh:
        if line.startswith(">"):
            flush()
            name, seq = line[1:].strip(), ""
        else:
            seq += line
    flush()

with outp.open("w") as out:
    for gid, (L, hdr, s) in sorted(best.items()):
        out.write(f">{gid} length={L}\n")
        s = s.replace("\n", "")
        for i in range(0, len(s), 80):
            out.write(s[i : i + 80] + "\n")
print(f"wrote {len(best)} representative proteins -> {outp}")
PY

echo "[OK] $PROTEINS_FA"
