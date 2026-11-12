# Asm1 — assembly QC

**Collects:** Assembly QC metrics and lineage choice that gate annotation.

**Does not collect:** —

## Entries

- [GSA-Asm1-001 · NCBI FCS-GX](#gsa-asm1-001--ncbi-fcs-gx)

### GSA-Asm1-001 · NCBI FCS-GX

| field | value |
|---|---|
| type | tool |
| stage | Asm1_assembly_qc / Asm1 |
| branches | — |
| what it does | Detects and removes foreign-organism contamination in assemblies before submission/annotation. |
| url | https://github.com/ncbi/fcs |
| doi | [10.1186/s13059-024-03198-7](https://doi.org/10.1186/s13059-024-03198-7) |
| venue / year | Genome Biology 2024 |
| venue_label | Allowlisted |
| latest release (GitHub API) | v0.5.5 (2025-03-18); last push 2025-03-18 |
| license | custom/other (see repo) |
| plant_evidence | Any eukaryote; avoids annotating bacterial/fungal contigs as plant genes. |
| existing_doc | none |
| io | `GENOME_FA` → contamination report (cleaned `GENOME_FA`) |
| layer_check | structure |
| verdict | include |
| checked_version | v0.5.5 (2025-03-18) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

[Back to catalog index](../README.md)
