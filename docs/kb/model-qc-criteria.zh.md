# 基因集够不够好？（判据）

[English](model-qc-criteria.md) · [知识单元](README.zh.md)

这是一个判据单元。分级、硬门槛和不通过规则只写在一处：[`docs/EVALUATION.md`](../EVALUATION.md)。本页解释各项检查测的是什么并指向原文，不抄阈值。

## 1. 是什么

一套基因集从三方面判断：**完整性**（该有的基因在不在）、**一致性**（基因组成是否与近缘物种相符，没有大量碎片、多余基因或污染）和**有效性**（GFF3 与蛋白是否一致、格式检查是否通过）。本仓库把这些检查落成三个完成等级：L0（临时）、L1（合格）和 L2（论文或 T2T 标准）。

## 2. 证据的结构

| 问题 | 常用指标 | 规则在哪里 |
|---|---|---|
| 保守基因在不在？ | 蛋白 BUSCO，并写明谱系 | [G6](../EVALUATION.md#g6--protein-busco-reported) |
| 坏模型或多余模型多不多？ | 单个模型打分与最差位点清单；OMArk 一致性 | [G7](../EVALUATION.md#g7--beyond-busco-triage)；[软指标](../EVALUATION.md#soft-metrics-interpret-do-not-fake-universal-cutoffs) |
| 文件之间是否一致？ | GFF3 校验；蛋白由同一份 GFF3 翻译 | [G4、G5](../EVALUATION.md#g4--models-validate) |
| 能声称哪个等级？ | L1 需过全部硬门槛；L2 另加检查 | [三个完成等级](../EVALUATION.md#three-finish-grades) |

## 3. 怎样认出可靠的质控报告（现场卡片）

- BUSCO 写明谱系数据集名称。
- BUSCO 不是唯一的检查。
- `grade=` 和 `status=` 分开写。
- 临时草稿不称为最终版。

## 4. 本仓库的默认路线与分支

按规则逐项核对用 [`docs/EVALUATION_CHECKLIST.md`](../EVALUATION_CHECKLIST.md)。质控工具见[方法目录第 10 节](../../catalog/METHODS_CATALOG.zh.md#section-10)。处理最差模型的收尾步骤（优先位点、人工校对、发布）是 [`catalog/`](../../catalog/README.md) 中的 LM01 至 LM06 文件夹。

## 5. 植物与葡萄中已知的情况

- BUSCO 只统计保守单拷贝基因，谱系特有、串联重复和与 TE 重叠的基因被低估（[G7 背景](../EVALUATION.md#g7--beyond-busco-triage)）。
- 葡萄 T2T 实例展示了达到 L2 的一种做法（[`docs/cases/vitis-t2t-s1-s5.md`](../cases/vitis-t2t-s1-s5.md)）。其他类群要按评估页的要求写出自己的谱系和校对说明。
- 植物整体的 OMArk 一致性参考值，本页不给出：**[待确认]**。

## 6. 论断与来源

引文保留原文英文。

| 论断 | 来源 | 原文引句 | 读了什么 |
|---|---|---|---|
| BUSCO 用通用单拷贝直系同源基因衡量完整性和冗余。 | Manni 等 2021，*Mol Biol Evol* 38:4647，[doi:10.1093/molbev/msab199](https://doi.org/10.1093/molbev/msab199) | “BUSCO estimates the completeness and redundancy of processed genomic data based on universal single-copy orthologs.” | 摘要（PubMed 34320186） |
| 完整性工具看不到过度预测和污染。 | Nevers 等 2025，*Nat Biotechnol* 43:124，[doi:10.1038/s41587-024-02147-w](https://doi.org/10.1038/s41587-024-02147-w) | “State-of-the-art tools to assess genome annotations measure the completeness of a gene repertoire but are blind to other errors, such as gene overprediction or contamination.” | 摘要（PubMed 38383603） |
| OMArk 增加与近缘物种的一致性比较并提示污染。 | Nevers 等 2025，同上 | “OMArk assesses not only the completeness but also the consistency of the gene repertoire as a whole relative to closely related species and reports likely contamination events.” | 摘要（PubMed 38383603） |
| 不写谱系的 BUSCO 数值无法解读。 | 本仓库 [`docs/EVALUATION.md`](../EVALUATION.md#g6--protein-busco-reported) G6 背景 | “Reporting C without the odb name is not interpretable.” | 当前 main 分支上的文件 |
| 葡萄的 L2 做法是实例，不是其他类群的勾选清单。 | 本仓库 [`docs/EVALUATION.md`](../EVALUATION.md) | “do not copy grape OMArk/window depth as a checkbox” | 当前 main 分支上的文件，非葡萄 L2 一节 |

## 7. 相关页面

- 书：[第 11 章 基因模型质控](../../book/chapters/11-gene-model-qc.zh.md)；[第 19 章 常见陷阱与质控](../../book/chapters/19-pitfalls-and-qc.zh.md)
- 知识单元：[基因模型及其证据](gene-model-concepts.zh.md)；[用可信 TE 库做 soft-mask](trusted-softmask.zh.md)
- 下一层：功能注释的检查见 [gene-function-annotation `docs/EVALUATION.md`](https://github.com/Xuzhen-Li/gene-function-annotation/blob/main/docs/EVALUATION.md)
