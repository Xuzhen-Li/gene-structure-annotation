# 用可信 TE 库做 soft-mask

[English](trusted-softmask.md) · [知识单元](README.zh.md)

## 1. 是什么

预测基因之前要先屏蔽基因组中的重复序列。**soft-mask** 把重复碱基写成小写、保留序列，基因预测软件会降低这些碱基的权重。**hard-mask** 把重复碱基换成 `N`，序列就丢了。重复序列靠一个转座子（TE）共有序列库来识别；用哪个库，决定哪些碱基被屏蔽。

## 2. 证据的结构

TE 库要经过四种产物，只有最后一种可以用来给基因注释做 soft-mask：

| 产物 | 是什么 | 能否用于基因 soft-mask |
|---|---|---|
| 原始发现库（例如 EDTA 输出） | 发现工具找到的全部序列 | 否 |
| 工作库 | 聚类和修剪后的共有序列 | 否 |
| 分类标签 | 给工作库加上的结构域和超家族名称 | 否，只是标签 |
| 可信库 | 做过有记录的宿主基因清除和成文的分类规则，带版本和 sha256 | 是 |

非 TE 重复（串联重复、端粒、rDNA）单独成一条线，不进入可信库。库本身在 [TE-Lib](https://github.com/Xuzhen-Li/TE-Lib) 中构建；本仓库只使用它（A0 步）。

## 3. 怎样认出正确的 soft-mask（现场卡片）

- 屏蔽后的基因组中重复序列是小写，不是成串的 `N`。
- 写明唯一的可信库文件及其版本和 sha256。
- METHODS 说明没有把工作库当作可信库。
- 不把屏蔽比例当作基因组的 TE 含量报告，两者不是同一个数。

通过与不通过的规则见 [`docs/EVALUATION.md`](../EVALUATION.md#g2--soft-mask-honesty) 的 G2 和自动不通过条款，本页不重复。

## 4. 本仓库的默认路线与分支

默认步骤是 [`docs/TE_LIBRARY.md`](../TE_LIBRARY.md) 和 [`docs/TRUSTED_TE_PATH.md`](../TRUSTED_TE_PATH.md) 中的 A0。之后要换库或改屏蔽设置，走分支 S10（[`catalog/_branches.md`](../../catalog/_branches.md)）。这一步的工具见[方法目录第 2 节](../../catalog/METHODS_CATALOG.zh.md#section-2)。

## 5. 植物与葡萄中已知的情况

- EDTA 以人工校对的水稻 TE 库为基准做了评测，并在玉米和果蝇上做了测试（见下表第 3 条）。
- 重复区里也有真基因，例如 NLR 抗病基因，这是不做 hard-mask 的原因之一（[`docs/EVALUATION.md`](../EVALUATION.md#g2--soft-mask-honesty) G2 背景）。
- 葡萄从发现到可信库的路线是 TE-Lib 中的实例（[soft-mask 交接](https://github.com/Xuzhen-Li/TE-Lib/blob/main/docs/detection/softmask_handoff.zh.md)）。宿主基因清除工具如何去掉侧翼序列，在那里标为 **[待确认]**，这里不作为事实重复。

## 6. 论断与来源

引文保留原文英文。

| 论断 | 来源 | 原文引句 | 读了什么 |
|---|---|---|---|
| BRAKER 要求基因组已做 soft-mask。 | BRAKER README（[Gaius-Augustus/BRAKER](https://github.com/Gaius-Augustus/BRAKER)） | “BRAKER should only be applied to genomes that have been softmasked for repeats!” | README 中典型调用一节 |
| 屏蔽可以避免重复区里的假基因结构。 | BRAKER README，同上 | “This will avoid the prediction of false positive gene structures in repetitive and low complexitiy regions.”（拼写照原文） | README 中关于基因组文件的一节 |
| EDTA 生成过滤后的非冗余 TE 库，以水稻为基准评测。 | Ou 等 2019，*Genome Biol* 20:275，[doi:10.1186/s13059-019-1905-y](https://doi.org/10.1186/s13059-019-1905-y) | “Using the most robust programs, we create a comprehensive pipeline called Extensive de-novo TE Annotator (EDTA) that produces a filtered non-redundant TE library for annotation of structurally intact and fragmented elements.” | 摘要（PubMed 31843001） |
| hard-mask 会删掉预测软件需要的序列。 | 本仓库 [`docs/EVALUATION.md`](../EVALUATION.md#g2--soft-mask-honesty) G2 背景 | “Hard-masking to `N` deletes sequence that predictors need; soft-mask (`-xsmall`) keeps bases but down-weights repeats” | 当前 main 分支上的文件 |
| 只有可信库可以用于基因 soft-mask。 | TE-Lib [`docs/detection/softmask_handoff.md`](https://github.com/Xuzhen-Li/TE-Lib/blob/main/docs/detection/softmask_handoff.md) | “This trusted file, with its version and sha256, is the only library that may be used for gene soft-mask or as EDTA `--curatedlib`.” | 当前 main 分支上的文件 |
| 非 TE 重复不进入可信库。 | 本仓库 [`docs/TE_LIBRARY.md`](../TE_LIBRARY.md) | “Non-TE repeats (TRF, telomere, rDNA, …) are a **separate non-TE track** — **never** enter `--curatedlib`.” | 当前 main 分支上的文件 |

## 7. 相关页面

- 书：[第 3 章 用可信库做 soft-mask](../../book/chapters/03-soft-mask-with-a-trusted-library.zh.md)
- TE-Lib：[home page](https://github.com/Xuzhen-Li/TE-Lib)（TE 类别、检测工具、可信库路线）
- 知识单元：[基因模型及其证据](gene-model-concepts.zh.md)；[基因集够不够好？](model-qc-criteria.zh.md)
