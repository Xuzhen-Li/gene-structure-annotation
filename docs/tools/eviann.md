# EviAnn — evidence-driven annotation (Iso-seq friendly)

**Role:** Primary backbone in **S3**.

## Get it
- https://github.com/alekseyzimin/EviAnn_release — follow current README (CLI moves).

## Idea
Build gene models mainly from **transcript evidence** (+ proteins), then optionally add BRAKER orphans (`MERGE_MODE=evi_backbone`).

## Inputs
- Genome FA  
- Iso-seq BAM / FLNC  
- Protein DB  

## How we use it here
1. Run EviAnn → evidence GFF.  
2. Run BRAKER3 → second GFF.  
3. Keep EviAnn genes; add non-overlapping BRAKER orphans.  
4. GSAman conflicts where they disagree.

## Pitfalls
- Treating EviAnn output as finished without AGAT/BUSCO.  
- Thin Iso-seq → empty backbone → fall back toward S1/S2.
