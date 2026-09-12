# A0 — Soft-mask (detailed)

See also [`../docs/DETAILED_GUIDE.md`](../docs/DETAILED_GUIDE.md) Step 3.

## 1. TE library
Prefer a curated species TE library (grape example: [vitis-te](https://github.com/Xuzhen-Li/vitis-te)). Else EDTA / RepeatModeler, then clean.

## 2. Remove host genes from lib (A0b)
BLAST TE consensi to UniProt plant / grape proteins; exclude significant gene hits (NLR, LRR, kinase, …) — ProtExcluder pattern.

## 3. Soft-mask
```bash
RepeatMasker -lib cleaned_te.lib -xsmall -pa "$THREADS" -dir "$WORK_DIR/mask" "$GENOME_FA"
# soft-masked = lowercase; set GENOME_SOFT to the *.masked file
```

## 4. Verify
```bash
# fraction soft-masked
python3 - <<'PY'
from pathlib import Path
import sys
fa=Path(sys.argv[1]).read_text().splitlines()
seq="".join(l for l in fa if not l.startswith(">"))
low=sum(1 for c in seq if c.islower())
print(f"softmasked_fraction={low/len(seq):.4f} total={len(seq)}")
PY
"$GENOME_SOFT"
```

**Never** use hard-masked `N` genome for BRAKER/GALBA.
