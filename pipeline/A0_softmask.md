# A0 — Soft-mask (detailed)

**Full TE scheme:** [`../docs/TE_LIBRARY.md`](../docs/TE_LIBRARY.md)  
**Lab TE notebook:** not vendored in git — see [vitis-te](https://github.com/Xuzhen-Li/vitis-te) + [`../docs/TE_LIBRARY.md`](../docs/TE_LIBRARY.md).

## Goal

Produce `GENOME_SOFT` (lowercase) safe for BRAKER/GALBA — without wiping NLR exons.

## What you may soft-mask with

| Use | Do not use |
|-----|------------|
| **Trusted curatedlib** (gated) | Raw EDTA TElib |
| Host-gene–purged lib (A0b) | Entire **working** lib as `--curatedlib` / RM lib |
| | `cat` of many haplotype TElibs + CD-HIT |
| | TEsorter `all.cls.lib` as the library |
| | non-TE-track (TRF/telomere/rDNA) |

## Order (pangenome TE → gene soft-mask)

1. EDTA discovery (per assembly / hap) — provenance only if already frozen.  
2. TEtrimmer → CD-HIT ~95% **working** lib (+ optional 80-80 family catalog).  
3. TEsorter domains (labels; does not replace working FASTA).  
4. Curation gate → emit **trusted** FASTA.  
5. Soft-mask with **trusted** via RepeatMasker `-xsmall` → `GENOME_SOFT`.  
6. LAI / panEDTA / panel TE GFF = pangenome TE track (after trusted), not a shortcut for A0.

Details: [`TE_LIBRARY.md`](../docs/TE_LIBRARY.md).

## Soft-mask command

```bash
# CLEAN_TE_LIB = trusted curatedlib
# -pa is RM "parallel chunks" (legacy), not always 1:1 with CPU threads; check your RM/rmblast docs.
RepeatMasker -lib "$CLEAN_TE_LIB" -xsmall -pa "$THREADS" \
  -dir "$WORK_DIR/mask" "$GENOME_FA"
# Prefer a single predictable masked path (avoid picking the wrong *.masked after re-runs):
cp "$WORK_DIR/mask/$(basename "$GENOME_FA").masked" "$GENOME_SOFT"
# fallback if RM naming differs:
# cp "$WORK_DIR/mask/"*.masked "$GENOME_SOFT"
```

## Verify

```bash
python3 - "$GENOME_SOFT" <<'PY'
from pathlib import Path
import sys
fa = Path(sys.argv[1]).read_text().splitlines()
seq = "".join(l for l in fa if not l.startswith(">"))
low = sum(1 for c in seq if c.islower())
print(f"softmasked_fraction={low/max(len(seq),1):.4f} total={len(seq)}")
PY
```

**Read this number correctly:** `softmasked_fraction` is the fraction of bases that are **lowercase after RepeatMasker against *this* trusted lib** — i.e. homology coverage to your curatedlib — **not** “genome TE content %”. A lean trusted set (e.g. only named Copia/Gypsy/hAT) often yields a **lower** fraction than the true TE landscape (plants frequently >>40–50% TE bases). That can be expected. **Do not** chase a higher fraction by feeding raw EDTA / the whole **working** lib into `-lib` (G2 / TE red lines).

**Never** hard-mask to `N` for BRAKER/GALBA.  
Gene explosion in repeats later → **S10** (remask with trusted lib).
