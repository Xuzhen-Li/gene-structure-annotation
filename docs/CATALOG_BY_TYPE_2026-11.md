# Software, databases and ideas by type (structural) — 2026-11

Second pass of the 2026-11 survey, sorted **by type** (按类型分类). It adds classic tools the pipelines already use and well-known tools the first pass skipped, so that the two files together form one inventory. It is a reading list: nothing here changes the default path in [`TOOLS.md`](TOOLS.md).

**Boundary (unchanged, see [`BOUNDARY.md`](BOUNDARY.md)).** Only things that make or check coordinates, GFF3 and proteins. TE *library construction* belongs to [`vitis-te`](https://github.com/Xuzhen-Li/vitis-te) and is not listed; soft-masking uses a trusted library only. NLR/TF/HRP classifiers, GO/KEGG and names live in [gene-function-annotation](https://github.com/Xuzhen-Li/gene-function-annotation).

First-pass file: [`CATALOG_NEW_TOOLS_2026-11.md`](CATALOG_NEW_TOOLS_2026-11.md). Rows already there are **not repeated**; the last section lists them by the same type classes so every entry has one class.

`·in repo` = the name already appears in this repo's docs (TOOLS, tools cards, notes, steps); the row adds the citation, release and type. `[待确认]` = something still unverified (named in the row). `[preprint]` = preprint only.

Snapshot: 2026-11-13 (Asia/Shanghai). DOIs resolved in Crossref (DataCite for Zenodo/Bioconductor) and titles matched; GitHub release/push dates from the GitHub API; other links by HTTP request, all on the same day.

## Type classes

| Type-class | Covers | New rows | First-pass rows |
|---|---|---|---|
| [assembly-qc](#assembly-qc) | Assembly and assembly QC that decide what gets annotated (Asm0, Asm1) | 16 | 1 |
| [soft-mask](#soft-mask) | Masking with a trusted library or library-free low-complexity masking (A0). No TE library construction. | 4 | 1 |
| [rna-evidence](#rna-evidence) | RNA-seq / Iso-Seq alignment, assembly and ORF calling (A1b) | 12 | 10 |
| [protein-evidence](#protein-evidence) | Protein-to-genome alignment (A2 inputs) | 4 | 0 |
| [ab-initio](#ab-initio) | Ab initio / evidence-hinted gene finders (A2) | 7 | 2 |
| [language-model](#language-model) | DNA language-model gene predictors (A2 / S13) | 0 | 6 |
| [lift-over](#lift-over) | Annotation transfer and homology-based projection (A2b / S11 / S4) | 4 | 4 |
| [combiner-pipeline](#combiner-pipeline) | Combiners and whole annotation pipelines (A4) | 8 | 3 |
| [ncrna-pseudogene](#ncrna-pseudogene) | Non-coding RNA and pseudogene loci | 5 | 10 |
| [model-qc](#model-qc) | Gene-model QC, protein extraction and comparison (A3, A5, LM01, LM02) | 3 | 2 |
| [curation-browser](#curation-browser) | Browsers, evidence packs and editors (LM03, LM04) | 4 | 2 |
| [gff-release](#gff-release) | GFF3 cleanup, validation and submission (LM06, A6) | 2 | 6 |
| [database](#database) | Reference genomes/annotations used as evidence | 4 | 1 |
| [standard-review](#standard-review) | Standards, formats and reviews | 5 | 3 |
| [idea](#idea) | Ideas not yet tied to one tool | 0 | 6 |

New rows in this file: 78. First-pass rows (indexed, not repeated): 57. Combined inventory: 135.

Columns: Name, Type (software / database / idea / software+database / database+software), Type-class, Stage, Year / latest release, What it does, Plant / eukaryote relevance, Source.

## Contents

- [assembly-qc](#assembly-qc) (16)
- [soft-mask](#soft-mask) (4)
- [rna-evidence](#rna-evidence) (12)
- [protein-evidence](#protein-evidence) (4)
- [ab-initio](#ab-initio) (7)
- [language-model](#language-model) (0)
- [lift-over](#lift-over) (4)
- [combiner-pipeline](#combiner-pipeline) (8)
- [ncrna-pseudogene](#ncrna-pseudogene) (5)
- [model-qc](#model-qc) (3)
- [curation-browser](#curation-browser) (4)
- [gff-release](#gff-release) (2)
- [database](#database) (4)
- [standard-review](#standard-review) (5)
- [idea](#idea) (0)
- [First-pass entries by type-class](#first-pass-entries-by-type-class)
- [Not verified yet](#not-verified-yet)
- [How entries were checked](#how-entries-were-checked)

## assembly-qc

Assembly and assembly QC that decide what gets annotated (Asm0, Asm1).

| Name | Type | Type-class | Stage | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|---|---|
| hifiasm ·in repo | software | assembly-qc | Asm0 | Nature Methods 2021; release 0.25.0 (2025-03-18); last push 2026-05-31 | Haplotype-resolved de novo assembler for PacBio HiFi reads (trio, Hi-C or ultra-long phasing modes). | Standard input assembler for heterozygous plant clones such as grapevine; decides how many haplotypes get annotated. | doi:[10.1038/s41592-020-01056-5](https://doi.org/10.1038/s41592-020-01056-5) · [GitHub](https://github.com/chhylp123/hifiasm) |
| Verkko | software | assembly-qc | Asm0 | Nature Biotechnology 2023; release v2.3.2 (2026-03-11); last push 2026-11-11 | Telomere-to-telomere diploid assembly combining HiFi and ultra-long ONT reads in a graph. | T2T plant haplotypes as annotation input. | doi:[10.1038/s41587-023-01662-6](https://doi.org/10.1038/s41587-023-01662-6) · [GitHub](https://github.com/marbl/verkko) |
| YaHS ·in repo | software | assembly-qc | Asm0 | Bioinformatics 2023; release v1.2.2 (2024-09-30); last push 2024-11-04 | Hi-C scaffolder producing chromosome-scale scaffolds from contigs. | Chromosome-level scaffolds before annotation; any eukaryote. | doi:[10.1093/bioinformatics/btac808](https://doi.org/10.1093/bioinformatics/btac808) · [GitHub](https://github.com/c-zhou/yahs) |
| RagTag | software | assembly-qc | Asm0 | Genome Biology 2022; release v2.1.1 (2026-10-01); last push 2026-10-01 | Reference-guided correction, scaffolding and patching of draft assemblies. | Order haplotype contigs onto a close reference (e.g. PN40024) before annotation. | doi:[10.1186/s13059-022-02823-7](https://doi.org/10.1186/s13059-022-02823-7) · [GitHub](https://github.com/malonge/RagTag) |
| GenomeScope 2.0 / Smudgeplot | software | assembly-qc | Asm1 | Nature Communications 2020; release v2.0.1 (2024-07-10); last push 2025-10-02 | k-mer profiling of genome size, heterozygosity and ploidy from reads. | Sanity check of expected size/heterozygosity for clonal or polyploid plants. | doi:[10.1038/s41467-020-14998-3](https://doi.org/10.1038/s41467-020-14998-3) · [GitHub](https://github.com/tbenavi1/genomescope2.0) |
| Merqury ·in repo | software | assembly-qc | Asm1 | Genome Biology 2020; release v1.4.1 (2026-07-06); last push 2026-07-06 | Reference-free k-mer QV, completeness and phasing assessment of assemblies. | Haplotype QV before annotation; any eukaryote. | doi:[10.1186/s13059-020-02134-9](https://doi.org/10.1186/s13059-020-02134-9) · [GitHub](https://github.com/marbl/merqury) |
| QUAST ·in repo | software | assembly-qc | Asm1 | Bioinformatics 2013; release quast_5.3.0 (2024-11-10); last push 2026-06-10 | Assembly contiguity and misassembly statistics, optionally against a reference. | Basic Asm1 metrics. | doi:[10.1093/bioinformatics/btt086](https://doi.org/10.1093/bioinformatics/btt086) · [GitHub](https://github.com/ablab/quast) |
| Inspector | software | assembly-qc | Asm1 | Genome Biology 2021; release v1.3 (2024-08-25); last push 2024-08-25 | Reference-free assembly evaluation and error correction using long reads. | Finds structural assembly errors that would break gene models. | doi:[10.1186/s13059-021-02527-4](https://doi.org/10.1186/s13059-021-02527-4) · [GitHub](https://github.com/Maggi-Chen/Inspector) |
| KAT (K-mer Analysis Toolkit) | software | assembly-qc | Asm1 | Bioinformatics 2017; release Release-2.4.1 (2018-04-10); last push 2022-11-25 | k-mer spectra comparison of reads vs assembly (copy-number plots). | Detects collapsed or duplicated haplotypes. | doi:[10.1093/bioinformatics/btw663](https://doi.org/10.1093/bioinformatics/btw663) · [GitHub](https://github.com/EarlhamInst/KAT) |
| BlobToolKit | software | assembly-qc | Asm1 | G3 Genes/Genomes/Genetics 2020; release 4.5.4 (2026-08-05); last push 2026-08-05 | Interactive GC/coverage/taxonomy plots to spot contaminant contigs. | Complements FCS-GX for plant assemblies with endophytes/pathogens. | doi:[10.1534/g3.119.400908](https://doi.org/10.1534/g3.119.400908) · [GitHub](https://github.com/genomehubs/blobtoolkit) |
| Tiara | software | assembly-qc | Asm1 | Bioinformatics 2022; release v1.0.3 (2022-10-30); last push 2024-03-02 | Deep-learning classification of contigs into nuclear, organellar and prokaryotic origin. | Flags plastid/mitochondrial contigs before nuclear gene annotation. | doi:[10.1093/bioinformatics/btab672](https://doi.org/10.1093/bioinformatics/btab672) · [GitHub](https://github.com/ibe-uw/tiara) |
| tidk | software | assembly-qc | Asm1 | Bioinformatics 2025; release v0.3.2 (2026-11-01); last push 2026-11-01 | Finds and plots telomeric repeats along an assembly. | Checks chromosome ends (plant TTTAGGG repeat). | doi:[10.1093/bioinformatics/btaf049](https://doi.org/10.1093/bioinformatics/btaf049) · [GitHub](https://github.com/tolkit/telomeric-identifier) |
| quarTeT | software | assembly-qc | Asm1 | Horticulture Research 2023; release v1.3.1 (2026-06-21); last push 2026-06-23 | Telomere-to-telomere toolkit: reference-guided assembly, gap filling, telomere and centromere identification. | Built and tested on plant genomes (Horticulture Research). | doi:[10.1093/hr/uhad127](https://doi.org/10.1093/hr/uhad127) · [GitHub](https://github.com/aaranyue/quarTeT) |
| GCI | software | assembly-qc | Asm1 | Bioinformatics 2024; release v1.1 (2026-10-13); last push 2026-11-02 | Genome Continuity Inspector: read-mapping based continuity score for near-complete assemblies. | Continuity check for T2T plant haplotypes. | doi:[10.1093/bioinformatics/btae633](https://doi.org/10.1093/bioinformatics/btae633) · [GitHub](https://github.com/yeeus/GCI) |
| gfastats | software | assembly-qc | Asm1 | Bioinformatics 2022; release v1.3.11 (2025-05-09); last push 2026-06-18 | Fast summary statistics and manipulation of FASTA/GFA assemblies. | Quick Asm1 metrics and AGP handling. | doi:[10.1093/bioinformatics/btac460](https://doi.org/10.1093/bioinformatics/btac460) · [GitHub](https://github.com/vgl-hub/gfastats) |
| CRAQ | software | assembly-qc | Asm1 | release v1.10 (2025-09-03); last push 2025-12-03 | Reference-free assembly assessment from clipped-read alignments (regional and structural errors). | [待确认] Developed on plant genomes. (no peer-reviewed paper found in this pass) | [GitHub](https://github.com/JiaoLaboratory/CRAQ) |

[Back to contents](#contents)

## soft-mask

Masking with a trusted library or library-free low-complexity masking (A0). No TE library construction..

| Name | Type | Type-class | Stage | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|---|---|
| RepeatMasker ·in repo | software | soft-mask | A0 | release v4.2.6 (2026-10-13); last push 2026-10-13 | Masks repeats with a supplied library (Dfam or a curated species library); -xsmall gives soft-masking. | Main A0 engine; use only with the trusted library from vitis-te. (no peer-reviewed paper found in this pass) | [GitHub](https://github.com/Dfam-consortium/RepeatMasker) · [site](https://www.repeatmasker.org/) |
| Dfam | database | soft-mask | A0 | Mobile DNA 2021 | Open database of TE families and profile HMMs used by RepeatMasker. | Plant coverage is thinner than for animals; species library from vitis-te stays primary. | doi:[10.1186/s13100-020-00230-y](https://doi.org/10.1186/s13100-020-00230-y) · [site](https://www.dfam.org/) |
| Tandem Repeats Finder (TRF) ·in repo | software | soft-mask | A0 | Nucleic Acids Research 1999; release v4.09.1 (2020-06-29); last push 2023-01-16 | Detects tandem repeats. | Mask satellites/tandem arrays that are not in the TE library. | doi:[10.1093/nar/27.2.573](https://doi.org/10.1093/nar/27.2.573) · [GitHub](https://github.com/Benson-Genomics-Lab/TRF) |
| WindowMasker | software | soft-mask | A0 | Bioinformatics 2006 | Library-free masking of over-represented k-mers (NCBI). | Low-complexity/over-represented sequence only; not a TE library. | doi:[10.1093/bioinformatics/bti774](https://doi.org/10.1093/bioinformatics/bti774) · [site](https://www.ncbi.nlm.nih.gov/IEB/ToolBox/CPP_DOC/lxr/source/src/app/winmasker/) |

[Back to contents](#contents)

## rna-evidence

RNA-seq / Iso-Seq alignment, assembly and ORF calling (A1b).

| Name | Type | Type-class | Stage | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|---|---|
| HISAT2 ·in repo | software | rna-evidence | A1b | Nature Biotechnology 2019; release v2.2.3 (2026-07-31); last push 2026-07-31 | Spliced aligner for short RNA-seq reads (graph-based index). | Default A1b aligner; plant introns are short and well handled. | doi:[10.1038/s41587-019-0201-4](https://doi.org/10.1038/s41587-019-0201-4) · [GitHub](https://github.com/DaehwanKimLab/hisat2) |
| STAR ·in repo | software | rna-evidence | A1b | Bioinformatics 2013; release 2.7.11b (2024-01-26); last push 2025-03-18 | Ultrafast spliced short-read aligner with two-pass junction discovery. | Alternative A1b aligner. | doi:[10.1093/bioinformatics/bts635](https://doi.org/10.1093/bioinformatics/bts635) · [GitHub](https://github.com/alexdobin/STAR) |
| minimap2 ·in repo | software | rna-evidence | A1b | Bioinformatics 2018; release v2.31 (2026-05-19); last push 2026-05-19 | Long-read and cDNA/Iso-Seq spliced aligner (-ax splice). | Aligns Iso-Seq/ONT cDNA to the genome for transcript evidence. | doi:[10.1093/bioinformatics/bty191](https://doi.org/10.1093/bioinformatics/bty191) · [GitHub](https://github.com/lh3/minimap2) |
| fastp | software | rna-evidence | A1b | Bioinformatics 2018; release v1.4.0 (2026-10-07); last push 2026-10-07 | All-in-one FASTQ QC and adapter trimming. | RNA-seq read QC before alignment. | doi:[10.1093/bioinformatics/bty560](https://doi.org/10.1093/bioinformatics/bty560) · [GitHub](https://github.com/OpenGene/fastp) |
| Trinity ·in repo | software | rna-evidence | A1b | Nature Biotechnology 2011; release Trinity-v2.15.2 (2024-07-31); last push 2026-04-23 | De novo and genome-guided transcriptome assembly from RNA-seq. | Feeds PASA; widely used in plant annotation. | doi:[10.1038/nbt.1883](https://doi.org/10.1038/nbt.1883) · [GitHub](https://github.com/trinityrnaseq/trinityrnaseq) |
| PASA ·in repo | software | rna-evidence | A1b | Nucleic Acids Research 2003; release pasa-v2.5.3 (2023-06-01); last push 2026-10-25 | Aligns and assembles transcripts into gene structures; also updates models with UTRs and isoforms. | Classic plant annotation component (A1b evidence, A4e update). | doi:[10.1093/nar/gkg770](https://doi.org/10.1093/nar/gkg770) · [GitHub](https://github.com/PASApipeline/PASApipeline) |
| TransDecoder ·in repo | software | rna-evidence | A1b | release TransDecoder-v7.0.0 (2026-11-02); last push 2026-11-02 | Finds candidate coding regions in transcripts (ORFs with homology/Pfam support). | StringTie→TransDecoder ORF track named in STAGE_IO. (no peer-reviewed paper found in this pass) | [GitHub](https://github.com/TransDecoder/TransDecoder) |
| IsoQuant ·in repo | software | rna-evidence | A1b | Nature Biotechnology 2023; release v4.1.0 (2026-10-20); last push 2026-11-11 | Long-read transcript discovery and quantification against a genome. | Iso-Seq/ONT transcript models for evidence. | doi:[10.1038/s41587-022-01565-y](https://doi.org/10.1038/s41587-022-01565-y) · [GitHub](https://github.com/ablab/IsoQuant) |
| Bambu ·in repo | software | rna-evidence | A1b | Nature Methods 2023; release v3.12.1 (2026-01-16); last push 2026-10-02 | Context-aware long-read transcript discovery and quantification (R/Bioconductor). | Controls false novel isoforms in long-read evidence. | doi:[10.1038/s41592-023-01908-w](https://doi.org/10.1038/s41592-023-01908-w) · [GitHub](https://github.com/GoekeLab/bambu) |
| SQANTI3 ·in repo | software | rna-evidence | A1b | Nature Methods 2024; release v6.1 (2026-10-20); last push 2026-10-28 | Classifies and filters long-read isoforms against a reference annotation. | Curates Iso-Seq evidence before it enters gene models. | doi:[10.1038/s41592-024-02229-2](https://doi.org/10.1038/s41592-024-02229-2) · [GitHub](https://github.com/ConesaLab/SQANTI3) |
| TAMA | software | rna-evidence | A1b | BMC Genomics 2020; last push 2023-04-12 | Collapses and merges long-read transcript models; annotation tools for Iso-Seq. | Iso-Seq evidence cleanup. | doi:[10.1186/s12864-020-07123-7](https://doi.org/10.1186/s12864-020-07123-7) · [GitHub](https://github.com/GenomeRIK/tama) |
| IsoSeq (PacBio) ·in repo | software | rna-evidence | A1b | release v26.2.0 (2026-06-24); last push 2026-06-24 | Official PacBio Iso-Seq processing (refine, cluster, collapse). | Upstream of Iso-Seq-based evidence. (no peer-reviewed paper found in this pass) | [GitHub](https://github.com/PacificBiosciences/IsoSeq) |

[Back to contents](#contents)

## protein-evidence

Protein-to-genome alignment (A2 inputs).

| Name | Type | Type-class | Stage | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|---|---|
| miniprot ·in repo | software | protein-evidence | A2 | Bioinformatics 2023; release v0.18 (2025-07-11); last push 2026-01-05 | Fast protein-to-genome spliced alignment. | Protein evidence from related plants (e.g. Arabidopsis, other Vitaceae). | doi:[10.1093/bioinformatics/btad014](https://doi.org/10.1093/bioinformatics/btad014) · [GitHub](https://github.com/lh3/miniprot) |
| GenomeThreader ·in repo | software | protein-evidence | A2 | Information and Software Technology 2005 | Spliced alignment of proteins/cDNA to genomes. | Classic protein-evidence aligner used in plant pipelines. | doi:[10.1016/j.infsof.2005.09.005](https://doi.org/10.1016/j.infsof.2005.09.005) · [site](https://genomethreader.org/) |
| Exonerate ·in repo | software | protein-evidence | A2 | BMC Bioinformatics 2005 | Generic sequence alignment including protein2genome spliced models. | Precise protein-to-genome models for curation. | doi:[10.1186/1471-2105-6-31](https://doi.org/10.1186/1471-2105-6-31) |
| Spaln ·in repo | software | protein-evidence | A2 | Bioinformatics 2008; last push 2026-07-11 | Spliced alignment of cDNA/protein to genome with species-specific parameters. | Has plant parameter sets. | doi:[10.1093/bioinformatics/btn460](https://doi.org/10.1093/bioinformatics/btn460) · [GitHub](https://github.com/ogotoh/spaln) |

[Back to contents](#contents)

## ab-initio

Ab initio / evidence-hinted gene finders (A2).

| Name | Type | Type-class | Stage | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|---|---|
| AUGUSTUS ·in repo | software | ab-initio | A2 | Bioinformatics 2008; release v3.5.0 (2022-09-24); last push 2026-05-30 | HMM gene finder with hints from RNA/protein evidence. | Core engine inside BRAKER; plant species parameters available. | doi:[10.1093/bioinformatics/btn013](https://doi.org/10.1093/bioinformatics/btn013) · [GitHub](https://github.com/Gaius-Augustus/Augustus) |
| BRAKER3 ·in repo | software | ab-initio | A2 | Genome Research 2024; release v3.0.8 (2024-02-17); last push 2026-06-17 | Fully automated pipeline combining GeneMark-ETP and AUGUSTUS with RNA-seq and protein evidence. | Default A2 primary draft engine. | doi:[10.1101/gr.278090.123](https://doi.org/10.1101/gr.278090.123) · [GitHub](https://github.com/Gaius-Augustus/BRAKER) |
| BRAKER2 ·in repo | software | ab-initio | A2 | NAR Genomics and Bioinformatics 2021; release v3.0.8 (2024-02-17); last push 2026-06-17 | Protein-evidence mode of BRAKER (GeneMark-EP+/AUGUSTUS). | Use when no RNA-seq. | doi:[10.1093/nargab/lqaa108](https://doi.org/10.1093/nargab/lqaa108) · [GitHub](https://github.com/Gaius-Augustus/BRAKER) |
| GALBA ·in repo | software | ab-initio | A2 | BMC Bioinformatics 2023; release v1.0.11 (2023-12-22); last push 2026-04-13 | Trains AUGUSTUS from miniprot protein alignments of a related species. | For large plant genomes where BRAKER protein mode struggles. | doi:[10.1186/s12859-023-05449-z](https://doi.org/10.1186/s12859-023-05449-z) · [GitHub](https://github.com/Gaius-Augustus/GALBA) |
| SNAP ·in repo | software | ab-initio | A2 | BMC Bioinformatics 2004; last push 2022-10-22 | Semi-HMM ab initio gene finder trainable on new genomes. | Used inside MAKER rounds. | doi:[10.1186/1471-2105-5-59](https://doi.org/10.1186/1471-2105-5-59) · [GitHub](https://github.com/KorfLab/SNAP) |
| GlimmerHMM ·in repo | software | ab-initio | A2 | Bioinformatics 2004 | Generalized HMM eukaryotic gene finder. | Older extra predictor for EVM weighting. | doi:[10.1093/bioinformatics/bth315](https://doi.org/10.1093/bioinformatics/bth315) · [site](https://ccb.jhu.edu/software/glimmerhmm/) |
| Tiberius ·in repo | software | ab-initio | A2 | Bioinformatics 2024; release v2.0.9 (2026-10-05); last push 2026-11-10 | End-to-end deep learning plus HMM ab initio gene prediction. | Trained on mammals; plant models are a compare track only. | doi:[10.1093/bioinformatics/btae685](https://doi.org/10.1093/bioinformatics/btae685) · [GitHub](https://github.com/Gaius-Augustus/Tiberius) |

[Back to contents](#contents)

## language-model

DNA language-model gene predictors (A2 / S13).

No new rows in this pass; see the first-pass index below.

[Back to contents](#contents)

## lift-over

Annotation transfer and homology-based projection (A2b / S11 / S4).

| Name | Type | Type-class | Stage | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|---|---|
| GeMoMa ·in repo | software | lift-over | A2b | Methods in Molecular Biology 2019 | Homology-based gene prediction using intron-position conservation and optional RNA-seq. | Named A2b second track in STAGE_IO; strong on plants. | doi:[10.1007/978-1-4939-9173-0_9](https://doi.org/10.1007/978-1-4939-9173-0_9) · [site](https://www.jstacs.de/index.php/GeMoMa) |
| Liftoff ·in repo | software | lift-over | A2b | Bioinformatics 2021; release 1.6.3 (2022-02-18); last push 2023-08-01 | Maps gene annotation from a reference to a target assembly of the same/close species. | Transfer PN40024 models to new haplotypes. | doi:[10.1093/bioinformatics/btaa1016](https://doi.org/10.1093/bioinformatics/btaa1016) · [GitHub](https://github.com/agshumate/Liftoff) |
| LiftOn ·in repo | software | lift-over | A2b | Genome Research 2024; release v1.0.14 (2026-09-25); last push 2026-10-28 | Combines DNA (Liftoff) and protein (miniprot) alignments to improve lift-over. | Fixes broken CDS after lift-over between grape haplotypes. | doi:[10.1101/gr.279620.124](https://doi.org/10.1101/gr.279620.124) · [GitHub](https://github.com/Kuanhao-Chao/LiftOn) |
| Comparative Annotation Toolkit (CAT) ·in repo | software | lift-over | A2b | Genome Research 2018; release v2.2.1 (2020-11-24); last push 2025-05-22 | Projects annotation through a Cactus whole-genome alignment and merges with ab initio. | Multi-genome annotation in pangenome projects. | doi:[10.1101/gr.233460.117](https://doi.org/10.1101/gr.233460.117) · [GitHub](https://github.com/ComparativeGenomicsToolkit/Comparative-Annotation-Toolkit) |

[Back to contents](#contents)

## combiner-pipeline

Combiners and whole annotation pipelines (A4).

| Name | Type | Type-class | Stage | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|---|---|
| EVidenceModeler (EVM) ·in repo | software | combiner-pipeline | A4 | Genome Biology 2008; release EVidenceModeler-v2.1.0 (2023-04-03); last push 2026-09-22 | Weighted consensus of predictions and alignments into gene models. | A4c–A4d combiner. | doi:[10.1186/gb-2008-9-1-r7](https://doi.org/10.1186/gb-2008-9-1-r7) · [GitHub](https://github.com/EVidenceModeler/EVidenceModeler) |
| TSEBRA ·in repo | software | combiner-pipeline | A4 | BMC Bioinformatics 2021; release v1.1.2.5 (2024-05-23); last push 2026-04-07 | Transcript selector combining BRAKER predictions using extrinsic evidence. | A4a combiner. | doi:[10.1186/s12859-021-04482-0](https://doi.org/10.1186/s12859-021-04482-0) · [GitHub](https://github.com/Gaius-Augustus/TSEBRA) |
| Mikado ·in repo | software | combiner-pipeline | A4 | GigaScience 2018; release v2.3.4 (2022-06-09); last push 2026-01-30 | Picks best transcript models at each locus from multiple assemblies/predictions. | A4b combiner; built for plant (wheat) annotation. | doi:[10.1093/gigascience/giy093](https://doi.org/10.1093/gigascience/giy093) · [GitHub](https://github.com/EI-CoreBioinformatics/mikado) |
| MAKER2 ·in repo | software | combiner-pipeline | A4 | BMC Bioinformatics 2011 | Annotation pipeline combining evidence alignment and ab initio predictors with AED scores. | Classic plant/non-model pipeline; AED score useful for QC. | doi:[10.1186/1471-2105-12-491](https://doi.org/10.1186/1471-2105-12-491) |
| funannotate ·in repo | software | combiner-pipeline | A4 | Zenodo concept DOI (latest record 2020); release v1.9.1 (2026-11-05); last push 2026-11-05 | Eukaryotic annotation pipeline (predict, update, annotate) built on EVM/PASA. | Built for fungi; usable on small plant genomes. | doi:[10.5281/zenodo.1134477](https://doi.org/10.5281/zenodo.1134477) · [GitHub](https://github.com/nextgenusfs/funannotate) |
| EGAPx ·in repo | software | combiner-pipeline | A4 | release v1.0.1 (2026-09-28); last push 2026-09-28 | Public release of NCBI's Eukaryotic Genome Annotation Pipeline. | A2d route in this repo. (no peer-reviewed paper found in this pass) | [GitHub](https://github.com/ncbi/egapx) |
| GETA ·in repo | software | combiner-pipeline | A4 | release v3.0.0 (2026-10-12); last push 2026-10-12 | Genome-wide Electronic Transcript Annotation pipeline (transcripts, homology, AUGUSTUS). | Used for plant genomes in China. (no peer-reviewed paper found in this pass) | [GitHub](https://github.com/chenlianfu/geta) |
| REAT | software | combiner-pipeline | A4 | release v0.6.1 (2022-01-21); last push 2025-02-28 | Robust Eukaryotic Annotation Toolkit (transcriptome, homology and prediction workflows, Mikado-based). | Plant-focused (Earlham Institute). (no peer-reviewed paper found in this pass) | [GitHub](https://github.com/EI-CoreBioinformatics/reat) |

[Back to contents](#contents)

## ncrna-pseudogene

Non-coding RNA and pseudogene loci.

| Name | Type | Type-class | Stage | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|---|---|
| ARAGORN | software | ncrna-pseudogene | ncRNA | Nucleic Acids Research 2004 | Detects tRNA and tmRNA genes. | Organellar tRNAs on plastid/mito contigs. | doi:[10.1093/nar/gkh152](https://doi.org/10.1093/nar/gkh152) |
| RNAmmer | software | ncrna-pseudogene | ncRNA | Nucleic Acids Research 2007 | HMM-based rRNA gene prediction. | rDNA arrays in plant assemblies. | doi:[10.1093/nar/gkm160](https://doi.org/10.1093/nar/gkm160) · [site](https://services.healthtech.dtu.dk/services/RNAmmer-1.2/) |
| CPAT | software | ncrna-pseudogene | ncRNA | Nucleic Acids Research 2013; release v3.0.5 (2024-01-26); last push 2024-02-29 | Alignment-free coding-potential assessment of transcripts. | Filters lncRNA vs coding transcripts. | doi:[10.1093/nar/gkt006](https://doi.org/10.1093/nar/gkt006) · [GitHub](https://github.com/liguowang/cpat) |
| LncFinder | software | ncrna-pseudogene | ncRNA | Briefings in Bioinformatics 2019 | lncRNA identification with heterologous features and machine learning (R package). | Includes plant (Arabidopsis) models. | doi:[10.1093/bib/bby065](https://doi.org/10.1093/bib/bby065) |
| PseudoPipe | software | ncrna-pseudogene | ncRNA | Bioinformatics 2006 | Homology-based pseudogene identification pipeline. | Classic pseudogene caller applied to plants. | doi:[10.1093/bioinformatics/btl116](https://doi.org/10.1093/bioinformatics/btl116) |

[Back to contents](#contents)

## model-qc

Gene-model QC, protein extraction and comparison (A3, A5, LM01, LM02).

| Name | Type | Type-class | Stage | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|---|---|
| gffread / gffcompare ·in repo | software | model-qc | A3 | F1000Research 2020; release v0.12.9 (2026-04-10); last push 2026-11-12 | Extract CDS/proteins from GFF (gffread) and compare two annotations at base/exon/locus level (gffcompare). | A3 protein extraction; A5/LM release diff between versions. | doi:[10.12688/f1000research.23297.2](https://doi.org/10.12688/f1000research.23297.2) · [GitHub](https://github.com/gpertea/gffread) |
| AGAT ·in repo | software | model-qc | A5 | Zenodo concept DOI (latest record 2026); release v1.7.0 (2026-04-10); last push 2026-09-07 | GFF/GTF toolkit: statistics, fixing, longest-isoform selection, ID management, format conversion. | A3 (longest isoform), A5 stats, A6 ID rules. | doi:[10.5281/zenodo.3552717](https://doi.org/10.5281/zenodo.3552717) · [GitHub](https://github.com/NBISweden/AGAT) |
| BUSCO ·in repo | software | model-qc | LM01 | Molecular Biology and Evolution 2021 | Completeness of a gene set against lineage single-copy orthologs (protein mode). | LM01 re-QC of merged set; use embryophyta/eudicots lineage. | doi:[10.1093/molbev/msab199](https://doi.org/10.1093/molbev/msab199) |

[Back to contents](#contents)

## curation-browser

Browsers, evidence packs and editors (LM03, LM04).

| Name | Type | Type-class | Stage | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|---|---|
| IGV ·in repo | software | curation-browser | LM03 | Nature Biotechnology 2011; last push 2026-11-12 | Desktop genome viewer for alignments and annotations. | LM03 evidence pack review. | doi:[10.1038/nbt.1754](https://doi.org/10.1038/nbt.1754) · [GitHub](https://github.com/igvteam/igv) |
| igv.js / igv-reports | software | curation-browser | LM03 | Bioinformatics 2023; release v1.17.0 (2026-09-02); last push 2026-09-02 | Embeddable IGV; igv-reports builds self-contained HTML pages of loci with tracks. | LM03: one HTML evidence page per priority locus for curators. | doi:[10.1093/bioinformatics/btac830](https://doi.org/10.1093/bioinformatics/btac830) · [GitHub](https://github.com/igvteam/igv-reports) |
| Apollo (2019 paper) | software | curation-browser | LM04 | PLOS Computational Biology 2019; release 2.9.0 (2026-07-15); last push 2026-07-15 | Collaborative web gene-model editor (Apollo 2). | Manual gene-model editing at LM04. (Overnight catalog lists Apollo 3 (new codebase); this row is the published Apollo 2 line.) | doi:[10.1371/journal.pcbi.1006790](https://doi.org/10.1371/journal.pcbi.1006790) · [GitHub](https://github.com/GMOD/Apollo) |
| Artemis / ACT | software | curation-browser | LM04 | Bioinformatics 2012; release v18.2.0 (2022-03-14); last push 2025-12-19 | Genome browser/annotation editor and comparison tool. | Small-scale manual edits. | doi:[10.1093/bioinformatics/btr703](https://doi.org/10.1093/bioinformatics/btr703) · [GitHub](https://github.com/sanger-pathogens/Artemis) |

[Back to contents](#contents)

## gff-release

GFF3 cleanup, validation and submission (LM06, A6).

| Name | Type | Type-class | Stage | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|---|---|
| SeqKit 2 ·in repo | software | gff-release | A3 | iMeta 2024; release v2.14.0 (2026-09-24); last push 2026-11-11 | FASTA/Q toolkit (stats, grep, translate, dedup). | A3/A6 protein FASTA checks before hand-off. | doi:[10.1002/imt2.191](https://doi.org/10.1002/imt2.191) · [GitHub](https://github.com/shenwei356/seqkit) |
| Genome Annotation Generator (GAG) | software | gff-release | LM06 | GigaScience 2018; release v2.0.1 (2017-04-06); last push 2018-03-05 | Generates and corrects NCBI .tbl annotation tables from GFF3. | GenBank submission prep. | doi:[10.1093/gigascience/giy018](https://doi.org/10.1093/gigascience/giy018) · [GitHub](https://github.com/genomeannotation/GAG) |

[Back to contents](#contents)

## database

Reference genomes/annotations used as evidence.

| Name | Type | Type-class | Stage | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|---|---|
| RNAcentral | database | database | ncRNA | Nucleic Acids Research 2021 | Integrated non-coding RNA sequence database. | Reference for ncRNA locus naming. | doi:[10.1093/nar/gkaa921](https://doi.org/10.1093/nar/gkaa921) · [site](https://rnacentral.org/) |
| Phytozome | database | database | A2 | Nucleic Acids Research 2012 | Plant genome and annotation portal (JGI). | Protein evidence and reference annotations for related plants. | doi:[10.1093/nar/gkr944](https://doi.org/10.1093/nar/gkr944) · [site](https://phytozome-next.jgi.doe.gov/) |
| Ensembl Plants (Ensembl Genomes 2022) | database | database | A2 | Nucleic Acids Research 2022 | Plant genomes, gene models and comparative data. | Includes Vitis vinifera; protein evidence source. | doi:[10.1093/nar/gkab1007](https://doi.org/10.1093/nar/gkab1007) · [site](https://plants.ensembl.org/) |
| Araport11 | database | database | A2 | The Plant Journal 2017 | Re-annotation of the Arabidopsis Col-0 genome. | High-quality protein evidence for eudicots. | doi:[10.1111/tpj.13415](https://doi.org/10.1111/tpj.13415) · [site](https://www.arabidopsis.org/) |

[Back to contents](#contents)

## standard-review

Standards, formats and reviews.

| Name | Type | Type-class | Stage | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|---|---|
| Sequence Ontology | idea | standard-review | LM06 | Genome Biology 2005; release v3.1 (2018-02-02); last push 2026-08-07 | Ontology of feature types used in GFF3 column 3. | Valid feature types in released GFF3. | doi:[10.1186/gb-2005-6-5-r44](https://doi.org/10.1186/gb-2005-6-5-r44) · [GitHub](https://github.com/The-Sequence-Ontology/SO-Ontologies) |
| GFF3 specification | idea | standard-review | LM06 | last push 2024-06-18 | Formal GFF3 format specification. | Reference for A6 hand-off and release validation. | [GitHub](https://github.com/The-Sequence-Ontology/Specifications) · [site](https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md) |
| The grapevine gene nomenclature system | idea | standard-review | A6 | BMC Genomics 2014 | Proposed naming rules for grapevine genes and loci. | Gene ID/name rules at A6/LM06 hand-off. | doi:[10.1186/1471-2164-15-1077](https://doi.org/10.1186/1471-2164-15-1077) |
| A beginner's guide to eukaryotic genome annotation | idea | standard-review | X | Nature Reviews Genetics 2012 | Review of evidence types, pipelines and quality metrics (AED). | Background for METHODS. | doi:[10.1038/nrg3174](https://doi.org/10.1038/nrg3174) |
| Ten steps to get started in genome assembly and annotation | idea | standard-review | X | F1000Research 2018 | Practical guide covering assembly through annotation. | Teaching reference. | doi:[10.12688/f1000research.13598.1](https://doi.org/10.12688/f1000research.13598.1) |

[Back to contents](#contents)

## idea

Ideas not yet tied to one tool.

No new rows in this pass; see the first-pass index below.

[Back to contents](#contents)

## First-pass entries by type-class

Every row of [`CATALOG_NEW_TOOLS_2026-11.md`](CATALOG_NEW_TOOLS_2026-11.md), given a type-class. Details and sources stay in that file.

| Type-class | Name | Type | First-pass section |
|---|---|---|---|
| assembly-qc | NCBI FCS-GX | software | Asm1 — assembly hygiene before annotation |
| soft-mask | ULTRA | software | A0 — soft-mask with a trusted library |
| rna-evidence | StringTie (v3 line) ·in repo | software | A1b — transcript and translation evidence |
| rna-evidence | FLIC (Full-length isoform constructor) | software | A1b — transcript and translation evidence |
| rna-evidence | Isocall | software | A1b — transcript and translation evidence |
| rna-evidence | ESPRESSO | software | A1b — transcript and translation evidence |
| rna-evidence | TAGET | software | A1b — transcript and translation evidence |
| rna-evidence | RiboCode | software | A1b — transcript and translation evidence |
| rna-evidence | Ribo-TISH | software | A1b — transcript and translation evidence |
| rna-evidence | PhyloCSF++ | software | A1b — transcript and translation evidence |
| rna-evidence | KuPID | software | A1b — transcript and translation evidence |
| rna-evidence | RiboBA | software | A1b — transcript and translation evidence |
| ab-initio | GeneMark-ETP ·in repo | software | A2 inputs — protein evidence and evidence-driven gene finders |
| ab-initio | ANNEVO (paper) ·in repo | software | A2 / S13 — ab initio and DNA language-model predictors |
| language-model | Carbon-A + Carbon Annotation Database (CADB) | software+database | A2 / S13 — ab initio and DNA language-model predictors |
| language-model | Nucleotide Transformer v3 (NTv3) ·in repo | software | A2 / S13 — ab initio and DNA language-model predictors |
| language-model | GENATATORs | software | A2 / S13 — ab initio and DNA language-model predictors |
| language-model | AgroNT | software | A2 / S13 — ab initio and DNA language-model predictors |
| language-model | PlantCaduceus | software | A2 / S13 — ab initio and DNA language-model predictors |
| language-model | Evo 2 | software | A2 / S13 — ab initio and DNA language-model predictors |
| lift-over | GrAnnoT | software | A2b / S11 / S4 — lift-over and comparative transfer |
| lift-over | TOGA (paper) ·in repo | software | A2b / S11 / S4 — lift-over and comparative transfer |
| lift-over | LiftoffTools | software | A2b / S11 / S4 — lift-over and comparative transfer |
| lift-over | GENESPACE | software | A2b / S11 / S4 — lift-over and comparative transfer |
| combiner-pipeline | EASEL | software | A4 — combiners and full pipelines |
| combiner-pipeline | Sylvan ·in repo | software | A4 — combiners and full pipelines |
| combiner-pipeline | Ensembl automatic annotation pipeline (ensembl-anno) | software | A4 — combiners and full pipelines |
| ncrna-pseudogene | Infernal 1.1 | software | Non-coding and pseudogene loci |
| ncrna-pseudogene | tRNAscan-SE 2.0 ·in repo | software | Non-coding and pseudogene loci |
| ncrna-pseudogene | barrnap | software | Non-coding and pseudogene loci |
| ncrna-pseudogene | ShortStack 4 | software | Non-coding and pseudogene loci |
| ncrna-pseudogene | PlantLncBoost | software | Non-coding and pseudogene loci |
| ncrna-pseudogene | FEELnc | software | Non-coding and pseudogene loci |
| ncrna-pseudogene | CPC2 | software | Non-coding and pseudogene loci |
| ncrna-pseudogene | P-GRe | software | Non-coding and pseudogene loci |
| ncrna-pseudogene | Shiu lab PseudogenePipeline | software | Non-coding and pseudogene loci |
| ncrna-pseudogene | miRDeep-P2 | software | Non-coding and pseudogene loci |
| model-qc | ABAQS | software | A5 / S5 — gene-model QC |
| model-qc | GeneValidator | software | A5 / S5 — gene-model QC |
| curation-browser | Apollo 3 | software | Curation and browsers (GSAman stage, S7) |
| curation-browser | JBrowse 2 | software | Curation and browsers (GSAman stage, S7) |
| gff-release | GenomeTools (gt gff3validator) | software | Release — GFF3 cleanup, validation and submission |
| gff-release | EMBLmyGFF3 | software | Release — GFF3 cleanup, validation and submission |
| gff-release | table2asn ·in repo | software | Release — GFF3 cleanup, validation and submission |
| gff-release | GFF3toolkit | software | Release — GFF3 cleanup, validation and submission |
| gff-release | noodles | software | Release — GFF3 cleanup, validation and submission |
| gff-release | gxfkit | software | Release — GFF3 cleanup, validation and submission |
| database | Rfam 15 | database | Non-coding and pseudogene loci |
| standard-review | LRGASP benchmark | idea | A1b — transcript and translation evidence |
| standard-review | Tips for improving genome annotation quality | idea | Standards and reviews (2023–2026) |
| standard-review | EBP annotation standards report | idea | Standards and reviews (2023–2026) |
| idea | Soft-mask hand-off rule (idea) | idea | A0 — soft-mask with a trusted library |
| idea | Chimeric mis-annotation survey | idea | A5 / S5 — gene-model QC |
| idea | Annotation affects orthology (idea) | idea | A5 / S5 — gene-model QC |
| idea | GeneWhisperer | idea | Curation and browsers (GSAman stage, S7) |
| idea | Human-AI collaborative annotation framework | idea | Curation and browsers (GSAman stage, S7) |
| idea | Family-window review using function results (idea) | idea | Curation and browsers (GSAman stage, S7) |

Candidates from this pass that turned out to be already in the first-pass file and were dropped: tRNAscan-SE (= tRNAscan-SE 2.0 ·in repo), GeneValidator (= GeneValidator).

[Back to contents](#contents)

## Not verified yet

- CRAQ [待确认]: no peer-reviewed paper found in this pass

[Back to contents](#contents)

## How entries were checked

- Candidates came from this repo's own pipeline docs (classics already in use), standard annotation literature and the gaps left by the first pass; checked 2026-11-13 (Asia/Shanghai).
- Each DOI was resolved in Crossref (DataCite for Zenodo and Bioconductor DOIs) and the returned title matched to the tool by hand; venue and year come from that record (print year where Crossref gives one).
- GitHub repositories were read with the GitHub API (latest release tag and date, last push, archived flag). Other official pages were requested over HTTP; a non-200 answer is noted in the row and the row is marked `[待确认]` until a person opens the page.
- No tool, paper, year or DOI was added from memory without a resolved record or official page. Items that could not be resolved keep `[待确认]`.

Total: 78 new entries in this file (68 software, 5 database, 5 idea, 0 combined software/database). With the first pass: 135.
