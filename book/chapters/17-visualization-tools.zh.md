# 第 17 章 可视化工具

*本章收录[主页“可视化工具”一节](../../README.zh.md#visualization)：该节说明、含论文、实验室、权威度和评价的完整工具表，以及评测要点。链接指回仓库。*

用于查看基因模型和作图的工具。标为“通用工具”的不专属于注释。已在前面类型小节出现的条目在这里再次列出并注明所在小节，不重复计数。

<a id="viz-1"></a>
## 基因组浏览器与编辑器

| 工具 | 角色 | 用途 / 何时用 | 原始论文 | 实验室（通讯作者，机构） | 权威度（档位 · 被引） | 评价（出处） |
|---|---|---|---|---|---|---|
| [IGV](https://github.com/igvteam/igv) | 备选，通用工具 | 用于查看序列比对与基因注释的桌面端基因组浏览器。（见第 11 节） | [Nature Biotechnology 2011](https://doi.org/10.1038/nbt.1754) | James T Robinson (Broad Institute) +1 | 标准 · 16992 次 | GitHub 最后提交 2026-11 |
| [igv.js / igv-reports](https://github.com/igvteam/igv-reports) | 备选，通用工具 | 可嵌入网页的 IGV 组件；igv-reports 可将指定位点及其证据轨道打包为独立的 HTML 页面。（见第 11 节） | [Bioinformatics 2022](https://doi.org/10.1093/bioinformatics/btac830) | James T Robinson (University of California San Diego) | 标准 · 648 次 | GitHub 最后提交 2026-11 |
| [JBrowse 2](https://github.com/GMOD/jbrowse-components) | 备选，通用工具 | 支持共线性与结构变异视图的基因组浏览器，可挂载各类证据轨道供人工校对使用。（见第 11 节） | [Genome biology 2023](https://doi.org/10.1186/s13059-023-02914-z) | Ian H Holmes (University of California, Berkeley) | 标准 · 907 次 | 作者摘要原句：“These improvements are enabled by a ground-up redesign using modern web technology.”；GitHub 最后提交 2026-11 |
| [Apollo 3](https://github.com/GMOD/Apollo3) | 备选 | 基于 JBrowse 2 的多人协作基因模型编辑器（支持本地或服务端部署）。Apollo 2（2019 年论文，doi:10.1371/journal.pcbi.1006790）为旧版服务端程序，仅在社区门户仍运行该版本时沿用。（见第 11 节） | [bioRxiv (Cold Spring Harbor Laboratory) 2026](https://doi.org/10.64898/2026.06.08.730970) | Ian H Holmes (University of California, Berkeley) | 较新 · 1 次 | 作者摘要原句：“Its functionality is inspired by existing manual genome annotation tools such as Apollo, Artemis, and Otter, combining features from those tools with an updated and more scalable architecture and technology stack.”；GitHub 最后提交 2026-11 |
| [Artemis / ACT](https://github.com/sanger-pathogens/Artemis) | 备选，通用工具 | 基因组浏览器、注释编辑器与序列比较工具。（见第 11 节） | [Bioinformatics 2011](https://doi.org/10.1093/bioinformatics/btr703) | Tim J. Carver (Wellcome Sanger Institute) | 标准 · 1410 次 | 论文摘要：“We present Artemis as a tool for integrated visualization and computational analysis of different types of HTS datasets in the context of a reference genome and its corresponding annotation.”；GitHub 最后提交 2025-12 |

<a id="viz-2"></a>
## 基因结构与异构体图

| 工具 | 角色 | 用途 / 何时用 | 原始论文 | 实验室（通讯作者，机构） | 权威度（档位 · 被引） | 评价（出处） |
|---|---|---|---|---|---|---|
| [GSDS 2.0](https://gsds.gao-lab.org/) | 备选 | 根据 GFF/BED 画外显子-内含子结构图的网页服务；基因家族文章常用。 | [Bioinformatics 2014](https://doi.org/10.1093/bioinformatics/btu817) | Ge Gao (Peking University) | 标准 · 5152 次 | 论文摘要：“Here, we reported the upgraded GSDS 2.0 with a newly designed interface, supports for more types of annotation features and formats, as well as an integrated visual editor for editing the generated figure.” |
| [IBS 2.0](https://ibs.renlab.org/) | 备选，通用工具 | 绘制基因结构和蛋白结构域示意图。 | [Nucleic Acids Research 2022](https://doi.org/10.1093/nar/gkac373) | Jian Min Ren (Sun Yat-sen University) | 成熟 · 279 次 | 论文摘要：“Here, we present a professional tool called IBS 2.0 for illustrating the organization of both protein and nucleotide sequences.” |
| [gggenes](https://github.com/wilkox/gggenes) | 备选 | ggplot2 扩展，为小片段或基因簇画基因箭头图（无论文）。 | 无文章 | — | 无论文 | 仓库简介：“➡️️➡️️⬅️️➡️️ Draw gene arrow maps in ggplot2”；GitHub 最后提交 2026-07 |
| [ggtranscript](https://github.com/dzhang32/ggtranscript) | 备选 | ggplot2 扩展，画转录本异构体结构；适合与参考注释对比异构体。 | [Bioinformatics 2022](https://doi.org/10.1093/bioinformatics/btac409) | David Zhang (Aligning Science Across Parkinson's) | 标准 · 911 次 | 论文摘要：“Here, we introduce ggtranscript, an R package that provides a fast and flexible method to visualize and compare transcripts.”；GitHub 最后提交 2024-08 |
| [ggsashimi](https://github.com/guigolab/ggsashimi) | 备选，通用工具 | 从 BAM 画剪接位点覆盖的 sashimi 图（命令行）。 | [PLoS Computational Biology 2018](https://doi.org/10.1371/journal.pcbi.1006360) | Alessandra Breschi (Universitat Pompeu Fabra) | 成熟 · 314 次 | 论文摘要：“We present ggsashimi, a command-line tool for the visualization of splicing events across multiple samples.”；GitHub 最后提交 2024-06 |
| [TBtools-II](https://github.com/CJ-Chen/TBtools-II) | 备选，通用工具 | 面向植物研究的桌面工具集，支持查看 GFF、提取序列与绘制基因结构图；便于快速抽查少量位点。（见第 11 节） | [Molecular Plant 2023](https://doi.org/10.1016/j.molp.2023.09.010) | Chengjie Chen (South China Agricultural University) +1 | 标准 · 4462 次 | GitHub 最后提交 2026-10 |

<a id="viz-3"></a>
## 轨道图与染色体图

| 工具 | 角色 | 用途 / 何时用 | 原始论文 | 实验室（通讯作者，机构） | 权威度（档位 · 被引） | 评价（出处） |
|---|---|---|---|---|---|---|
| [pyGenomeTracks](https://github.com/deeptools/pyGenomeTracks) | 备选，通用工具 | 脚本化、可复现的浏览器式轨道图（基因、覆盖度、Hi-C）。 | [Bioinformatics 2020](https://doi.org/10.1093/bioinformatics/btaa692) | Fidel Ramírez (Max Planck Institute of Immunobiology and Epigenetics) | 标准 · 575 次 | GitHub 最后提交 2026-11 |
| [Gviz](https://bioconductor.org/packages/Gviz/) | 备选，通用工具 | R/Bioconductor 区域轨道图，展示基因模型与数据。 | [Methods in molecular biology 2016](https://doi.org/10.1007/978-1-4939-3578-9_16) | Florian Hahne (Novartis (Switzerland)) | 标准 · 988 次 | 无摘要或仓库说明可引；见原文 |
| [karyoploteR](https://bioconductor.org/packages/karyoploteR/) | 备选，通用工具 | R/Bioconductor 包，沿整条染色体作图，如基因密度。 | [Bioinformatics 2017](https://doi.org/10.1093/bioinformatics/btx346) | Bernat Gel (Institut d'Investigació en Ciències de la Salut Germans Trias i Pujol) | 标准 · 845 次 | 无摘要或仓库说明可引；见原文 |
| [plotgardener](https://github.com/PhanstielLab/plotgardener) | 备选，通用工具 | R 包，精确排版多面板基因组图。 | [Bioinformatics 2022](https://doi.org/10.1093/bioinformatics/btac057) | Douglas H. Phanstiel (University of North Carolina at Chapel Hill) | 成熟 · 170 次 | 论文摘要：“We present plotgardener, a coordinate-based genomic data visualization package that offers a new paradigm for multi-plot figure generation in R.”；GitHub 最后提交 2026-07 |
| Circos | 备选，通用工具 | 环形基因组图，展示密度、连线与共线性。 | [Genome Research 2009](https://doi.org/10.1101/gr.092759.109) | Martin I. Krzywinski (Canada's Michael Smith Genome Sciences Centre) | 标准 · 12544 次 | 无摘要或仓库说明可引；见原文 |

<a id="viz-4"></a>
## 共线性图与点图

| 工具 | 角色 | 用途 / 何时用 | 原始论文 | 实验室（通讯作者，机构） | 权威度（档位 · 被引） | 评价（出处） |
|---|---|---|---|---|---|---|
| [JCVI (MCscan)](https://github.com/tanghaibao/jcvi) | 备选，通用工具 | Python 工具包，做注释基因组间共线性、宏/微共线性图和点图。 | [iMeta 2024](https://doi.org/10.1002/imt2.211) | Haibao Tang (Fujian Agriculture and Forestry University) +1 | 标准 · 576 次 | GitHub 最后提交 2026-11 |
| [D-GENIES](https://github.com/genotoul-bioinfo/dgenies) | 备选，通用工具 | 全基因组比对的交互式点图。 | [PeerJ 2018](https://doi.org/10.7717/peerj.4958) | Christophe Klopp (Institut National de Recherche pour l'Agriculture, l'Alimentation et l'Environnement) | 标准 · 892 次 | GitHub 最后提交 2026-09 |
| [GENESPACE](https://github.com/jtlovell/GENESPACE) | 备选 | 基于共线性约束做跨基因组直系同源分析，并在共线性背景下定位缺失或新增基因。（见第 7 节） | [eLife 2022](https://doi.org/10.7554/eLife.78526) | John T. Lovell (Lawrence Berkeley National Laboratory) | 成熟 · 439 次 | 论文摘要：“Here, we present GENESPACE, which addresses these challenges by integrating conserved gene order and orthology to define the expected physical position of all genes across multiple genomes.”；GitHub 最后提交 2025-01 |
