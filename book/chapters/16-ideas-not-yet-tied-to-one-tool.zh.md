# 第 16 章 尚未落到单一工具的想法

*本章收录[主页第 15 节](../../README.zh.md#section-15)：该节说明、含论文、实验室、权威度和评价的完整工具表，以及评测要点。链接指回仓库。*

2026-11 调研记录的思路。在完成实测前，不改变默认路径。

**需要：** 视具体思路而定；在完成实测前，不改变默认路径。[按场景列出的数据需求](../../README.zh.md#data-needs)

**分组：**
- *流程规则*（互补）：Soft-mask hand-off rule (idea)、Family-window check using function results (idea)、Track annotation edit distance (AED) per model、Harmonise models across haplotypes before pangenome PAV。经测试验证后将纳入本仓库流程的规则。
- *已知错误类型*（互补）：Chimeric mis-annotation survey、Annotation affects orthology (idea)。阐述基因模型错误如何传导至直系同源推断与功能分析。
- *AI 辅助校对*（可替代）：GeneWhisperer、Human-AI collaborative annotation framework。目前仅停留在方案阶段；采用时必须保留人工签字确认。


| 工具 | 角色 | 用途 / 何时用 | 原始论文 | 实验室（通讯作者，机构） | 权威度（档位 · 被引） | 评价（出处） |
|---|---|---|---|---|---|---|
| [Soft-mask hand-off rule (idea)](https://github.com/Xuzhen-Li/gene-structure-annotation/blob/main/docs/BOUNDARY.md) | 思路 | 结构注释直接消费外部产出的审定版 TE 库；需在 METHODS 中记录库名称、版本与 sha256 校验值，并确保库中已剔除 NLR 等基因家族序列（见现有的 ProtExcluder 说明）。 | 无文章 | — | 无论文 | 仓库简介：“Pipelines for structural genome annotation, providing gene models and GFF3 outputs from FASTA and evidence.”；GitHub 最后提交 2026-11 |
| Chimeric mis-annotation survey | 思路 | 指出融合（嵌合）基因模型在非模式真核生物注释中依然普遍存在，并给出相应的检测启发式规则。 | [BMC Genomics 2025](https://doi.org/10.1186/s12864-025-11765-w) | Andreas Bachler (Commonwealth Scientific and Industrial Research Organisation) | 较新 · 7 次 | 作者摘要原句：“By addressing these annotation errors, we improve genomic data reliability and facilitate a deeper understanding of non-model organisms.” |
| Annotation affects orthology (idea) | 思路 | 基因结构注释策略的选择会影响下游直系同源推断；在得出跨物种结论前应先比对注释方案。 | [Bioinformatics 2025](https://doi.org/10.1093/bioinformatics/btaf365) | Silvia Prieto-Baños (SIB Swiss Institute of Bioinformatics) +1 | 较新 · 26 次 | 作者摘要原句：“We observe significant discrepancies between sources, namely in the proportion of orthologous genes per genome, the completeness of Hierarchical Orthologous Groups, and the accuracy and recall of the predicted orthologs on a standard orthology benchmark.” |
| GeneWhisperer | 思路 | 配备专用任务工具、辅助人工基因注释的大语言模型助手（预印本）。 | [bioRxiv (Cold Spring Harbor Laboratory) 2025](https://doi.org/10.1101/2025.03.30.646211) | Xiaomei Li (Commonwealth Scientific and Industrial Research Organisation) | 较新 · 5 次 | 论文摘要：“In response to these challenges, we present GeneWhisperer, an innovative assistant system designed to facilitate the manual gene functional annotation process.” |
| Human-AI collaborative annotation framework | 思路 | 在 AI 工具与人工校对员之间划分基因组注释任务的概念框架。 | [Briefings in Bioinformatics 2025](https://doi.org/10.1093/bib/bbaf377) | Xiaomei Li (Commonwealth Scientific and Industrial Research Organisation) +1 | 较新 · 8 次 | 作者摘要原句：“These combined outcomes from automated tools and manual curation highlight the importance of integrating human expertise with artificial intelligence (AI) capabilities to improve both the accuracy and efficiency of genome annotation.” |
| [Family-window check using function results (idea)](https://github.com/Xuzhen-Li/gene-function-annotation) | 思路 | 场景 S7 可读取 gene-function-annotation 产出的 NLR/TF 基因家族窗口列表，并回头复核这些窗口内的基因模型；家族分类器本身仍保留在功能注释目录中。 | 无文章 | — | 无论文 | 仓库简介：“Assigns functional labels like GO, KEGG, and domains to protein sequences after structure annotation.”；GitHub 最后提交 2026-11 |
| Track annotation edit distance (AED) per model | 思路 | 把每个模型与证据的一致程度（AED，由 Eilbeck 等 2009 年提出，MAKER2 会输出）作为发布中的一列保存，方便校对人员先看证据弱的模型。 | [BMC Bioinformatics 2009](https://doi.org/10.1186/1471-2105-10-67) | Mark D. Yandell (University of Utah) | 成熟 · 171 次 | 无摘要或仓库说明可引；见原文 |
| [Harmonise models across haplotypes before pangenome PAV](https://github.com/Xuzhen-Li/vitis-pangenome) | 思路 | 将蛋白序列交由 vitis-pangenome 分析前，先利用共线性（SynGAP 方式）让两套单倍型互相对照打磨，确保基因 PAV 反映真实生物学差异而非注释噪声。 | [Genome biology 2024](https://doi.org/10.1186/s13059-024-03359-8) | Chengjie Chen (South China Agricultural University) +1 | 较新 · 18 次 | GitHub 最后提交 2026-11 |
