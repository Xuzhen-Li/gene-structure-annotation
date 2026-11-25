# 第 15 章 标准与综述

*本章收录[主页第 14 节](../../README.zh.md#section-14)：该节说明、含论文、实验室、权威度和评价的完整工具表，以及评测要点。链接指回仓库。*

相关标准、文件格式与综述文献，并非数据配方。

**需要：** 并非数据配方。本节收录的是标准、格式与综述。[按场景列出的数据需求](../../README.zh.md#data-needs)

**分组：**
- *格式与命名*（互补）：Sequence Ontology、GFF3 specification、The grapevine gene nomenclature system。每次发布均须遵循的规范。
- *指南与基准*（互补）：A beginner's guide to eukaryotic genome annotation、Ten steps to get started in genome assembly and annotation、Twelve quick steps for genome assembly and annotation、Tips for improving genome annotation quality、Welcome to the big leaves (plant annotation best practice)、Ab initio gene predictor benchmark、LRGASP benchmark、EBP annotation standards report、Plant microRNA annotation criteria。建议先读植物最佳实践论文；各基准测试则指出了不同工具的常见失效场景。


| 工具 | 角色 | 用途 / 何时用 | 原始论文 | 实验室（通讯作者，机构） | 权威度（档位 · 被引） | 评价（出处） |
|---|---|---|---|---|---|---|
| [Sequence Ontology](https://github.com/The-Sequence-Ontology/SO-Ontologies) | 参考 | 定义 GFF3 第三列特征类型（feature type）的标准本体。 | [Genome biology 2005](https://doi.org/10.1186/gb-2005-6-5-r44) | Michael Ashburner (University of Cambridge) | 标准 · 929 次 | GitHub 最后提交 2026-08 |
| [GFF3 specification](https://github.com/The-Sequence-Ontology/Specifications) | 参考 | GFF3 文件格式的正式规范文档。 | 无文章 | — | 无论文 | 仓库简介：“GFF and GVF specification documents”；GitHub 最后提交 2024-06 |
| The grapevine gene nomenclature system | 参考 | 葡萄基因与基因组位点的命名规则建议。 | [BMC Genomics 2014](https://doi.org/10.1186/1471-2164-15-1077) | Jérôme Grimplet (Consejo Superior de Investigaciones Científicas) | 成熟 · 124 次 | 作者摘要原句：“To better exploit the results obtained by the international community, we think that a coordinated nomenclature for gene naming in species with sequenced genomes is essential.” |
| A beginner's guide to eukaryotic genome annotation | 参考 | 真核基因组注释入门综述，涵盖证据类型、常用流程与质量评估指标（如 AED）。 | [Nat Rev Genet 2012](https://doi.org/10.1038/nrg3174) | Mark D. Yandell (University of Utah) | 标准 · 797 次 | 无摘要或仓库说明可引；见原文 |
| Ten steps to get started in genome assembly and annotation | 参考 | 从基因组组装到注释的十步实操指南。 | [F1000Research 2018](https://doi.org/10.12688/f1000research.13598.1) | Henrik Lantz (Uppsala University) | 成熟 · 157 次 | 论文摘要：“As a part of the ELIXIR-EXCELERATE efforts in capacity building, we present here 10 steps to facilitate researchers getting started in genome assembly and genome annotation.” |
| [LRGASP benchmark](https://github.com/LRGASP/lrgasp-submissions) | 参考 | 长读长 RNA-seq 转录本识别与定量方法的社区基准评测，展示了测序深度、读长与准确度之间的权衡关系。 | [Nature Methods 2024](https://doi.org/10.1038/s41592-024-02298-3) | Christopher Vollmers (University of California, Santa Cruz) +6 | 成熟 · 312 次 | GitHub 最后提交 2023-12 |
| Tips for improving genome annotation quality | 参考 | 提升基因组注释质量的实操核对清单，涵盖证据选择、重复序列屏蔽强度、人工校对与评估指标。 | [Genomics Communications 2025](https://doi.org/10.48130/gcomm-0025-0006) | Lan Lan (Murdoch University) | 较新 · 21 次 | 作者摘要原句：“To reduce the annotation errors, we briefly list six tips during the annotation process, and the noteworthy details in different widely used annotation tools/pipelines such as MAKER and EvidenceModeler, to improve annotation quality.” |
| [EBP annotation standards report](https://www.earthbiogenome.org/report-on-annotation-standards) | 参考 | 地球生物基因组计划（EBP）关于注释最低标准与元数据的规范报告。 | 无文章 | — | 无论文 | 无摘要或仓库说明可引；见原文 |
| Welcome to the big leaves (plant annotation best practice) | 参考 | 评测植物注释流程，并针对非模式植物的证据准备、重复序列屏蔽和 BUSCO 评估给出实操建议。 | [Applications in Plant Sciences 2023](https://doi.org/10.1002/aps3.11533) | Jill Wegrzyn (University of Connecticut) | 较新 · 67 次 | 无摘要或仓库说明可引；见原文 |
| Ab initio gene predictor benchmark | 参考 | 在多种真核生物上对从头基因预测工具做基准测试；解释了为什么在长且内含子多的基因上外显子水平准确率会下降。 | [BMC Genomics 2020](https://doi.org/10.1186/s12864-020-6707-9) | Julie Thompson (Centre National de la Recherche Scientifique) | 成熟 · 122 次 | 作者摘要原句：“New benchmark methods are needed to evaluate the accuracy of gene prediction methods in the face of incomplete genome assemblies, low genome coverage and quality, complex gene structures, or a lack of suitable sequences for evidence-based annotations.” |
| Twelve quick steps for genome assembly and annotation | 参考 | 面向教学体量的组装、屏蔽、注释与质控简明演练；可作为前述入门指南的简短补充。 | [PLoS Computational Biology 2020](https://doi.org/10.1371/journal.pcbi.1008325) | Hyungtaek Jung (Queensland University of Technology) +1 | 小众 · 94 次 | 作者摘要原句：“In genomics, generating a high-quality genome assembly/annotation has become an indispensable tool for better understanding the biology of any species.” |
| Plant microRNA annotation criteria | 参考 | 基于小 RNA 数据认定植物 miRNA 位点的社区标准；是发布集中所有 miRNA 注释的准入门槛。 | [The Plant Cell 2018](https://doi.org/10.1105/tpc.17.00851) | Blake C. Meyers (Donald Danforth Plant Science Center) | 成熟 · 486 次 | 作者摘要原句：“We argue that improved annotation systems are needed for miRNAs and all other classes of plant small RNAs.” |
| RGASP transcript reconstruction assessment | 参考 | RNA-seq 转录本重建方法基准评测；选组装工具时参考。 | [Nature Methods 2013](https://doi.org/10.1038/nmeth.2714) | Paul Bertone (European Bioinformatics Institute) | 标准 · 827 次 | 作者摘要原句：“Consequently, the complexity of higher eukaryotic genomes imposes severe limitations on transcript recall and splice product discrimination that are likely to remain limiting factors for the analysis of current-generation RNA-seq data.” |
