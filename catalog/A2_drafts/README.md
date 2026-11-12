# A2 — drafts (A2 primary, A2b second predictor, A2c transfer, A2d EGAPx, A2e S11 gap-fill, protein evidence)

**Collects:** Gene predictors (evidence-based, ab initio, deep learning), annotation transfer, protein evidence databases.

**Does not collect:** Functional annotation tools; prokaryote-only predictors.

## Entries

- [GSA-A2-001 · GeneMark-ETP](#gsa-a2-001--genemark-etp)
- [GSA-A2-002 · Carbon-A + Carbon Annotation Database (CADB)](#gsa-a2-002--carbon-a--carbon-annotation-database-cadb)
- [GSA-A2-003 · Nucleotide Transformer v3 (NTv3)](#gsa-a2-003--nucleotide-transformer-v3-ntv3)
- [GSA-A2-004 · GENATATORs](#gsa-a2-004--genatators)
- [GSA-A2-005 · AgroNT](#gsa-a2-005--agront)
- [GSA-A2-006 · PlantCaduceus](#gsa-a2-006--plantcaduceus)
- [GSA-A2-007 · Evo 2](#gsa-a2-007--evo-2)
- [GSA-A2-008 · ANNEVO (paper)](#gsa-a2-008--annevo-paper)
- [GSA-A2-009 · GrAnnoT](#gsa-a2-009--grannot)
- [GSA-A2-010 · TOGA (paper)](#gsa-a2-010--toga-paper)
- [GSA-A2-011 · LiftoffTools](#gsa-a2-011--liftofftools)
- [GSA-A2-012 · Rfam 15](#gsa-a2-012--rfam-15)
- [GSA-A2-013 · Infernal 1.1](#gsa-a2-013--infernal-11)
- [GSA-A2-014 · tRNAscan-SE 2.0](#gsa-a2-014--trnascan-se-20)
- [GSA-A2-015 · barrnap](#gsa-a2-015--barrnap)
- [GSA-A2-016 · ShortStack 4](#gsa-a2-016--shortstack-4)
- [GSA-A2-017 · PlantLncBoost](#gsa-a2-017--plantlncboost)
- [GSA-A2-018 · FEELnc](#gsa-a2-018--feelnc)
- [GSA-A2-019 · CPC2](#gsa-a2-019--cpc2)
- [GSA-A2-020 · P-GRe](#gsa-a2-020--p-gre)
- [GSA-A2-021 · Shiu lab PseudogenePipeline](#gsa-a2-021--shiu-lab-pseudogenepipeline)
- [GSA-A2-022 · miRDeep-P2](#gsa-a2-022--mirdeep-p2)

## A2 — evidence-driven gene finder

### GSA-A2-001 · GeneMark-ETP

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / A2 |
| branches | S1 |
| what it does | Gene finder integrating transcript and protein evidence with self-training (core of BRAKER3). |
| url | https://github.com/gatech-genemark/GeneMark-ETP |
| doi | [10.1101/gr.278373.123](https://doi.org/10.1101/gr.278373.123) |
| venue / year | Genome Research 2024 |
| venue_label | Allowlisted |
| latest release (GitHub API) | etp-v1.02-preprint (2023-11-07); last push 2025-04-11 |
| license | no licence file |
| plant_evidence | Large plant genomes; benchmark paper covers plants. |
| existing_doc | [`docs/SCENARIOS.md`](../../docs/SCENARIOS.md) |
| io | `GENOME_SOFT` (+ evidence) → `DRAFT_GFF` / `DRAFT_GFF_B` |
| layer_check | structure |
| verdict | include — update to something already mentioned (not a new tool) |
| checked_version | etp-v1.02-preprint (2023-11-07) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

## A2b / S13 — ab initio and DNA language-model predictors (compare tracks)

### GSA-A2-002 · Carbon-A + Carbon Annotation Database (CADB)

| field | value |
|---|---|
| type | tool + db |
| stage | A2_drafts / A2b (S13 compare) |
| branches | S13 |
| what it does | 1.2B-parameter encoder predicting protein-coding genes from DNA across eukaryotes with per-gene confidence; CADB applies it to GenBank assemblies (566M loci). |
| url | https://huggingface.co/HuggingFaceBio/Carbon-A-1.2B |
| doi | [10.64898/2026.10.20.760448](https://doi.org/10.64898/2026.10.20.760448) |
| venue / year | preprint 2026 |
| venue_label | Preprint |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Includes plants; preprint Oct 2026 - treat as compare track only. |
| existing_doc | none |
| io | `GENOME_SOFT` (+ evidence) → `DRAFT_GFF` / `DRAFT_GFF_B` |
| layer_check | structure |
| verdict | needs evidence |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-003 · Nucleotide Transformer v3 (NTv3)

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / A2b (S13 compare) |
| branches | S13 |
| what it does | Long-context cross-kingdom DNA foundation model; reports gene-annotation performance above ab initio predictors in mammals, plants, insects. |
| url | https://github.com/instadeepai/nucleotide-transformer |
| doi | [10.64898/2025.12.22.695963](https://doi.org/10.64898/2025.12.22.695963) |
| venue / year | preprint 2025 |
| venue_label | Preprint |
| latest release (GitHub API) | tag ntv3-initial-release; last push 2026-11-02 |
| license | custom/other (see repo) |
| plant_evidence | Plant genomes in post-training; preprint.DOI prefix [待确认] |
| existing_doc | [`docs/PEER_PIPELINES.md`](../../docs/PEER_PIPELINES.md), [`docs/RELATED_SOFTWARE.md`](../../docs/RELATED_SOFTWARE.md) |
| io | `GENOME_SOFT` (+ evidence) → `DRAFT_GFF` / `DRAFT_GFF_B` |
| layer_check | structure |
| verdict | include — update to something already mentioned (not a new tool) |
| checked_version | tag ntv3-initial-release |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-004 · GENATATORs

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / A2b (S13 compare) |
| branches | S13 |
| what it does | Ab initio gene annotation with DNA language models (preprint 2026). |
| url | — |
| doi | [10.64898/2026.06.17.732686](https://doi.org/10.64898/2026.06.17.732686) |
| venue / year | preprint 2026 |
| venue_label | Preprint |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | [待确认] plant coverage. |
| existing_doc | none |
| io | `GENOME_SOFT` (+ evidence) → `DRAFT_GFF` / `DRAFT_GFF_B` |
| layer_check | structure |
| verdict | needs evidence |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-005 · AgroNT

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / A2b (S13 compare) |
| branches | S13 |
| what it does | DNA language model trained on 48 edible-plant genomes; downstream tasks include regulatory and splice-site style predictions. |
| url | https://huggingface.co/InstaDeepAI/agro-nucleotide-transformer-1b |
| doi | [10.1038/s42003-024-06465-2](https://doi.org/10.1038/s42003-024-06465-2) |
| venue / year | Communications Biology 2024 |
| venue_label | Below allowlist [待确认: Nature Portfolio journal] |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Plant-specific foundation model; feature source, not a gene caller. |
| existing_doc | none |
| io | `GENOME_SOFT` (+ evidence) → `DRAFT_GFF` / `DRAFT_GFF_B` |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-006 · PlantCaduceus

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / A2b (S13 compare) |
| branches | S13 |
| what it does | Cross-species plant DNA language model at single-nucleotide resolution (splice/TIS/TTS annotation tasks). |
| url | https://github.com/kuleshov-group/PlantCaduceus |
| doi | [10.1073/pnas.2421738122](https://doi.org/10.1073/pnas.2421738122) |
| venue / year | PNAS 2025 |
| venue_label | Below allowlist |
| latest release (GitHub API) | —; last push 2026-08-07 |
| license | Apache-2.0 |
| plant_evidence | Trained on 16 angiosperms; feature source for annotation QC. |
| existing_doc | none |
| io | `GENOME_SOFT` (+ evidence) → `DRAFT_GFF` / `DRAFT_GFF_B` |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-007 · Evo 2

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / A2b (S13 compare) |
| branches | S13 |
| what it does | Genome language model across domains of life; zero-shot features for exon/intron and variant effect. |
| url | https://github.com/ArcInstitute/evo2 |
| doi | [10.1101/2025.02.18.638918](https://doi.org/10.1101/2025.02.18.638918) |
| venue / year | preprint 2025 |
| venue_label | Preprint |
| latest release (GitHub API) | v0.5.0 (2026-02-28); last push 2026-06-19 |
| license | Apache-2.0 |
| plant_evidence | Idea-level for annotation; large GPU needs. |
| existing_doc | none |
| io | `GENOME_SOFT` (+ evidence) → `DRAFT_GFF` / `DRAFT_GFF_B` |
| layer_check | structure |
| verdict | needs evidence |
| checked_version | v0.5.0 (2026-02-28) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-008 · ANNEVO (paper)

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / A2b (S13 compare) |
| branches | S13 |
| what it does | Deep-learning ab initio annotation modelling evolutionary context (preprint version of the tool already noted in this repo). |
| url | https://github.com/xjtu-omics/ANNEVO |
| doi | [10.21203/rs.3.rs-6402260/v1](https://doi.org/10.21203/rs.3.rs-6402260/v1) |
| venue / year | preprint 2025 |
| venue_label | Preprint |
| latest release (GitHub API) | v2.3.2 (2026-06-07); last push 2026-08-11 |
| license | custom/other (see repo) |
| plant_evidence | Plant models exist; non-commercial licence. |
| existing_doc | [`README.md`](../../README.md), [`README.zh.md`](../../README.zh.md), [`docs/COMPARE_HELIXER_BRAKER.md`](../../docs/COMPARE_HELIXER_BRAKER.md) |
| io | `GENOME_SOFT` (+ evidence) → `DRAFT_GFF` / `DRAFT_GFF_B` |
| layer_check | structure |
| verdict | include — update to something already mentioned (not a new tool) |
| checked_version | v2.3.2 (2026-06-07) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

## A2c — annotation transfer

### GSA-A2-009 · GrAnnoT

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / A2c |
| branches | S11, S4 |
| what it does | Transfers GFF3 annotation through a pangenome graph (GFA) to embedded genomes; outputs graph annotation (GAF) and per-genome GFF3. |
| url | https://forge.ird.fr/diade/dynadiv/grannot |
| doi | [10.24072/pcjournal.651](https://doi.org/10.24072/pcjournal.651) |
| venue / year | Peer Community Journal 2025 |
| venue_label | Below allowlist |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Pangenome-aware transfer between grapevine haplotypes/accessions. |
| existing_doc | none |
| io | reference GFF + genomes / graph → transferred GFF |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-010 · TOGA (paper)

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / A2c |
| branches | S11, S4 |
| what it does | Annotation projection integrated with orthology inference from whole-genome alignments. |
| url | https://github.com/hillerlab/TOGA |
| doi | [10.1126/science.abn3107](https://doi.org/10.1126/science.abn3107) |
| venue / year | Science 2023 |
| venue_label | Allowlisted |
| latest release (GitHub API) | v1.1.7 (2024-01-17); last push 2025-11-23 |
| license | MIT |
| plant_evidence | Vertebrate-developed; TOGA2 already noted here. |
| existing_doc | [`docs/EVALUATION.md`](../../docs/EVALUATION.md), [`docs/PEER_PIPELINES.md`](../../docs/PEER_PIPELINES.md), [`docs/RELATED_SOFTWARE.md`](../../docs/RELATED_SOFTWARE.md) |
| io | reference GFF + genomes / graph → transferred GFF |
| layer_check | structure |
| verdict | include — update to something already mentioned (not a new tool) |
| checked_version | v1.1.7 (2024-01-17) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-011 · LiftoffTools

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / A2c |
| branches | S11, S4 |
| what it does | Compares annotations mapped between assemblies: sequence variants in genes, synteny, copy-number changes. |
| url | https://github.com/agshumate/LiftoffTools |
| doi | [10.12688/f1000research.124059.2](https://doi.org/10.12688/f1000research.124059.2) |
| venue / year | F1000Research 2024 |
| venue_label | Below allowlist |
| latest release (GitHub API) | v0.4.4 (2022-10-19); last push 2023-08-01 |
| license | GPL-3.0 |
| plant_evidence | Check Liftoff transfers between grapevine haplotypes. |
| existing_doc | none |
| io | reference GFF + genomes / graph → transferred GFF |
| layer_check | structure |
| verdict | include |
| checked_version | v0.4.4 (2022-10-19) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

## Non-coding and pseudogene loci — extra annotation tracks [待确认: stage placement; kept apart from the protein-coding release]

### GSA-A2-012 · Rfam 15

| field | value |
|---|---|
| type | db |
| stage | A2_drafts / non-coding track |
| branches | any |
| what it does | RNA family covariance models; scan with Infernal cmscan for rRNA, snoRNA, riboswitch-like loci. |
| url | https://rfam.org |
| doi | [10.1093/nar/gkae1023](https://doi.org/10.1093/nar/gkae1023) |
| venue / year | Nucleic Acids Research 2024 |
| venue_label | Allowlisted |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Plant snoRNA/rRNA/miRNA precursors. |
| existing_doc | none |
| io | `GENOME_FA` / transcripts → ncRNA or pseudogene GFF track |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-013 · Infernal 1.1

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / non-coding track |
| branches | any |
| what it does | Covariance-model RNA homology search (engine for Rfam). |
| url | https://github.com/EddyRivasLab/infernal |
| doi | [10.1093/bioinformatics/btt509](https://doi.org/10.1093/bioinformatics/btt509) |
| venue / year | Bioinformatics 2013 |
| venue_label | Below allowlist |
| latest release (GitHub API) | tag ssu-align-0.1@4835; last push 2026-11-12 |
| license | custom/other (see repo) |
| plant_evidence | All eukaryotes. |
| existing_doc | none |
| io | `GENOME_FA` / transcripts → ncRNA or pseudogene GFF track |
| layer_check | structure |
| verdict | include |
| checked_version | tag ssu-align-0.1@4835 |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-014 · tRNAscan-SE 2.0

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / non-coding track |
| branches | any |
| what it does | tRNA gene detection with isotype classification and pseudo-tRNA flags. |
| url | https://github.com/UCSC-LoweLab/tRNAscan-SE |
| doi | [10.1093/nar/gkab688](https://doi.org/10.1093/nar/gkab688) |
| venue / year | Nucleic Acids Research 2021 |
| venue_label | Allowlisted |
| latest release (GitHub API) | v2.0.13 (2026-07-05); last push 2026-07-05 |
| license | GPL-3.0 |
| plant_evidence | Nuclear and organellar tRNAs. |
| existing_doc | [`docs/notes/ncrna_tesorter.md`](../../docs/notes/ncrna_tesorter.md) |
| io | `GENOME_FA` / transcripts → ncRNA or pseudogene GFF track |
| layer_check | structure |
| verdict | include — update to something already mentioned (not a new tool) |
| checked_version | v2.0.13 (2026-07-05) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-015 · barrnap

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / non-coding track |
| branches | any |
| what it does | Fast rRNA locus prediction (includes eukaryotic models). |
| url | https://github.com/tseemann/barrnap |
| doi | none found |
| venue / year | — |
| venue_label | — (no paper) |
| latest release (GitHub API) | v1.10.5 (2026-04-12); last push 2026-04-12 |
| license | GPL-3.0 |
| plant_evidence | Quick rDNA-array marking in assemblies. |
| existing_doc | none |
| io | `GENOME_FA` / transcripts → ncRNA or pseudogene GFF track |
| layer_check | structure |
| verdict | include |
| checked_version | v1.10.5 (2026-04-12) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-016 · ShortStack 4

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / non-coding track |
| branches | any |
| what it does | Small-RNA locus annotation and MIRNA calling from sRNA-seq. |
| url | https://github.com/MikeAxtell/ShortStack |
| doi | [10.1261/rna.035279.112](https://doi.org/10.1261/rna.035279.112) |
| venue / year | RNA 2013 |
| venue_label | Below allowlist |
| latest release (GitHub API) | v4.1.2 (2025-05-24); last push 2025-10-23 |
| license | MIT |
| plant_evidence | Plant-developed; miRNA and phasiRNA loci.DOI is the original paper; v4 release notes on GitHub |
| existing_doc | none |
| io | `GENOME_FA` / transcripts → ncRNA or pseudogene GFF track |
| layer_check | structure |
| verdict | include |
| checked_version | v4.1.2 (2025-05-24) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-017 · PlantLncBoost

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / non-coding track |
| branches | any |
| what it does | Gradient-boosting plant lncRNA identification from sequence features. |
| url | https://github.com/xuechantian/PlantLncBoost |
| doi | [10.1111/nph.70211](https://doi.org/10.1111/nph.70211) |
| venue / year | New Phytologist 2025 |
| venue_label | Below allowlist |
| latest release (GitHub API) | —; last push 2025-03-24 |
| license | no licence file |
| plant_evidence | Plant-specific lncRNA calling after transcript assembly.GitHub path [待确认] |
| existing_doc | none |
| io | `GENOME_FA` / transcripts → ncRNA or pseudogene GFF track |
| layer_check | structure |
| verdict | needs evidence |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-018 · FEELnc

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / non-coding track |
| branches | any |
| what it does | lncRNA annotation from transcript assemblies (filter, coding potential, classifier). |
| url | https://github.com/tderrien/FEELnc |
| doi | [10.1093/nar/gkw1306](https://doi.org/10.1093/nar/gkw1306) |
| venue / year | Nucleic Acids Research 2017 |
| venue_label | Allowlisted |
| latest release (GitHub API) | v.0.2.1 (2022-07-20); last push 2025-07-23 |
| license | GPL-3.0 |
| plant_evidence | Any eukaryote. |
| existing_doc | none |
| io | `GENOME_FA` / transcripts → ncRNA or pseudogene GFF track |
| layer_check | structure |
| verdict | include |
| checked_version | v.0.2.1 (2022-07-20) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-019 · CPC2

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / non-coding track |
| branches | any |
| what it does | Fast coding-potential calculator for transcripts. |
| url | https://cpc2.gao-lab.org/ |
| doi | [10.1093/nar/gkx428](https://doi.org/10.1093/nar/gkx428) |
| venue / year | Nucleic Acids Research 2017 |
| venue_label | Allowlisted |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Species-neutral coding potential filter. |
| existing_doc | none |
| io | `GENOME_FA` / transcripts → ncRNA or pseudogene GFF track |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-020 · P-GRe

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / non-coding track |
| branches | any |
| what it does | Pseudogene prediction: finds loci from parent proteins, rebuilds pseudo-CDS, reports frameshifts/stops, outputs GFF. |
| url | — |
| doi | [10.1016/j.ygeno.2026.111216](https://doi.org/10.1016/j.ygeno.2026.111216) |
| venue / year | Genomics 2026 |
| venue_label | Below allowlist |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Designed for plants/eukaryotes. |
| existing_doc | none |
| io | `GENOME_FA` / transcripts → ncRNA or pseudogene GFF track |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-021 · Shiu lab PseudogenePipeline

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / non-coding track |
| branches | any |
| what it does | Classic plant pseudogene pipeline with repeat filtering and GFF output. |
| url | https://github.com/ShiuLab/PseudogenePipeline |
| doi | none found |
| venue / year | — |
| venue_label | — (no paper) |
| latest release (GitHub API) | v1.0.0 (2022-05-10); last push 2023-06-08 |
| license | CC0-1.0 |
| plant_evidence | Arabidopsis/rice-era plant pipeline. |
| existing_doc | none |
| io | `GENOME_FA` / transcripts → ncRNA or pseudogene GFF track |
| layer_check | structure |
| verdict | include |
| checked_version | v1.0.0 (2022-05-10) |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

### GSA-A2-022 · miRDeep-P2

| field | value |
|---|---|
| type | tool |
| stage | A2_drafts / non-coding track |
| branches | any |
| what it does | Fast plant miRNA locus discovery from sRNA-seq with updated plant criteria. |
| url | — |
| doi | [10.1093/bioinformatics/bty972](https://doi.org/10.1093/bioinformatics/bty972) |
| venue / year | Bioinformatics 2018 |
| venue_label | Below allowlist |
| latest release (GitHub API) | — |
| license | — |
| plant_evidence | Plant-specific. |
| existing_doc | none |
| io | `GENOME_FA` / transcripts → ncRNA or pseudogene GFF track |
| layer_check | structure |
| verdict | include |
| checked_version | — |
| checked_at_CST | 2026-11-12 |
| checked_by | overnight survey (DOI via Crossref/DataCite, repo via GitHub API) |

[Back to catalog index](../README.md)
