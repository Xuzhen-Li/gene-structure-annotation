# Helixer — deep-learning ab initio genes

**Role:** RAGNAROK / Sylvan draft engine; optional GPU path (**S13**).

## Get it
https://github.com/weberlab-hhu/Helixer — pick the lineage model matching your clade (land_plant / vertebrate / invertebrate / fungi).

## Idea
Predict genes without RNA; combine with evidence via **Mikado** (or EVM) and penalize microexon-rich models (RAGNAROK plant scoring YAML).

## Pitfalls
- Microexon inflation → Mikado plant filter.  
- Still soft-mask / TE-aware before trusting gene counts.
