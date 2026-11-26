# 编号体系

[English](NUMBERING.md) · [知识单元](README.zh.md)

本仓库同时用到几套编号。新页面用现行编号；旧编号留在旧页面中，不重新编号。本页给出对照。

| 编号体系 | 标签 | 状态 | 定义在 |
|---|---|---|---|
| 目录类型小节 | 1–15 与可视化 | 现行 | [`catalog/METHODS_CATALOG.zh.md`](../../catalog/METHODS_CATALOG.zh.md)；TSV 的 `section` 列 |
| 书章 | 第 1–20 章与附录 A；第 *n* + 1 章对应类型小节 *n*，第 17 章对应可视化 | 现行 | [`book/`](../../book/README.zh.md) |
| 分支编号 | S1–S14：草稿路线 S1、S2、S3、S6、S11、S13、S14；叠加 S4、S5、S7–S10、S12 | 现行 | [`docs/ROADMAP.md`](../ROADMAP.md)；[`catalog/_branches.md`](../../catalog/_branches.md) |
| 完成等级与门槛 | L0、L1、L2；G1–G9 | 现行 | [`docs/EVALUATION.md`](../EVALUATION.md) |
| 阶段编号 | Asm0、Asm1、A0–A6、收尾 01–06 | 流程步骤现行 | [`docs/STAGE_IO.md`](../STAGE_IO.md) |
| 首批卡片的阶段文件夹 | `Asm0_assembly/` … `LM06_release/`；文件夹 `LMnn` 即收尾第 *nn* 步 | 旧视图（2026-11 首批） | [`catalog/README.md`](../../catalog/README.md) |
| 类型键 | `assembly-qc` … `idea` | 旧（2026-11 调研） | [`docs/CATALOG_BY_TYPE_2026-11.md`](../CATALOG_BY_TYPE_2026-11.md) |

## 类型小节、旧类型键与书章对照

| 类型小节（现行） | 类型键（旧） | 书章 |
|---|---|---|
| [1. 组装与组装质控](../../catalog/METHODS_CATALOG.zh.md#section-1) | `assembly-qc` | [第 2 章 组装与组装质控](../../book/chapters/02-assembly-and-assembly-qc.zh.md) |
| [2. 用可信库做 soft-mask](../../catalog/METHODS_CATALOG.zh.md#section-2) | `soft-mask` | [第 3 章 用可信库做 soft-mask](../../book/chapters/03-soft-mask-with-a-trusted-library.zh.md) |
| [3. RNA 与 Iso-Seq 证据](../../catalog/METHODS_CATALOG.zh.md#section-3) | `rna-evidence` | [第 4 章 RNA 与 Iso-Seq 证据](../../book/chapters/04-rna-and-iso-seq-evidence.zh.md) |
| [4. 蛋白证据](../../catalog/METHODS_CATALOG.zh.md#section-4) | `protein-evidence` | [第 5 章 蛋白证据](../../book/chapters/05-protein-evidence.zh.md) |
| [5. 从头基因预测](../../catalog/METHODS_CATALOG.zh.md#section-5) | `ab-initio` | [第 6 章 从头基因预测](../../book/chapters/06-ab-initio-gene-finders.zh.md) |
| [6. DNA 语言模型预测](../../catalog/METHODS_CATALOG.zh.md#section-6) | `language-model` | [第 7 章 DNA 语言模型预测](../../book/chapters/07-dna-language-model-predictors.zh.md) |
| [7. 注释转移（lift-over）](../../catalog/METHODS_CATALOG.zh.md#section-7) | `lift-over` | [第 8 章 注释转移（lift-over）](../../book/chapters/08-lift-over-and-annotation-transfer.zh.md) |
| [8. 合并器与注释流程](../../catalog/METHODS_CATALOG.zh.md#section-8) | `combiner-pipeline` | [第 9 章 合并器与注释流程](../../book/chapters/09-combiners-and-annotation-pipelines.zh.md) |
| [9. 非编码 RNA 与假基因位点](../../catalog/METHODS_CATALOG.zh.md#section-9) | `ncrna-pseudogene` | [第 10 章 非编码 RNA 与假基因位点](../../book/chapters/10-non-coding-rna-and-pseudogene-loci.zh.md) |
| [10. 基因模型质控](../../catalog/METHODS_CATALOG.zh.md#section-10) | `model-qc` | [第 11 章 基因模型质控](../../book/chapters/11-gene-model-qc.zh.md) |
| [11. 人工校对与浏览器](../../catalog/METHODS_CATALOG.zh.md#section-11) | `curation-browser` | [第 12 章 人工校对与浏览器](../../book/chapters/12-curation-and-browsers.zh.md) |
| [12. GFF3 清理与发布](../../catalog/METHODS_CATALOG.zh.md#section-12) | `gff-release` | [第 13 章 GFF3 清理与发布](../../book/chapters/13-gff3-cleanup-and-release.zh.md) |
| [13. 参考数据库](../../catalog/METHODS_CATALOG.zh.md#section-13) | `database` | [第 14 章 参考数据库](../../book/chapters/14-reference-databases.zh.md) |
| [14. 标准与综述](../../catalog/METHODS_CATALOG.zh.md#section-14) | `standard-review` | [第 15 章 标准与综述](../../book/chapters/15-standards-and-overview-papers.zh.md) |
| [15. 尚未落到单一工具的想法](../../catalog/METHODS_CATALOG.zh.md#section-15) | `idea` | [第 16 章 尚未落到单一工具的想法](../../book/chapters/16-ideas-not-yet-tied-to-one-tool.zh.md) |
