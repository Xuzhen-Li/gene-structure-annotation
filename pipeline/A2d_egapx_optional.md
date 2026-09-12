# A2d — Optional: NCBI EGAPx (eudicot / rosids)

Upstream: [ncbi/egapx](https://github.com/ncbi/egapx).

EGAPx supports **Eudicots — Rosids** (among others). *Vitis* is in scope.
It chains miniprot/ProSplign + STAR/minimap2 RNA → **Gnomon**, optional ncRNA.

## When to consider it

- You want an NCBI-style structural set for comparison or GenBank prep.
- You can supply taxid + multi-tissue RNA (Beenome100 protocol: prefer conspecific ≥10M mapped reads).

## When not to

- Offline cluster without pulling NCBI evidence packages.
- You already committed to BRAKER3+GeMoMa+EVM and only need last-mile curation.

## Vitis note

Set `taxid` to *Vitis vinifera* (or closest available genus taxid if species missing).
Keep EGAPx GFF as an **extra** prediction set for A4 merge / GSAman evidence — not an automatic replacement for the lab default path.

Protocol pattern (Beenome100): YAML with `genome`, `taxid`, `short_reads`, optional custom proteins.
