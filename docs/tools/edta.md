# EDTA — plant TE library + annotation

**Role:** Preferred *de novo* TE step before soft-mask (Copetti #949 tracks; genepal; RAGNAROK optional).

## Get it
https://github.com/oushujun/EDTA · biocontainer / Singularity recommended.

## Minimal
```bash
EDTA.pl --genome "$GENOME_FA" --species others --anno 1 --threads "$THREADS"
# Soft-mask for gene prediction (not the aggressive MAKER.masked alone):
# perl EDTA/util/make_masked.pl -genome genome.fa -hardmask 0 -minlen 80 \
#   -rmout genome.fa.mod.EDTA.anno/genome.fa.mod.EDTA.TEanno.out
```
Then ProtExcluder-clean lib if needed → set `GENOME_SOFT`.

## Pitfalls
- Using hard-masked MAKER file for BRAKER.  
- Skipping CDS/`--cds` hint → gene fragments in TE lib (**S10**).
