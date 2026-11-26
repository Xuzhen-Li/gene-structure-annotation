# gene-structure-annotation
[English](README.md)

本仓库是关于植物基因组基因结构注释的知识库：基因模型是什么，每一步有哪些证据、软件和数据库，怎样检查一套基因集，以及一条带小型示例脚本的参考路线。以葡萄（*Vitis*）贯穿举例，内容同样适用于其他植物基因组。

本页是英文首页 [`README.md`](README.md) 的平行译本，结构相同。

## 本仓库怎么组织

结构与 [TE-Lib](https://github.com/Xuzhen-Li/TE-Lib) 一致：先知识，再软件，再流程。全部页面按主题索引在 [`docs/KNOWLEDGE_MAP.zh.md`](docs/KNOWLEDGE_MAP.zh.md)。

| 部分 | 用来 | 位置 |
|---|---|---|
| 知识单元 | 读一个概念或一组判据，每句话都有论断和来源 | [`docs/kb/`](docs/kb/README.zh.md) |
| 书 | 学习概念和每一步的取舍 | [`book/`](book/README.zh.md)；目录见下 |
| 主题 | 把一步的所有内容放在一处看 | [`docs/KNOWLEDGE_MAP.zh.md`](docs/KNOWLEDGE_MAP.zh.md#topics) |
| 软件与数据库 | 按步骤比较 207 条工具、数据库与思路，附论文、实验室和权威度 | [`catalog/METHODS_CATALOG.zh.md`](catalog/METHODS_CATALOG.zh.md)；[`catalog/README.by-type.zh.md`](catalog/README.by-type.zh.md)；[`catalog/SOFTWARE_AUTHORITY.tsv`](catalog/SOFTWARE_AUTHORITY.tsv) |
| 参考流程 | 走一条路线并选分支 | [`docs/workflow/README.zh.md`](docs/workflow/README.zh.md)；[使用方法](#使用方法) |
| 检查 | 判断一套基因集是否合格 | [`docs/EVALUATION.md`](docs/EVALUATION.md)；[`docs/EVALUATION_CHECKLIST.md`](docs/EVALUATION_CHECKLIST.md) |
| 示例代码与测试数据 | 阅读或运行展示每一步的小脚本 | [`pipeline/`](pipeline/00_overview.md)；[`examples/`](examples/plant_sim/README.md)；[`tests/`](tests/README.md) |
| 图 | 查看各页用到的示意图和统计图 | [`docs/figures/guide/`](docs/figures/guide/README.md) |
| 英文页面 | 阅读英文原版 | [`README.md`](README.md) |
| 旧页面 | 查找作为记录保留的带日期清单、检查和勘误 | [`docs/KNOWLEDGE_MAP.zh.md`](docs/KNOWLEDGE_MAP.zh.md#older-pages) |

`pipeline/` 里的代码是本仓库所述各步的参考代码，规模小，在玩具数据上测试过，不是维护中的软件。

## 知识地图

先读知识单元，再读需要那一步的书章：

- [基因模型及其证据](docs/kb/gene-model-concepts.zh.md)
- [用可信 TE 库做 soft-mask](docs/kb/trusted-softmask.zh.md)
- [基因集够不够好？（判据）](docs/kb/model-qc-criteria.zh.md)
- 编号体系及旧编号与现行编号的对照：[`docs/kb/NUMBERING.zh.md`](docs/kb/NUMBERING.zh.md)
- 全部主题、工具、步骤卡片和示例代码：[`docs/KNOWLEDGE_MAP.zh.md`](docs/KNOWLEDGE_MAP.zh.md)

## 书的目录

书稿《植物基因结构注释学习笔记：以葡萄为例》有中英文两版。从 [`book/README.zh.md`](book/README.zh.md) 开始读，全文见 [`book/BOOK_full.zh.md`](book/BOOK_full.zh.md)。

- [前言](book/chapters/00-preface.zh.md)
- [第 1 章 概念与原理](book/chapters/01-concepts.zh.md)
- [第 2 章 组装与组装质控](book/chapters/02-assembly-and-assembly-qc.zh.md)
- [第 3 章 用可信库做 soft-mask](book/chapters/03-soft-mask-with-a-trusted-library.zh.md)
- [第 4 章 RNA 与 Iso-Seq 证据](book/chapters/04-rna-and-iso-seq-evidence.zh.md)
- [第 5 章 蛋白证据](book/chapters/05-protein-evidence.zh.md)
- [第 6 章 从头基因预测](book/chapters/06-ab-initio-gene-finders.zh.md)
- [第 7 章 DNA 语言模型预测](book/chapters/07-dna-language-model-predictors.zh.md)
- [第 8 章 注释转移（lift-over）](book/chapters/08-lift-over-and-annotation-transfer.zh.md)
- [第 9 章 合并器与注释流程](book/chapters/09-combiners-and-annotation-pipelines.zh.md)
- [第 10 章 非编码 RNA 与假基因位点](book/chapters/10-non-coding-rna-and-pseudogene-loci.zh.md)
- [第 11 章 基因模型质控](book/chapters/11-gene-model-qc.zh.md)
- [第 12 章 人工校对与浏览器](book/chapters/12-curation-and-browsers.zh.md)
- [第 13 章 GFF3 清理与发布](book/chapters/13-gff3-cleanup-and-release.zh.md)
- [第 14 章 参考数据库](book/chapters/14-reference-databases.zh.md)
- [第 15 章 标准与综述](book/chapters/15-standards-and-overview-papers.zh.md)
- [第 16 章 尚未落到单一工具的想法](book/chapters/16-ideas-not-yet-tied-to-one-tool.zh.md)
- [第 17 章 可视化工具](book/chapters/17-visualization-tools.zh.md)
- [第 18 章 怎么选工具](book/chapters/18-choosing-tools.zh.md)
- [第 19 章 常见问题与质控](book/chapters/19-pitfalls-and-qc.zh.md)
- [第 20 章 实例：葡萄基因组走 S1 路线](book/chapters/20-worked-example.zh.md)
- [附录 A 术语表](book/chapters/appendix-a-glossary.zh.md)

## 概述

结构注释是核心层。它用于在基因组上寻找基因位置并提供坐标、GFF3 和蛋白质序列。

![Structure overview](docs/figures/structure_overview.png)

![Structural annotation route](docs/figures/guide/structure_route_map_v2.png)

*图：本仓库的结构注释路线。从组装质控到交给 gene-function-annotation 的发布共六个阶段，标出每个阶段的默认工具和六条主分支（S1、S11、S2、S3、S13、S14）。按手头数据只选一条主分支。示意图，据 README（使用方法、分支路线、默认路线）为本仓库绘制；可编辑 SVG：[`structure_route_map_v2.svg`](docs/figures/guide/structure_route_map_v2.svg)。*

TE soft-mask 是必需的前置步骤。构建 TE 库是一项独立任务，请参考 [TE-Lib](https://github.com/Xuzhen-Li/TE-Lib) 和 [`docs/TE_LIBRARY.md`](docs/TE_LIBRARY.md)。
GO、KEGG 和易读名称位于相邻仓库 [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation) 中。本仓库不生成功能注释表格。

三个层级：
1. 结构层：本仓库。
2. 功能层：[`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation)。
3. TE 库构建：[TE-Lib](https://github.com/Xuzhen-Li/TE-Lib) 和 [`TE_LIBRARY.md`](docs/TE_LIBRARY.md)。

边界定义详见 [`docs/BOUNDARY.md`](docs/BOUNDARY.md)。

入门：英文见 [`docs/START_HERE.md`](docs/START_HERE.md)，中文见 [`docs/zh/README.md`](docs/zh/README.md)。旧的快速开始页、课堂页和任务看板列在[旧页面](docs/KNOWLEDGE_MAP.zh.md#older-pages)。


完整方法目录见 [`catalog/METHODS_CATALOG.zh.md`](catalog/METHODS_CATALOG.zh.md)，概要见下文[方法目录](#方法目录)。

## 使用方法

下面的命令是书中各步的参考代码，在玩具数据上测试过，不是维护中的软件。步骤顺序以哪一页为准，见 [`docs/workflow/README.zh.md`](docs/workflow/README.zh.md)。

中文教学入口为 [`docs/zh/`](docs/zh/)。
如果已完成组装，请将 Asm0/Asm1 视为检查清单，并设置 `ASSEMBLY_OK=yes`。在运行任何 `mkdir` 之前，修改 `local.env` 中的每一个 `/path/to`。
如果使用高质量的参考 GFF，请在问答中设置 `close_curated_ref: true`（参考 `examples/plant_sim/03_solanum_s11`）。默认 `false` 指向 S1；半成品的 Liftoff 保持 `false`。

第一步：提供证据文件。
```bash
git clone https://github.com/Xuzhen-Li/gene-structure-annotation.git
cd gene-structure-annotation
cp pipeline/flow_tool/answers.example.yaml my_answers.yaml
# edit yes/no: RNA? proteins? close reference? paper bar?
python3 pipeline/flow_tool/flow.py --answers my_answers.yaml -o my_plan.md
```
打开 `my_plan.md`，其中包含所选分支及各个阶段的说明。

第二步：配置路径。
```bash
cp config/example.env config/local.env
# set GENOME_FA, BUSCO_LINEAGE, RNA_BAM / PROTEIN_DB, TE lib, WORK_DIR, THREADS
```

第三步：执行分析。
完成 `my_plan.md`。阅读 [Wiki Concepts](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Concepts) 或 [`docs/zh/05_softmask与A0.md`](docs/zh/05_softmask与A0.md)。单独填写 `grade=` 和 `status=`。不要填写 `status=L1`。
仅在勾选完 [Done when](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Start-tonight#done-when) 且 `python3 pipeline/print_qc_commands.py` 退出码为 0 并无 `[STOP]` 提示后，在集群上运行。否则不要设置 `RUN=1`。使用 `--env config/example.env` 浏览时会显示 `[STOP]`；这是正常现象。
按照 `my_plan.md` 的阶段操作并对照 [`docs/EVALUATION_CHECKLIST.md`](docs/EVALUATION_CHECKLIST.md)。完整规则见 [`docs/EVALUATION.md`](docs/EVALUATION.md)。
临时结果不等于 L1。L0 与 L1 的区别请看 [`docs/EVALUATION.md`](docs/EVALUATION.md)。
包含 RNA 和蛋白质且无近缘参考序列的默认分支为 S1。
移交至功能注释请参考 [`docs/HANDOFF_STRUCTURE_TO_FUNCTION.md`](docs/HANDOFF_STRUCTURE_TO_FUNCTION.md)，需包含 `RELEASE_TAG` 和 `PROTEINS_FA=…/release/<TAG>/proteins.faa`。

## 分支路线

根据已有证据选择分支。
S11: 高质量参考 GFF (Liftoff, LiftOn, CAT)。仅 Lift 为 S11-lite。
S1: RNA 和蛋白质 (BRAKER, StringTie)。
S2: 仅蛋白质 (GALBA, GeMoMa)。
S3: 大量 Iso-seq 数据 (IsoQuant, SQANTI)。
S13: GPU 从头预测比冲 (Helixer, Tiberius, ANNEVO)。
S14: 完整经典 PASA 加 EVM 路线 (`docs/steps/dclab/`)。Integrate 步骤 (EVM) 仅在 S14 路线或存在第二套基因集（双轨，即两套基因预测结果）时运行。

叠加层：
L2: L1 接受标准叠加 S5 层，达到论文或 T2T 标准。
S7: 设置 `plant_tandem_focus: true` 时叠加植物 NLR 或串联重复区域分析。

完整路线图位于 [`docs/ROADMAP.md`](docs/ROADMAP.md)。
含工具选择与判断节点的流程图（2026-11-14）：[`docs/ROADMAP.md#workflow-2026-11-14`](docs/ROADMAP.md#workflow-2026-11-14)。

![Which branch to run](docs/figures/guide/structure_branch_decision_v2.png)

*图：按手头数据选主分支，并列出每条分支的首选工具和主要检查项（与第 18 章表格及 README 分支路线一致）。S13、S14、S4 和叠加项只在主草案旁边并行运行。示意图，为本仓库绘制；可编辑 SVG：[`structure_branch_decision_v2.svg`](docs/figures/guide/structure_branch_decision_v2.svg)。*

## 文档目录

知识地图：[`docs/KNOWLEDGE_MAP.zh.md`](docs/KNOWLEDGE_MAP.zh.md)。知识单元：[`docs/kb/`](docs/kb/README.zh.md)。流程索引：[`docs/workflow/README.zh.md`](docs/workflow/README.zh.md)。按日期的改动：[`CHANGELOG.zh.md`](CHANGELOG.zh.md)。

中文教学和起点位于 [`docs/zh/`](docs/zh/) 和 [`docs/START_HERE.md`](docs/START_HERE.md)。

自动计划生成：[`pipeline/flow_tool/`](pipeline/flow_tool/)
阶段输入输出与评估：[`docs/STAGE_IO.md`](docs/STAGE_IO.md)、[`docs/EVALUATION_CHECKLIST.md`](docs/EVALUATION_CHECKLIST.md)、[`docs/EVALUATION.md`](docs/EVALUATION.md)
TE soft-mask：[`docs/TE_LIBRARY.md`](docs/TE_LIBRARY.md)、[`docs/TRUSTED_TE_PATH.md`](docs/TRUSTED_TE_PATH.md)
分支路线图与流程：[`docs/ROADMAP.md`](docs/ROADMAP.md)、[`docs/QUICKSTART.md`](docs/QUICKSTART.md)
三层边界定义：[`docs/BOUNDARY.md`](docs/BOUNDARY.md)
组装后说明单页：[`docs/POST_ASSEMBLY.md`](docs/POST_ASSEMBLY.md)
质控资源：[`docs/QUALITY_SOURCES.md`](docs/QUALITY_SOURCES.md)
EDTA 使用方法：[`docs/tools/edta.md`](docs/tools/edta.md)
BUSCO 参考库：[`docs/LINEAGES.md`](docs/LINEAGES.md)
S11 间隙填充：[`pipeline/A2e_s11_gapfill.md`](pipeline/A2e_s11_gapfill.md)、[`pipeline/A2c_liftoff.md`](pipeline/A2c_liftoff.md)
黄金数据集检查清单：[`examples/golden_pack/`](examples/golden_pack/)
蛋白质数据库：[`pipeline/A2_protein_db.md`](pipeline/A2_protein_db.md)
Helixer 与 BRAKER 对比：[`docs/COMPARE_HELIXER_BRAKER.md`](docs/COMPARE_HELIXER_BRAKER.md)
合并与输入模式：[`docs/MERGE_AND_ENTRIES.md`](docs/MERGE_AND_ENTRIES.md)
EGAPx 对比：[`docs/EGAPX_COMPARE.md`](docs/EGAPX_COMPARE.md)
场景与工具：[`docs/SCENARIOS.md`](docs/SCENARIOS.md)、[`docs/TOOLS.md`](docs/TOOLS.md)、[`docs/cases/vitis-t2t-s1-s5.md`](docs/cases/vitis-t2t-s1-s5.md)、[`docs/TUTORIALS_AND_MEETINGS.md`](docs/TUTORIALS_AND_MEETINGS.md)、[`docs/PLAYBOOK.md`](docs/PLAYBOOK.md)

## 适用范围

本项目不包含功能注释。GO/KEGG 注释请使用 [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation)。
本项目不是独立的 TE 库构建工具。请参考 [TE-Lib](https://github.com/Xuzhen-Li/TE-Lib) 和 `docs/TE_LIBRARY.md`。
本项目不支持泛基因组图谱。请参考 [vitis-pangenome](https://github.com/Xuzhen-Li/vitis-pangenome)。
请勿上传私有 FASTQ/BAM 文件。

作者：Xuzhen Li，[ORCID](https://orcid.org/0000-0003-3670-6657)。

## 方法目录

完整目录（含各节说明、工具表、权威度规则、流程覆盖表、所需数据和图注）见 [`catalog/METHODS_CATALOG.zh.md`](catalog/METHODS_CATALOG.zh.md)。不含各节说明的同样表格见 [`docs/software/README.zh.md`](docs/software/README.zh.md)；按类型的索引见 [`catalog/README.by-type.zh.md`](catalog/README.by-type.zh.md)；逐条数据见 [`catalog/SOFTWARE_AUTHORITY.tsv`](catalog/SOFTWARE_AUTHORITY.tsv)。目录共 **207 条**，2026-11-26 按 TSV 重新统计（命令和分项见 [`catalog/COUNTS.md`](catalog/COUNTS.md)）。目录是阅读清单，下面的默认路线不随它改变。

<a id="default-route"></a>
### 默认路线

默认分支是 S1（有 RNA 和蛋白、没有近缘参考）。先用 TE-Lib 的库经 RepeatMasker 做 soft-mask（A0）；RNA 用 HISAT2 或 STAR 比对、StringTie 组装；长读长用 minimap2 和 IsoQuant；然后用 BRAKER4 加蛋白证据（miniprot 提示或 GeMoMa）。其他分支：S11（Liftoff、LiftOn、CAT），S2（GALBA2、GeMoMa），S3（IsoQuant、SQANTI3），S13（Helixer、Tiberius、ANNEVO），S14（PASA 加 EVM）。这条路线以本页“使用方法”“分支路线”和各节“分组”以及 `docs/ROADMAP.md` 为准；下表把这些工具标为默认或分支工具，其余条目标为备选。

<a id="tier-rule"></a><a id="pipelines"></a><a id="section-1"></a><a id="section-2"></a><a id="section-3"></a><a id="section-4"></a><a id="section-5"></a><a id="section-6"></a><a id="section-7"></a><a id="section-8"></a><a id="section-9"></a><a id="section-10"></a><a id="section-11"></a><a id="section-12"></a><a id="section-13"></a><a id="section-14"></a><a id="section-15"></a><a id="visualization"></a><a id="data-needs"></a><a id="1-组装与组装质控"></a><a id="10-基因模型质控"></a><a id="11-人工校对与浏览器"></a><a id="12-gff3-清理与发布"></a><a id="13-参考数据库"></a><a id="14-标准与综述"></a><a id="15-尚未落到单一工具的想法"></a><a id="2-用可信库做-soft-mask"></a><a id="3-rna-与-iso-seq-证据"></a><a id="4-蛋白证据"></a><a id="5-从头基因预测"></a><a id="6-dna-语言模型预测"></a><a id="7-注释转移lift-over"></a><a id="8-合并器与注释流程"></a><a id="9-非编码-rna-与假基因位点"></a><a id="viz-1"></a><a id="viz-2"></a><a id="viz-3"></a><a id="viz-4"></a><a id="共线性图与点图"></a><a id="可视化工具"></a><a id="基因组之外还需要的数据"></a><a id="基因组浏览器与编辑器"></a><a id="基因结构与异构体图"></a><a id="整套流程覆盖哪些步骤"></a><a id="权威度规则"></a><a id="目录"></a><a id="跨切陷阱"></a><a id="轨道图与染色体图"></a>
### 目录各节

| 小节 | 条目数 | 完整表格 |
|---|---|---|
| 1. 组装与组装质控 | 22 | [第 1 节](catalog/METHODS_CATALOG.zh.md#section-1) |
| 2. 用可信库做 soft-mask | 11 | [第 2 节](catalog/METHODS_CATALOG.zh.md#section-2) |
| 3. RNA 与 Iso-Seq 证据 | 31 | [第 3 节](catalog/METHODS_CATALOG.zh.md#section-3) |
| 4. 蛋白证据 | 8 | [第 4 节](catalog/METHODS_CATALOG.zh.md#section-4) |
| 5. 从头基因预测 | 12 | [第 5 节](catalog/METHODS_CATALOG.zh.md#section-5) |
| 6. DNA 语言模型预测 | 11 | [第 6 节](catalog/METHODS_CATALOG.zh.md#section-6) |
| 7. 注释转移（lift-over） | 10 | [第 7 节](catalog/METHODS_CATALOG.zh.md#section-7) |
| 8. 合并器与注释流程 | 15 | [第 8 节](catalog/METHODS_CATALOG.zh.md#section-8) |
| 9. 非编码 RNA 与假基因位点 | 17 | [第 9 节](catalog/METHODS_CATALOG.zh.md#section-9) |
| 10. 基因模型质控 | 7 | [第 10 节](catalog/METHODS_CATALOG.zh.md#section-10) |
| 11. 人工校对与浏览器 | 8 | [第 11 节](catalog/METHODS_CATALOG.zh.md#section-11) |
| 12. GFF3 清理与发布 | 11 | [第 12 节](catalog/METHODS_CATALOG.zh.md#section-12) |
| 13. 参考数据库 | 11 | [第 13 节](catalog/METHODS_CATALOG.zh.md#section-13) |
| 14. 标准与综述 | 13 | [第 14 节](catalog/METHODS_CATALOG.zh.md#section-14) |
| 15. 尚未落到单一工具的想法 | 8 | [第 15 节](catalog/METHODS_CATALOG.zh.md#section-15) |
| 可视化工具 | 12 | [可视化](catalog/METHODS_CATALOG.zh.md#visualization) |
| 权威度规则 | — | [权威度规则](catalog/METHODS_CATALOG.zh.md#tier-rule) |
| 整套流程覆盖哪些步骤 | — | [整套流程覆盖哪些步骤](catalog/METHODS_CATALOG.zh.md#pipelines) |
| 基因组之外还需要的数据 | — | [基因组之外还需要的数据](catalog/METHODS_CATALOG.zh.md#data-needs) |
| 图注与许可 | — | [图注与许可](catalog/METHODS_CATALOG.zh.md#figure-credits) |

## 许可

本仓库的代码（脚本、流程文件、配置示例和测试）采用 [MIT 许可](LICENSE)。为本仓库撰写的文字、表格和绘制的图采用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hans)。转载自已发表论文的图沿用原文许可，见各图注。详见 [`NOTICE.md`](NOTICE.md)。

<a id="figure-credits"></a>
## 图注与许可

`docs/figures/` 中的自绘概览图归本仓库所有。下方的目录配图均为取自 CC BY 论文的原始未修改 JPEG（Europe PMC 许可字段为 `cc by`，于 2026-11-13 核实），未包含任何 NC/ND 限制素材。

| 文件 | 图注与出处 |
|---|---|
| [`docs/figures/catalog/08_compleasm_vs_busco.jpg`](docs/figures/catalog/08_compleasm_vs_busco.jpg) | 同一批组装上 compleasm 与 BUSCO 的表现对比（图 1）。 Huang 与 Li 2023，《Bioinformatics》图 1，doi:10.1093/bioinformatics/btad595，PMC10558035，CC BY。 |
| [`docs/figures/catalog/03_stringtie2_plant_rnaseq.jpg`](docs/figures/catalog/03_stringtie2_plant_rnaseq.jpg) | StringTie2 在植物 RNA-seq 数据上的转录本组装效果（图 2）。 Kovaka 等 2019，《Genome Biology》图 2，doi:10.1186/s13059-019-1910-1，PMC6912988，CC BY。 |
| [`docs/figures/catalog/07_isoquant_real_reads.jpg`](docs/figures/catalog/07_isoquant_real_reads.jpg) | IsoQuant 在真实长读长 RNA 数据上的表现（图 2）。原图尺寸较扁（719×189）。 Prjibelski 等 2023，《Nature Biotechnology》图 2，doi:10.1038/s41587-022-01565-y，PMC10344776，CC BY。 |
| [`docs/figures/catalog/04_galba_f1_plants.jpg`](docs/figures/catalog/04_galba_f1_plants.jpg) | GALBA 在植物数据上的蛋白比对基因预测表现（图 5）。 Brůna 等 2023，《BMC Bioinformatics》图 5，doi:10.1186/s12859-023-05449-z，PMC10472564，CC BY。 |
| [`docs/figures/catalog/05_helixer_cassava_locus.jpg`](docs/figures/catalog/05_helixer_cassava_locus.jpg) | Helixer 在木薯某一位点预测的基因模型（图 3）。 Stiehler 等 2021，《Bioinformatics》图 3，doi:10.1093/bioinformatics/btaa1044，PMC8016489，CC BY。 |
| [`docs/figures/catalog/12_tiberius_pr_vs_peers.jpg`](docs/figures/catalog/12_tiberius_pr_vs_peers.jpg) | Tiberius 与同类基因预测工具的精确率-召回率对比（图 3）。 Gabriel、Becker、Hoff 与 Stanke 2024，《Bioinformatics》图 3，doi:10.1093/bioinformatics/btae685，PMC11645249，CC BY。 |
| [`docs/figures/catalog/06_helixer_2026_exon_pr.jpg`](docs/figures/catalog/06_helixer_2026_exon_pr.jpg) | Helixer 2026 方法论文中的外显子级别精确率-召回率（图 1）。 Holst 等 2026，《Nature Methods》图 1，doi:10.1038/s41592-025-02939-1，PMC13076211，CC BY。 |
| [`docs/figures/catalog/09_tsebra_sn_sp_arabidopsis.jpg`](docs/figures/catalog/09_tsebra_sn_sp_arabidopsis.jpg) | TSEBRA 在拟南芥上的敏感度与特异度表现（图 3）。 Gabriel 等 2021，《BMC Bioinformatics》图 3，doi:10.1186/s12859-021-04482-0，PMC8620231，CC BY。 |
| [`docs/figures/catalog/10_mikado_arabidopsis_locus.jpg`](docs/figures/catalog/10_mikado_arabidopsis_locus.jpg) | Mikado 在拟南芥某一位点的转录本筛选过程（图 1）。 Venturini 等 2018，《GigaScience》图 1，doi:10.1093/gigascience/giy093，PMC6105091，CC BY。 |
| [`docs/figures/catalog/13_evm_rice_locus.jpg`](docs/figures/catalog/13_evm_rice_locus.jpg) | EVidenceModeler 在水稻某一位点生成的共识基因模型（图 5）。 Haas 等 2008，《Genome Biology》图 5，doi:10.1186/gb-2008-9-1-r7，PMC2395244，CC BY。 |
| [`docs/figures/catalog/01_busco_v5_eukaryote_workflows.jpg`](docs/figures/catalog/01_busco_v5_eukaryote_workflows.jpg) | BUSCO v5 的真核基因组评估流程（图 2）。 Manni 等 2021，《Molecular Biology and Evolution》图 2，doi:10.1093/molbev/msab199，PMC8476166，CC BY。 |
| [`docs/figures/catalog/02_omark_uniprot_proteomes.jpg`](docs/figures/catalog/02_omark_uniprot_proteomes.jpg) | OMArk 在 UniProt 参考蛋白组上的一致性评估（图 4）。 Nevers 等 2025，《Nature Biotechnology》43(1):124-133，图 4，doi:10.1038/s41587-024-02147-w（线上发表于 2024-02-21），PMC11738984，CC BY。 |
| [`docs/figures/catalog/11_psauron_tair10_cds.jpg`](docs/figures/catalog/11_psauron_tair10_cds.jpg) | PSAURON 在 TAIR10 CDS 上的打分分布（图 5）。 Sommer、Zimin 与 Salzberg 2025，《NAR Genomics and Bioinformatics》图 5，doi:10.1093/nargab/lqae189，PMC11704789，CC BY。 |

