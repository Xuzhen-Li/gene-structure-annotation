# Last mile 04 — GSAman / manual curation

**Collects:** Manual curation tools (GSAman, browsers/editors) and curation ideas.

**Does not collect:** HRP and other NLR classifiers (gene-function-annotation F8). LM04 only *uses* the F8 NLR result to mark windows for curation.

## Entries

- [GSA-LM04-001 · Apollo 3](#gsa-lm04-001--apollo-3)
- [GSA-LM04-002 · JBrowse 2](#gsa-lm04-002--jbrowse-2)
- [GSA-LM04-003 · GeneWhisperer](#gsa-lm04-003--genewhisperer)
- [GSA-LM04-004 · Human-AI collaborative annotation framework](#gsa-lm04-004--human-ai-collaborative-annotation-framework)
- [GSA-LM04-005 · Family-window review using function results (idea)](#gsa-lm04-005--family-window-review-using-function-results-idea)

### GSA-LM04-001 · Apollo 3

| field | value |
|---|---|
| type | tool |
| stage | LM04_gsaman_curation / last mile 04 |
| branches | S5, S7 |
| what it does | JBrowse 2-based collaborative gene-model editor (local or server). |
| url | https://github.com/GMOD/Apollo3 |
| doi | [10.64898/2026.06.08.730970](https://doi.org/10.64898/2026.06.08.730970) |
| venue / year | preprint 2026 |
| venue_label | Preprint |
| latest release (GitHub API) | v0.3.8 (2025-09-15); last push 2026-11-11 |
| license | Apache-2.0 |
| plant_evidence | Manual curation of grapevine gene families. |
| existing_doc | none |
| io | draft GFF + evidence tracks → `CURATED_GFF` |
| layer_check | structure |
| verdict | needs evidence |
| checked_version | v0.3.8 (2025-09-15) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-LM04-002 · JBrowse 2

| field | value |
|---|---|
| type | tool |
| stage | LM04_gsaman_curation / last mile 04 |
| branches | S5, S7 |
| what it does | Genome browser with synteny and SV views; host evidence tracks for curation. |
| url | https://github.com/GMOD/jbrowse-components |
| doi | [10.1186/s13059-023-02914-z](https://doi.org/10.1186/s13059-023-02914-z) |
| venue / year | Genome Biology 2023 |
| venue_label | Allowlisted |
| latest release (GitHub API) | v4.3.0 (2026-05-21); last push 2026-11-12 |
| license | Apache-2.0 |
| plant_evidence | Any genome. |
| existing_doc | none |
| io | draft GFF + evidence tracks → `CURATED_GFF` |
| layer_check | structure |
| verdict | include |
| checked_version | v4.3.0 (2026-05-21) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-LM04-003 · GeneWhisperer

| field | value |
|---|---|
| type | idea |
| stage | LM04_gsaman_curation / last mile 04 |
| branches | S5, S7 |
| what it does | LLM assistant with task tools for manual gene annotation (preprint). |
| url | — |
| doi | [10.1101/2025.03.30.646211](https://doi.org/10.1101/2025.03.30.646211) |
| venue / year | preprint 2025 |
| venue_label | Preprint |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Idea for curator support; keep human sign-off. |
| existing_doc | none |
| io | draft GFF + evidence tracks → `CURATED_GFF` |
| layer_check | structure |
| verdict | needs evidence |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-LM04-004 · Human-AI collaborative annotation framework

| field | value |
|---|---|
| type | idea |
| stage | LM04_gsaman_curation / last mile 04 |
| branches | S5, S7 |
| what it does | Conceptual framework for dividing genome-annotation work between AI and curators. |
| url | — |
| doi | [10.1093/bib/bbaf377](https://doi.org/10.1093/bib/bbaf377) |
| venue / year | Briefings in Bioinformatics 2025 |
| venue_label | Below allowlist |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Guides how to log AI-suggested edits. |
| existing_doc | none |
| io | draft GFF + evidence tracks → `CURATED_GFF` |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-LM04-005 · Family-window review using function results (idea)

| field | value |
|---|---|
| type | idea |
| stage | LM04_gsaman_curation / last mile 04 |
| branches | S5, S7 |
| what it does | Scenario S7 can take an NLR/TF window list produced in gene-function-annotation and re-check gene models in those windows; the classifiers themselves stay in the function catalog. |
| url | https://github.com/Xuzhen-Li/gene-function-annotation |
| doi | none found |
| venue / year | — |
| venue_label | — (no paper) |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Grapevine NLR and terpene synthase clusters. |
| existing_doc | none |
| io | draft GFF + evidence tracks → `CURATED_GFF` |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

[Back to catalog index](../README.md)
