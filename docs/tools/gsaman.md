# GSAman — manual gene-structure curation

**Role:** Last mile (Chen, Chen & Xia 2026, *The Innovation*). Stages 03–04 in this repo.

## Get it
- Follow the paper / authors’ distribution for GSAman (desktop curation tool).  
- You need a machine that can load genome + BAM + GFF tracks.

## What to load
See [`../../pipeline/03_evidence_checklist.md`](../../pipeline/03_evidence_checklist.md):

- Soft-masked FASTA  
- Current GFF  
- RNA / Iso-seq BAM  
- Protein alignments  
- Homolog GFF  
- Work list = `priority.tsv`

## How to work (discipline)
1. Sort priority worst-first (+ family boosts).  
2. Open locus **with neighbors** (tandems).  
3. Tag error class: fragmentation / fusion / splice / tandem-collapse ([`../ERROR_CLASSES.md`](../ERROR_CLASSES.md)).  
4. Edit → export GFF often → `CURATED_GFF`.  
5. Changelog TSV every fix.  
6. Stop with **S12** rules — not infinite polish.

## After each round
```bash
DRAFT_GFF="$CURATED_GFF" bash pipeline/A3_proteins_from_gff.sh
bash pipeline/01_qc_busco_psauron.sh
```

## Pitfalls
- Curating TE ORFs.  
- “Fixing” without RNA/protein evidence.  
- No changelog → unreproducible METHODS.
