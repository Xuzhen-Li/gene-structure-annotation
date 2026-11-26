# 按类型的目录索引

[English](README.by-type.md) · [完整目录](METHODS_CATALOG.zh.md) · [条目数](COUNTS.md) · [按阶段的索引](README.md)

方法目录每个类型小节一行。条目数来自 [`SOFTWARE_AUTHORITY.tsv`](SOFTWARE_AUTHORITY.tsv)（207 条，2026-11-26）。类型键是 2026-11 调研文件 [`docs/CATALOG_BY_TYPE_2026-11.md`](../docs/CATALOG_BY_TYPE_2026-11.md) 中的标签，该文件作为旧记录保留。本目录下的文件夹按阶段存放首批卡片，其索引 [`README.md`](README.md) 保持不变，作为第二种视图。

| # | 类型小节 | 类型键（旧） | 条目数 | 默认与分支工具 | 书章 | 知识单元 |
|---|---|---|---|---|---|---|
| 1 | [1. 组装与组装质控](METHODS_CATALOG.zh.md#section-1) | `assembly-qc` | 22 | hifiasm | [第 2章](../book/chapters/02-assembly-and-assembly-qc.zh.md) | — |
| 2 | [2. 用可信库做 soft-mask](METHODS_CATALOG.zh.md#section-2) | `soft-mask` | 11 | RepeatMasker | [第 3章](../book/chapters/03-soft-mask-with-a-trusted-library.zh.md) | [trusted-softmask](../docs/kb/trusted-softmask.zh.md) |
| 3 | [3. RNA 与 Iso-Seq 证据](METHODS_CATALOG.zh.md#section-3) | `rna-evidence` | 31 | HISAT2, STAR, minimap2, PASA, IsoQuant, SQANTI3, StringTie (v3 line) | [第 4章](../book/chapters/04-rna-and-iso-seq-evidence.zh.md) | [gene-model-concepts](../docs/kb/gene-model-concepts.zh.md) |
| 4 | [4. 蛋白证据](METHODS_CATALOG.zh.md#section-4) | `protein-evidence` | 8 | miniprot | [第 5章](../book/chapters/05-protein-evidence.zh.md) | [gene-model-concepts](../docs/kb/gene-model-concepts.zh.md) |
| 5 | [5. 从头基因预测](METHODS_CATALOG.zh.md#section-5) | `ab-initio` | 12 | BRAKER4, GALBA2, Tiberius, ANNEVO, Helixer | [第 6章](../book/chapters/06-ab-initio-gene-finders.zh.md) | [gene-model-concepts](../docs/kb/gene-model-concepts.zh.md) |
| 6 | [6. DNA 语言模型预测](METHODS_CATALOG.zh.md#section-6) | `language-model` | 11 | — | [第 7章](../book/chapters/07-dna-language-model-predictors.zh.md) | [gene-model-concepts](../docs/kb/gene-model-concepts.zh.md) |
| 7 | [7. 注释转移（lift-over）](METHODS_CATALOG.zh.md#section-7) | `lift-over` | 10 | GeMoMa, Liftoff, LiftOn, Comparative Annotation Toolkit (CAT) | [第 8章](../book/chapters/08-lift-over-and-annotation-transfer.zh.md) | [gene-model-concepts](../docs/kb/gene-model-concepts.zh.md) |
| 8 | [8. 合并器与注释流程](METHODS_CATALOG.zh.md#section-8) | `combiner-pipeline` | 15 | EVidenceModeler (EVM) | [第 9章](../book/chapters/09-combiners-and-annotation-pipelines.zh.md) | [gene-model-concepts](../docs/kb/gene-model-concepts.zh.md) |
| 9 | [9. 非编码 RNA 与假基因位点](METHODS_CATALOG.zh.md#section-9) | `ncrna-pseudogene` | 17 | — | [第 10章](../book/chapters/10-non-coding-rna-and-pseudogene-loci.zh.md) | — |
| 10 | [10. 基因模型质控](METHODS_CATALOG.zh.md#section-10) | `model-qc` | 7 | — | [第 11章](../book/chapters/11-gene-model-qc.zh.md) | [model-qc-criteria](../docs/kb/model-qc-criteria.zh.md) |
| 11 | [11. 人工校对与浏览器](METHODS_CATALOG.zh.md#section-11) | `curation-browser` | 8 | — | [第 12章](../book/chapters/12-curation-and-browsers.zh.md) | — |
| 12 | [12. GFF3 清理与发布](METHODS_CATALOG.zh.md#section-12) | `gff-release` | 11 | — | [第 13章](../book/chapters/13-gff3-cleanup-and-release.zh.md) | [gene-model-concepts](../docs/kb/gene-model-concepts.zh.md) |
| 13 | [13. 参考数据库](METHODS_CATALOG.zh.md#section-13) | `database` | 11 | — | [第 14章](../book/chapters/14-reference-databases.zh.md) | — |
| 14 | [14. 标准与综述](METHODS_CATALOG.zh.md#section-14) | `standard-review` | 13 | — | [第 15章](../book/chapters/15-standards-and-overview-papers.zh.md) | — |
| 15 | [15. 尚未落到单一工具的想法](METHODS_CATALOG.zh.md#section-15) | `idea` | 8 | — | [第 16章](../book/chapters/16-ideas-not-yet-tied-to-one-tool.zh.md) | — |
| viz | [可视化工具](METHODS_CATALOG.zh.md#visualization) | — | 12 | — | [第 17 章](../book/chapters/17-visualization-tools.zh.md) | — |

**合计：207**

## 没有卡片的阶段文件夹

以下阶段文件夹没有首批卡片，保留它们是为了让阶段链接仍然有效；这些步骤的工具见上面的类型小节。

- Asm0 — assembly: [`Asm0_assembly/`](Asm0_assembly/README.md)
- A4 — aggregation (A4a TSEBRA, A4b Mikado, A4c–A4d EVM, A4e PASA update): [`A4_aggregation/`](A4_aggregation/README.md)
- A3 — proteins from GFF: [`A3_proteins/`](A3_proteins/README.md)
- Last mile 01 — BUSCO / PSAURON QC: [`LM01_qc_busco_psauron/`](LM01_qc_busco_psauron/README.md)
- Last mile 02 — priority loci (02, 02b): [`LM02_priority_loci/`](LM02_priority_loci/README.md)
- Last mile 03 — evidence pack: [`LM03_evidence_pack/`](LM03_evidence_pack/README.md)
- A6 / A6b — hand-off to function: [`A6_handoff_to_function/`](A6_handoff_to_function/README.md)
