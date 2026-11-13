# Last mile 06 — release

**Collects:** GFF3 validation, format conversion, archive submission.

**Does not collect:** —

## Entries

- [GSA-LM06-001 · GenomeTools (gt gff3validator)](#gsa-lm06-001--genometools-gt-gff3validator)
- [GSA-LM06-002 · EMBLmyGFF3](#gsa-lm06-002--emblmygff3)
- [GSA-LM06-003 · table2asn](#gsa-lm06-003--table2asn)
- [GSA-LM06-004 · GFF3toolkit](#gsa-lm06-004--gff3toolkit)
- [GSA-LM06-005 · noodles](#gsa-lm06-005--noodles)
- [GSA-LM06-006 · gxfkit](#gsa-lm06-006--gxfkit)

### GSA-LM06-001 · GenomeTools (gt gff3validator)

| field | value |
|---|---|
| type | tool |
| stage | LM06_release / last mile 06 |
| branches | all (S12 freeze) |
| what it does | GFF3 validation, sorting, tidy. |
| url | https://github.com/genometools/genometools |
| doi | [10.1109/TCBB.2013.68](https://doi.org/10.1109/TCBB.2013.68) |
| venue / year | IEEE/ACM Transactions on Computational Biology and Bioinformatics 2013 |
| venue_label | Below allowlist |
| latest release (GitHub API) | v1.6.6 (2025-10-06); last push 2025-11-10 |
| license | custom/other (see repo) |
| plant_evidence | Any genome release. |
| existing_doc | none |
| io | release GFF + FASTA → validated GFF / submission files |
| layer_check | structure |
| verdict | include |
| checked_version | v1.6.6 (2025-10-06) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-LM06-002 · EMBLmyGFF3

| field | value |
|---|---|
| type | tool |
| stage | LM06_release / last mile 06 |
| branches | all (S12 freeze) |
| what it does | Converts GFF3 + FASTA to EMBL flat file for ENA submission. |
| url | https://github.com/NBISweden/EMBLmyGFF3 |
| doi | [10.1186/s13104-018-3686-x](https://doi.org/10.1186/s13104-018-3686-x) |
| venue / year | BMC Research Notes 2018 |
| venue_label | Below allowlist |
| latest release (GitHub API) | v2.4 (2025-07-31); last push 2025-07-31 |
| license | GPL-3.0 |
| plant_evidence | ENA submission of plant annotations. |
| existing_doc | none |
| io | release GFF + FASTA → validated GFF / submission files |
| layer_check | structure |
| verdict | include |
| checked_version | v2.4 (2025-07-31) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-LM06-003 · table2asn

| field | value |
|---|---|
| type | tool |
| stage | LM06_release / last mile 06 |
| branches | all (S12 freeze) |
| what it does | NCBI tool converting GFF3/FASTA to ASN.1 submission with validation report. |
| url | https://www.ncbi.nlm.nih.gov/genbank/table2asn/ |
| doi | none found |
| venue / year | — |
| venue_label | — (no paper) |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | GenBank submission. |
| existing_doc | [`docs/PEER_PIPELINES.md`](../../docs/PEER_PIPELINES.md), [`docs/notes/eviann.md`](../../docs/notes/eviann.md) |
| io | release GFF + FASTA → validated GFF / submission files |
| layer_check | structure |
| verdict | include — update to something already mentioned (not a new tool) |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-LM06-004 · GFF3toolkit

| field | value |
|---|---|
| type | tool |
| stage | LM06_release / last mile 06 |
| branches | all (S12 freeze) |
| what it does | GFF3 QC/fix/merge utilities from the i5k Workspace@NAL. |
| url | https://github.com/NAL-i5K/GFF3toolkit |
| doi | none found |
| venue / year | — |
| venue_label | — (no paper) |
| latest release (GitHub API) | v2.1.0 (2021-12-09); last push 2026-11-04 |
| license | custom/other (see repo) |
| plant_evidence | Arthropod origin, format-generic. |
| existing_doc | none |
| io | release GFF + FASTA → validated GFF / submission files |
| layer_check | structure |
| verdict | include |
| checked_version | v2.1.0 (2021-12-09) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-LM06-005 · noodles

| field | value |
|---|---|
| type | tool |
| stage | LM06_release / last mile 06 |
| branches | all (S12 freeze) |
| what it does | Rust I/O libraries including GFF3/GTF readers and writers. |
| url | https://github.com/zaeleus/noodles |
| doi | none found |
| venue / year | — |
| venue_label | — (no paper) |
| latest release (GitHub API) | tag noodles-vcf-0.96.0; last push 2026-11-09 |
| license | MIT |
| plant_evidence | Building fast custom GFF checks. |
| existing_doc | none |
| io | release GFF + FASTA → validated GFF / submission files |
| layer_check | structure |
| verdict | include |
| checked_version | tag noodles-vcf-0.96.0 |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-LM06-006 · gxfkit

| field | value |
|---|---|
| type | tool |
| stage | LM06_release / last mile 06 |
| branches | all (S12 freeze) |
| what it does | Rust GFF3/GTF conversion aiming at AGAT-compatible output with large speedups. |
| url | https://github.com/benngaihk/gxfkit |
| doi | none found |
| venue / year | — |
| venue_label | — (no paper) |
| latest release (GitHub API) | v0.0.2 (2026-07-06); last push 2026-07-07 |
| license | MIT |
| plant_evidence | Early single-developer project - verify output against AGAT before use. |
| existing_doc | none |
| io | release GFF + FASTA → validated GFF / submission files |
| layer_check | structure |
| verdict | include |
| checked_version | v0.0.2 (2026-07-06) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

[Back to catalog index](../README.md)
