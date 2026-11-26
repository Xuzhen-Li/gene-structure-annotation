# 基因模型及其证据

[English](gene-model-concepts.md) · [知识单元](README.zh.md)

## 1. 是什么

基因模型描述组装基因组上的一个基因：基因本身、一个或多个转录本（mRNA），以及每个转录本的外显子、编码区（CDS）和非翻译区（UTR）。结构注释把这些模型写成 GFF3 行，并给出预测的蛋白序列。名称、GO 和通路属于另一层，在 [gene-function-annotation](https://github.com/Xuzhen-Li/gene-function-annotation) 中处理。

## 2. 证据的结构

一个模型最多来自四类证据，之后再做检查：

| 证据 | 提供什么 | 书 |
|---|---|---|
| 转录本（短读长 RNA-seq、长读长） | 外显子和内含子位置；长读长可给出完整异构体 | [第 4 章](../../book/chapters/04-rna-and-iso-seq-evidence.zh.md) |
| 近缘物种的蛋白 | 剪接比对，标出编码外显子 | [第 5 章](../../book/chapters/05-protein-evidence.zh.md) |
| 从头预测与语言模型预测 | 统计或学习得到的基因结构，没有证据比对上的地方也能给出 | [第 6 章](../../book/chapters/06-ab-initio-gene-finders.zh.md)、[第 7 章](../../book/chapters/07-dna-language-model-predictors.zh.md) |
| 近缘的人工校对参考注释 | 从相关基因组转移过来的模型 | [第 8 章](../../book/chapters/08-lift-over-and-annotation-transfer.zh.md) |

合并器和注释流程把这几条证据合成一套基因集（[第 9 章](../../book/chapters/09-combiners-and-annotation-pipelines.zh.md)）。它们都要求先对基因组的重复序列做 soft-mask（见[用可信 TE 库做 soft-mask](trusted-softmask.zh.md)）。

## 3. 怎样认出可用的基因模型（现场卡片）

- 每条 CDS 行的 `Parent` 是一个 mRNA，每个 mRNA 的 `Parent` 是一个基因。
- 每条 CDS 行都填了 phase 列。
- 蛋白文件由同一份 GFF3 翻译得到，ID 一致。
- METHODS 写明一条主草稿路线和各工具版本。

后两条对应的发布检查是 [`docs/EVALUATION.md`](../EVALUATION.md) 中的 G3 和 G5，本页不重复。

## 4. 本仓库的默认路线与分支

默认路线和各分支（S1、S11、S2、S3、S13、S14）见 [README 分支路线](../../README.zh.md#分支路线)、[`docs/ROADMAP.md`](../ROADMAP.md) 和 [`catalog/_branches.md`](../../catalog/_branches.md)。流程索引见 [`docs/workflow/README.zh.md`](../workflow/README.zh.md)。

## 5. 植物与葡萄中已知的情况

- 植物基因组大、转座子多、常为多倍体；来源见书第 1 章 [1.2 节](../../book/chapters/01-concepts.md#12-why-plant-genomes-are-hard)。
- 相邻基因被并成一个的嵌合基因模型，是近年植物和无脊椎动物基因组注释中已知的错误类型（同上）。
- 葡萄实例见 [`docs/cases/vitis-t2t-s1-s5.md`](../cases/vitis-t2t-s1-s5.md)。葡萄基因模型中合并或拆分错误所占比例，本页不给出数字：**[待确认]**。

## 6. 论断与来源

引文保留原文英文。

| 论断 | 来源 | 原文引句 | 读了什么 |
|---|---|---|---|
| GFF3 中 `Parent` 属性把外显子归入转录本、把转录本归入基因。 | GFF3 规范，Sequence Ontology（[gff3.md](https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md)） | “A parent ID can be used to group exons into transcripts, transcripts into genes, an so forth.”（拼写照原文） | 规范正文，`Parent` 属性的定义 |
| 每条 CDS 行必须有 phase。 | GFF3 规范，同上 | “The phase is REQUIRED for all CDS features.” | 规范正文，第 8 列 |
| 小团队也能注释真核基因组，但仍然困难。 | Yandell 与 Ence 2012，*Nat Rev Genet* 13:329，[doi:10.1038/nrg3174](https://doi.org/10.1038/nrg3174) | “Although annotating a eukaryotic genome assembly is now within the reach of non-experts, it remains a challenging task.” | 摘要（PubMed 22510764） |
| 不做屏蔽就预测，会在重复区产生假基因结构。 | BRAKER README（[Gaius-Augustus/BRAKER](https://github.com/Gaius-Augustus/BRAKER)） | “This will avoid the prediction of false positive gene structures in repetitive and low complexitiy regions.”（拼写照原文） | README 中关于基因组文件的一节 |
| 植物基因组因体量、转座子和多倍性而难以注释。 | 书第 1 章 1.2 节，引用 [doi:10.1002/aps3.11533](https://doi.org/10.1002/aps3.11533) | “Plant genomes are large, rich in transposable elements and often polyploid” | 章节正文；本页未重新打开所引论文 |

## 7. 相关页面

- 书：[第 1 章 概念与原则](../../book/chapters/01-concepts.zh.md)；[第 13 章 GFF3 清理与发布](../../book/chapters/13-gff3-cleanup-and-release.zh.md)
- 知识单元：[用可信 TE 库做 soft-mask](trusted-softmask.zh.md)；[基因集够不够好？](model-qc-criteria.zh.md)
- 按步骤查软件：[`catalog/README.by-type.md`](../../catalog/README.by-type.md)
- 结构、功能与 TE 三层的边界：[`docs/BOUNDARY.md`](../BOUNDARY.md)
