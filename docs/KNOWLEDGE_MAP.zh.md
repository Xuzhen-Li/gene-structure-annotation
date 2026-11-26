# 知识地图

[English](KNOWLEDGE_MAP.md)

本页按主题和页面类型列出本仓库的全部内容。本仓库是关于植物基因组的基因结构注释的知识库：书讲清每一步，目录比较软件和数据库，参考流程给出一种跑法，示例代码展示每一步在小数据上的样子。结构与 [TE-Lib](https://github.com/Xuzhen-Li/TE-Lib) 一致。

TE-Lib 原名 vitis-te。较早的页面仍用旧名，GitHub 会把旧链接转到新地址。

- [知识单元与流程索引](#knowledge-units)
- [主题](#topics)
- [学习](#learn)
- [参考流程](#reference-workflow)
- [软件清单与来源](#software-lists-and-sources)
- [示例代码与测试数据](#example-code)
- [图](#figures)
- [旧页面与勘误](#older-pages)
- [其他文件](#other-files)

<a id="knowledge-units"></a>
## 知识单元与流程索引

- [基因模型及其证据](kb/gene-model-concepts.zh.md)
- [用可信 TE 库做 soft-mask](kb/trusted-softmask.zh.md)
- [基因集够不够好？（判据）](kb/model-qc-criteria.zh.md)
- 编号对照: [`kb/NUMBERING.zh.md`](kb/NUMBERING.zh.md)
- 流程索引: [`workflow/README.zh.md`](workflow/README.zh.md)
- 完整方法目录: [`catalog/METHODS_CATALOG.zh.md`](../catalog/METHODS_CATALOG.zh.md); [`catalog/README.by-type.zh.md`](../catalog/README.by-type.zh.md); [`catalog/COUNTS.md`](../catalog/COUNTS.md)
- docs/tools 与 docs/notes 的重叠: [`TOOLS_NOTES_OVERLAP.md`](TOOLS_NOTES_OVERLAP.md)

<a id="topics"></a>
## 主题

每个主题列出讲解它的书章、比较工具的目录小节，以及（如果有）单个工具笔记、带命令的工具卡片、早期步骤卡片、其他页面和示例代码。工具卡片和笔记多为英文。

### 概念与原理

- 书：[第 1 章 概念与原理](../book/chapters/01-concepts.zh.md)

### 1. 组装与组装质控

- 书：[第 2 章 组装与组装质控](../book/chapters/02-assembly-and-assembly-qc.zh.md)
- 目录：[方法目录第 1 节](../catalog/METHODS_CATALOG.zh.md#section-1)
- 工具卡片：[hifiasm — HiFi contig assembly](../docs/tools/hifiasm.md)
- 早期步骤卡片：[Asm0 — assembly](../catalog/Asm0_assembly/README.md); [Asm1 — assembly QC](../catalog/Asm1_assembly_qc/README.md)
- 示例代码与数据：[Asm0 — Genome assembly (before annotation)](../pipeline/Asm0_assembly.md); [Asm1 — Assembly QC gate](../pipeline/Asm1_assembly_qc.md)

### 2. 用可信库做 soft-mask

- 书：[第 3 章 用可信库做 soft-mask](../book/chapters/03-soft-mask-with-a-trusted-library.zh.md)
- 目录：[方法目录第 2 节](../catalog/METHODS_CATALOG.zh.md#section-2)
- 单个工具笔记：[Earl Grey](../docs/notes/earlgrey.md)
- 工具卡片：[EDTA — de novo TE library (step 1 of the lab scheme)](../docs/tools/edta.md); [ProtExcluder (pattern) — clean host genes out of TE libraries](../docs/tools/protexcluder.md); [RepeatMasker — soft-mask TE](../docs/tools/repeatmasker.md)
- 早期步骤卡片：[A0 / A0b — soft-mask with a trusted library](../catalog/A0_softmask/README.md)
- 其他页面：[TE library scheme → soft-mask (A0)](../docs/TE_LIBRARY.md); [Trusted TE path — copy-paste checklist (A0)](../docs/TRUSTED_TE_PATH.md)
- 示例代码与数据：[A0 — Soft-mask (detailed)](../pipeline/A0_softmask.md); [A0b — Optional host-gene purge (ProtExcluder-style)](../pipeline/A0b_protexcluder.md)

### 3. RNA 与 Iso-Seq 证据

- 书：[第 4 章 RNA 与 Iso-Seq 证据](../book/chapters/04-rna-and-iso-seq-evidence.zh.md)
- 目录：[方法目录第 3 节](../catalog/METHODS_CATALOG.zh.md#section-3)
- 单个工具笔记：[IsoAnnot / FIT (with SQANTI3)](../docs/notes/isoannot_fit.md); [IsoQuant](../docs/notes/isoquant.md); [Long-read isoform peers (beyond IsoQuant / SQANTI3)](../docs/notes/lr_isoform_peers.md); [Mikado + Portcullis](../docs/notes/mikado_portcullis.md); [SQANTI3](../docs/notes/sqanti3.md)
- 工具卡片：[HISAT2 / STAR — short-read RNA alignment](../docs/tools/hisat2_star.md); [minimap2 — Iso-seq / long RNA](../docs/tools/minimap2.md); [PASA — transcript assemblies for training + polish](../docs/tools/pasa.md); [StringTie — transcript assembly (sanity track)](../docs/tools/stringtie.md)
- 早期步骤卡片：[A1 / A1b — engine choice and RNA / Iso-Seq evidence](../catalog/A1_engine_and_rna/README.md)
- 示例代码与数据：[A1b — RNA align (detailed)](../pipeline/A1b_rna_align.md)

### 4. 蛋白证据

- 书：[第 5 章 蛋白证据](../book/chapters/05-protein-evidence.zh.md)
- 目录：[方法目录第 4 节](../catalog/METHODS_CATALOG.zh.md#section-4)
- 单个工具笔记：[MetaEuk](../docs/notes/metaeuk.md); [miniprot · Spaln (protein-to-genome)](../docs/notes/miniprot_spaln.md); [ProtHint · miniprothint](../docs/notes/prothint_miniprothint.md)
- 工具卡片：[miniprot — fast protein-to-genome alignment](../docs/tools/miniprot.md)
- 示例代码与数据：[A2 — PROTEIN_DB for BRAKER / GALBA](../pipeline/A2_protein_db.md)

### 5. 从头基因预测

- 书：[第 6 章 从头基因预测](../book/chapters/06-ab-initio-gene-finders.zh.md)
- 目录：[方法目录第 5 节](../catalog/METHODS_CATALOG.zh.md#section-5)
- 单个工具笔记：[ANNEVO (Kai Ye / 叶凯 lab, XJTU)](../docs/notes/annevo.md); [BRAKER4 (Gaius-Augustus) — Snakemake rewrite of BRAKER](../docs/notes/braker4.md); [Classic ab initio engines (high citation building blocks)](../docs/notes/classic_abinitio.md); [GALBA2](../docs/notes/galba2.md); [Helixer](../docs/notes/helixer.md); [Tiberius](../docs/notes/tiberius.md)
- 工具卡片：[BRAKER3 — primary gene prediction (RNA + proteins)](../docs/tools/braker3.md); [BRAKER4 — preferred modern BRAKER runner](../docs/tools/braker4.md); [GALBA — protein-only gene prediction](../docs/tools/galba.md); [Helixer — deep-learning ab initio genes](../docs/tools/helixer.md)
- 早期步骤卡片：[A2](../catalog/A2_drafts/README.md)
- 其他页面：[Helixer ↔ BRAKER — classroom compare (not default production)](../docs/COMPARE_HELIXER_BRAKER.md)
- 示例代码与数据：[A1 — Choose the draft engine](../pipeline/A1_choose_engine.md); [`A2_run_draft.sh`](../pipeline/A2_run_draft.sh); [A2b — Second prediction set](../pipeline/A2b_second_predictor.md)

### 6. DNA 语言模型预测

- 书：[第 7 章 DNA 语言模型预测](../book/chapters/07-dna-language-model-predictors.zh.md)
- 目录：[方法目录第 6 节](../catalog/METHODS_CATALOG.zh.md#section-6)
- 单个工具笔记：[OrionGeno (BGI Research)](../docs/notes/oriongeno.md)

### 7. 注释转移（lift-over）

- 书：[第 8 章 注释转移（lift-over）](../book/chapters/08-lift-over-and-annotation-transfer.zh.md)
- 目录：[方法目录第 7 节](../catalog/METHODS_CATALOG.zh.md#section-7)
- 单个工具笔记：[Comparative Annotation Toolkit (CAT)](../docs/notes/cat.md); [CESAR2.0](../docs/notes/cesar2.md); [LiftOn](../docs/notes/lifton.md); [TOGA2](../docs/notes/toga2.md)
- 工具卡片：[GeMoMa — homology projection from an annotated genome](../docs/tools/gemoma.md); [Liftoff — map annotation GFF to a new assembly](../docs/tools/liftoff.md); [LiftOn — T2T-grade lift (Liftoff + miniprot)](../docs/tools/lifton.md); [SynGAP — haplotype / synteny annotation polish](../docs/tools/syngap.md)
- 早期步骤卡片：[Last mile 05 — SynGAP polish / multi-haplotype harmonisation](../catalog/LM05_syngap_polish/README.md)
- 示例代码与数据：[A2c — Liftoff (detailed)](../pipeline/A2c_liftoff.md); [A2e — S11 gap-fill (after Liftoff)](../pipeline/A2e_s11_gapfill.md); [Optional: SynGAP polish](../pipeline/05_syngap_polish.md)

### 8. 合并器与注释流程

- 书：[第 9 章 合并器与注释流程](../book/chapters/09-combiners-and-annotation-pipelines.zh.md)
- 目录：[方法目录第 8 节](../catalog/METHODS_CATALOG.zh.md#section-8)
- 单个工具笔记：[combinr · InGenAnnot (combiners)](../docs/notes/combinr_ingenannot.md); [NCBI EGAPx / Gnomon (institutional)](../docs/notes/egapx_gnomon.md); [EviAnn (Evidence Annotation)](../docs/notes/eviann.md); [FINDER](../docs/notes/finder.md); [funannotate2](../docs/notes/funannotate2.md); [GETA](../docs/notes/geta.md); [MAKER / MAKER2 (mainstream, high citation)](../docs/notes/maker2.md); [MoGAAAP](../docs/notes/mogaaap.md)
- 工具卡片：[EGAPx — NCBI’s annotation pipeline (optional parallel)](../docs/tools/egapx.md); [EviAnn — evidence-driven annotation (Iso-seq friendly)](../docs/tools/eviann.md); [EVidenceModeler (EVM) — merge competing gene predictions](../docs/tools/evm.md); [MAKER-P — classical plant annotation engine](../docs/tools/maker_p.md); [Mikado — pick best transcripts at overlapping loci](../docs/tools/mikado.md); [TSEBRA — combine two BRAKER-family GTFs](../docs/tools/tsebra.md)
- 早期步骤卡片：[A4 — aggregation (A4a TSEBRA, A4b Mikado, A4c–A4d EVM, A4e PASA update)](../catalog/A4_aggregation/README.md)
- 其他页面：[EGAPx / S8 — optional 对照 & GenBank door (not default)](../docs/EGAPX_COMPARE.md)
- 示例代码与数据：[A2d — Optional: NCBI EGAPx (eudicot / rosids)](../pipeline/A2d_egapx_optional.md); [A4 multi-source aggregation (EVM main path, TSEBRA / Mikado / PASA optional)](../pipeline/A4_aggregation.md); [`A4_merge_sets.sh`](../pipeline/A4_merge_sets.sh); [`A4a_tsebra_optional.sh`](../pipeline/A4a_tsebra_optional.sh); [`A4b_mikado_optional.sh`](../pipeline/A4b_mikado_optional.sh); [`A4c_evm_inputs.py`](../pipeline/A4c_evm_inputs.py); [`A4d_evm_run.sh`](../pipeline/A4d_evm_run.sh); [`A4e_pasa_update.sh`](../pipeline/A4e_pasa_update.sh); [Aggregation toy data (simulated) (`examples/aggregation_toy/`)](../examples/aggregation_toy/README.md)

### 9. 非编码 RNA 与假基因位点

- 书：[第 10 章 非编码 RNA 与假基因位点](../book/chapters/10-non-coding-rna-and-pseudogene-loci.zh.md)
- 目录：[方法目录第 9 节](../catalog/METHODS_CATALOG.zh.md#section-9)
- 单个工具笔记：[ncRNA + TE classification side-lanes](../docs/notes/ncrna_tesorter.md)

### 10. 基因模型质控

- 书：[第 11 章 基因模型质控](../book/chapters/11-gene-model-qc.zh.md)
- 目录：[方法目录第 10 节](../catalog/METHODS_CATALOG.zh.md#section-10)
- 单个工具笔记：[OMArk · compleasm (annotation/assembly QC)](../docs/notes/omark_compleasm.md); [PSAURON · GAQET2 · AnnoAudit (QC packs)](../docs/notes/psauron_gaqet_annoaudit.md)
- 工具卡片：[BUSCO — completeness](../docs/tools/busco.md); [OMArk + Compleasm — extra proteome / assembly QC](../docs/tools/omark_compleasm.md); [PSAURON — protein coding-likelihood scores](../docs/tools/psauron.md)
- 早期步骤卡片：[A5 — structure QC (A5b–A5e, structure_qa qa01–qa10)](../catalog/A5_structure_qc/README.md); [Last mile 01 — BUSCO / PSAURON QC](../catalog/LM01_qc_busco_psauron/README.md)
- 其他页面：[Recommended BUSCO / Compleasm lineages (plants)](../docs/LINEAGES.md)
- 示例代码与数据：[`A5_agat_stats.sh`](../pipeline/A5_agat_stats.sh); [`A5b_omark_compleasm.sh`](../pipeline/A5b_omark_compleasm.sh); [A5c — Expression + domain filter (GetaFilter idea)](../pipeline/A5c_expression_pfam_filter.md); [`A5d_stage_counts.sh`](../pipeline/A5d_stage_counts.sh); [`A5e_filter_proteins.sh`](../pipeline/A5e_filter_proteins.sh); [`01_qc_busco_psauron.sh`](../pipeline/01_qc_busco_psauron.sh); [`protein_stop_check.py`](../pipeline/protein_stop_check.py); [Structure QA step / 结构注释质量评估 (`pipeline/structure_qa/`)](../pipeline/structure_qa/README.md); [Simulated example for the structure QA step / 结构质量评估模拟示例 (`examples/structure_qa_sim/`)](../examples/structure_qa_sim/README.md)

### 11. 人工校对与浏览器

- 书：[第 12 章 人工校对与浏览器](../book/chapters/12-curation-and-browsers.zh.md)
- 目录：[方法目录第 11 节](../catalog/METHODS_CATALOG.zh.md#section-11)
- 工具卡片：[GSAman — manual gene-structure curation](../docs/tools/gsaman.md)
- 早期步骤卡片：[Last mile 02 — priority loci (02, 02b)](../catalog/LM02_priority_loci/README.md); [Last mile 03 — evidence pack](../catalog/LM03_evidence_pack/README.md); [Last mile 04 — GSAman / manual curation](../catalog/LM04_gsaman_curation/README.md)
- 其他页面：[Four structural error classes (from GSAman)](../docs/ERROR_CLASSES.md)
- 示例代码与数据：[`02_priority_loci.py`](../pipeline/02_priority_loci.py); [`02b_merge_priority_r2.py`](../pipeline/02b_merge_priority_r2.py); [03 — Evidence pack for GSAman (detailed)](../pipeline/03_evidence_checklist.md); [04 — GSAman curation (detailed)](../pipeline/04_gsaman_curation.md)

### 12. GFF3 清理与发布

- 书：[第 13 章 GFF3 清理与发布](../book/chapters/13-gff3-cleanup-and-release.zh.md)
- 目录：[方法目录第 12 节](../catalog/METHODS_CATALOG.zh.md#section-12)
- 工具卡片：[AGAT + gffread — GFF hygiene and proteins](../docs/tools/agat_gffread.md)
- 早期步骤卡片：[A3 — proteins from GFF](../catalog/A3_proteins/README.md); [A6 / A6b — hand-off to function](../catalog/A6_handoff_to_function/README.md); [Last mile 06 — release](../catalog/LM06_release/README.md)
- 示例代码与数据：[`A3_proteins_from_gff.sh`](../pipeline/A3_proteins_from_gff.sh); [A6 — Hand-off to function (FA is NEVER a product of this repo)](../pipeline/A6_handoff_to_function.md); [`A6b_rename_gff.py`](../pipeline/A6b_rename_gff.py); [06 — Release qualified GFF (detailed)](../pipeline/06_release_gff.md); [`longest_isoform.py`](../pipeline/longest_isoform.py); [Golden pack (EXAMPLE checklist) — structure L0 / L1 (`examples/golden_pack/`)](../examples/golden_pack/README.md)

### 13. 参考数据库

- 书：[第 14 章 参考数据库](../book/chapters/14-reference-databases.zh.md)
- 目录：[方法目录第 13 节](../catalog/METHODS_CATALOG.zh.md#section-13)
- 早期步骤卡片：[Database index](../catalog/_databases.md)

### 14. 标准与综述

- 书：[第 15 章 标准与综述](../book/chapters/15-standards-and-overview-papers.zh.md)
- 目录：[方法目录第 14 节](../catalog/METHODS_CATALOG.zh.md#section-14)
- 单个工具笔记：[Dario Copetti — practical plant annotation scheme](../docs/notes/copetti.md)
- 早期步骤卡片：[跨阶段：整套流程、综述与标准](../catalog/X_cross_stage/README.md)

### 15. 尚未落到单一工具的想法

- 书：[第 16 章 尚未落到单一工具的想法](../book/chapters/16-ideas-not-yet-tied-to-one-tool.zh.md)
- 目录：[方法目录第 15 节](../catalog/METHODS_CATALOG.zh.md#section-15)

### 可视化工具

- 书：[第 17 章 可视化工具](../book/chapters/17-visualization-tools.zh.md)
- 目录：[方法目录中的可视化工具](../catalog/METHODS_CATALOG.zh.md#visualization)

### 怎么选工具

- 书：[第 18 章 怎么选工具](../book/chapters/18-choosing-tools.zh.md)
- 早期步骤卡片：[Branch view (S1–S14)](../catalog/_branches.md)

### 常见问题与质控

- 书：[第 19 章 常见问题与质控](../book/chapters/19-pitfalls-and-qc.zh.md)

### 实例：葡萄基因组走 S1 路线

- 书：[第 20 章 实例：葡萄基因组走 S1 路线](../book/chapters/20-worked-example.zh.md)
- 其他页面：[Case: *Vitis* T2T assembly → publication-grade structure (S1 engine + S5 bar)](../docs/cases/vitis-t2t-s1-s5.md)
- 示例代码与数据：[植物模拟三例 (`examples/plant_sim/`)](../examples/plant_sim/README.md)

### 术语表

- 书：[附录 A 术语表](../book/chapters/appendix-a-glossary.zh.md)

<a id="learn"></a>
## 学习

- 书：[《植物基因结构注释学习笔记：以葡萄为例》](../book/README.zh.md); [《植物基因结构注释学习笔记：以葡萄为例》](../book/BOOK_full.zh.md); [Book file index · 全书文件索引](../book/INDEX.md); [前言](../book/chapters/00-preface.zh.md)
- 双语说明：[Bilingual teaching track](../docs/BILINGUAL.md)
- 中文教学页（34）：
  - [为什么要做结构注释？](zh/00_为什么要做结构注释.md)
  - [什么是基因结构注释？](zh/01_什么是结构注释.md)
  - [TE 与基因结构注释的关系](zh/02_TE与基因的关系.md)
  - [怎么开始跑（结构注释）](zh/03_怎么开始跑.md)
  - [分支怎么选（结构）](zh/04_分支怎么选.md)
  - [Soft-mask 与 A0（地板怎么铺）](zh/05_softmask与A0.md)
  - [质控课：BUSCO 不是唯一分数](zh/06_质控课.md)
  - [S1 精讲：BRAKER 路线（默认草稿）](zh/07_S1精讲_BRAKER路线.md)
  - [S11 精讲：Liftover 优先](zh/08_S11精讲_liftover优先.md)
  - [S2 / S3 / S13 / S14 速览（其他草稿支）](zh/09_S2_S3_S13_S14速览.md)
  - [合并、优先表、GSAman 与 S12 停手](zh/10_合并与GSAman.md)
  - [验收：L0 / L1 / L2](zh/11_验收L0L1L2.md)
  - [flow 工具怎么用（结构）](zh/12_flow工具怎么用.md)
  - [常见翻车（结构注释）](zh/13_常见翻车.md)
  - [为什么这样选证据？](zh/14_为什么这样选证据.md)
  - [为什么质控是这些指标？](zh/15_为什么质控是这些指标.md)
  - [为什么 TE 库必须是 trusted？](zh/16_为什么TE要trusted.md)
  - [外部软件流程教程与会议](zh/17_外部教程与会议.md)
  - [TE 流程课（借鉴实验室 pangenome `03_TE`）](zh/18_TE流程课_借鉴实验室03_TE.md)
  - [术语表（结构注释教学）](zh/99_术语表.md)
  - [中文指针](zh/A2e_s11_gapfill.md)
  - [中文指针](zh/COMPARE_HELIXER_BRAKER.md)
  - [中文指针](zh/EGAPX_COMPARE.md)
  - [入门 FAQ（稍有基础、第一次跟最短路径）](zh/FAQ_入门.md)
  - [中文指针](zh/LINEAGES.md)
  - [中文指针](zh/MERGE_AND_ENTRIES.md)
  - [中文指针](zh/PROVISIONAL_NOT_L1.md)
  - [中文教学入口](zh/README.md)
  - [中文指针](zh/TRUSTED_TE_PATH.md)
  - [中文指针](zh/golden_pack.md)
  - [交接指针](zh/交接_结构到功能.md)
  - [三种植物模拟（练习仓库改进）](zh/植物三种模拟.md)
  - [读 plan 时看什么（英文 plan 指针）](zh/读plan.md)
  - [结构注释](zh/验收勾选表.md)

<a id="reference-workflow"></a>
## 参考流程

下列页面给出一条参考路线，以及怎样选分支、怎样检查结果。它们是知识库的一部分，不是维护中的软件。

- [Start here — gene structure](../docs/START_HERE.md)
- [Quickstart — run once, understand the project](../docs/QUICKSTART.md)
- [Branch roadmap — gene structure](../docs/ROADMAP.md)
- [Gene structure playbook — assembly to qualified GFF](../docs/PLAYBOOK.md)
- [Detailed guide — every step from assembly to qualified annotation](../docs/DETAILED_GUIDE.md)
- [Stage reference (assembly → release)](../docs/FULL_PIPELINE.md)
- [Upstream structural spine (optional)](../docs/steps/MAIN.md)
- [S14 — EVM consensus path (`docs/steps/dclab/`)](../docs/steps/dclab/README.md)
- [Stage I/O — what goes in, what comes out](../docs/STAGE_IO.md)
- [Scenarios — how to annotate in each situation](../docs/SCENARIOS.md)
- [Post-assembly path (one page)](../docs/POST_ASSEMBLY.md)
- [Entry modes + merge QC (process guide)](../docs/MERGE_AND_ENTRIES.md)
- [Boundary — three layers (do not mix)](../docs/BOUNDARY.md)
- [Handoff card — structure → function](../docs/HANDOFF_STRUCTURE_TO_FUNCTION.md)
- [Install / 安装 — gene-structure-annotation](../docs/INSTALL_STRUCTURE.md)
- [Preflight check before RUN=1 / 运行前检查](../docs/PREFLIGHT.md)
- [Flow tool — progressive automation](../docs/FLOW_TOOL.md)
- [Final evaluation criteria — gene structure](../docs/EVALUATION.md)
- [Structure release checklist (pass / fail)](../docs/EVALUATION_CHECKLIST.md)
- [AI-assisted annotation — prompts, data, order, checks](../docs/AI_ASSIST.md)

<a id="software-lists-and-sources"></a>
## 软件清单与来源

- [按分析步骤整理的软件指南](../docs/software/README.zh.md)
- [`SOFTWARE_AUTHORITY.tsv`](../catalog/SOFTWARE_AUTHORITY.tsv)
- [Catalog — new structural tools, databases and ideas by stage (2026-11)](../catalog/README.md)
- [Tools — gene structure (this repo)](../docs/TOOLS.md)
- [Related software (structural)](../docs/RELATED_SOFTWARE.md)
- [Peer structural pipelines (biology-wide)](../docs/PEER_PIPELINES.md)
- [Annotation quality — methods, papers, repos](../docs/QUALITY_SOURCES.md)
- [支撑本仓库的综述与评测论文](../docs/REVIEWS.md)
- [External tutorials & meetings — gene structure](../docs/TUTORIALS_AND_MEETINGS.md)

<a id="example-code"></a>
## 示例代码与测试数据

示例代码展示每一步怎么做，规模很小，在玩具数据上测试过。各步的脚本已在上面对应主题下列出，这里只列通用部分。

- [Pipeline folder overview](../pipeline/00_overview.md)
- [flow_tool (structure) — step 1 (`pipeline/flow_tool/`)](../pipeline/flow_tool/README.md) · 3 个文件
- [`preflight.py`](../pipeline/preflight.py)
- [`print_qc_commands.py`](../pipeline/print_qc_commands.py)
- [`check_release_pack.py`](../pipeline/check_release_pack.py)
- [`_env_guards.sh`](../pipeline/_env_guards.sh)
- [`sbatch_s1_examples.sh`](../pipeline/sbatch_s1_examples.sh)
- [`sbatch_s11_examples.sh`](../pipeline/sbatch_s11_examples.sh)
- [config/ (`config/`)](../config/) · 6 个文件
- [envs/ (`envs/`)](../envs/) · 3 个文件
- [scripts/ (`scripts/`)](../scripts/) · 2 个文件
- [Tests (`tests/`)](../tests/README.md) · 22 个文件
- [testdata/ (`testdata/`)](../testdata/) · 12 个文件
- [skills/ (`skills/`)](../skills/) · 1 个文件

<a id="figures"></a>
## 图

- [Figures](../docs/figures/README.md); [Figures for the guide](../docs/figures/guide/README.md) · 53 个文件

<a id="older-pages"></a>
## 旧页面与勘误

下列页面保留作历史记录，内容未改。当前内容以上面各节为准。

| 页面 | 说明 |
|---|---|
| [Audit 2026-09-14 — gene-structure-annotation](../docs/AUDIT_2026-09-14.md) | 2026-09-14 对照文献检查本仓库各页的记录。 |
| [Self-audit — gene-structure-annotation](../docs/SELF_AUDIT.md) | 2026-09-14 对分支选择和同类流程清单的自查记录。 |
| [Software, databases and ideas by type (structural) — 2026-11](../docs/CATALOG_BY_TYPE_2026-11.md) | 2026-11 按类型整理的第一版清单。现行目录是首页的方法目录和 catalog/SOFTWARE_AUTHORITY.tsv。 |
| [New tools, databases and ideas by stage (structural) — 2026-11 survey](../docs/CATALOG_NEW_TOOLS_2026-11.md) | 2026-11 按阶段整理的第一版清单。现行目录同上。 |
| [Erratum to gene-function-annotation catalog v4 (NLR-Annotator, NLRSeek, plantiSMASH 2.0)](../docs/CATALOG_NEW_TOOLS_2026-11_ERRATUM_NLR_PLANTISMASH.md) | 对 2026-11 清单的勘误（NLR-Annotator、NLRSeek、plantiSMASH 2.0）。 |
| [Erratum: GSAman tool paper vs last-mile opinion DOI](../docs/GSAMAN_DOI_ERRATUM.md) | 勘误：GSAman 工具论文对应哪个 DOI。 |
| [Classroom tonight (structure) — offline mirror](../docs/CLASSROOM_TONIGHT.md) | Wiki 上一次课堂入门清单的离线副本。现行入口是 docs/START_HERE.md。 |
| [Wiki 页 Start-tonight](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Start-tonight) | 第一次上手用的 Wiki 页，不在克隆的仓库里。 |
| [Annotation board（Project #2）](https://github.com/users/Xuzhen-Li/projects/2) | 注释仓库的任务看板。 |

<a id="other-files"></a>
## 其他文件

- `.github/` · 5 个文件
- `.gitignore`
- `CONTRIBUTING.md`
- `README.md`
- `README.zh.md`
- `CHANGELOG.md`
- `LICENSE`
- `NOTICE.md`
