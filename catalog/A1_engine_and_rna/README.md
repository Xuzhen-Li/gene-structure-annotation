# A1 / A1b — engine choice and RNA / Iso-Seq evidence

**Collects:** RNA and Iso-Seq alignment, transcript assembly (evidence and compare set), translation and coding-potential evidence, engine-choice rules.

**Does not collect:** Pangenome-level expression analysis (vitis-pangenome).

## Entries

- [GSA-A1-001 · StringTie (v3 line)](#gsa-a1-001--stringtie-v3-line)
- [GSA-A1-002 · FLIC (Full-length isoform constructor)](#gsa-a1-002--flic-full-length-isoform-constructor)
- [GSA-A1-003 · Isocall](#gsa-a1-003--isocall)
- [GSA-A1-004 · ESPRESSO](#gsa-a1-004--espresso)
- [GSA-A1-005 · TAGET](#gsa-a1-005--taget)
- [GSA-A1-006 · LRGASP benchmark](#gsa-a1-006--lrgasp-benchmark)
- [GSA-A1-007 · KuPID](#gsa-a1-007--kupid)
- [GSA-A1-008 · RiboCode](#gsa-a1-008--ribocode)
- [GSA-A1-009 · Ribo-TISH](#gsa-a1-009--ribo-tish)
- [GSA-A1-010 · PhyloCSF++](#gsa-a1-010--phylocsf)
- [GSA-A1-011 · RiboBA](#gsa-a1-011--riboba)

## Transcript evidence

### GSA-A1-001 · StringTie (v3 line)

| field | value |
|---|---|
| type | tool |
| stage | A1_engine_and_rna / A1b |
| branches | S1, S3 |
| what it does | Reference-guided / de novo transcript assembly from short and long RNA reads; used as transcript evidence and as the compare track. |
| url | https://github.com/gpertea/stringtie |
| doi | [10.1186/s13059-019-1910-1](https://doi.org/10.1186/s13059-019-1910-1) |
| venue / year | Genome Biology 2019 |
| venue_label | Allowlisted |
| latest release (GitHub API) | v3.0.3 (2025-11-13); last push 2026-11-11 |
| license | MIT |
| plant_evidence | Standard plant evidence track; check release notes for long-read mode changes. |
| existing_doc | [`README.md`](../../README.md), [`README.zh.md`](../../README.zh.md), [`docs/DETAILED_GUIDE.md`](../../docs/DETAILED_GUIDE.md) |
| io | RNA / long-read FASTQ → `RNA_BAM`, transcript GTF (evidence / compare) |
| layer_check | structure |
| verdict | include — update to something already mentioned (not a new tool) |
| checked_version | v3.0.3 (2025-11-13) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A1-002 · FLIC (Full-length isoform constructor)

| field | value |
|---|---|
| type | tool |
| stage | A1_engine_and_rna / A1b |
| branches | S1, S3 |
| what it does | Builds full-length isoforms from long reads using replicate concordance and TSS/polyA peak calling. |
| url | https://github.com/albidgy/FLIC |
| doi | [10.1093/bioinformatics/btaf551](https://doi.org/10.1093/bioinformatics/btaf551) |
| venue / year | Bioinformatics 2025 |
| venue_label | Below allowlist |
| latest release (GitHub API) | —; last push 2026-09-01 |
| license | MIT |
| plant_evidence | Benchmarked on Arabidopsis cDNA; useful where reference annotation is weak. |
| existing_doc | none |
| io | RNA / long-read FASTQ → `RNA_BAM`, transcript GTF (evidence / compare) |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A1-003 · Isocall

| field | value |
|---|---|
| type | tool |
| stage | A1_engine_and_rna / A1b |
| branches | S1, S3 |
| what it does | Joint calling of known and novel isoforms across many PacBio Iso-Seq samples (alternative to isoseq cluster/collapse). |
| url | https://github.com/PacificBiosciences/isocall |
| doi | none found |
| venue / year | — |
| venue_label | — (no paper) |
| latest release (GitHub API) | 1.3.0 (2026-08-06); last push 2026-08-06 |
| license | custom/other (see repo) |
| plant_evidence | Multi-tissue Iso-Seq for plant annotation; vendor marks it as in active development. |
| existing_doc | none |
| io | RNA / long-read FASTQ → `RNA_BAM`, transcript GTF (evidence / compare) |
| layer_check | structure |
| verdict | include |
| checked_version | 1.3.0 (2026-08-06) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A1-004 · ESPRESSO

| field | value |
|---|---|
| type | tool |
| stage | A1_engine_and_rna / A1b |
| branches | S1, S3 |
| what it does | Discovery and quantification of isoforms from error-prone long-read RNA-seq. |
| url | https://github.com/Xinglab/espresso |
| doi | [10.1126/sciadv.abq5072](https://doi.org/10.1126/sciadv.abq5072) |
| venue / year | Science Advances 2023 |
| venue_label | Allowlisted |
| latest release (GitHub API) | v1.6.0 (2025-09-19); last push 2026-03-19 |
| license | custom/other (see repo) |
| plant_evidence | ONT cDNA/direct RNA evidence; developed on human data. |
| existing_doc | none |
| io | RNA / long-read FASTQ → `RNA_BAM`, transcript GTF (evidence / compare) |
| layer_check | structure |
| verdict | include |
| checked_version | v1.6.0 (2025-09-19) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A1-005 · TAGET

| field | value |
|---|---|
| type | tool |
| stage | A1_engine_and_rna / A1b |
| branches | S1, S3 |
| what it does | Iso-Seq toolkit: alignment with CNN splice-site correction, isoform classification, expression. |
| url | — |
| doi | [10.1038/s41467-023-41649-0](https://doi.org/10.1038/s41467-023-41649-0) |
| venue / year | Nature Communications 2023 |
| venue_label | Allowlisted |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Human-tumour development; usable for any eukaryote with a reference [待确认 plant use]. Code link: see paper [待确认]. |
| existing_doc | none |
| io | RNA / long-read FASTQ → `RNA_BAM`, transcript GTF (evidence / compare) |
| layer_check | structure |
| verdict | needs evidence |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A1-006 · LRGASP benchmark

| field | value |
|---|---|
| type | idea |
| stage | A1_engine_and_rna / A1b |
| branches | S1, S3 |
| what it does | Community benchmark of long-read RNA-seq methods for transcript identification and quantification; shows trade-offs between read depth, length and accuracy. |
| url | https://github.com/LRGASP/lrgasp-submissions |
| doi | [10.1038/s41592-024-02298-3](https://doi.org/10.1038/s41592-024-02298-3) |
| venue / year | Nature Methods 2024 |
| venue_label | Allowlisted |
| latest release (GitHub API) | — |
| license | MIT |
| plant_evidence | Choose long-read evidence strategy for plant annotation; includes non-model organism data. |
| existing_doc | none |
| io | RNA / long-read FASTQ → `RNA_BAM`, transcript GTF (evidence / compare) |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A1-007 · KuPID

| field | value |
|---|---|
| type | tool |
| stage | A1_engine_and_rna / A1b |
| branches | S1, S3 |
| what it does | k-mer-based upstream preprocessing of long reads for isoform discovery (preprint). |
| url | — |
| doi | [10.64898/2025.12.05.692400](https://doi.org/10.64898/2025.12.05.692400) |
| venue / year | preprint 2025 |
| venue_label | Preprint |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | [待确认] plant tests. |
| existing_doc | none |
| io | RNA / long-read FASTQ → `RNA_BAM`, transcript GTF (evidence / compare) |
| layer_check | structure |
| verdict | needs evidence |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

## Translation and coding-potential evidence

### GSA-A1-008 · RiboCode

| field | value |
|---|---|
| type | tool |
| stage | A1_engine_and_rna / A1b |
| branches | S1, S3 (optional) |
| what it does | Identifies actively translated ORFs from ribosome-profiling data. |
| url | https://github.com/xryanglab/RiboCode |
| doi | [10.1093/nar/gky179](https://doi.org/10.1093/nar/gky179) |
| venue / year | Nucleic Acids Research 2018 |
| venue_label | Allowlisted |
| latest release (GitHub API) | v1.2.13 (2021-12-28); last push 2022-07-29 |
| license | MIT |
| plant_evidence | Ribo-seq support for CDS boundaries, uORFs and small ORFs in plants. |
| existing_doc | none |
| io | Ribo-seq reads or multi-genome alignment → ORF / coding-evidence track |
| layer_check | structure |
| verdict | include |
| checked_version | v1.2.13 (2021-12-28) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A1-009 · Ribo-TISH

| field | value |
|---|---|
| type | tool |
| stage | A1_engine_and_rna / A1b |
| branches | S1, S3 (optional) |
| what it does | Translation initiation sites and ORFs from (QTI-seq / regular) Ribo-seq. |
| url | https://github.com/zhpn1024/ribotish |
| doi | [10.1038/s41467-017-01981-8](https://doi.org/10.1038/s41467-017-01981-8) |
| venue / year | Nature Communications 2017 |
| venue_label | Allowlisted |
| latest release (GitHub API) | v0.2.8 (2025-10-21); last push 2025-10-21 |
| license | GPL-3.0 |
| plant_evidence | Start-codon evidence for CDS curation. |
| existing_doc | none |
| io | Ribo-seq reads or multi-genome alignment → ORF / coding-evidence track |
| layer_check | structure |
| verdict | include |
| checked_version | v0.2.8 (2025-10-21) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A1-010 · PhyloCSF++

| field | value |
|---|---|
| type | tool |
| stage | A1_engine_and_rna / A1b |
| branches | S1, S3 (optional) |
| what it does | Fast PhyloCSF: codon-substitution evidence of protein-coding potential from multi-species alignments. |
| url | https://github.com/cpockrandt/PhyloCSFpp |
| doi | [10.1093/bioinformatics/btab756](https://doi.org/10.1093/bioinformatics/btab756) |
| venue / year | Bioinformatics 2021 |
| venue_label | Below allowlist |
| latest release (GitHub API) | v1.2.0 (2022-01-04); last push 2022-01-26 |
| license | custom/other (see repo) |
| plant_evidence | Coding-vs-noncoding evidence where a whole-genome alignment of relatives exists. |
| existing_doc | none |
| io | Ribo-seq reads or multi-genome alignment → ORF / coding-evidence track |
| layer_check | structure |
| verdict | include |
| checked_version | v1.2.0 (2022-01-04) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A1-011 · RiboBA

| field | value |
|---|---|
| type | tool |
| stage | A1_engine_and_rna / A1b |
| branches | S1, S3 (optional) |
| what it does | Bias-aware probabilistic ORF identification across Ribo-seq protocols (preprint). |
| url | — |
| doi | [10.64898/2026.03.17.712439](https://doi.org/10.64898/2026.03.17.712439) |
| venue / year | preprint 2026 |
| venue_label | Preprint |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Ribo-seq CDS evidence [待确认] plant tests. |
| existing_doc | none |
| io | Ribo-seq reads or multi-genome alignment → ORF / coding-evidence track |
| layer_check | structure |
| verdict | needs evidence |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

[Back to catalog index](../README.md)
