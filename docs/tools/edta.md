# EDTA — de novo TE library (step 1 of the lab scheme)

**Role:** Usual *de novo* starter before soft-mask. **Not** a finished library.  
**Full order:** [`../TE_LIBRARY.md`](../TE_LIBRARY.md) (EDTA → TEtrimmer → TEsorter → curate → ProtExcluder → RepeatMasker → LAI).  
**Home:** [vitis-te](https://github.com/Xuzhen-Li/vitis-te).

## Get it

https://github.com/oushujun/EDTA · biocontainer / Singularity recommended.

## Minimal

```bash
EDTA.pl --genome "$GENOME_FA" --species others --sensitive 1 --anno 1 --threads "$THREADS"
# Prefer reducing gene fragments:
# EDTA.pl ... --cds genes.cds.fa
```

Next (required for structure A0): TEtrimmer → TEsorter → manual check → CD-HIT/80-80 → A0b → RepeatMasker `-xsmall`.  
Do **not** feed raw EDTA hard-mask / MAKER.masked into BRAKER.

## Pitfalls

- Treating EDTA raw as gold-standard TE lib.  
- Using hard-masked MAKER file for BRAKER.  
- Skipping CDS/`--cds` hint → gene fragments in TE lib (**S10**).  
- Running LAI on uncurated EDTA output.
