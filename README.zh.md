# gene-structure-annotation
[English](README.md)

本项目提供基因组结构注释的分析流程。
中文教学位于 [`docs/zh/`](docs/zh/)。
可运行的文档保持英文格式 [`docs/BILINGUAL.md`](docs/BILINGUAL.md)。
植物模拟数据位于 [`examples/plant_sim/`](examples/plant_sim/)。

## 概述

结构注释是核心层。它用于在基因组上寻找基因位置并提供坐标、GFF3 和蛋白质序列。

![Structure overview](docs/figures/structure_overview.png)

TE soft-mask 是必需的前置步骤。构建 TE 库是一项独立任务，请参考 [vitis-te](https://github.com/Xuzhen-Li/vitis-te) 和 [`docs/TE_LIBRARY.md`](docs/TE_LIBRARY.md)。
GO、KEGG 和易读名称位于相邻仓库 [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation) 中。本仓库不生成功能注释表格。

三个层级：
1. 结构层：本仓库。
2. 功能层：[`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation)。
3. TE 库构建：[vitis-te](https://github.com/Xuzhen-Li/vitis-te) 和 [`TE_LIBRARY.md`](docs/TE_LIBRARY.md)。

边界定义详见 [`docs/BOUNDARY.md`](docs/BOUNDARY.md)。

中文最短路径位于 [`docs/zh/README.md`](docs/zh/README.md)。英文入口位于 [`docs/START_HERE.md`](docs/START_HERE.md)。
快速开始指南位于 [Wiki Start-tonight](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Start-tonight)。离线版本位于 [`docs/CLASSROOM_TONIGHT.md`](docs/CLASSROOM_TONIGHT.md)。
任务看板位于 [Annotation board (Project #2)](https://github.com/users/Xuzhen-Li/projects/2)。


本页同时也是 2026-11 方法目录，分 15 个类型小节，共收录 135 条工具、数据库与思路。默认路径不变（见「使用方法」和 `docs/ROADMAP.md`）。阶段顺序仍以路线图和 `catalog/` 为准。

## 使用方法

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

## 文档目录

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
本项目不是独立的 TE 库构建工具。请参考 [vitis-te](https://github.com/Xuzhen-Li/vitis-te) 和 `docs/TE_LIBRARY.md`。
本项目不支持泛基因组图谱。请参考 [vitis-pangenome](https://github.com/Xuzhen-Li/vitis-pangenome)。
请勿上传私有 FASTQ/BAM 文件。

作者：Xuzhen Li，[ORCID](https://orcid.org/0000-0003-3670-6657)。

## 方法目录

本页按类型列出 2026-11 调研整理的 135 条方法、工具、数据库与思路（类型目录 78 条，`catalog/` 首轮卡片 57 条）。默认路径仍以「使用方法」和 `docs/ROADMAP.md` 为准，本目录不作改动。阶段顺序仍见路线图和 `catalog/`。完整表格与勘误见 `docs/CATALOG_BY_TYPE_2026-11.md` 和 `docs/CATALOG_NEW_TOOLS_2026-11.md`。

## 目录

1. [组装与组装质控](#section-1) (17)
2. [用可信库做 soft-mask](#section-2) (5)
3. [RNA 与 Iso-Seq 证据](#section-3) (22)
4. [蛋白证据](#section-4) (4)
5. [从头基因预测](#section-5) (9)
6. [DNA 语言模型预测](#section-6) (6)
7. [注释转移（lift-over）](#section-7) (8)
8. [合并器与注释流程](#section-8) (11)
9. [非编码 RNA 与假基因位点](#section-9) (15)
10. [基因模型质控](#section-10) (5)
11. [人工校对与浏览器](#section-11) (6)
12. [GFF3 清理与发布](#section-12) (8)
13. [参考数据库](#section-13) (5)
14. [标准与综述](#section-14) (8)
15. [尚未落到单一工具的想法](#section-15) (6)

- [基因组之外还需要的数据](#data-needs)
- [图注与许可](#figure-credits)

各节与本库阶段的对应关系：组装与质控（Asm0/Asm1）→ soft-mask（A0）→ 证据与一条草案分支（S11/S1/S2/S3/S13/S14）→ 合并器（A4）→ 模型质控与 last-mile → 发布与移交（A6）。阶段编号仍见 `docs/ROADMAP.md` 和 `catalog/`。

<a id="section-1"></a>
## 1. 组装与组装质控

用于判断组装能否进入注释，或直接生成单倍型 FASTA 的工具（Asm0、Asm1）。

**需要：** 组装 FASTA；若需检查 k-mer 或碱基准确度，还需附上组装所用的测序读长。BUSCO 需选用与类群匹配的 lineage（见 `docs/LINEAGES.md`）。[按场景列出的数据需求](#data-needs)

各条目的单句简介译自英文目录，英文原句见英文版 README。

![compleasm versus BUSCO](docs/figures/catalog/08_compleasm_vs_busco.jpg)

*同一批组装上 compleasm 与 BUSCO 的表现对比（图 1）。 Huang 与 Li 2023，《Bioinformatics》图 1，doi:10.1093/bioinformatics/btad595，PMC10558035，CC BY。*

- **hifiasm** (tool) — 面向 PacBio HiFi 读长的单倍型分型从头组装工具（支持 trio、Hi-C 或超长读长分型模式）。 [doi:10.1038/s41592-020-01056-5](https://doi.org/10.1038/s41592-020-01056-5) · [link](https://github.com/chhylp123/hifiasm)
- **Verkko** (tool) — 在组装图中结合 HiFi 与超长 ONT 读长的端粒到端粒（T2T）二倍体组装工具。 [doi:10.1038/s41587-023-01662-6](https://doi.org/10.1038/s41587-023-01662-6) · [link](https://github.com/marbl/verkko)
- **YaHS** (tool) — 利用 Hi-C 数据将 contig 挂载为染色体级别 scaffold 的组装工具。 [doi:10.1093/bioinformatics/btac808](https://doi.org/10.1093/bioinformatics/btac808) · [link](https://github.com/c-zhou/yahs)
- **RagTag** (tool) — 基于参考基因组对草案组装做纠错、挂载（scaffolding）与补洞（patching）的工具。 [doi:10.1186/s13059-022-02823-7](https://doi.org/10.1186/s13059-022-02823-7) · [link](https://github.com/malonge/RagTag)
- **GenomeScope 2.0 / Smudgeplot** (tool) — 根据测序读长的 k-mer 分布估算基因组大小、杂合度与倍性。 [doi:10.1038/s41467-020-14998-3](https://doi.org/10.1038/s41467-020-14998-3) · [link](https://github.com/tbenavi1/genomescope2.0)
- **Merqury** (tool) — 无需参考基因组，基于 k-mer 评估组装的碱基质量值（QV）、完整性与分型质量。 [doi:10.1186/s13059-020-02134-9](https://doi.org/10.1186/s13059-020-02134-9) · [link](https://github.com/marbl/merqury)
- **QUAST** (tool) — 统计组装连续性与错误组装指标，可选用参考基因组作比对。 [doi:10.1093/bioinformatics/btt086](https://doi.org/10.1093/bioinformatics/btt086) · [link](https://github.com/ablab/quast)
- **Inspector** (tool) — 利用长读长数据做无参考组装评估与碱基纠错。 [doi:10.1186/s13059-021-02527-4](https://doi.org/10.1186/s13059-021-02527-4) · [link](https://github.com/Maggi-Chen/Inspector)
- **KAT (K-mer Analysis Toolkit)** (tool) — 比较测序读长与组装结果的 k-mer 频谱（绘制拷贝数分布图）。 [doi:10.1093/bioinformatics/btw663](https://doi.org/10.1093/bioinformatics/btw663) · [link](https://github.com/EarlhamInst/KAT)
- **BlobToolKit** (tool) — 通过交互式 GC 含量、覆盖度与物种分类图识别污染 contig。 [doi:10.1534/g3.119.400908](https://doi.org/10.1534/g3.119.400908) · [link](https://github.com/genomehubs/blobtoolkit)
- **Tiara** (tool) — 利用深度学习将 contig 划分为核基因组、细胞器基因组或原核生物来源。 [doi:10.1093/bioinformatics/btab672](https://doi.org/10.1093/bioinformatics/btab672) · [link](https://github.com/ibe-uw/tiara)
- **tidk** (tool) — 在组装序列上检索端粒重复序列并绘图。 [doi:10.1093/bioinformatics/btaf049](https://doi.org/10.1093/bioinformatics/btaf049) · [link](https://github.com/tolkit/telomeric-identifier)
- **quarTeT** (tool) — 端粒到端粒（T2T）分析工具包：涵盖基于参考的组装、补洞以及端粒与着丝粒识别。 [doi:10.1093/hr/uhad127](https://doi.org/10.1093/hr/uhad127) · [link](https://github.com/aaranyue/quarTeT)
- **GCI** (tool) — Genome Continuity Inspector：基于读长回贴计算近完整组装的连续性得分。 [doi:10.1093/bioinformatics/btae633](https://doi.org/10.1093/bioinformatics/btae633) · [link](https://github.com/yeeus/GCI)
- **gfastats** (tool) — 对 FASTA/GFA 格式组装文件做快速统计与处理的工具。 [doi:10.1093/bioinformatics/btac460](https://doi.org/10.1093/bioinformatics/btac460) · [link](https://github.com/vgl-hub/gfastats)
- **CRAQ** (tool) — 根据软剪切（clipped）读长比对结果做无参考组装评估，检测局部与结构组装错误。 [link](https://github.com/JiaoLaboratory/CRAQ) [待确认]
- **NCBI FCS-GX** (tool) — 在提交或注释前检测并剔除组装中的外源物种污染。 [doi:10.1186/s13059-024-03198-7](https://doi.org/10.1186/s13059-024-03198-7) · [link](https://github.com/ncbi/fcs)

<a id="section-2"></a>
## 2. 用可信库做 soft-mask

利用可信 TE 库屏蔽重复序列，或屏蔽低复杂度序列。本库不负责构建 TE 库。

**需要：** 一份可信的 TE 库（来自 vitis-te 或其他审定库）。本节仅做 soft-mask，不构建 TE 库。[按场景列出的数据需求](#data-needs)


- **RepeatMasker** (tool) — 利用给定的重复序列库（Dfam 或经审定的物种专有库）屏蔽重复序列；`-xsmall` 参数输出 soft-masking 结果。 [link](https://github.com/Dfam-consortium/RepeatMasker)
- **Dfam** (resource) — RepeatMasker 所用的转座子（TE）家族与隐马尔可夫模型（profile HMM）公开数据库。 [doi:10.1186/s13100-020-00230-y](https://doi.org/10.1186/s13100-020-00230-y) · [link](https://www.dfam.org/)
- **Tandem Repeats Finder (TRF)** (tool) — 检测串联重复序列。 [doi:10.1093/nar/27.2.573](https://doi.org/10.1093/nar/27.2.573) · [link](https://github.com/Benson-Genomics-Lab/TRF)
- **WindowMasker** (tool) — 无需重复序列库，直接基于高频 k-mer 做序列屏蔽的工具（NCBI）。 [doi:10.1093/bioinformatics/bti774](https://doi.org/10.1093/bioinformatics/bti774) · [link](https://www.ncbi.nlm.nih.gov/IEB/ToolBox/CPP_DOC/lxr/source/src/app/winmasker/)
- **ULTRA** (tool) — 对串联重复与低复杂度重复做概率标注；输出结果可配合可信 TE 库用于 soft-masking。 [doi:10.1093/bioadv/vbae149](https://doi.org/10.1093/bioadv/vbae149) · [link](https://github.com/TravisWheelerLab/ULTRA)

<a id="section-3"></a>
## 3. RNA 与 Iso-Seq 证据

提供基因模型证据的短读长与长读长 RNA 比对、转录本组装及 ORF 预测（A1b）。

**需要：** 尽可能使用同一基因型的短读长 RNA-seq（FASTQ 或现成的 `RNA_BAM`）；若走 S3 分支，需补充高深度 Iso-Seq / 长读长转录组。[按场景列出的数据需求](#data-needs)

![StringTie2 plant RNA-seq](docs/figures/catalog/03_stringtie2_plant_rnaseq.jpg)

*StringTie2 在植物 RNA-seq 数据上的转录本组装效果（图 2）。 Kovaka 等 2019，《Genome Biology》图 2，doi:10.1186/s13059-019-1910-1，PMC6912988，CC BY。*

![IsoQuant real reads](docs/figures/catalog/07_isoquant_real_reads.jpg)

*IsoQuant 在真实长读长 RNA 数据上的表现（图 2）。原图尺寸较扁（719×189）。 Prjibelski 等 2023，《Nature Biotechnology》图 2，doi:10.1038/s41587-022-01565-y，PMC10344776，CC BY。*

- **HISAT2** (tool) — 面向短读长 RNA-seq 的剪接比对工具（基于图索引）。 [doi:10.1038/s41587-019-0201-4](https://doi.org/10.1038/s41587-019-0201-4) · [link](https://github.com/DaehwanKimLab/hisat2)
- **STAR** (tool) — 超快速短读长剪接比对工具，支持两轮（two-pass）剪接位点发现。 [doi:10.1093/bioinformatics/bts635](https://doi.org/10.1093/bioinformatics/bts635) · [link](https://github.com/alexdobin/STAR)
- **minimap2** (tool) — 面向长读长及 cDNA/Iso-Seq 数据的剪接比对工具（`-ax splice`）。 [doi:10.1093/bioinformatics/bty191](https://doi.org/10.1093/bioinformatics/bty191) · [link](https://github.com/lh3/minimap2)
- **fastp** (tool) — 一体化 FASTQ 质控与接头切除工具。 [doi:10.1093/bioinformatics/bty560](https://doi.org/10.1093/bioinformatics/bty560) · [link](https://github.com/OpenGene/fastp)
- **Trinity** (tool) — 利用 RNA-seq 数据做从头或基因组引导的转录本组装。 [doi:10.1038/nbt.1883](https://doi.org/10.1038/nbt.1883) · [link](https://github.com/trinityrnaseq/trinityrnaseq)
- **PASA** (tool) — 将转录本比对并组装为基因结构，同时利用此信息更新基因模型的 UTR 与可变剪接异构体。 [doi:10.1093/nar/gkg770](https://doi.org/10.1093/nar/gkg770) · [link](https://github.com/PASApipeline/PASApipeline)
- **TransDecoder** (tool) — 在转录本中识别候选编码区（结合同源比对或 Pfam 支持的 ORF）。 [link](https://github.com/TransDecoder/TransDecoder)
- **IsoQuant** (tool) — 基于参考基因组做长读长转录本发现与定量。 [doi:10.1038/s41587-022-01565-y](https://doi.org/10.1038/s41587-022-01565-y) · [link](https://github.com/ablab/IsoQuant)
- **Bambu** (tool) — 结合上下文信息的长读长转录本发现与定量工具（R/Bioconductor 包）。 [doi:10.1038/s41592-023-01908-w](https://doi.org/10.1038/s41592-023-01908-w) · [link](https://github.com/GoekeLab/bambu)
- **SQANTI3** (tool) — 对照参考注释对长读长转录本异构体做分类与过滤。 [doi:10.1038/s41592-024-02229-2](https://doi.org/10.1038/s41592-024-02229-2) · [link](https://github.com/ConesaLab/SQANTI3)
- **TAMA** (tool) — 归并冗余的长读长转录本模型并提供 Iso-Seq 注释辅助功能。 [doi:10.1186/s12864-020-07123-7](https://doi.org/10.1186/s12864-020-07123-7) · [link](https://github.com/GenomeRIK/tama)
- **IsoSeq (PacBio)** (tool) — PacBio 官方 Iso-Seq 数据处理流程（含 refine、cluster、collapse 步骤）。 [link](https://github.com/PacificBiosciences/IsoSeq)
- **StringTie (v3 line)** (tool) — 利用短读长与长读长 RNA 数据做参考引导或从头转录本组装；在本库中用作转录本证据与对照轨道。 [doi:10.1186/s13059-019-1910-1](https://doi.org/10.1186/s13059-019-1910-1) · [link](https://github.com/gpertea/stringtie)
- **FLIC (Full-length isoform constructor)** (tool) — 综合生物学重复一致性及 TSS/polyA 峰识别结果，由长读长数据构建全长转录本异构体。 [doi:10.1093/bioinformatics/btaf551](https://doi.org/10.1093/bioinformatics/btaf551) · [link](https://github.com/albidgy/FLIC)
- **Isocall** (tool) — 跨多个 PacBio Iso-Seq 样本联合识别已知与新转录本异构体（可替代 isoseq cluster/collapse）。 [link](https://github.com/PacificBiosciences/isocall)
- **ESPRESSO** (tool) — 从含测序错误的长读长 RNA-seq 数据中发现并定量转录本异构体。 [doi:10.1126/sciadv.abq5072](https://doi.org/10.1126/sciadv.abq5072) · [link](https://github.com/Xinglab/espresso)
- **TAGET** (tool) — Iso-Seq 分析工具包：涵盖基于 CNN 剪接位点校正的比对、异构体分类与表达定量。 [doi:10.1038/s41467-023-41649-0](https://doi.org/10.1038/s41467-023-41649-0) [待确认]
- **RiboCode** (tool) — 根据核糖体印迹（Ribo-seq）数据识别处于活跃翻译状态的 ORF。 [doi:10.1093/nar/gky179](https://doi.org/10.1093/nar/gky179) · [link](https://github.com/xryanglab/RiboCode)
- **Ribo-TISH** (tool) — 利用常规 Ribo-seq 或 QTI-seq 数据识别翻译起始位点与 ORF。 [doi:10.1038/s41467-017-01981-8](https://doi.org/10.1038/s41467-017-01981-8) · [link](https://github.com/zhpn1024/ribotish)
- **PhyloCSF++** (tool) — PhyloCSF 加速版：基于多物种序列比对的密码子替换模式评估蛋白编码潜能。 [doi:10.1093/bioinformatics/btab756](https://doi.org/10.1093/bioinformatics/btab756) · [link](https://github.com/cpockrandt/PhyloCSFpp)
- **KuPID** (tool) — 基于 k-mer 的长读长上游预处理工具，用于辅助下游转录本异构体发现（预印本）。 [doi:10.64898/2025.12.05.692400](https://doi.org/10.64898/2025.12.05.692400) [待确认]
- **RiboBA** (tool) — 兼容多种 Ribo-seq 实验方案、可校正偏好性的概率型 ORF 识别工具（预印本）。 [doi:10.64898/2026.03.17.712439](https://doi.org/10.64898/2026.03.17.712439) [待确认]

<a id="section-4"></a>
## 4. 蛋白证据

将蛋白比对到基因组，为基因模型提供提示（hint）或同源草案（A2 输入）。

**需要：** 来自近缘物种或审定数据库的蛋白集（`PROTEIN_DB`），用于比对到基因组（miniprot、GeneMark-EP、GALBA / GeMoMa）。[按场景列出的数据需求](#data-needs)

![GALBA plant F1](docs/figures/catalog/04_galba_f1_plants.jpg)

*GALBA 在植物数据上的蛋白比对基因预测表现（图 5）。 Brůna 等 2023，《BMC Bioinformatics》图 5，doi:10.1186/s12859-023-05449-z，PMC10472564，CC BY。*

- **miniprot** (tool) — 快速的蛋白到基因组剪接比对工具。 [doi:10.1093/bioinformatics/btad014](https://doi.org/10.1093/bioinformatics/btad014) · [link](https://github.com/lh3/miniprot)
- **GenomeThreader** (tool) — 将蛋白或 cDNA 序列剪接比对到基因组的工具。 [doi:10.1016/j.infsof.2005.09.005](https://doi.org/10.1016/j.infsof.2005.09.005) · [link](https://genomethreader.org/)
- **Exonerate** (tool) — 通用序列比对工具，支持 protein2genome 剪接比对模式。 [doi:10.1186/1471-2105-6-31](https://doi.org/10.1186/1471-2105-6-31)
- **Spaln** (tool) — 带物种特异参数的 cDNA/蛋白到基因组剪接比对工具。 [doi:10.1093/bioinformatics/btn460](https://doi.org/10.1093/bioinformatics/btn460) · [link](https://github.com/ogotoh/spaln)

<a id="section-5"></a>
## 5. 从头基因预测

在屏蔽后的基因组上预测基因模型的从头预测或证据引导预测工具（A2）。

**需要：** 已做 soft-mask 的基因组；若预测工具支持引入证据提示（BRAKER），再附上 RNA 和/或蛋白。Helixer / Tiberius 可仅凭基因组运行，但在有 RNA 数据时，不应悄悄替代基于证据的 S1 草案。[按场景列出的数据需求](#data-needs)

![Helixer cassava locus](docs/figures/catalog/05_helixer_cassava_locus.jpg)

*Helixer 在木薯某一位点预测的基因模型（图 3）。 Stiehler 等 2021，《Bioinformatics》图 3，doi:10.1093/bioinformatics/btaa1044，PMC8016489，CC BY。*

- **AUGUSTUS** (tool) — 结合 RNA 与蛋白证据提示（hints）的 HMM 基因预测工具。 [doi:10.1093/bioinformatics/btn013](https://doi.org/10.1093/bioinformatics/btn013) · [link](https://github.com/Gaius-Augustus/Augustus)
- **BRAKER3** (tool) — 结合 RNA-seq 与蛋白证据、自动串联 GeneMark-ETP 与 AUGUSTUS 的全自动基因预测流程。 [doi:10.1101/gr.278090.123](https://doi.org/10.1101/gr.278090.123) · [link](https://github.com/Gaius-Augustus/BRAKER)
- **BRAKER2** (tool) — BRAKER 的蛋白证据模式（串联 GeneMark-EP+ 与 AUGUSTUS）。 [doi:10.1093/nargab/lqaa108](https://doi.org/10.1093/nargab/lqaa108) · [link](https://github.com/Gaius-Augustus/BRAKER)
- **GALBA** (tool) — 利用近缘物种的 miniprot 蛋白比对结果训练 AUGUSTUS。 [doi:10.1186/s12859-023-05449-z](https://doi.org/10.1186/s12859-023-05449-z) · [link](https://github.com/Gaius-Augustus/GALBA)
- **SNAP** (tool) — 可在新基因组上重新训练的半隐马尔可夫（semi-HMM）从头基因预测工具。 [doi:10.1186/1471-2105-5-59](https://doi.org/10.1186/1471-2105-5-59) · [link](https://github.com/KorfLab/SNAP)
- **GlimmerHMM** (tool) — 基于广义隐马尔可夫模型（GHMM）的真核从头基因预测工具。 [doi:10.1093/bioinformatics/bth315](https://doi.org/10.1093/bioinformatics/bth315) · [link](https://ccb.jhu.edu/software/glimmerhmm/)
- **Tiberius** (tool) — 结合端到端深度学习与 HMM 的从头基因预测工具。 [doi:10.1093/bioinformatics/btae685](https://doi.org/10.1093/bioinformatics/btae685) · [link](https://github.com/Gaius-Augustus/Tiberius)
- **GeneMark-ETP** (tool) — 整合转录本与蛋白证据并支持自训练的基因预测工具（BRAKER3 的核心组件）。 [doi:10.1101/gr.278373.123](https://doi.org/10.1101/gr.278373.123) · [link](https://github.com/gatech-genemark/GeneMark-ETP)
- **ANNEVO (paper)** (tool) — 对演化上下文建模的深度学习从头基因注释工具（本库此前已收录该工具的预印本版本）。 [doi:10.21203/rs.3.rs-6402260/v1](https://doi.org/10.21203/rs.3.rs-6402260/v1) · [link](https://github.com/xjtu-omics/ANNEVO)

<a id="section-6"></a>
## 6. DNA 语言模型预测

基于 DNA 语言模型的基因预测工具；除非另有书面说明，在本库中仅作 S13 对照轨道。

**需要：** 已做 soft-mask 的基因组，以及运行常规 S13 对照所需的 GPU。除非另有书面说明，输出结果仅作对照轨道。[按场景列出的数据需求](#data-needs)

![Tiberius precision-recall](docs/figures/catalog/12_tiberius_pr_vs_peers.jpg)

*Tiberius 与同类基因预测工具的精确率-召回率对比（图 3）。 Gabriel、Becker、Hoff 与 Stanke 2024，《Bioinformatics》图 3，doi:10.1093/bioinformatics/btae685，PMC11645249，CC BY。*

![Helixer 2026 exon precision-recall](docs/figures/catalog/06_helixer_2026_exon_pr.jpg)

*Helixer 2026 方法论文中的外显子级别精确率-召回率（图 1）。 Holst 等 2026，《Nature Methods》图 1，doi:10.1038/s41592-025-02939-1，PMC13076211，CC BY。*

- **Carbon-A + Carbon Annotation Database (CADB)** (tool / resource) — 含 1.2B 参数的编码器模型，直接从真核生物 DNA 预测蛋白编码基因并给出单基因置信度；配套 CADB 库已将其用于注释 GenBank 组装（共 566M 个位点）。 [doi:10.64898/2026.10.20.760448](https://doi.org/10.64898/2026.10.20.760448) · [link](https://huggingface.co/HuggingFaceBio/Carbon-A-1.2B)
- **Nucleotide Transformer v3 (NTv3)** (tool) — 长上下文跨界 DNA 基础模型；文中报告其在哺乳动物、植物与昆虫上的基因注释表现优于传统从头预测工具。 [doi:10.64898/2025.12.22.695963](https://doi.org/10.64898/2025.12.22.695963) · [link](https://github.com/instadeepai/nucleotide-transformer) [待确认]
- **GENATATORs** (tool) — 基于 DNA 语言模型的从头基因注释工具（2026 预印本）。 [doi:10.64898/2026.06.17.732686](https://doi.org/10.64898/2026.06.17.732686) [待确认]
- **AgroNT** (tool) — 在 48 个食用植物基因组上训练的 DNA 语言模型，下游可用于调控元件与剪接位点等预测任务。 [doi:10.1038/s42003-024-06465-2](https://doi.org/10.1038/s42003-024-06465-2) · [link](https://huggingface.co/InstaDeepAI/agro-nucleotide-transformer-1b)
- **PlantCaduceus** (tool) — 单碱基分辨率的跨物种植物 DNA 语言模型，支持剪接位点、TIS 与 TTS 等注释任务。 [doi:10.1073/pnas.2421738122](https://doi.org/10.1073/pnas.2421738122) · [link](https://github.com/kuleshov-group/PlantCaduceus)
- **Evo 2** (tool) — 跨生命域的基因组语言模型，提供外显子/内含子边界识别与变异效应预测的零样本（zero-shot）特征。 [doi:10.1101/2025.02.18.638918](https://doi.org/10.1101/2025.02.18.638918) · [link](https://github.com/ArcInstitute/evo2)

<a id="section-7"></a>
## 7. 注释转移（lift-over）

将近缘、已审定的注释转移到新组装上（A2b / S11 / S4）。

**需要：** 近缘且已审定的参考 GFF（同种或可信单倍型）及目标基因组；若要申报完整 S11 而非 S11-lite，还需准备补缺（gap-fill）证据。[按场景列出的数据需求](#data-needs)


- **GeMoMa** (tool) — 利用内含子位置保守性及可选 RNA-seq 数据的同源基因预测工具。 [doi:10.1007/978-1-4939-9173-0_9](https://doi.org/10.1007/978-1-4939-9173-0_9) · [link](https://www.jstacs.de/index.php/GeMoMa)
- **Liftoff** (tool) — 将参考基因组注释投射到同种或近缘物种目标组装上的工具。 [doi:10.1093/bioinformatics/btaa1016](https://doi.org/10.1093/bioinformatics/btaa1016) · [link](https://github.com/agshumate/Liftoff)
- **LiftOn** (tool) — 结合 DNA（Liftoff）与蛋白（miniprot）比对结果以改进注释转移质量。 [doi:10.1101/gr.279620.124](https://doi.org/10.1101/gr.279620.124) · [link](https://github.com/Kuanhao-Chao/LiftOn)
- **Comparative Annotation Toolkit (CAT)** (tool) — 通过 Cactus 全基因组比对投射基因注释，并与从头预测结果合并。 [doi:10.1101/gr.233460.117](https://doi.org/10.1101/gr.233460.117) · [link](https://github.com/ComparativeGenomicsToolkit/Comparative-Annotation-Toolkit)
- **GrAnnoT** (tool) — 通过泛基因组图（GFA）将 GFF3 注释转移至图内嵌合的各个基因组，输出图注释（GAF）与单基因组 GFF3。 [doi:10.24072/pcjournal.651](https://doi.org/10.24072/pcjournal.651) · [link](https://forge.ird.fr/diade/dynadiv/grannot)
- **TOGA (paper)** (tool) — 基于全基因组比对、将注释投射与直系同源推断相结合的工具。 [doi:10.1126/science.abn3107](https://doi.org/10.1126/science.abn3107) · [link](https://github.com/hillerlab/TOGA)
- **LiftoffTools** (tool) — 比较不同组装间的转移注释结果，分析基因序列变异、共线性与拷贝数变化。 [doi:10.12688/f1000research.124059.2](https://doi.org/10.12688/f1000research.124059.2) · [link](https://github.com/agshumate/LiftoffTools)
- **GENESPACE** (tool) — 基于共线性约束做跨基因组直系同源分析，并在共线性背景下定位缺失或新增基因。 [doi:10.7554/eLife.78526](https://doi.org/10.7554/eLife.78526) · [link](https://github.com/jtlovell/GENESPACE)

<a id="section-8"></a>
## 8. 合并器与注释流程

合并多套草案基因集，或封装整套注释流程的工具（A4）。

**需要：** 两套及以上的草案基因集和/或转录本组装结果，以及用于打分的证据（RNA、蛋白、剪接位点）。EVM 仅用于 S14 或真正的双轨合并，并非每个基因组都要跑。[按场景列出的数据需求](#data-needs)

![TSEBRA Arabidopsis](docs/figures/catalog/09_tsebra_sn_sp_arabidopsis.jpg)

*TSEBRA 在拟南芥上的敏感度与特异度表现（图 3）。 Gabriel 等 2021，《BMC Bioinformatics》图 3，doi:10.1186/s12859-021-04482-0，PMC8620231，CC BY。*

![Mikado Arabidopsis locus](docs/figures/catalog/10_mikado_arabidopsis_locus.jpg)

*Mikado 在拟南芥某一位点的转录本筛选过程（图 1）。 Venturini 等 2018，《GigaScience》图 1，doi:10.1093/gigascience/giy093，PMC6105091，CC BY。*

![EVidenceModeler rice locus](docs/figures/catalog/13_evm_rice_locus.jpg)

*EVidenceModeler 在水稻某一位点生成的共识基因模型（图 5）。 Haas 等 2008，《Genome Biology》图 5，doi:10.1186/gb-2008-9-1-r7，PMC2395244，CC BY。*

- **EVidenceModeler (EVM)** (tool) — 对多套基因预测与序列比对结果做加权整合，生成共识基因模型。 [doi:10.1186/gb-2008-9-1-r7](https://doi.org/10.1186/gb-2008-9-1-r7) · [link](https://github.com/EVidenceModeler/EVidenceModeler)
- **TSEBRA** (tool) — 利用外部证据对多套 BRAKER 预测结果做筛选合并的转录本选择器。 [doi:10.1186/s12859-021-04482-0](https://doi.org/10.1186/s12859-021-04482-0) · [link](https://github.com/Gaius-Augustus/TSEBRA)
- **Mikado** (tool) — 在每个基因位点上从多套转录本组装或预测结果中筛选最优转录本模型。 [doi:10.1093/gigascience/giy093](https://doi.org/10.1093/gigascience/giy093) · [link](https://github.com/EI-CoreBioinformatics/mikado)
- **MAKER2** (tool) — 整合序列比对证据与从头预测工具、并给出 AED 质量评分的注释流程。 [doi:10.1186/1471-2105-12-491](https://doi.org/10.1186/1471-2105-12-491)
- **funannotate** (tool) — 基于 EVM/PASA 构建的真核基因组注释流程（含 predict、update、annotate 模块）。 [doi:10.5281/zenodo.1134477](https://doi.org/10.5281/zenodo.1134477) · [link](https://github.com/nextgenusfs/funannotate)
- **EGAPx** (tool) — NCBI 真核基因组注释流程（EGAP）的公开版本。 [link](https://github.com/ncbi/egapx)
- **GETA** (tool) — 全基因组电子转录本注释流程，串联转录本、同源比对与 AUGUSTUS 预测。 [link](https://github.com/chenlianfu/geta)
- **REAT** (tool) — 基于 Mikado 整合转录组、同源证据与基因预测工作流的真核注释工具包。 [link](https://github.com/EI-CoreBioinformatics/reat)
- **EASEL** (tool) — Nextflow 注释流程：串联 StringTie2/PsiCLASS 转录本组装、TransDecoder、基于转录本与 OrthoDB 蛋白提示训练的 AUGUSTUS，并利用 RNA 二级结构等特征做随机森林过滤。 [link](https://gitlab.com/PlantGenomicsLab/easel)
- **Sylvan** (tool) — Snakemake 注释流程：整合 EVM/PASA、GETA、Helixer、Liftoff 与 miniprot 证据，再经半监督随机森林过滤与边界校正。 [link](https://github.com/plantgenomicslab/Sylvan) [待确认]
- **Ensembl automatic annotation pipeline (ensembl-anno)** (tool) — Ensembl 自动基因注释流程的公开代码库。 [link](https://github.com/Ensembl/ensembl-anno) [待确认]

<a id="section-9"></a>
## 9. 非编码 RNA 与假基因位点

蛋白编码草案之外的位点：tRNA、rRNA、miRNA、lncRNA 与假基因。

**需要：** 基因组序列；许多 ncRNA 工具还需协方差模型或参考 RNA 集。除非另有书面的合并规则，蛋白编码草案与 ncRNA 位点应作为独立产物分别保存。[按场景列出的数据需求](#data-needs)


- **ARAGORN** (tool) — 检测 tRNA 与 tmRNA 基因。 [doi:10.1093/nar/gkh152](https://doi.org/10.1093/nar/gkh152)
- **RNAmmer** (tool) — 基于 HMM 预测 rRNA 基因。 [doi:10.1093/nar/gkm160](https://doi.org/10.1093/nar/gkm160) · [link](https://services.healthtech.dtu.dk/services/RNAmmer-1.2/)
- **CPAT** (tool) — 无需序列比对的转录本编码潜能评估工具。 [doi:10.1093/nar/gkt006](https://doi.org/10.1093/nar/gkt006) · [link](https://github.com/liguowang/cpat)
- **LncFinder** (tool) — 结合多源序列特征与机器学习方法识别 lncRNA 的 R 包。 [doi:10.1093/bib/bby065](https://doi.org/10.1093/bib/bby065)
- **PseudoPipe** (tool) — 基于同源比对的假基因识别流程。 [doi:10.1093/bioinformatics/btl116](https://doi.org/10.1093/bioinformatics/btl116)
- **Infernal 1.1** (tool) — 基于协方差模型（covariance-model）的 RNA 同源搜索工具（Rfam 的底层引擎）。 [doi:10.1093/bioinformatics/btt509](https://doi.org/10.1093/bioinformatics/btt509) · [link](https://github.com/EddyRivasLab/infernal)
- **tRNAscan-SE 2.0** (tool) — 检测 tRNA 基因，给出反密码子分型（isotype）并标记假 tRNA。 [doi:10.1093/nar/gkab688](https://doi.org/10.1093/nar/gkab688) · [link](https://github.com/UCSC-LoweLab/tRNAscan-SE)
- **barrnap** (tool) — 快速预测 rRNA 位点的工具（内置真核模型）。 [link](https://github.com/tseemann/barrnap)
- **ShortStack 4** (tool) — 利用 sRNA-seq 数据注释小 RNA 位点并识别 MIRNA。 [doi:10.1261/rna.035279.112](https://doi.org/10.1261/rna.035279.112) · [link](https://github.com/MikeAxtell/ShortStack)
- **PlantLncBoost** (tool) — 基于序列特征与梯度提升算法识别植物 lncRNA。 [doi:10.1111/nph.70211](https://doi.org/10.1111/nph.70211) · [link](https://github.com/xuechantian/PlantLncBoost) [待确认]
- **FEELnc** (tool) — 从转录本组装结果中注释 lncRNA（含过滤、编码潜能计算与分类模块）。 [doi:10.1093/nar/gkw1306](https://doi.org/10.1093/nar/gkw1306) · [link](https://github.com/tderrien/FEELnc)
- **CPC2** (tool) — 快速计算转录本编码潜能的工具。 [doi:10.1093/nar/gkx428](https://doi.org/10.1093/nar/gkx428) · [link](https://cpc2.gao-lab.org/)
- **P-GRe** (tool) — 假基因预测工具：根据母本蛋白定位基因组位点、重建假 CDS、报告移码与提前终止密码子并输出 GFF。 [doi:10.1016/j.ygeno.2026.111216](https://doi.org/10.1016/j.ygeno.2026.111216)
- **Shiu lab PseudogenePipeline** (tool) — 经典的植物假基因识别流程，包含重复序列过滤与 GFF 输出。 [link](https://github.com/ShiuLab/PseudogenePipeline)
- **miRDeep-P2** (tool) — 采用更新版植物注释标准、从 sRNA-seq 数据中快速发现植物 miRNA 位点。 [doi:10.1093/bioinformatics/bty972](https://doi.org/10.1093/bioinformatics/bty972)

<a id="section-10"></a>
## 10. 基因模型质控

检查基因模型及其翻译所得蛋白序列（A3、A5、last-mile 01–02）。

**需要：** 由 GFF 翻译出的蛋白序列（`PROTEINS_FA`）与 BUSCO lineage；PSAURON 和 OMArk 使用同一套蛋白。RNA BAM 非必需，但有助于检查证据支持率。[按场景列出的数据需求](#data-needs)

![BUSCO v5 eukaryote workflows](docs/figures/catalog/01_busco_v5_eukaryote_workflows.jpg)

*BUSCO v5 的真核基因组评估流程（图 2）。 Manni 等 2021，《Molecular Biology and Evolution》图 2，doi:10.1093/molbev/msab199，PMC8476166，CC BY。*

![OMArk UniProt proteomes](docs/figures/catalog/02_omark_uniprot_proteomes.jpg)

*OMArk 在 UniProt 参考蛋白组上的一致性评估（图 4）。 Nevers 等 2025，《Nature Biotechnology》43(1):124-133，图 4，doi:10.1038/s41587-024-02147-w（线上发表于 2024-02-21），PMC11738984，CC BY。*

![PSAURON TAIR10 CDS](docs/figures/catalog/11_psauron_tair10_cds.jpg)

*PSAURON 在 TAIR10 CDS 上的打分分布（图 5）。 Sommer、Zimin 与 Salzberg 2025，《NAR Genomics and Bioinformatics》图 5，doi:10.1093/nargab/lqae189，PMC11704789，CC BY。*

- **gffread / gffcompare** (tool) — 从 GFF 提取 CDS 或蛋白序列（gffread），并在碱基、外显子与位点水平比对两套注释（gffcompare）。 [doi:10.12688/f1000research.23297.2](https://doi.org/10.12688/f1000research.23297.2) · [link](https://github.com/gpertea/gffread)
- **AGAT** (tool) — GFF/GTF 处理工具包：提供统计、结构修复、最长转录本提取、ID 管理与格式转换功能。 [doi:10.5281/zenodo.3552717](https://doi.org/10.5281/zenodo.3552717) · [link](https://github.com/NBISweden/AGAT)
- **BUSCO** (tool) — 基于类群特异单拷贝直系同源基因库评估基因集完整性（蛋白模式）。 [doi:10.1093/molbev/msab199](https://doi.org/10.1093/molbev/msab199)
- **ABAQS** (tool) — 综合完整性、基因模型合法性与蛋白结构域特征检查的注释质量评分工具（ABAQS）。 [link](https://github.com/mycocosm-lbl/abaqs) [待确认]
- **GeneValidator** (tool) — 将每个预测蛋白与数据库同源序列做比对（检查长度、覆盖度、重复与融合基因），标记存疑基因模型。 [doi:10.1093/bioinformatics/btw015](https://doi.org/10.1093/bioinformatics/btw015) · [link](https://github.com/wurmlab/genevalidator)

<a id="section-11"></a>
## 11. 人工校对与浏览器

用于 last-mile 校对的证据包、基因组浏览器与编辑器（LM03–LM04）。

**需要：** 在打开 GSAman 或浏览器前，备好草案 GFF、基因组及证据包（BAM、蛋白比对、RNA 覆盖度）。[按场景列出的数据需求](#data-needs)


- **IGV** (tool) — 用于查看序列比对与基因注释的桌面端基因组浏览器。 [doi:10.1038/nbt.1754](https://doi.org/10.1038/nbt.1754) · [link](https://github.com/igvteam/igv)
- **igv.js / igv-reports** (tool) — 可嵌入网页的 IGV 组件；igv-reports 可将指定位点及其证据轨道打包为独立的 HTML 页面。 [doi:10.1093/bioinformatics/btac830](https://doi.org/10.1093/bioinformatics/btac830) · [link](https://github.com/igvteam/igv-reports)
- **Apollo (2019 paper)** (tool) — 支持多人协作的网页端基因模型校对编辑器（Apollo 2）。 [doi:10.1371/journal.pcbi.1006790](https://doi.org/10.1371/journal.pcbi.1006790) · [link](https://github.com/GMOD/Apollo)
- **Artemis / ACT** (tool) — 基因组浏览器、注释编辑器与序列比较工具。 [doi:10.1093/bioinformatics/btr703](https://doi.org/10.1093/bioinformatics/btr703) · [link](https://github.com/sanger-pathogens/Artemis)
- **Apollo 3** (tool) — 基于 JBrowse 2 的多人协作基因模型校对编辑器（支持本地或服务端部署）。 [doi:10.64898/2026.06.08.730970](https://doi.org/10.64898/2026.06.08.730970) · [link](https://github.com/GMOD/Apollo3)
- **JBrowse 2** (tool) — 支持共线性与结构变异视图的基因组浏览器，可挂载各类证据轨道供人工校对使用。 [doi:10.1186/s13059-023-02914-z](https://doi.org/10.1186/s13059-023-02914-z) · [link](https://github.com/GMOD/jbrowse-components)

<a id="section-12"></a>
## 12. GFF3 清理与发布

GFF3 清理、格式校验与提交（last-mile 06、A6）。

**需要：** 审定后的 GFF 与基因组，外加 `docs/PLAYBOOK.md` 中列出的 METHODS 与核对表字段。[按场景列出的数据需求](#data-needs)


- **SeqKit 2** (tool) — FASTA/Q 序列处理工具包（统计、检索、翻译、去冗余等）。 [doi:10.1002/imt2.191](https://doi.org/10.1002/imt2.191) · [link](https://github.com/shenwei356/seqkit)
- **Genome Annotation Generator (GAG)** (tool) — 由 GFF3 生成并校正 NCBI 提交所需的 `.tbl` 注释表。 [doi:10.1093/gigascience/giy018](https://doi.org/10.1093/gigascience/giy018) · [link](https://github.com/genomeannotation/GAG)
- **GenomeTools (gt gff3validator)** (tool) — GFF3 格式校验、排序与规范化整理工具。 [doi:10.1109/TCBB.2013.68](https://doi.org/10.1109/TCBB.2013.68) · [link](https://github.com/genometools/genometools)
- **EMBLmyGFF3** (tool) — 将 GFF3 与 FASTA 转换为用于 ENA 提交的 EMBL 平面文件格式。 [doi:10.1186/s13104-018-3686-x](https://doi.org/10.1186/s13104-018-3686-x) · [link](https://github.com/NBISweden/EMBLmyGFF3)
- **table2asn** (tool) — NCBI 官方工具，将 GFF3/FASTA 转换为提交用的 ASN.1 格式并生成校验报告。 [link](https://www.ncbi.nlm.nih.gov/genbank/table2asn/)
- **GFF3toolkit** (tool) — i5k Workspace@NAL 开发的 GFF3 质控、修复与合并工具集。 [link](https://github.com/NAL-i5K/GFF3toolkit)
- **noodles** (tool) — Rust 编写的生物信息学格式 I/O 库，包含 GFF3/GTF 读写模块。 [link](https://github.com/zaeleus/noodles)
- **gxfkit** (tool) — Rust 编写的 GFF3/GTF 转换工具，力求输出格式兼容 AGAT 且运行速度大幅提升。 [link](https://github.com/benngaihk/gxfkit)

<a id="section-13"></a>
## 13. 参考数据库

用作证据或近缘 GFF 的参考基因组与注释库。

**需要：** 无需额外测序——这里收录的是用作证据或近缘 GFF 的参考基因组与注释。请核对所用版本是否与 METHODS 中记录的一致。[按场景列出的数据需求](#data-needs)


- **RNAcentral** (resource) — 综合性的非编码 RNA 序列数据库。 [doi:10.1093/nar/gkaa921](https://doi.org/10.1093/nar/gkaa921) · [link](https://rnacentral.org/)
- **Phytozome** (resource) — JGI 维护的植物基因组与注释门户数据库。 [doi:10.1093/nar/gkr944](https://doi.org/10.1093/nar/gkr944) · [link](https://phytozome-next.jgi.doe.gov/)
- **Ensembl Plants (Ensembl Genomes 2022)** (resource) — 收录植物基因组、基因模型与比较基因组学数据的综合数据库。 [doi:10.1093/nar/gkab1007](https://doi.org/10.1093/nar/gkab1007) · [link](https://plants.ensembl.org/)
- **Araport11** (resource) — 拟南芥 Col-0 基因组的重注释参考版本。 [doi:10.1111/tpj.13415](https://doi.org/10.1111/tpj.13415) · [link](https://www.arabidopsis.org/)
- **Rfam 15** (resource) — RNA 家族协方差模型数据库；可配合 Infernal cmscan 扫描 rRNA、snoRNA 与核糖体开关（riboswitch）等位点。 [doi:10.1093/nar/gkae1023](https://doi.org/10.1093/nar/gkae1023) · [link](https://rfam.org)

<a id="section-14"></a>
## 14. 标准与综述

相关标准、文件格式与综述文献，并非数据配方。

**需要：** 并非数据配方。本节收录的是标准、格式与综述。[按场景列出的数据需求](#data-needs)


- **Sequence Ontology** (idea) — 定义 GFF3 第三列特征类型（feature type）的标准本体。 [doi:10.1186/gb-2005-6-5-r44](https://doi.org/10.1186/gb-2005-6-5-r44) · [link](https://github.com/The-Sequence-Ontology/SO-Ontologies)
- **GFF3 specification** (idea) — GFF3 文件格式的正式规范文档。 [link](https://github.com/The-Sequence-Ontology/Specifications)
- **The grapevine gene nomenclature system** (idea) — 葡萄基因与基因组位点的命名规则建议。 [doi:10.1186/1471-2164-15-1077](https://doi.org/10.1186/1471-2164-15-1077)
- **A beginner's guide to eukaryotic genome annotation** (idea) — 真核基因组注释入门综述，涵盖证据类型、常用流程与质量评估指标（如 AED）。 [doi:10.1038/nrg3174](https://doi.org/10.1038/nrg3174)
- **Ten steps to get started in genome assembly and annotation** (idea) — 从基因组组装到注释的十步实操指南。 [doi:10.12688/f1000research.13598.1](https://doi.org/10.12688/f1000research.13598.1)
- **LRGASP benchmark** (idea) — 长读长 RNA-seq 转录本识别与定量方法的社区基准评测，展示了测序深度、读长与准确度之间的权衡关系。 [doi:10.1038/s41592-024-02298-3](https://doi.org/10.1038/s41592-024-02298-3) · [link](https://github.com/LRGASP/lrgasp-submissions)
- **Tips for improving genome annotation quality** (idea) — 提升基因组注释质量的实操核对清单，涵盖证据选择、重复序列屏蔽强度、人工校对与评估指标。 [doi:10.48130/gcomm-0025-0006](https://doi.org/10.48130/gcomm-0025-0006)
- **EBP annotation standards report** (idea) — 地球生物基因组计划（EBP）关于注释最低标准与元数据的规范报告。 [link](https://www.earthbiogenome.org/report-on-annotation-standards)

<a id="section-15"></a>
## 15. 尚未落到单一工具的想法

2026-11 调研记录的思路。在完成实测前，不改变默认路径。

**需要：** 视具体思路而定；在完成实测前，不改变默认路径。[按场景列出的数据需求](#data-needs)


- **Soft-mask hand-off rule (idea)** (idea) — 结构注释直接消费外部产出的审定版 TE 库；需在 METHODS 中记录库名称、版本与 sha256 校验值，并确保库中已剔除 NLR 等基因家族序列（见现有的 ProtExcluder 说明）。 [link](https://github.com/Xuzhen-Li/gene-structure-annotation/blob/main/docs/BOUNDARY.md)
- **Chimeric mis-annotation survey** (idea) — 指出融合（嵌合）基因模型在非模式真核生物注释中依然普遍存在，并给出相应的检测启发式规则。 [doi:10.1186/s12864-025-11765-w](https://doi.org/10.1186/s12864-025-11765-w)
- **Annotation affects orthology (idea)** (idea) — 基因结构注释策略的选择会影响下游直系同源推断；在得出跨物种结论前应先比对注释方案。 [doi:10.1093/bioinformatics/btaf365](https://doi.org/10.1093/bioinformatics/btaf365)
- **GeneWhisperer** (idea) — 配备专用任务工具、辅助人工基因注释的大语言模型助手（预印本）。 [doi:10.1101/2025.03.30.646211](https://doi.org/10.1101/2025.03.30.646211)
- **Human-AI collaborative annotation framework** (idea) — 在 AI 工具与人工校对员之间划分基因组注释任务的概念框架。 [doi:10.1093/bib/bbaf377](https://doi.org/10.1093/bib/bbaf377)
- **Family-window review using function results (idea)** (idea) — 场景 S7 可读取 gene-function-annotation 产出的 NLR/TF 基因家族窗口列表，并回头复核这些窗口内的基因模型；家族分类器本身仍保留在功能注释目录中。 [link](https://github.com/Xuzhen-Li/gene-function-annotation)

<a id="data-needs"></a>
## 基因组之外还需要的数据

主要输入是基因组 FASTA（`GENOME_FA`）。下文说明不同场景通常还需补充哪些数据。在改动经过实测验证前，默认 S1 路径保持不变。

| 场景 | 最低要求 | 建议再加 | 本库常用工具 | 常见陷阱 |
|---|---|---|---|---|
| 组装已完成（Asm0/Asm1 作检查清单） | `GENOME_FA`，`ASSEMBLY_OK=yes` | 组装所用的测序读长（用于 k-mer / QV 检查）；匹配的 BUSCO lineage | BUSCO（基因组模式）、compleasm（可选） | 选错类群的 lineage，或混用 odb10 与 odb12 名称却未注明（`docs/LINEAGES.md`） |
| Soft-mask（A0） | 可信 TE 库 | 在 METHODS 中注明库的版本与来源 | RepeatMasker / EDTA `make_masked.pl`（仅做屏蔽） | 在本库中构建新 TE 库 — 那是 vitis-te 的工作 |
| 默认 S1（有 RNA 和蛋白，无近缘 GFF） | RNA-seq（或 `RNA_BAM`）与 `PROTEIN_DB` | 同一基因型、多组织的 RNA | HISAT2/STAR、StringTie、BRAKER3/4、GeMoMa 或 miniprot | 将其他品种的 RNA 当作目标基因型使用 |
| 仅有蛋白（S2） | `PROTEIN_DB` | 亲缘关系更近的蛋白组，而非泛用数据集 | GALBA / GALBA2、GeMoMa、miniprot | 仅凭蛋白证据就声称有完整的 UTR |
| 深度 Iso-Seq（S3） | 长读长 RNA + 比对工具（minimap2） | 补充短读长 RNA；采用 SQANTI 类过滤 | IsoQuant、SQANTI、EviAnn，孤儿基因再用 BRAKER | 跳过 SQANTI（或同等级）过滤步骤 |
| 近缘已整理 GFF（S11） | 可信的近缘 GFF | 用于补缺的证据（RNA / 蛋白） | Liftoff、LiftOn、CAT；随后进入主干质控 | 将仅做坐标转移的 S11-lite 当作 L1 发布 |
| GPU 从头预测对照（S13） | 已做 soft-mask 的基因组 + GPU | 同时保留一套基于证据的草案作对照 | Helixer、Tiberius、ANNEVO | 在有 RNA 数据的情况下悄悄替代 S1 |
| 经典 EVM 流程（S14） | 用于训练和赋权的 RNA 和/或蛋白 | 记录明确的 EVM 权重 | PASA、AUGUSTUS/GeneMark、EVM | 把 EVM 当成所有基因组的必跑步骤 |
| 论文 / T2T 标准（S5 叠加） | S1 或 S14 草案，外加深层质控 | OMArk、更细致的 GSAman 校对、证据包 | OMArk、PSAURON、BUSCO 蛋白模式、GSAman | 将临时的合并结果直接当作 L1 |
| 多单倍型（S4 / LM05） | 第二套单倍型组装 | 注释转移后运行 SynGAP | Liftoff、SynGAP | 因 BUSCO Duplicated 偏高就丢掉单倍型（见 S9） |
| 移交功能注释（A6） | 发布标签与 `proteins.faa`（每个基因一条代表序列） | 若下游功能库需要坐标，附上审定后的 GFF | AGAT / gffread | 未打 `RELEASE_TAG` 就交出尚未冻结的草案 |

### 跨切陷阱

- 构建 TE 库属于独立任务（归 vitis-te）。本库仅使用可信库做 soft-mask。
- GO / KEGG / 结构域 / 可读基因名 / NLR 与 TF 分类器（含 HRP）归属 gene-function-annotation。蛋白工具中提到的 “structure” 多指三维结构，而非基因模型。
- `grade=` 与 `status=` 是两个独立字段，切勿写成 `status=L1`。临时结果不等于 L1（`docs/EVALUATION.md`）。
- 「近缘参考」是指同种 / 同一品种或近乎一致的单倍型，且 GFF 可信，而不是「同科里刚好有个 GFF」。
- BUSCO lineage 必须与物种所属类群匹配，并注明使用的是 odb10 还是 odb12（`docs/LINEAGES.md`）。Compleasm 适合用作对照，不能自动替代 BUSCO。
- BUSCO Duplicated 偏高可能源于真实的单倍型（S9），切勿单纯为了压低 D 值而丢掉单倍型。
- 若运行 TSEBRA 后基因数量大幅缩水，需先执行 A5d 单拷贝/多拷贝检查（Copetti），再决定是否采纳合并结果。

目录中仍标有 `[待确认]` 的条目（如 CRAQ）保留原标记，直至核对原始出处后再作更新。

更详细的说明（含英文表格）见 [`docs/SCENARIOS.md#data-needs-zh`](docs/SCENARIOS.md#data-needs-zh)。


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

