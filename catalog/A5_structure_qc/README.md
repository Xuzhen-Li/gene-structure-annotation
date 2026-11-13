# A5 — structure QC (A5b–A5e, structure_qa qa01–qa10)

**Collects:** Structure QC tools and metrics, annotation benchmarks. The A5c Pfam/BLASTP filter is model-support QC, not functional annotation: a model may be dropped only when RNA, Pfam and homology support are **all** absent; grapevine disease-resistance and specialised-metabolism genes must not be removed on expression alone.

**Does not collect:** GO/domains as functional labels and function-table QC (gene-function-annotation F10).

## Entries

- [GSA-A5-001 · ABAQS](#gsa-a5-001--abaqs)
- [GSA-A5-002 · Chimeric mis-annotation survey](#gsa-a5-002--chimeric-mis-annotation-survey)
- [GSA-A5-003 · Annotation affects orthology (idea)](#gsa-a5-003--annotation-affects-orthology-idea)
- [GSA-A5-004 · GeneValidator](#gsa-a5-004--genevalidator)

### GSA-A5-001 · ABAQS

| field | value |
|---|---|
| type | tool |
| stage | A5_structure_qc / A5 |
| branches | S5 |
| what it does | Accuracy-Based Annotation Quality Score combining completeness, gene-model validity and protein-profile checks. |
| url | https://github.com/mycocosm-lbl/abaqs |
| doi | none found |
| venue / year | — |
| venue_label | — (no paper) |
| latest release (GitHub API) | REL_0 (2025-10-31); last push 2026-11-04 |
| license | custom/other (see repo) |
| plant_evidence | From JGI MycoCosm (fungi) [待确认 plant use]. |
| existing_doc | none |
| io | `MERGED_GFF` / `PROTEINS_FA` → QC table |
| layer_check | structure |
| verdict | include |
| checked_version | REL_0 (2025-10-31) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A5-002 · Chimeric mis-annotation survey

| field | value |
|---|---|
| type | idea |
| stage | A5_structure_qc / A5 |
| branches | S5 |
| what it does | Shows fused (chimeric) gene models remain common in non-model eukaryote annotations; gives detection heuristics. |
| url | — |
| doi | [10.1186/s12864-025-11765-w](https://doi.org/10.1186/s12864-025-11765-w) |
| venue / year | BMC Genomics 2025 |
| venue_label | Below allowlist |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Directly relevant to merged tandem NLR/terpene clusters in grapevine. |
| existing_doc | none |
| io | `MERGED_GFF` / `PROTEINS_FA` → QC table |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A5-003 · Annotation affects orthology (idea)

| field | value |
|---|---|
| type | idea |
| stage | A5_structure_qc / A5 |
| branches | S5 |
| what it does | Structural annotation choices change orthology inference; compare annotations before cross-species claims. |
| url | — |
| doi | [10.1093/bioinformatics/btaf365](https://doi.org/10.1093/bioinformatics/btaf365) |
| venue / year | Bioinformatics 2025 |
| venue_label | Below allowlist |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Applies to any comparative plant study. |
| existing_doc | none |
| io | `MERGED_GFF` / `PROTEINS_FA` → QC table |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A5-004 · GeneValidator

| field | value |
|---|---|
| type | tool |
| stage | A5_structure_qc / A5 |
| branches | S5 |
| what it does | Flags problem gene models by comparing each protein with database homologs (length, coverage, duplication, merged genes). |
| url | https://github.com/wurmlab/genevalidator |
| doi | [10.1093/bioinformatics/btw015](https://doi.org/10.1093/bioinformatics/btw015) |
| venue / year | Bioinformatics 2016 |
| venue_label | Below allowlist |
| latest release (GitHub API) | — |
| license | AGPL-3.0 |
| plant_evidence | Any eukaryote; useful for merged tandem genes. Last push 2024-03. |
| existing_doc | none |
| io | `MERGED_GFF` / `PROTEINS_FA` → QC table |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

[Back to catalog index](../README.md)
