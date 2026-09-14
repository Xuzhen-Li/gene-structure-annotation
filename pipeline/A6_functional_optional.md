# A6 — Hand-off only (not a product of this repo)

This repository’s **primary product** is structural:

- qualified **GFF3** (gene / mRNA / CDS), and  
- **`proteins.faa`**, plus METHODS.

**GO / KEGG / domains / readable names are not done here.**

When structure release is frozen (`RELEASE_TAG`):

1. Point `PROTEINS_FA` at this release’s proteins.  
2. Continue in sibling [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation)  
   (`pipeline/flow_tool/` → F1 default).

There is no `F1_diamond.sh` / eggNOG / InterProScan in *this* repo.  
Ignore any old note that called functional annotation the “PRIMARY product” here — that was a leftover from before the structure/function split.
