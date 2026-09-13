# OMArk + Compleasm — extra proteome / assembly QC

**Role:** **S5** mandatory for publication-grade structure; optional on S1 drafts.  
**Helper:** `pipeline/A5b_omark_compleasm.sh` (prints or runs when env is wired).  
**Vitis T2T case:** [`../cases/vitis-t2t-s1-s5.md`](../cases/vitis-t2t-s1-s5.md) §4.

## Install (cluster)

```bash
# typical bioconda / pip — use whatever your site supports
# conda install -c bioconda omamer omark compleasm
# or: pip install omamer omark
```

Upstream: [OMArk](https://github.com/DessimozLab/OMArk) · [OMAmer](https://github.com/DessimozLab/omamer) · [Compleasm](https://github.com/huangnengCSU/Compleasm).

## OMAmer database (wire once)

Download from OMA Browser current release: https://omabrowser.org/oma/current/

| DB file | When to use |
|---------|-------------|
| **`LUCA.h5`** (recommended for OMArk) | Full OMArk features: lineage + **contamination** detection |
| `Viridiplantae.h5` | Smaller disk; plant-focused — **weaker contamination calls** outside plants |

```bash
# Example layout — put on shared scratch, not in git
mkdir -p /shared/db/omamer
cd /shared/db/omamer
# Prefer LUCA for S5 papers (large download):
curl -fL -O https://omabrowser.org/All/LUCA.h5
# Optional smaller plant DB (not a full substitute for LUCA on S5):
# curl -fL -O https://omabrowser.org/All/Viridiplantae.h5
```

In `config/local.env`:

```bash
OMAMER_DB="/shared/db/omamer/LUCA.h5"   # path to the .h5 file
OMARK_OUT="$WORK_DIR/qc/omark"
# Optional NCBI taxid hint if you use -t (Vitis vinifera = 29760):
# OMARK_TAXID=29760
```

## Run on your proteins (S5)

```bash
# 1) OMAmer search
omamer search \
  --db "$OMAMER_DB" \
  --query "$PROTEINS_FA" \
  --out "$OMARK_OUT/proteins.omamer"

# 2) OMArk ( -d is the same .h5 )
mkdir -p "$OMARK_OUT/omark_output"
omark \
  -f "$OMARK_OUT/proteins.omamer" \
  -d "$OMAMER_DB" \
  -o "$OMARK_OUT/omark_output"
# optional: -t "$OMARK_TAXID"
```

Or via helper once `OMAMER_DB` is set:

```bash
RUN=1 bash pipeline/A5b_omark_compleasm.sh
```

**Save into the release `qc/`:** `proteins.omamer`, `omark_output/` summaries/plots, plus the DB **filename + OMA release date** in METHODS (not the .h5 itself).

## Compleasm (optional but useful)

```bash
# Proteome mode (A5b default when compleasm is on PATH):
compleasm protein -p "$PROTEINS_FA" -l "${COMPLEASM_LINEAGE:-eudicots}" \
  -o "$OMARK_OUT/compleasm" -t "$THREADS"

# Assembly mode (Asm1 extra):
compleasm run -a "$GENOME_FA" -l eudicots -t "$THREADS" -o "$WORK_DIR/asm/compleasm"
```

## How to feed OMArk into priority round 2

OMArk output layout varies by version. Typical use for S5:

1. Open the OMArk summary / per-gene tables under `omark_output/`.  
2. Export gene IDs that are **missing**, **inconsistent**, or flagged oddly relative to the chosen clade.  
3. Write a two-column TSV `gene_id\\treason` (reason e.g. `omark:missing`).  
4. Merge with PSAURON/BUSCO lists via `pipeline/02b_merge_priority_r2.py`.

## Pitfalls

- Using only `Viridiplantae.h5` and then claiming full contamination QC.  
- Replacing BUSCO with OMArk — papers want **both**.  
- Committing `.h5` databases into git.  
- Running A5b without `OMAMER_DB` and treating the printed STOP as “done”.
