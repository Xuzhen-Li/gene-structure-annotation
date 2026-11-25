# Chapter 20. Worked example: a grapevine genome on route S1

This chapter walks through the teaching plan in [`examples/plant_sim/01_vitis_s1_s7/plan.md`](../../examples/plant_sim/01_vitis_s1_s7/plan.md). The genome is simulated (Vitis_vinifera_sim); the point is the order of decisions, not real numbers. The plan was produced by `pipeline/flow_tool/flow.py`.

## 20.1 The chooser decision

The answers say: RNA and proteins are available, there is no close curated reference, no deep Iso-Seq, no GPU comparison and no EVM stack, and the project cares about tandem disease-gene windows. The flow tool therefore picks S1 as the primary draft, adds overlay S7 for tandem and disease windows, and targets grade L1. This matches Chapter 18: BRAKER with RNA and proteins is the default when no close reference exists ([doi:10.1101/gr.278090.123](https://doi.org/10.1101/gr.278090.123)).

## 20.2 The stages

| No. | Stage | Tools | What to record | Why |
|---|---|---|---|---|
| 1 | Asm0 assembly or accepted FASTA | hifiasm or the given genome | Source, version, ploidy, stable headers | Later steps depend on stable sequence names |
| 2 | Asm1 assembly QC | BUSCO genome mode, seqkit | Lineage name (viridiplantae_odb12), ASSEMBLY_OK | Lineage must match the clade (`docs/LINEAGES.md`) |
| 3 | A0 soft-mask | RepeatMasker -xsmall with the trusted library | Library version and sha256 | Soft-mask only; the masked fraction is not genome TE% (Chapter 1.4) |
| 4 | A1b RNA alignment | HISAT2 or STAR; minimap2 for long reads | Stranded BAM | Evidence for BRAKER and StringTie |
| 5 | S1 draft | BRAKER4/3, StringTie and TransDecoder as a comparison track | DRAFT_GFF and the comparison track | The comparison is not a second gene set for EVM |
| 6 | A4 merge skipped | none | MERGED_GFF set to DRAFT_GFF | One primary draft needs no EVM or TSEBRA |
| 7 | A5 counts | AGAT | Gene, mRNA and CDS counts | Compare with related species |
| 8 | A3 proteins | gffread or AGAT | One representative protein per gene and the isoform rule | Input for QC and for the function repository |
| 9 | QC | BUSCO protein mode, PSAURON; OMArk if L2 | C/D/F/M with lineage; PSAURON table | Completeness and spurious-protein triage ([doi:10.1093/nargab/lqae189](https://doi.org/10.1093/nargab/lqae189)) |
| 10 to 12 | S7 overlay | families.tsv, `pipeline/02_priority_loci.py --families`, GSAman | Priority table; curated windows | Tandem NLR and QTL windows need manual curation ([doi:10.1016/j.xinn.2026.101471](https://doi.org/10.1016/j.xinn.2026.101471)) |
| 13 | Release | gffread validation, release folder, METHODS | Release tag and QC snapshot | Gates in `docs/EVALUATION.md` |
| 14 | A6 hand-off | gene-function-annotation, frame F1 | RELEASE_TAG and proteins | Function labels are added in the sibling repository |

## 20.3 What to take away

- The decision comes from the data, and every overlay is written down beside the primary route.
- Comparison tracks (StringTie here) are kept for checking, not merged silently.
- Manual curation is limited to windows that matter for the project; the rest can stay a draft if METHODS says so.
- A real case on a T2T grapevine genome is described in [`docs/cases/vitis-t2t-s1-s5.md`](../../docs/cases/vitis-t2t-s1-s5.md).
