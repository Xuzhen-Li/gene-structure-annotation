# 第 8 章 注释转移（lift-over）

*本章收录[主页第 7 节](../../README.zh.md#section-7)：该节说明、含论文、实验室、权威度和评价的完整工具表，以及评测要点。链接指回仓库。*

将近缘、已审定的注释转移到新组装上（A2b / S11 / S4）。

**需要：** 近缘且已审定的参考 GFF（同种或可信单倍型）及目标基因组；若要申报完整 S11 而非 S11-lite，还需准备补缺（gap-fill）证据。[按场景列出的数据需求](../../README.zh.md#data-needs)

**分组：**
- *坐标转移*（可替代）：Liftoff、LiftOn、Comparative Annotation Toolkit (CAT)、GrAnnoT。有近缘且经人工审校的参考（S11）时，优先选用兼顾蛋白的 LiftOn 而非 Liftoff；多基因组经 HAL 比对时用 CAT；跨泛基因组图谱时用 GrAnnoT。
- *基于同源的预测*（可替代）：GeMoMa、TOGA2。GeMoMa 根据参考蛋白和内含子位置预测新模型；TOGA2 经全基因组比对链投射基因并推断直系同源。两者都比坐标转移更适合较远的参考。
- *转移后的检查与打磨*（互补）：LiftoffTools、GENESPACE、SynGAP。LiftoffTools 报告有变化的基因，GENESPACE 显示共线性缺口（用于检查）；然后用 SynGAP 修正缺失或拆分的模型。


| 工具 | 角色 | 用途 / 何时用 | 原始论文 | 实验室（通讯作者，机构） | 权威度（档位 · 被引） | 评价（出处） |
|---|---|---|---|---|---|---|
| [GeMoMa](https://www.jstacs.de/index.php/GeMoMa) | 分支 S2 | 利用内含子位置保守性及可选 RNA-seq 数据的同源基因预测工具。 | [Methods in molecular biology 2019](https://doi.org/10.1007/978-1-4939-9173-0_9) | Jens Keilwagen (Julius Kühn-Institut) | 标准 · 617 次 | 无摘要或仓库说明可引；见原文 |
| [Liftoff](https://github.com/agshumate/Liftoff) | 分支 S11 | 将参考基因组注释投射到同种或近缘物种目标组装上的工具。 | [Bioinformatics 2021](https://doi.org/10.1093/bioinformatics/btaa1016) | Alaina Shumate (Johns Hopkins University) | 标准 · 1144 次 | 作者摘要原句：“We show that Liftoff can accurately map 99.9% of genes between two versions of the human reference genome with an average sequence identity >99.9%.”；GitHub 最后提交 2023-08 |
| [LiftOn](https://github.com/Kuanhao-Chao/LiftOn) | 分支 S11 | 结合 DNA（Liftoff）与蛋白（miniprot）比对结果以改进注释转移质量。 | [Genome Research 2024](https://doi.org/10.1101/gr.279620.124) | Kuan-Hao Chao (Johns Hopkins University) | 较新 · 51 次 | 作者摘要原句：“Here we introduce LiftOn, a homology-based software tool that integrates DNA and protein alignments to enhance the accuracy of genome-scale annotation and to allow mapping between relatively distant species.”；GitHub 最后提交 2026-10 |
| [Comparative Annotation Toolkit (CAT)](https://github.com/ComparativeGenomicsToolkit/Comparative-Annotation-Toolkit) | 分支 S11 | 通过 Cactus 全基因组比对投射基因注释，并与从头预测结果合并。 | [Genome Research 2018](https://doi.org/10.1101/gr.233460.117) | Benedict Paten (Howard Hughes Medical Institute) | 成熟 · 141 次 | 作者摘要原句：“We show that CAT can be used to improve annotations on the rat genome, annotate the great apes, annotate a diverse set of mammals, and annotate personal, diploid human genomes.”；GitHub 最后提交 2025-05 |
| [GrAnnoT](https://forge.ird.fr/diade/dynadiv/grannot) | 备选 | 通过泛基因组图（GFA）将 GFF3 注释转移至图内嵌合的各个基因组，输出图注释（GAF）与单基因组 GFF3。 | [Peer Community Journal 2025](https://doi.org/10.24072/pcjournal.651) | François Sabot (Institut de Recherche pour le Développement) | 较新 · 10 次 | 论文摘要：“We introduce here GrAnnoT, a tool designed for an efficient and reliable integration of annotation information in such variation graphs.” |
| [TOGA2](https://github.com/hillerlab/TOGA2) | 备选 | TOGA2 是 TOGA 的快速升级版，基于全基因组比对将注释投射与直系同源推断整合在一起。方法论文仍引 TOGA（见下）。 | [Science 2023](https://doi.org/10.1126/science.abn3107) | Michael Hiller (Goethe University Frankfurt) +1 | 成熟 · 237 次 | GitHub 最后提交 2026-11 |
| [LiftoffTools](https://github.com/agshumate/LiftoffTools) | 备选 | 比较不同组装间的转移注释结果，分析基因序列变异、共线性与拷贝数变化。 | [F1000Research 2022](https://doi.org/10.12688/f1000research.124059.2) | Alaina Shumate (Johns Hopkins University) | 小众 · 22 次 | 论文摘要：“Here we present LiftoffTools, a toolkit to automate the detection and analysis of gene sequence variants, synteny, and gene copy number changes.”；GitHub 最后提交 2023-08 |
| [GENESPACE](https://github.com/jtlovell/GENESPACE) | 备选 | 基于共线性约束做跨基因组直系同源分析，并在共线性背景下定位缺失或新增基因。 | [eLife 2022](https://doi.org/10.7554/eLife.78526) | John T. Lovell (Lawrence Berkeley National Laboratory) | 成熟 · 439 次 | 论文摘要：“Here, we present GENESPACE, which addresses these challenges by integrating conserved gene order and orthology to define the expected physical position of all genes across multiple genomes.”；GitHub 最后提交 2025-01 |
| [SynGAP](https://github.com/yanyew/SynGAP) | 备选 | 利用与近缘已注释基因组的共线性关系，检出并修正缺失、拆分或错误合并的基因模型；对应跨单倍型的 LM05 打磨步骤。 | [Genome biology 2024](https://doi.org/10.1186/s13059-024-03359-8) | Chengjie Chen (South China Agricultural University) +1 | 较新 · 18 次 | 作者摘要原句：“SynGAP offers exceptional capabilities in the improvement of gene structure annotation quality and the profiling of integrative gene synteny between species.”；GitHub 最后提交 2025-12 |
| [AugustusCGP](https://github.com/Gaius-Augustus/Augustus) | 备选 | AUGUSTUS 的比较模式，在多基因组比对上同时预测基因；CAT 使用它。 | [Bioinformatics 2016](https://doi.org/10.1093/bioinformatics/btw494) | Stefanie König (Universität Greifswald) +1 | 小众 · 70 次 | GitHub 最后提交 2026-11 |
