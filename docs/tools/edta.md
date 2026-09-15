# EDTA — de novo TE library (step 1 of the lab scheme)

**Role:** Usual *de novo* starter (`01_discovery`). **Not** a finished library / not curatedlib.  
**Full order:** [`../TE_LIBRARY.md`](../TE_LIBRARY.md) — EDTA → TEtrimmer **working** → TEsorter labels → gate **trusted** → soft-mask; panEDTA/LAI after.  
**Home:** [vitis-te](https://github.com/Xuzhen-Li/vitis-te). Lab detailed notebook is private (not in git).

## Get it

https://github.com/oushujun/EDTA · biocontainer / Singularity recommended.  
Pin the **EDTA major version** (v1 vs v2 behaviour for LINE/SINE etc.) in METHODS.

## Minimal command (edit flags for your species)

```bash
EDTA.pl \
  --genome "$GENOME_FA" \
  --species others \
  --sensitive 1 \
  --anno 1 \
  --threads "$THREADS"
# --species: use EDTA special cases only when documented (e.g. rice/maize); else others.
# --sensitive 1: pulls a heavier RepeatModeler-class path — expect much more CPU/time.
# --u <mu>: OPTIONAL substitution rate for LTR age. **Do not copy grape values blindly.**
```

### Grape-panel example only (do not paste for other species)

```bash
# Vitis teaching defaults — μ from Zhou et al. 2019 (population-calibrated). Non-grape: choose μ from literature or omit/document.
EDTA.pl \
  --genome "$GENOME_FA" \
  --species others \
  --sensitive 1 \
  --anno 1 \
  --u 5.4e-9 \
  --threads "$THREADS"
# First grape round often without --cds (CDS = PN40024.v4.1 later for gate / panEDTA)
```

Sequence names **≤13 chars**; keep your own `id_map.tsv` if you rename.

Next for structure A0: TEtrimmer → working → TEsorter → CDS+class **emit trusted** → RepeatMasker `-xsmall`.  
**Optional:** A0b / ProtExcluder after trusted.  
Do **not** feed raw EDTA / whole working / `cat`+CD-HIT into `--curatedlib` or BRAKER soft-mask.

## Non-grape / classifiers

- TEsorter clade DB: plants often `rexdb-plant`; **animals/other clades need the matching DB** — do not assume plant.  
- Contig IDs >13 characters: rename before EDTA.

## Pitfalls

- Treating EDTA raw as gold-standard TE lib.  
- Copying grape `--u 5.4e-9` into unrelated taxa METHODS.  
- Feeding the entire **working** lib as `--curatedlib` to inflate soft-mask %.  
- Hard-masked MAKER file for BRAKER.  
- Non-TE-track repeats (TRF/telomere/rDNA) in curatedlib.  
- `--overwrite` on a frozen EDTA discovery tree.  
- Running LAI / K2P on uncurated EDTA output.

Related: [`../../pipeline/A0_softmask.md`](../../pipeline/A0_softmask.md) · optional [`../../pipeline/A0b_protexcluder.md`](../../pipeline/A0b_protexcluder.md).
