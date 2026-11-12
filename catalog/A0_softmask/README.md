# A0 / A0b — soft-mask with a trusted library

**Collects:** Only masking with a trusted library: masking tools, checks of the soft-mask result, diagnosis of TE-driven gene inflation and the S10 loop back.

**Does not collect:** EDTA/panEDTA library building, TE library curation and TE classification (layer 3, [vitis-te](https://github.com/Xuzhen-Li/vitis-te)); using a raw EDTA library as gold standard. `docs/tools/edta.md` is only a pointer to the upstream library build.

## Entries

- [GSA-A0-001 · ULTRA](#gsa-a0-001--ultra)
- [GSA-A0-002 · Soft-mask hand-off rule (idea)](#gsa-a0-002--soft-mask-hand-off-rule-idea)

### GSA-A0-001 · ULTRA

| field | value |
|---|---|
| type | tool |
| stage | A0_softmask / A0 |
| branches | all; S10 loop |
| what it does | Probabilistic labeling of tandem / low-complexity repeats; output can feed soft-masking alongside a trusted TE library. |
| url | https://github.com/TravisWheelerLab/ULTRA |
| doi | [10.1093/bioadv/vbae149](https://doi.org/10.1093/bioadv/vbae149) |
| venue / year | Bioinformatics Advances 2024 |
| venue_label | Below allowlist |
| latest release (GitHub API) | 1.2.1 (2025-10-08); last push 2026-08-28 |
| license | BSD-3-Clause |
| plant_evidence | Tandem arrays near centromeres and gene clusters in plant genomes; masking only, not library building. |
| existing_doc | none |
| io | `GENOME_FA` + trusted library → `GENOME_SOFT` |
| layer_check | structure |
| verdict | include |
| checked_version | 1.2.1 (2025-10-08) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A0-002 · Soft-mask hand-off rule (idea)

| field | value |
|---|---|
| type | idea |
| stage | A0_softmask / A0 |
| branches | all; S10 loop |
| what it does | Structure consumes a curated TE library produced elsewhere; record library name, version and sha256 in METHODS, and keep NLR/gene families out of the library (see existing ProtExcluder note). |
| url | https://github.com/Xuzhen-Li/gene-structure-annotation/blob/main/docs/BOUNDARY.md |
| doi | none found |
| venue / year | — |
| venue_label | — (no paper) |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Applies to every plant genome; library construction tools are listed for the TE repo, not here. |
| existing_doc | none |
| io | `GENOME_FA` + trusted library → `GENOME_SOFT` |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

[Back to catalog index](../README.md)
