# New tools, databases and ideas by stage (structural) — 2026-11 survey

Survey of annotation software, databases and ideas published or released mostly in 2023–2026, sorted by the **structure** stages of this repo. It is a reading list, not a change to the default path: nothing here replaces the order in [`TOOLS.md`](TOOLS.md) until someone tests it.

**Boundary (see [`BOUNDARY.md`](BOUNDARY.md)).** This page lists only things that make or check coordinates, GFF3 and proteins.

- TE *library construction* (de novo TE finders, library curation tools) belongs to [`vitis-te`](https://github.com/Xuzhen-Li/vitis-te) and is **not** listed here. Structure only soft-masks with a trusted library.
- Functional labels (GO/KEGG/names/domains) and family classifiers such as HRP or NLR classifiers live in [gene-function-annotation](https://github.com/Xuzhen-Li/gene-function-annotation). Scenario S7 may *use* a window list from there to review gene models (see the curation section).
- Product handed to the function repo: `proteins.faa` → `merged_function_table.tsv` on that side (the older name `functional_master.tsv` in some pages here refers to the same table).

**Stage names.** Section titles use the stage IDs of [`STAGE_IO.md`](STAGE_IO.md) (Asm1, A0, A1b, A2, A2b, A4, A5 …). Scenario IDs (S1–S14, see [`ROADMAP.md`](ROADMAP.md)) are mentioned only where a tool fits one scenario. The numbered order in `TOOLS.md` is a third list; it is not used as a stage name here.

`[待确认]` = not yet verified (link, version, plant use or paper). Preprints are labelled; treat them as compare tracks.

Already cited elsewhere in this repo and therefore **not repeated** here: Helixer (*Nat Methods* 2025), EviAnn (*Nat Methods* 2026) and Tiberius multi-clade preprint ([`REVIEWS.md`](REVIEWS.md)); OMArk, PSAURON, compleasm papers ([`QUALITY_SOURCES.md`](QUALITY_SOURCES.md)); "Building better genome annotations" and "Welcome to the big leaves" ([`REVIEWS.md`](REVIEWS.md)). Rows marked `·in repo` add a newer paper, release or angle for a tool that is already mentioned.

## Contents

- [Asm1 — assembly hygiene before annotation](#asm1--assembly-hygiene-before-annotation) (1)
- [A0 — soft-mask with a trusted library](#a0--soft-mask-with-a-trusted-library) (2)
- [A1b — transcript and translation evidence](#a1b--transcript-and-translation-evidence) (11)
- [A2 inputs — protein evidence and evidence-driven gene finders](#a2-inputs--protein-evidence-and-evidence-driven-gene-finders) (1)
- [A2 / S13 — ab initio and DNA language-model predictors](#a2--s13--ab-initio-and-dna-language-model-predictors) (7)
- [A2b / S11 / S4 — lift-over and comparative transfer](#a2b--s11--s4--lift-over-and-comparative-transfer) (4)
- [A4 — combiners and full pipelines](#a4--combiners-and-full-pipelines) (3)
- [Non-coding and pseudogene loci](#non-coding-and-pseudogene-loci) (11)
- [A5 / S5 — gene-model QC](#a5--s5--gene-model-qc) (4)
- [Curation and browsers (GSAman stage, S7)](#curation-and-browsers-gsaman-stage-s7) (5)
- [Release — GFF3 cleanup, validation and submission](#release--gff3-cleanup-validation-and-submission) (6)
- [Standards and reviews (2023–2026)](#standards-and-reviews-20232026) (2)
- [How entries were checked](#how-entries-were-checked)

## Asm1 — assembly hygiene before annotation

Checks on the assembly that change what gets annotated.

| Name | Type | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|
| NCBI FCS-GX | software | Genome Biology 2024; release v0.5.5 (2025-03-18); last push 2025-03-18 | Detects and removes foreign-organism contamination in assemblies before submission/annotation. | Any eukaryote; avoids annotating bacterial/fungal contigs as plant genes. | doi:[10.1186/s13059-024-03198-7](https://doi.org/10.1186/s13059-024-03198-7) · [GitHub](https://github.com/ncbi/fcs) |

[Back to contents](#contents)

## A0 — soft-mask with a trusted library

Masking inputs only. Library building is out of scope (vitis-te).

| Name | Type | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|
| ULTRA | software | Bioinformatics Advances 2024; release 1.2.1 (2025-10-08); last push 2026-08-28 | Probabilistic labeling of tandem / low-complexity repeats; output can feed soft-masking alongside a trusted TE library. | Tandem arrays near centromeres and gene clusters in plant genomes; masking only, not library building. | doi:[10.1093/bioadv/vbae149](https://doi.org/10.1093/bioadv/vbae149) · [GitHub](https://github.com/TravisWheelerLab/ULTRA) |
| Soft-mask hand-off rule (idea) | idea | — | Structure consumes a curated TE library produced elsewhere; record library name, version and sha256 in METHODS, and keep NLR/gene families out of the library (see existing ProtExcluder note). | Applies to every plant genome; library construction tools are listed for the TE repo, not here. | [site](https://github.com/Xuzhen-Li/gene-structure-annotation/blob/main/docs/BOUNDARY.md) |

[Back to contents](#contents)

## A1b — transcript and translation evidence

Short/long-read transcript assembly, isoform calling, Ribo-seq and coding-potential evidence for gene models.

| Name | Type | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|
| StringTie (v3 line) ·in repo | software | Genome Biology 2019; release v3.0.3 (2025-11-13); last push 2026-11-11 | Reference-guided / de novo transcript assembly from short and long RNA reads; used as transcript evidence and as the compare track. | Standard plant evidence track; check release notes for long-read mode changes. | doi:[10.1186/s13059-019-1910-1](https://doi.org/10.1186/s13059-019-1910-1) · [GitHub](https://github.com/gpertea/stringtie) |
| FLIC (Full-length isoform constructor) | software | Bioinformatics 2025; last push 2026-09-01 | Builds full-length isoforms from long reads using replicate concordance and TSS/polyA peak calling. | Benchmarked on Arabidopsis cDNA; useful where reference annotation is weak. | doi:[10.1093/bioinformatics/btaf551](https://doi.org/10.1093/bioinformatics/btaf551) · [GitHub](https://github.com/albidgy/FLIC) |
| Isocall | software | release 1.3.0 (2026-08-06); last push 2026-08-06 | Joint calling of known and novel isoforms across many PacBio Iso-Seq samples (alternative to isoseq cluster/collapse). | Multi-tissue Iso-Seq for plant annotation; vendor marks it as in active development. | [GitHub](https://github.com/PacificBiosciences/isocall) |
| ESPRESSO | software | Science Advances 2023; release v1.6.0 (2025-09-19); last push 2026-03-19 | Discovery and quantification of isoforms from error-prone long-read RNA-seq. | ONT cDNA/direct RNA evidence; developed on human data. | doi:[10.1126/sciadv.abq5072](https://doi.org/10.1126/sciadv.abq5072) · [GitHub](https://github.com/Xinglab/espresso) |
| TAGET | software | Nature Communications 2023 | Iso-Seq toolkit: alignment with CNN splice-site correction, isoform classification, expression. | Human-tumour development; usable for any eukaryote with a reference [待确认 plant use].  Code link: see paper [待确认]. | doi:[10.1038/s41467-023-41649-0](https://doi.org/10.1038/s41467-023-41649-0) |
| RiboCode | software | Nucleic Acids Research 2018; release v1.2.13 (2021-12-28); last push 2022-07-29 | Identifies actively translated ORFs from ribosome-profiling data. | Ribo-seq support for CDS boundaries, uORFs and small ORFs in plants. | doi:[10.1093/nar/gky179](https://doi.org/10.1093/nar/gky179) · [GitHub](https://github.com/xryanglab/RiboCode) |
| Ribo-TISH | software | Nature Communications 2017; release v0.2.8 (2025-10-21); last push 2025-10-21 | Translation initiation sites and ORFs from (QTI-seq / regular) Ribo-seq. | Start-codon evidence for CDS curation. | doi:[10.1038/s41467-017-01981-8](https://doi.org/10.1038/s41467-017-01981-8) · [GitHub](https://github.com/zhpn1024/ribotish) |
| PhyloCSF++ | software | Bioinformatics 2021; release v1.2.0 (2022-01-04); last push 2022-01-26 | Fast PhyloCSF: codon-substitution evidence of protein-coding potential from multi-species alignments. | Coding-vs-noncoding evidence where a whole-genome alignment of relatives exists. | doi:[10.1093/bioinformatics/btab756](https://doi.org/10.1093/bioinformatics/btab756) · [GitHub](https://github.com/cpockrandt/PhyloCSFpp) |
| LRGASP benchmark | idea | Nature Methods 2024 | Community benchmark of long-read RNA-seq methods for transcript identification and quantification; shows trade-offs between read depth, length and accuracy. | Choose long-read evidence strategy for plant annotation; includes non-model organism data. | doi:[10.1038/s41592-024-02298-3](https://doi.org/10.1038/s41592-024-02298-3) · [GitHub](https://github.com/LRGASP/lrgasp-submissions) |
| KuPID | software | preprint 2025 | k-mer-based upstream preprocessing of long reads for isoform discovery (preprint). | [待确认] plant tests. | doi:[10.64898/2025.12.05.692400](https://doi.org/10.64898/2025.12.05.692400) |
| RiboBA | software | preprint 2026 | Bias-aware probabilistic ORF identification across Ribo-seq protocols (preprint). | Ribo-seq CDS evidence [待确认] plant tests. | doi:[10.64898/2026.03.17.712439](https://doi.org/10.64898/2026.03.17.712439) |

[Back to contents](#contents)

## A2 inputs — protein evidence and evidence-driven gene finders

Tools that turn protein/transcript alignments into gene-structure hints.

| Name | Type | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|
| GeneMark-ETP ·in repo | software | Genome Research 2024; release etp-v1.02-preprint (2023-11-07); last push 2025-04-11 | Gene finder integrating transcript and protein evidence with self-training (core of BRAKER3). | Large plant genomes; benchmark paper covers plants. | doi:[10.1101/gr.278373.123](https://doi.org/10.1101/gr.278373.123) · [GitHub](https://github.com/gatech-genemark/GeneMark-ETP) |

[Back to contents](#contents)

## A2 / S13 — ab initio and DNA language-model predictors

Compare tracks; do not silently replace an evidence-based draft when RNA exists.

| Name | Type | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|
| Carbon-A + Carbon Annotation Database (CADB) | software+database | preprint 2026 | 1.2B-parameter encoder predicting protein-coding genes from DNA across eukaryotes with per-gene confidence; CADB applies it to GenBank assemblies (566M loci). | Includes plants; preprint Oct 2026 - treat as compare track only. | doi:[10.64898/2026.10.20.760448](https://doi.org/10.64898/2026.10.20.760448) · [site](https://huggingface.co/HuggingFaceBio/Carbon-A-1.2B) |
| Nucleotide Transformer v3 (NTv3) ·in repo | software | preprint 2025; tag ntv3-initial-release; last push 2026-11-02 | Long-context cross-kingdom DNA foundation model; reports gene-annotation performance above ab initio predictors in mammals, plants, insects. | Plant genomes in post-training; preprint. DOI prefix [待确认] | doi:[10.64898/2025.12.22.695963](https://doi.org/10.64898/2025.12.22.695963) · [GitHub](https://github.com/instadeepai/nucleotide-transformer) |
| GENATATORs | software | preprint 2026 | Ab initio gene annotation with DNA language models (preprint 2026). | [待确认] plant coverage. | doi:[10.64898/2026.06.17.732686](https://doi.org/10.64898/2026.06.17.732686) |
| AgroNT | software | Communications Biology 2024 | DNA language model trained on 48 edible-plant genomes; downstream tasks include regulatory and splice-site style predictions. | Plant-specific foundation model; feature source, not a gene caller. | doi:[10.1038/s42003-024-06465-2](https://doi.org/10.1038/s42003-024-06465-2) · [site](https://huggingface.co/InstaDeepAI/agro-nucleotide-transformer-1b) |
| PlantCaduceus | software | PNAS 2025; last push 2026-08-07 | Cross-species plant DNA language model at single-nucleotide resolution (splice/TIS/TTS annotation tasks). | Trained on 16 angiosperms; feature source for annotation QC. | doi:[10.1073/pnas.2421738122](https://doi.org/10.1073/pnas.2421738122) · [GitHub](https://github.com/kuleshov-group/PlantCaduceus) |
| Evo 2 | software | preprint 2025; release v0.5.0 (2026-02-28); last push 2026-06-19 | Genome language model across domains of life; zero-shot features for exon/intron and variant effect. | Idea-level for annotation; large GPU needs. | doi:[10.1101/2025.02.18.638918](https://doi.org/10.1101/2025.02.18.638918) · [GitHub](https://github.com/ArcInstitute/evo2) |
| ANNEVO (paper) ·in repo | software | preprint 2025; release v2.3.2 (2026-06-07); last push 2026-08-11 | Deep-learning ab initio annotation modelling evolutionary context (preprint version of the tool already noted in this repo). | Plant models exist; non-commercial licence. | doi:[10.21203/rs.3.rs-6402260/v1](https://doi.org/10.21203/rs.3.rs-6402260/v1) · [GitHub](https://github.com/xjtu-omics/ANNEVO) |

[Back to contents](#contents)

## A2b / S11 / S4 — lift-over and comparative transfer

Moving gene models between genomes or haplotypes, and checking transferred sets.

| Name | Type | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|
| GrAnnoT | software | Peer Community Journal 2025 | Transfers GFF3 annotation through a pangenome graph (GFA) to embedded genomes; outputs graph annotation (GAF) and per-genome GFF3. | Pangenome-aware transfer between grapevine haplotypes/accessions. | doi:[10.24072/pcjournal.651](https://doi.org/10.24072/pcjournal.651) · [site](https://forge.ird.fr/diade/dynadiv/grannot) |
| TOGA (paper) ·in repo | software | Science 2023; release v1.1.7 (2024-01-17); last push 2025-11-23 | Annotation projection integrated with orthology inference from whole-genome alignments. | Vertebrate-developed; TOGA2 already noted here. | doi:[10.1126/science.abn3107](https://doi.org/10.1126/science.abn3107) · [GitHub](https://github.com/hillerlab/TOGA) |
| LiftoffTools | software | F1000Research 2024; release v0.4.4 (2022-10-19); last push 2023-08-01 | Compares annotations mapped between assemblies: sequence variants in genes, synteny, copy-number changes. | Check Liftoff transfers between grapevine haplotypes. | doi:[10.12688/f1000research.124059.2](https://doi.org/10.12688/f1000research.124059.2) · [GitHub](https://github.com/agshumate/LiftoffTools) |
| GENESPACE | software | eLife 2022; release v1.2.3 (2023-05-03); last push 2025-01-24 | Synteny-constrained orthology across genomes; finds missing/extra genes in syntenic context. | Plant pangenomes; flags genes lost by annotation rather than biology. | doi:[10.7554/eLife.78526](https://doi.org/10.7554/eLife.78526) · [GitHub](https://github.com/jtlovell/GENESPACE) |

[Back to contents](#contents)

## A4 — combiners and full pipelines

End-to-end or consensus pipelines that produce a merged GFF.

| Name | Type | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|
| EASEL | software | — | Nextflow pipeline: StringTie2/PsiCLASS transcripts, TransDecoder, AUGUSTUS trained on transcript and OrthoDB protein hints, random-forest filtering using RNA-folding and other features. | Plant-focused (UConn Plant Computational Genomics). No dedicated paper found; related benchmark: doi 10.1002/aps3.11533. | [site](https://gitlab.com/PlantGenomicsLab/easel) |
| Sylvan ·in repo | software | release v2.1.0 (2026-07-09); last push 2026-11-03 | Snakemake pipeline combining EVM/PASA, GETA, Helixer, Liftoff and miniprot evidence, then semi-supervised random-forest filtering and boundary refinement. | Plant-oriented (land_plant Helixer model); no paper found [待确认]. | [GitHub](https://github.com/plantgenomicslab/Sylvan) |
| Ensembl automatic annotation pipeline (ensembl-anno) | software | — | Public code of Ensembl's automatic gene annotation pipeline. | Used for Ensembl/DToL eukaryotes; plant use [待确认].  Last push 2026-11-12. | [GitHub](https://github.com/Ensembl/ensembl-anno) |

[Back to contents](#contents)

## Non-coding and pseudogene loci

Locating ncRNA genes and pseudogenes (coordinates). Their functional interpretation sits in the function repo.

| Name | Type | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|
| Rfam 15 | database | Nucleic Acids Research 2024 | RNA family covariance models; scan with Infernal cmscan for rRNA, snoRNA, riboswitch-like loci. | Plant snoRNA/rRNA/miRNA precursors. | doi:[10.1093/nar/gkae1023](https://doi.org/10.1093/nar/gkae1023) · [site](https://rfam.org) |
| Infernal 1.1 | software | Bioinformatics 2013; tag ssu-align-0.1@4835; last push 2026-11-12 | Covariance-model RNA homology search (engine for Rfam). | All eukaryotes. | doi:[10.1093/bioinformatics/btt509](https://doi.org/10.1093/bioinformatics/btt509) · [GitHub](https://github.com/EddyRivasLab/infernal) |
| tRNAscan-SE 2.0 ·in repo | software | Nucleic Acids Research 2021; release v2.0.13 (2026-07-05); last push 2026-07-05 | tRNA gene detection with isotype classification and pseudo-tRNA flags. | Nuclear and organellar tRNAs. | doi:[10.1093/nar/gkab688](https://doi.org/10.1093/nar/gkab688) · [GitHub](https://github.com/UCSC-LoweLab/tRNAscan-SE) |
| barrnap | software | release v1.10.5 (2026-04-12); last push 2026-04-12 | Fast rRNA locus prediction (includes eukaryotic models). | Quick rDNA-array marking in assemblies. | [GitHub](https://github.com/tseemann/barrnap) |
| ShortStack 4 | software | RNA 2013; release v4.1.2 (2025-05-24); last push 2025-10-23 | Small-RNA locus annotation and MIRNA calling from sRNA-seq. | Plant-developed; miRNA and phasiRNA loci. DOI is the original paper; v4 release notes on GitHub | doi:[10.1261/rna.035279.112](https://doi.org/10.1261/rna.035279.112) · [GitHub](https://github.com/MikeAxtell/ShortStack) |
| PlantLncBoost | software | New Phytologist 2025; last push 2025-03-24 | Gradient-boosting plant lncRNA identification from sequence features. | Plant-specific lncRNA calling after transcript assembly. GitHub path [待确认] | doi:[10.1111/nph.70211](https://doi.org/10.1111/nph.70211) · [GitHub](https://github.com/xuechantian/PlantLncBoost) |
| FEELnc | software | Nucleic Acids Research 2017; release v.0.2.1 (2022-07-20); last push 2025-07-23 | lncRNA annotation from transcript assemblies (filter, coding potential, classifier). | Any eukaryote. | doi:[10.1093/nar/gkw1306](https://doi.org/10.1093/nar/gkw1306) · [GitHub](https://github.com/tderrien/FEELnc) |
| CPC2 | software | Nucleic Acids Research 2017 | Fast coding-potential calculator for transcripts. | Species-neutral coding potential filter. | doi:[10.1093/nar/gkx428](https://doi.org/10.1093/nar/gkx428) · [site](https://cpc2.gao-lab.org/) |
| P-GRe | software | Genomics 2026 | Pseudogene prediction: finds loci from parent proteins, rebuilds pseudo-CDS, reports frameshifts/stops, outputs GFF. | Designed for plants/eukaryotes. | doi:[10.1016/j.ygeno.2026.111216](https://doi.org/10.1016/j.ygeno.2026.111216) |
| Shiu lab PseudogenePipeline | software | release v1.0.0 (2022-05-10); last push 2023-06-08 | Classic plant pseudogene pipeline with repeat filtering and GFF output. | Arabidopsis/rice-era plant pipeline. | [GitHub](https://github.com/ShiuLab/PseudogenePipeline) |
| miRDeep-P2 | software | Bioinformatics 2018 | Fast plant miRNA locus discovery from sRNA-seq with updated plant criteria. | Plant-specific. | doi:[10.1093/bioinformatics/bty972](https://doi.org/10.1093/bioinformatics/bty972) |

[Back to contents](#contents)

## A5 / S5 — gene-model QC

Scores and checks of gene models. Model-support filters (e.g. the optional Pfam/RNA filter in `pipeline/A5c_expression_pfam_filter.md`) are structure QC, not functional annotation.

| Name | Type | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|
| ABAQS | software | release REL_0 (2025-10-31); last push 2026-11-04 | Accuracy-Based Annotation Quality Score combining completeness, gene-model validity and protein-profile checks. | From JGI MycoCosm (fungi) [待确认 plant use]. | [GitHub](https://github.com/mycocosm-lbl/abaqs) |
| Chimeric mis-annotation survey | idea | BMC Genomics 2025 | Shows fused (chimeric) gene models remain common in non-model eukaryote annotations; gives detection heuristics. | Directly relevant to merged tandem NLR/terpene clusters in grapevine. | doi:[10.1186/s12864-025-11765-w](https://doi.org/10.1186/s12864-025-11765-w) |
| Annotation affects orthology (idea) | idea | Bioinformatics 2025 | Structural annotation choices change orthology inference; compare annotations before cross-species claims. | Applies to any comparative plant study. | doi:[10.1093/bioinformatics/btaf365](https://doi.org/10.1093/bioinformatics/btaf365) |
| GeneValidator | software | Bioinformatics 2016 | Flags problem gene models by comparing each protein with database homologs (length, coverage, duplication, merged genes). | Any eukaryote; useful for merged tandem genes. Last push 2024-03. | doi:[10.1093/bioinformatics/btw015](https://doi.org/10.1093/bioinformatics/btw015) · [GitHub](https://github.com/wurmlab/genevalidator) |

[Back to contents](#contents)

## Curation and browsers (GSAman stage, S7)

Editing and reviewing gene models.

| Name | Type | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|
| Apollo 3 | software | preprint 2026; release v0.3.8 (2025-09-15); last push 2026-11-11 | JBrowse 2-based collaborative gene-model editor (local or server). | Manual curation of grapevine gene families. | doi:[10.64898/2026.06.08.730970](https://doi.org/10.64898/2026.06.08.730970) · [GitHub](https://github.com/GMOD/Apollo3) |
| JBrowse 2 | software | Genome Biology 2023; release v4.3.0 (2026-05-21); last push 2026-11-12 | Genome browser with synteny and SV views; host evidence tracks for curation. | Any genome. | doi:[10.1186/s13059-023-02914-z](https://doi.org/10.1186/s13059-023-02914-z) · [GitHub](https://github.com/GMOD/jbrowse-components) |
| GeneWhisperer | idea | preprint 2025 | LLM assistant with task tools for manual gene annotation (preprint). | Idea for curator support; keep human sign-off. | doi:[10.1101/2025.03.30.646211](https://doi.org/10.1101/2025.03.30.646211) |
| Human-AI collaborative annotation framework | idea | Briefings in Bioinformatics 2025 | Conceptual framework for dividing genome-annotation work between AI and curators. | Guides how to log AI-suggested edits. | doi:[10.1093/bib/bbaf377](https://doi.org/10.1093/bib/bbaf377) |
| Family-window review using function results (idea) | idea | — | Scenario S7 can take an NLR/TF window list produced in gene-function-annotation and re-check gene models in those windows; the classifiers themselves stay in the function catalog. | Grapevine NLR and terpene synthase clusters. | [site](https://github.com/Xuzhen-Li/gene-function-annotation) |

[Back to contents](#contents)

## Release — GFF3 cleanup, validation and submission

Format checks and archive submission.

| Name | Type | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|
| GenomeTools (gt gff3validator) | software | IEEE/ACM Transactions on Computational Biology and Bioinformatics 2013; release v1.6.6 (2025-10-06); last push 2025-11-10 | GFF3 validation, sorting, tidy. | Any genome release. | doi:[10.1109/TCBB.2013.68](https://doi.org/10.1109/TCBB.2013.68) · [GitHub](https://github.com/genometools/genometools) |
| EMBLmyGFF3 | software | BMC Research Notes 2018; release v2.4 (2025-07-31); last push 2025-07-31 | Converts GFF3 + FASTA to EMBL flat file for ENA submission. | ENA submission of plant annotations. | doi:[10.1186/s13104-018-3686-x](https://doi.org/10.1186/s13104-018-3686-x) · [GitHub](https://github.com/NBISweden/EMBLmyGFF3) |
| table2asn ·in repo | software | — | NCBI tool converting GFF3/FASTA to ASN.1 submission with validation report. | GenBank submission. | [site](https://www.ncbi.nlm.nih.gov/genbank/table2asn/) |
| GFF3toolkit | software | release v2.1.0 (2021-12-09); last push 2026-11-04 | GFF3 QC/fix/merge utilities from the i5k Workspace@NAL. | Arthropod origin, format-generic. | [GitHub](https://github.com/NAL-i5K/GFF3toolkit) |
| noodles | software | tag noodles-vcf-0.96.0; last push 2026-11-09 | Rust I/O libraries including GFF3/GTF readers and writers. | Building fast custom GFF checks. | [GitHub](https://github.com/zaeleus/noodles) |
| gxfkit | software | release v0.0.2 (2026-07-06); last push 2026-07-07 | Rust GFF3/GTF conversion aiming at AGAT-compatible output with large speedups. | Early single-developer project - verify output against AGAT before use. | [GitHub](https://github.com/benngaihk/gxfkit) |

[Back to contents](#contents)

## Standards and reviews (2023–2026)

Papers to cite or follow when writing METHODS.

| Name | Type | Year / latest release | What it does | Plant / eukaryote relevance | Source |
|---|---|---|---|---|---|
| Tips for improving genome annotation quality | idea | Genomics Communications 2025 | Practical checklist: evidence choice, masking level, manual review, metrics. | Plant-genome authors. | doi:[10.48130/gcomm-0025-0006](https://doi.org/10.48130/gcomm-0025-0006) |
| EBP annotation standards report | idea | — | Earth BioGenome Project report on minimum annotation standards and metadata. | Reference for METHODS wording. | [site](https://www.earthbiogenome.org/report-on-annotation-standards) |

[Back to contents](#contents)

## How entries were checked

- Searched 2026-11-12/13 (CST): Crossref title search, web search (papers 2023–2026, tool pages), GitHub API, and the existing docs of this repo.
- Each DOI was resolved in Crossref (or DataCite for Zenodo) and its title matched to the tool; venue/year come from that record. GitHub repos were opened with the API; release tag and last push date are from the API on the day of the survey.
- Items that could not be resolved keep `[待确认]`. No tool or paper was added from memory without a resolved record or official page.
- TE-library tools found in the same search are handed to the vitis-te maintainers separately, not listed here.

Entries: 57. Marked `·in repo` = name already appears somewhere in this repo's docs (entry adds a newer paper/release or a new angle).
