# A0 — Soft-mask (detailed)

**Full TE scheme (EDTA → trim → sort → curate → mask):** [`../docs/TE_LIBRARY.md`](../docs/TE_LIBRARY.md)  
Also: [`../docs/DETAILED_GUIDE.md`](../docs/DETAILED_GUIDE.md) Step 3 · [`A0b_protexcluder.md`](A0b_protexcluder.md) · [vitis-te](https://github.com/Xuzhen-Li/vitis-te).

## Goal

Produce `GENOME_SOFT` (lowercase soft-mask) safe for BRAKER/GALBA — without wiping NLR exons.

## Order (do not skip curation)

1. **EDTA** on this assembly (`--species others` unless rice/maize); optional `--cds`.  
2. **TEtrimmer** (boundaries) → **TEsorter** (lineage names only).  
3. Manual spot-check (LTR FP, LINE/SINE, CDS contamination).  
4. Curated lib: drop CDS → CD-HIT ~85% → 80-80 collapse.  
5. **A0b** ProtExcluder / host-gene purge (NLR, kinase, …).  
6. **RepeatMasker `-lib curated.fa -xsmall`** → `GENOME_SOFT`.  
7. LAI / LTR age only **after** curated lib.

Raw EDTA ≠ gold library. Details and METHODS bullets: [`TE_LIBRARY.md`](../docs/TE_LIBRARY.md).

## Soft-mask command

```bash
# CLEAN_TE_LIB = curated + host-gene-purged FASTA
RepeatMasker -lib "$CLEAN_TE_LIB" -xsmall -pa "$THREADS" \
  -dir "$WORK_DIR/mask" "$GENOME_FA"
cp "$WORK_DIR/mask/"*.masked "$GENOME_SOFT"
```

## Verify

```bash
python3 - <<'PY'
from pathlib import Path
import sys
fa=Path(sys.argv[1]).read_text().splitlines()
seq="".join(l for l in fa if not l.startswith(">"))
low=sum(1 for c in seq if c.islower())
print(f"softmasked_fraction={low/max(len(seq),1):.4f} total={len(seq)}")
PY
"$GENOME_SOFT"
```

**Never** use hard-masked `N` genome for BRAKER/GALBA.  
If gene models explode inside repeats later → **S10** (remask with curated lib, re-enter draft).
