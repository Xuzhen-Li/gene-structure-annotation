# 第 12 章 人工校对与浏览器

*本章收录[主页第 11 节](../../README.zh.md#section-11)：该节说明、含论文、实验室、权威度和评价的完整工具表，以及评测要点。链接指回仓库。*

用于 last-mile 校对的证据包、基因组浏览器与编辑器（LM03–LM04）。

**需要：** 在打开 GSAman 或浏览器前，备好草案 GFF、基因组及证据包（BAM、蛋白比对、RNA 覆盖度）。[按场景列出的数据需求](../../README.zh.md#data-needs)

**分组：**
- *协作式网页校对*（互补）：Apollo 3、JBrowse 2。Apollo 3 是 JBrowse 2 上的插件，团队校对时两者一起用。
- *桌面与人工校对工具*（可替代）：IGV、Artemis / ACT、GSAman、TBtools-II。用于本地检查少量位点；LM04 的模型编辑使用 GSAman。


| 工具 | 角色 | 用途 / 何时用 | 原始论文 | 实验室（通讯作者，机构） | 权威度（档位 · 被引） | 评价（出处） |
|---|---|---|---|---|---|---|
| [IGV](https://github.com/igvteam/igv) | 备选，通用工具 | 用于查看序列比对与基因注释的桌面端基因组浏览器。 | [Nature Biotechnology 2011](https://doi.org/10.1038/nbt.1754) | James T Robinson (Broad Institute) +1 | 标准 · 16992 次 | GitHub 最后提交 2026-11 |
| [igv.js / igv-reports](https://github.com/igvteam/igv-reports) | 备选，通用工具 | 可嵌入网页的 IGV 组件；igv-reports 可将指定位点及其证据轨道打包为独立的 HTML 页面。 | [Bioinformatics 2022](https://doi.org/10.1093/bioinformatics/btac830) | James T Robinson (University of California San Diego) | 标准 · 648 次 | GitHub 最后提交 2026-11 |
| [Artemis / ACT](https://github.com/sanger-pathogens/Artemis) | 备选，通用工具 | 基因组浏览器、注释编辑器与序列比较工具。 | [Bioinformatics 2011](https://doi.org/10.1093/bioinformatics/btr703) | Tim J. Carver (Wellcome Sanger Institute) | 标准 · 1410 次 | 论文摘要：“We present Artemis as a tool for integrated visualization and computational analysis of different types of HTS datasets in the context of a reference genome and its corresponding annotation.”；GitHub 最后提交 2025-12 |
| [Apollo 3](https://github.com/GMOD/Apollo3) | 备选 | 基于 JBrowse 2 的多人协作基因模型编辑器（支持本地或服务端部署）。Apollo 2（2019 年论文，doi:10.1371/journal.pcbi.1006790）为旧版服务端程序，仅在社区门户仍运行该版本时沿用。 | [bioRxiv (Cold Spring Harbor Laboratory) 2026](https://doi.org/10.64898/2026.06.08.730970) | Ian H Holmes (University of California, Berkeley) | 较新 · 1 次 | 作者摘要原句：“Its functionality is inspired by existing manual genome annotation tools such as Apollo, Artemis, and Otter, combining features from those tools with an updated and more scalable architecture and technology stack.”；GitHub 最后提交 2026-11 |
| [JBrowse 2](https://github.com/GMOD/jbrowse-components) | 备选，通用工具 | 支持共线性与结构变异视图的基因组浏览器，可挂载各类证据轨道供人工校对使用。 | [Genome biology 2023](https://doi.org/10.1186/s13059-023-02914-z) | Ian H Holmes (University of California, Berkeley) | 标准 · 907 次 | 作者摘要原句：“These improvements are enabled by a ground-up redesign using modern web technology.”；GitHub 最后提交 2026-11 |
| GSAman | 备选 | 结合比对证据人工编辑基因结构模型的桌面工具；对应 LM04 人工校对步骤。 | [The Innovation 2026](https://doi.org/10.1016/j.xinn.2026.101471) | Chengjie Chen (South China Agricultural University) +2 | 较新 · 5 次 | 作者摘要原句：“In contrast to web-based platforms such as Apollo2, which generally require server deployment and do not provide full offline functionality, GSAman delivers a fully local, responsive interface for real-time annotation refinement, thereby improving …” |
| [TBtools-II](https://github.com/CJ-Chen/TBtools-II) | 备选，通用工具 | 面向植物研究的桌面工具集，支持查看 GFF、提取序列与绘制基因结构图；便于快速抽查少量位点。 | [Molecular Plant 2023](https://doi.org/10.1016/j.molp.2023.09.010) | Chengjie Chen (South China Agricultural University) +1 | 标准 · 4462 次 | GitHub 最后提交 2026-10 |
| ORCAE | 备选 | 维基式网页平台，供社区人工校对基因模型。 | [Nature Methods 2012](https://doi.org/10.1038/nmeth.2242) | Lieven Sterck (Ghent University) | 成熟 · 226 次 | 无摘要或仓库说明可引；见原文 |
