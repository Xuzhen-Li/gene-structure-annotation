---
name: plant-gene-annotation
description: >
  Eukaryotic gene prediction for new plant assemblies.
  Use when running BRAKER3, GALBA, GeMoMa, RepeatMasker
  softmask, or OrthoDB Viridiplantae protein hints.
---

# plant-gene-annotation

Evidence dominates algorithm. A pretty BUSCO score on a TE-stuffed GFF is not an annotation.

## Tool defaults

| Evidence you actually have | First tool |
|----------------------------|------------|
| RNA-seq + proteins | BRAKER3, smallest OrthoDB partition that contains the clade |
| Proteins only, close relatives | GALBA |
| Project a close annotated genome | GeMoMa |
| TE library for this assembly | see `vitis-te`; soft-mask first |

OrthoDB partition: Viridiplantae or eudicots. Not all Metazoa. Not "the biggest protein set".

## Order

1. Soft-mask repeats (`vitis-te` curated lib). Hard-mask destroys exons.
2. Filter the TE lib so NLR / R-genes are not in it.
3. Run BRAKER3 / GALBA / GeMoMa from the table above.
4. Keep one representative isoform for counts; do not pretend you have UTRs if the GFF has none.
5. Sanity-check gene number, length, and BUSCO against a near relative + ploidy.

## Plant traps

| Trap | What it looks like | What it is |
|------|--------------------|------------|
| TE ORFs as genes | extra 10–40k "genes" | unmasked LTR / Helitron ORFs |
| One isoform, no UTRs | mRNA:gene == 1 | normal for ab initio; not a transcriptome |
| NLR tandem merge/split | one huge gene or shredded cluster | predictor cannot see array boundaries |
| High BUSCO-D | "haplotigs leftover" | often real WGD / heterozygous pairs |
| Over-masking | missing multi-copy defense genes | NLR/R-genes were in the TE lib |

## Sanity

- Gene count vs nearest relative, scaled by ploidy — not vs human, and not vs Arabidopsis if the species is a recent polyploid.
- Mono-exonic fraction: plants have many real single-exon genes. Do not apply vertebrate mono-exonic cutoffs.
- Protein-length histogram should be unimodal around the clade mean. A second spike at ~100 aa is usually TE fragments.
- BUSCO-C high + gene count 2× relative → check ploidy / haplotigs before you purge.

## Red lines

- Do not hard-mask a plant genome and then run a gene predictor.
- Do not feed OrthoDB Metazoa (or "all proteins") to a Vitis BRAKER3 run.
- Do not put NLR / R-gene proteins into the RepeatMasker library.
- Do not interpret mRNA:gene == 1 as a failed annotation.
- Do not call high BUSCO-D haplotig error without a ploidy / WGD check.

Related: `vitis-te`, `vitis-synteny`, `vitis-pangenome`.

Adapted from GPTomics/bioSkills (MIT); rewritten for plants/Vitis.
