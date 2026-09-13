# EDTA — de novo TE library (step 1 of the lab scheme)

**Role:** Usual *de novo* starter (`01_discovery`). **Not** a finished library / not curatedlib.  
**Full order:** [`../TE_LIBRARY.md`](../TE_LIBRARY.md) — EDTA → TEtrimmer **working** → TEsorter labels → gate **trusted** → soft-mask; panEDTA/LAI after.  
**Home:** [vitis-te](https://github.com/Xuzhen-Li/vitis-te) · lab notebook `03_TE/`.

## Get it

https://github.com/oushujun/EDTA · biocontainer / Singularity recommended.

## Minimal (grape panel defaults)

```bash
EDTA.pl \
  --genome "$GENOME_FA" \
  --species others \
  --sensitive 1 \
  --anno 1 \
  --u 5.4e-9 \
  --threads "$THREADS"
# First grape round often without --cds (CDS = PN40024.v4.1 later for gate / panEDTA)
# Sequence names ≤13 chars; keep id_map.tsv
```

Next for structure A0: TEtrimmer → working lib → TEsorter → curation gate → **trusted** → A0b if needed → RepeatMasker `-xsmall`.  
Do **not** feed raw EDTA / whole working lib / `cat`+CD-HIT into `--curatedlib` or BRAKER soft-mask.  
Do **not** feed hard-mask / MAKER.masked into BRAKER.

## Pitfalls

- Treating EDTA raw as gold-standard TE lib.  
- Feeding the entire **working** lib as `--curatedlib`.  
- Using hard-masked MAKER file for BRAKER.  
- Putting 03b non-TE (TRF/telomere/rDNA) into curatedlib.  
- Running LAI / K2P on uncurated EDTA output.
