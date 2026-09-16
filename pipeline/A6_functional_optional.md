# A6 — Hand-off only (not a product of this repo)

This repository’s **primary product** is structural:

- qualified **GFF3** (gene / mRNA / CDS), and  
- **proteins** FASTA, plus METHODS.

**GO / KEGG / domains / readable names are not done here.**

When structure release is frozen (`RELEASE_TAG`), `pipeline/06_release_gff.md` writes under `release/<TAG>/`:

| File | Role |
|------|------|
| `<TAG>.gff3` / `<TAG>.proteins.faa` | Versioned names |
| `genes.gff3` / **`proteins.faa`** | Stable aliases — **point function `PROTEINS_FA` here** |

1. Set function `PROTEINS_FA` to `…/release/<TAG>/proteins.faa` (not a missing path).  
2. Continue in sibling [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation)  
   (`pipeline/flow_tool/` → F1 default).

There is no `F1_diamond.sh` / eggNOG / InterProScan in *this* repo.  
Ignore any old note that called functional annotation the “PRIMARY product” here — that was a leftover from before the structure/function split.
