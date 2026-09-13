---
name: gene-structure-annotation
description: >
  Use this when predicting gene models on a new genome assembly
  (BRAKER / GALBA / GeMoMa / Liftoff / EVM), soft-masking repeats,
  or choosing structural-annotation evidence branches.
---

# gene-structure-annotation

Evidence dominates algorithm. A pretty BUSCO score on a TE-stuffed GFF is not an annotation.

Canonical playbook: this repository (`docs/PLAYBOOK.md`, `docs/steps/MAIN.md`).  
Functional annotation after proteins exist: `gene-function-annotation`.

## Tool defaults

| Evidence you actually have | First tool |
|----------------------------|------------|
| RNA-seq + proteins | BRAKER4/3 (or BRAKER3), OrthoDB partition for the clade |
| Proteins only, close relatives | GALBA |
| Project a close annotated genome | GeMoMa / Liftoff / LiftOn |
| TE library for this assembly | soft-mask first (species TE lib); never hard-mask to N before ab initio |

OrthoDB / protein hints: use the **smallest partition that contains the clade**. Not "all Metazoa" for a plant; not "all plants" if a tighter set exists.

## Order

1. Asm QC gate (genome BUSCO / contiguity).
2. Soft-mask repeats. Hard-mask destroys exons.
3. Keep genes (e.g. NLR / immune / multi-copy defense) **out** of the TE lib when that matters for the clade.
4. Pick **one** branch (S1–S14); default S1 if RNA + proteins.
5. Merge → AGAT → representative proteins → protein BUSCO (+ PSAURON / OMArk as needed).
6. GSAman / priority curation depth by scenario → qualify → release GFF + proteins.
7. Hand `proteins.faa` to `gene-function-annotation` for FA.

## Common traps

| Trap | What it looks like | What it is |
|------|--------------------|------------|
| TE ORFs as genes | extra tens of k "genes" | unmasked repeat ORFs |
| One isoform, no UTRs | mRNA:gene ≈ 1 | normal for ab initio |
| Tandem merge/split | one huge gene or shredded cluster | predictor cannot see array boundaries |
| High BUSCO-D | "haplotigs leftover" | often real WGD / heterozygous pairs |
| Over-masking | missing multi-copy genes | those proteins were in the TE lib |

## Sanity

- Gene count vs nearest relative, scaled by ploidy.
- Mono-exonic fraction: many clades have real single-exon genes — do not apply the wrong kingdom’s cutoffs.
- Protein-length histogram: a spike at ~100 aa is often TE fragments.
- BUSCO-C high + gene count ~2× relative → check ploidy / haplotigs before you purge.

## Red lines

- Do not hard-mask then run a gene predictor.
- Do not feed the wrong OrthoDB kingdom to BRAKER.
- Do not put clade-critical multi-copy gene proteins into the RepeatMasker library without review.
- Do not interpret mRNA:gene ≈ 1 as a failed annotation by itself.
- Do not call high BUSCO-D haplotig error without a ploidy / WGD check.

Related: `gene-function-annotation`, species TE / synteny / pangenome playbooks as needed.

## Evidence chooser (Ji NRG 2026)

Close curated reference → S11 liftover first. RNA+proteins → S1 (+ StringTie compare). Proteins only → S2. Iso-seq/EviAnn → S3. GPU ab initio → S13 compare. Function → sibling gene-function-annotation, not an S-branch. See `docs/REVIEWS.md`.
