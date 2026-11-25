# Chapter 17. Visualization tools

*This chapter reproduces [README section Visualization tools](../../README.md#visualization): the section notes, the full tool table with paper, lab, tier and evaluation, and the benchmark notes. Links point back into the repository.*

Tools for looking at gene models and for figures. Rows marked general-purpose are not specific to annotation. Rows that already appear in a type section are listed again here with a pointer and are not counted twice.

<a id="viz-1"></a>
## Genome browsers and editors

| Tool | Role | What it does / when to use | Paper | Lab (corresponding author, institution) | Tier · citations | Evaluation (source) |
|---|---|---|---|---|---|---|
| [IGV](https://github.com/igvteam/igv) | alternative, general-purpose | Desktop genome viewer for alignments and annotations. (see section 11) | [Nature Biotechnology 2011](https://doi.org/10.1038/nbt.1754) | James T Robinson (Broad Institute) +1 | standard · 16992 | GitHub last push 2026-11 |
| [igv.js / igv-reports](https://github.com/igvteam/igv-reports) | alternative, general-purpose | Embeddable IGV; igv-reports builds self-contained HTML pages of loci with tracks. (see section 11) | [Bioinformatics 2022](https://doi.org/10.1093/bioinformatics/btac830) | James T Robinson (University of California San Diego) | standard · 648 | GitHub last push 2026-11 |
| [JBrowse 2](https://github.com/GMOD/jbrowse-components) | alternative, general-purpose | Genome browser with synteny and SV views; host evidence tracks for curation. (see section 11) | [Genome biology 2023](https://doi.org/10.1186/s13059-023-02914-z) | Ian H Holmes (University of California, Berkeley) | standard · 907 | Authors: “These improvements are enabled by a ground-up redesign using modern web technology.”; GitHub last push 2026-11 |
| [Apollo 3](https://github.com/GMOD/Apollo3) | alternative | Collaborative gene-model editor built on JBrowse 2 for local or server deployment. Apollo 2 (2019 paper, doi:10.1371/journal.pcbi.1006790) is the older server release; use it only when a community portal still runs it. (see section 11) | [bioRxiv (Cold Spring Harbor Laboratory) 2026](https://doi.org/10.64898/2026.06.08.730970) | Ian H Holmes (University of California, Berkeley) | newer · 1 | Authors: “Its functionality is inspired by existing manual genome annotation tools such as Apollo, Artemis, and Otter, combining features from those tools with an updated and more scalable architecture and technology stack.”; GitHub last push 2026-11 |
| [Artemis / ACT](https://github.com/sanger-pathogens/Artemis) | alternative, general-purpose | Genome browser/annotation editor and comparison tool. (see section 11) | [Bioinformatics 2011](https://doi.org/10.1093/bioinformatics/btr703) | Tim J. Carver (Wellcome Sanger Institute) | standard · 1410 | Paper: “We present Artemis as a tool for integrated visualization and computational analysis of different types of HTS datasets in the context of a reference genome and its corresponding annotation.”; GitHub last push 2025-12 |

<a id="viz-2"></a>
## Gene-structure and isoform diagrams

| Tool | Role | What it does / when to use | Paper | Lab (corresponding author, institution) | Tier · citations | Evaluation (source) |
|---|---|---|---|---|---|---|
| [GSDS 2.0](https://gsds.gao-lab.org/) | alternative | Web server that draws exon-intron diagrams from GFF/BED; common in gene-family papers. | [Bioinformatics 2014](https://doi.org/10.1093/bioinformatics/btu817) | Ge Gao (Peking University) | standard · 5152 | Paper: “Here, we reported the upgraded GSDS 2.0 with a newly designed interface, supports for more types of annotation features and formats, as well as an integrated visual editor for editing the generated figure.” |
| [IBS 2.0](https://ibs.renlab.org/) | alternative, general-purpose | Draws gene structures and protein domain diagrams for figures. | [Nucleic Acids Research 2022](https://doi.org/10.1093/nar/gkac373) | Jian Min Ren (Sun Yat-sen University) | established · 279 | Paper: “Here, we present a professional tool called IBS 2.0 for illustrating the organization of both protein and nucleotide sequences.” |
| [gggenes](https://github.com/wilkox/gggenes) | alternative | ggplot2 extension that draws gene arrow maps for small loci or clusters (no paper). | no paper | — | no paper | Repo description: “➡️️➡️️⬅️️➡️️ Draw gene arrow maps in ggplot2”; GitHub last push 2026-07 |
| [ggtranscript](https://github.com/dzhang32/ggtranscript) | alternative | ggplot2 extension for transcript isoform structures; good for comparing isoforms against a reference. | [Bioinformatics 2022](https://doi.org/10.1093/bioinformatics/btac409) | David Zhang (Aligning Science Across Parkinson's) | standard · 911 | Paper: “Here, we introduce ggtranscript, an R package that provides a fast and flexible method to visualize and compare transcripts.”; GitHub last push 2024-08 |
| [ggsashimi](https://github.com/guigolab/ggsashimi) | alternative, general-purpose | Command-line sashimi plots of splice junction coverage from BAM files. | [PLoS Computational Biology 2018](https://doi.org/10.1371/journal.pcbi.1006360) | Alessandra Breschi (Universitat Pompeu Fabra) | established · 314 | Paper: “We present ggsashimi, a command-line tool for the visualization of splicing events across multiple samples.”; GitHub last push 2024-06 |
| [TBtools-II](https://github.com/CJ-Chen/TBtools-II) | alternative, general-purpose | Plant-focused desktop toolkit for GFF viewing, sequence extraction and gene-structure plotting; convenient for quick checks on a few loci. (see section 11) | [Molecular Plant 2023](https://doi.org/10.1016/j.molp.2023.09.010) | Chengjie Chen (South China Agricultural University) +1 | standard · 4462 | GitHub last push 2026-10 |

<a id="viz-3"></a>
## Track and chromosome plots

| Tool | Role | What it does / when to use | Paper | Lab (corresponding author, institution) | Tier · citations | Evaluation (source) |
|---|---|---|---|---|---|---|
| [pyGenomeTracks](https://github.com/deeptools/pyGenomeTracks) | alternative, general-purpose | Scripted, reproducible browser-style track figures (genes, coverage, Hi-C). | [Bioinformatics 2020](https://doi.org/10.1093/bioinformatics/btaa692) | Fidel Ramírez (Max Planck Institute of Immunobiology and Epigenetics) | standard · 575 | GitHub last push 2026-11 |
| [Gviz](https://bioconductor.org/packages/Gviz/) | alternative, general-purpose | R/Bioconductor track plots of gene models and data for a region. | [Methods in molecular biology 2016](https://doi.org/10.1007/978-1-4939-3578-9_16) | Florian Hahne (Novartis (Switzerland)) | standard · 988 | no abstract or repo text available; see paper |
| [karyoploteR](https://bioconductor.org/packages/karyoploteR/) | alternative, general-purpose | R/Bioconductor package to plot data along whole chromosomes, e.g. gene density. | [Bioinformatics 2017](https://doi.org/10.1093/bioinformatics/btx346) | Bernat Gel (Institut d'Investigació en Ciències de la Salut Germans Trias i Pujol) | standard · 845 | no abstract or repo text available; see paper |
| [plotgardener](https://github.com/PhanstielLab/plotgardener) | alternative, general-purpose | R package for precise multi-panel genomic figures. | [Bioinformatics 2022](https://doi.org/10.1093/bioinformatics/btac057) | Douglas H. Phanstiel (University of North Carolina at Chapel Hill) | established · 170 | Paper: “We present plotgardener, a coordinate-based genomic data visualization package that offers a new paradigm for multi-plot figure generation in R.”; GitHub last push 2026-07 |
| Circos | alternative, general-purpose | Circular genome plots for densities, links and synteny. | [Genome Research 2009](https://doi.org/10.1101/gr.092759.109) | Martin I. Krzywinski (Canada's Michael Smith Genome Sciences Centre) | standard · 12544 | no abstract or repo text available; see paper |

<a id="viz-4"></a>
## Synteny and dot plots

| Tool | Role | What it does / when to use | Paper | Lab (corresponding author, institution) | Tier · citations | Evaluation (source) |
|---|---|---|---|---|---|---|
| [JCVI (MCscan)](https://github.com/tanghaibao/jcvi) | alternative, general-purpose | Python toolkit for synteny, macro/micro-synteny plots and dot plots between annotated genomes. | [iMeta 2024](https://doi.org/10.1002/imt2.211) | Haibao Tang (Fujian Agriculture and Forestry University) +1 | standard · 576 | GitHub last push 2026-11 |
| [D-GENIES](https://github.com/genotoul-bioinfo/dgenies) | alternative, general-purpose | Interactive dot plots of whole-genome alignments. | [PeerJ 2018](https://doi.org/10.7717/peerj.4958) | Christophe Klopp (Institut National de Recherche pour l'Agriculture, l'Alimentation et l'Environnement) | standard · 892 | GitHub last push 2026-09 |
| [GENESPACE](https://github.com/jtlovell/GENESPACE) | alternative | Synteny-constrained orthology across genomes; finds missing/extra genes in syntenic context. (see section 7) | [eLife 2022](https://doi.org/10.7554/eLife.78526) | John T. Lovell (Lawrence Berkeley National Laboratory) | established · 439 | Paper: “Here, we present GENESPACE, which addresses these challenges by integrating conserved gene order and orthology to define the expected physical position of all genes across multiple genomes.”; GitHub last push 2025-01 |
