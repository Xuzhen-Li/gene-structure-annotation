# Cross-stage — whole pipelines, reviews, standards

**Collects:** Pipelines covering many stages, reviews, benchmark and standards papers.

**Does not collect:** —

## Entries

- [GSA-X-001 · EASEL](#gsa-x-001--easel)
- [GSA-X-002 · Sylvan](#gsa-x-002--sylvan)
- [GSA-X-003 · Ensembl automatic annotation pipeline (ensembl-anno)](#gsa-x-003--ensembl-automatic-annotation-pipeline-ensembl-anno)
- [GSA-X-004 · Tips for improving genome annotation quality](#gsa-x-004--tips-for-improving-genome-annotation-quality)
- [GSA-X-005 · EBP annotation standards report](#gsa-x-005--ebp-annotation-standards-report)

## Whole pipelines

### GSA-X-001 · EASEL

| field | value |
|---|---|
| type | tool |
| stage | X_cross_stage |
| branches | — |
| what it does | Nextflow pipeline: StringTie2/PsiCLASS transcripts, TransDecoder, AUGUSTUS trained on transcript and OrthoDB protein hints, random-forest filtering using RNA-folding and other features. |
| url | https://gitlab.com/PlantGenomicsLab/easel |
| doi | none found |
| venue / year | — |
| venue_label | — (no paper) |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Plant-focused (UConn Plant Computational Genomics). No dedicated paper found; related benchmark: doi 10.1002/aps3.11533. |
| existing_doc | none |
| io | genome + evidence → GFF3 (whole pipeline) |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-X-002 · Sylvan

| field | value |
|---|---|
| type | tool |
| stage | X_cross_stage |
| branches | — |
| what it does | Snakemake pipeline combining EVM/PASA, GETA, Helixer, Liftoff and miniprot evidence, then semi-supervised random-forest filtering and boundary refinement. |
| url | https://github.com/plantgenomicslab/Sylvan |
| doi | none found |
| venue / year | — |
| venue_label | — (no paper) |
| latest release (GitHub API) | v2.1.0 (2026-07-09); last push 2026-11-03 |
| license | MIT |
| plant_evidence | Plant-oriented (land_plant Helixer model); no paper found [待确认]. |
| existing_doc | [`docs/tools/helixer.md`](../../docs/tools/helixer.md), [`pipeline/A2b_second_predictor.md`](../../pipeline/A2b_second_predictor.md) |
| io | genome + evidence → GFF3 (whole pipeline) |
| layer_check | structure |
| verdict | include — update to something already mentioned (not a new tool) |
| checked_version | v2.1.0 (2026-07-09) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-X-003 · Ensembl automatic annotation pipeline (ensembl-anno)

| field | value |
|---|---|
| type | tool |
| stage | X_cross_stage |
| branches | — |
| what it does | Public code of Ensembl's automatic gene annotation pipeline. |
| url | https://github.com/Ensembl/ensembl-anno |
| doi | none found |
| venue / year | — |
| venue_label | — (no paper) |
| latest release (GitHub API) | — |
| license | Apache-2.0 |
| plant_evidence | Used for Ensembl/DToL eukaryotes; plant use [待确认]. Last push 2026-11-12. |
| existing_doc | none |
| io | genome + evidence → GFF3 (whole pipeline) |
| layer_check | structure |
| verdict | needs evidence |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

## Reviews and standards

### GSA-X-004 · Tips for improving genome annotation quality

| field | value |
|---|---|
| type | idea |
| stage | X_cross_stage |
| branches | — |
| what it does | Practical checklist: evidence choice, masking level, manual review, metrics. |
| url | — |
| doi | [10.48130/gcomm-0025-0006](https://doi.org/10.48130/gcomm-0025-0006) |
| venue / year | Genomics Communications 2025 |
| venue_label | Below allowlist |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Plant-genome authors. |
| existing_doc | none |
| io | — |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-X-005 · EBP annotation standards report

| field | value |
|---|---|
| type | idea |
| stage | X_cross_stage |
| branches | — |
| what it does | Earth BioGenome Project report on minimum annotation standards and metadata. |
| url | https://www.earthbiogenome.org/report-on-annotation-standards |
| doi | none found |
| venue / year | — |
| venue_label | — (no paper) |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Reference for METHODS wording. |
| existing_doc | none |
| io | — |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

[Back to catalog index](../README.md)
