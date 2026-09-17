# Boundary — three layers (do not mix)

Short English map of who owns what. Structure never ships FA tables.

| Layer | Where | Owns | Does **not** own |
|-------|--------|------|------------------|
| **1. Structure** (+ TE soft-mask for gene calling) | **this repo** | Coordinates / GFF3 / proteins / METHODS; A0 soft-mask with a **trusted** TE lib only | GO / KEGG / names / domain tables; TE *library construction* |
| **2. Function** | [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation) | Labels after proteins exist (`functional_master.tsv`, GO/KEGG-ish, domains, names) | BRAKER / soft-mask / GFF editing / gene finding |
| **3. TE library build** | [`vitis-te`](https://github.com/Xuzhen-Li/vitis-te) + [`TE_LIBRARY.md`](TE_LIBRARY.md) | Building / curating the TE library (separate job) | Gene models; functional labels |

**Hard rule:** TE soft-mask is a **prerequisite floor inside structure** (trusted lib only). TE library *construction* is layer 3 — not function, not optional garnish on structure.  
**Hard rule:** GO/KEGG/names live **only** in gene-function-annotation. After structure release, hand off via [`HANDOFF_STRUCTURE_TO_FUNCTION.md`](HANDOFF_STRUCTURE_TO_FUNCTION.md) / [`pipeline/A6_handoff_to_function.md`](../pipeline/A6_handoff_to_function.md).

**Board:** [Annotation board (Project #2)](https://github.com/users/Xuzhen-Li/projects/2) — structure → function.
