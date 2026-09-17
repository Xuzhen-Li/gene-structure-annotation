# A6 — Hand-off to function (FA is NEVER a product of this repo)

This repository’s **only primary products** are **structural**:

- qualified **GFF3** (gene / mRNA / CDS coordinates), and  
- **proteins** FASTA, plus METHODS.

**Functional annotation (GO / KEGG / domains / readable names) is never produced, merged, or shipped from this repo.**  
There is no `F1_diamond.sh` / eggNOG / InterProScan / `functional_master.tsv` here.  
Ignore any old note that called functional annotation the “PRIMARY product” of structure — that was a leftover from before the structure/function split.

When structure release is frozen (`RELEASE_TAG`), `pipeline/06_release_gff.md` writes under `release/<TAG>/`:

| File | Role |
|------|------|
| `<TAG>.gff3` / `<TAG>.proteins.faa` | Versioned names |
| `genes.gff3` / **`proteins.faa`** | Stable aliases — **point function `PROTEINS_FA` here** |

1. Set function `PROTEINS_FA` to `…/release/<TAG>/proteins.faa` (not a missing or root-copy path).  
2. Continue in sibling [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation)  
   (`pipeline/flow_tool/` → F1 default).

Boundary (three layers): [`docs/BOUNDARY.md`](../docs/BOUNDARY.md).  
Handoff card: [`docs/HANDOFF_STRUCTURE_TO_FUNCTION.md`](../docs/HANDOFF_STRUCTURE_TO_FUNCTION.md).
