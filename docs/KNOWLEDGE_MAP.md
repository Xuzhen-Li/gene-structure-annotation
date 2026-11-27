# Knowledge map

[中文](KNOWLEDGE_MAP.zh.md)

This page indexes every part of this repository, by topic and by kind of page. The repository is a knowledge base on structural gene annotation of plant genomes: the book explains each step, the catalogue compares software and databases, the reference workflow shows one way to run the steps, and the example code shows what a step looks like on small data. The layout follows [TE-Lib](https://github.com/Xuzhen-Li/TE-Lib).

TE-Lib was formerly named vitis-te. Older pages still use that name; GitHub redirects the old links.

- [Knowledge units and workflow index](#knowledge-units)
- [Topics](#topics)
- [Learn](#learn)
- [Reference workflow](#reference-workflow)
- [Software lists and sources](#software-lists-and-sources)
- [Example code and test data](#example-code)
- [Figures](#figures)
- [Older pages and corrections](#older-pages)
- [Other repository files](#other-files)

<a id="knowledge-units"></a>
## Knowledge units and workflow index

- [Structural gene annotation: an overview](kb/field-overview.md)
- [Gene models and the evidence behind them](kb/gene-model-concepts.md)
- [Soft-masking with a trusted TE library](kb/trusted-softmask.md)
- [Is the gene set good enough? (criteria)](kb/model-qc-criteria.md)
- Numbering schemes: [`kb/NUMBERING.md`](kb/NUMBERING.md)
- Workflow index: [`workflow/README.md`](workflow/README.md)
- Full methods catalogue: [`catalog/METHODS_CATALOG.md`](../catalog/METHODS_CATALOG.md); [`catalog/README.by-type.md`](../catalog/README.by-type.md); [`catalog/COUNTS.md`](../catalog/COUNTS.md)
- Overlap of docs/tools and docs/notes: [`TOOLS_NOTES_OVERLAP.md`](TOOLS_NOTES_OVERLAP.md)

<a id="topics"></a>
## Topics

Each topic lists the book chapter that explains it, the catalogue section that compares the tools, and, where they exist, notes on single tools, tool cards with commands, first-pass step cards, other pages and the example code.

### Concepts and principles

- Book: [Chapter 1. Concepts and principles](../book/chapters/01-concepts.md)

### 1. Assembly and assembly QC

- Book: [Chapter 2. Assembly and assembly QC](../book/chapters/02-assembly-and-assembly-qc.md)
- Catalogue: [section 1 of the Methods catalog](../catalog/METHODS_CATALOG.md#section-1)
- Tool cards: [hifiasm — HiFi contig assembly](../docs/tools/hifiasm.md)
- First-pass step cards: [Asm0 — assembly](../catalog/Asm0_assembly/README.md); [Asm1 — assembly QC](../catalog/Asm1_assembly_qc/README.md)
- Example code and data: [Asm0 — Genome assembly (before annotation)](../pipeline/Asm0_assembly.md); [Asm1 — Assembly QC gate](../pipeline/Asm1_assembly_qc.md)

### 2. Soft-mask with a trusted library

- Book: [Chapter 3. Soft-mask with a trusted library](../book/chapters/03-soft-mask-with-a-trusted-library.md)
- Catalogue: [section 2 of the Methods catalog](../catalog/METHODS_CATALOG.md#section-2)
- Notes on single tools: [Earl Grey](../docs/notes/earlgrey.md)
- Tool cards: [EDTA — de novo TE library (step 1 of the lab scheme)](../docs/tools/edta.md); [ProtExcluder (pattern) — clean host genes out of TE libraries](../docs/tools/protexcluder.md); [RepeatMasker — soft-mask TE](../docs/tools/repeatmasker.md)
- First-pass step cards: [A0 / A0b — soft-mask with a trusted library](../catalog/A0_softmask/README.md)
- Other pages: [TE library scheme → soft-mask (A0)](../docs/TE_LIBRARY.md); [Trusted TE path — copy-paste checklist (A0)](../docs/TRUSTED_TE_PATH.md)
- Example code and data: [A0 — Soft-mask (detailed)](../pipeline/A0_softmask.md); [A0b — Optional host-gene purge (ProtExcluder-style)](../pipeline/A0b_protexcluder.md)

### 3. RNA and Iso-Seq evidence

- Book: [Chapter 4. RNA and Iso-Seq evidence](../book/chapters/04-rna-and-iso-seq-evidence.md)
- Catalogue: [section 3 of the Methods catalog](../catalog/METHODS_CATALOG.md#section-3)
- Notes on single tools: [IsoAnnot / FIT (with SQANTI3)](../docs/notes/isoannot_fit.md); [IsoQuant](../docs/notes/isoquant.md); [Long-read isoform peers (beyond IsoQuant / SQANTI3)](../docs/notes/lr_isoform_peers.md); [Mikado + Portcullis](../docs/notes/mikado_portcullis.md); [SQANTI3](../docs/notes/sqanti3.md)
- Tool cards: [HISAT2 / STAR — short-read RNA alignment](../docs/tools/hisat2_star.md); [minimap2 — Iso-seq / long RNA](../docs/tools/minimap2.md); [PASA — transcript assemblies for training + polish](../docs/tools/pasa.md); [StringTie — transcript assembly (sanity track)](../docs/tools/stringtie.md)
- First-pass step cards: [A1 / A1b — engine choice and RNA / Iso-Seq evidence](../catalog/A1_engine_and_rna/README.md)
- Example code and data: [A1b — RNA align (detailed)](../pipeline/A1b_rna_align.md)

### 4. Protein evidence

- Book: [Chapter 5. Protein evidence](../book/chapters/05-protein-evidence.md)
- Catalogue: [section 4 of the Methods catalog](../catalog/METHODS_CATALOG.md#section-4)
- Notes on single tools: [MetaEuk](../docs/notes/metaeuk.md); [miniprot · Spaln (protein-to-genome)](../docs/notes/miniprot_spaln.md); [ProtHint · miniprothint](../docs/notes/prothint_miniprothint.md)
- Tool cards: [miniprot — fast protein-to-genome alignment](../docs/tools/miniprot.md)
- Example code and data: [A2 — PROTEIN_DB for BRAKER / GALBA](../pipeline/A2_protein_db.md)

### 5. Ab initio gene finders

- Book: [Chapter 6. Ab initio gene finders](../book/chapters/06-ab-initio-gene-finders.md)
- Catalogue: [section 5 of the Methods catalog](../catalog/METHODS_CATALOG.md#section-5)
- Notes on single tools: [ANNEVO (Kai Ye / 叶凯 lab, XJTU)](../docs/notes/annevo.md); [BRAKER4 (Gaius-Augustus) — Snakemake rewrite of BRAKER](../docs/notes/braker4.md); [Classic ab initio engines (high citation building blocks)](../docs/notes/classic_abinitio.md); [GALBA2](../docs/notes/galba2.md); [Helixer](../docs/notes/helixer.md); [Tiberius](../docs/notes/tiberius.md)
- Tool cards: [BRAKER3 — primary gene prediction (RNA + proteins)](../docs/tools/braker3.md); [BRAKER4 — preferred modern BRAKER runner](../docs/tools/braker4.md); [GALBA — protein-only gene prediction](../docs/tools/galba.md); [Helixer — deep-learning ab initio genes](../docs/tools/helixer.md)
- First-pass step cards: [A2](../catalog/A2_drafts/README.md)
- Other pages: [Helixer ↔ BRAKER — classroom compare (not default production)](../docs/COMPARE_HELIXER_BRAKER.md)
- Example code and data: [A1 — Choose the draft engine](../pipeline/A1_choose_engine.md); [`A2_run_draft.sh`](../pipeline/A2_run_draft.sh); [A2b — Second prediction set](../pipeline/A2b_second_predictor.md)

### 6. DNA language-model predictors

- Book: [Chapter 7. DNA language-model predictors](../book/chapters/07-dna-language-model-predictors.md)
- Catalogue: [section 6 of the Methods catalog](../catalog/METHODS_CATALOG.md#section-6)
- Notes on single tools: [OrionGeno (BGI Research)](../docs/notes/oriongeno.md)

### 7. Lift-over and annotation transfer

- Book: [Chapter 8. Lift-over and annotation transfer](../book/chapters/08-lift-over-and-annotation-transfer.md)
- Catalogue: [section 7 of the Methods catalog](../catalog/METHODS_CATALOG.md#section-7)
- Notes on single tools: [Comparative Annotation Toolkit (CAT)](../docs/notes/cat.md); [CESAR2.0](../docs/notes/cesar2.md); [LiftOn](../docs/notes/lifton.md); [TOGA2](../docs/notes/toga2.md)
- Tool cards: [GeMoMa — homology projection from an annotated genome](../docs/tools/gemoma.md); [Liftoff — map annotation GFF to a new assembly](../docs/tools/liftoff.md); [LiftOn — T2T-grade lift (Liftoff + miniprot)](../docs/tools/lifton.md); [SynGAP — haplotype / synteny annotation polish](../docs/tools/syngap.md)
- First-pass step cards: [Last mile 05 — SynGAP polish / multi-haplotype harmonisation](../catalog/LM05_syngap_polish/README.md)
- Example code and data: [A2c — Liftoff (detailed)](../pipeline/A2c_liftoff.md); [A2e — S11 gap-fill (after Liftoff)](../pipeline/A2e_s11_gapfill.md); [Optional: SynGAP polish](../pipeline/05_syngap_polish.md)

### 8. Combiners and annotation pipelines

- Book: [Chapter 9. Combiners and annotation pipelines](../book/chapters/09-combiners-and-annotation-pipelines.md)
- Catalogue: [section 8 of the Methods catalog](../catalog/METHODS_CATALOG.md#section-8)
- Notes on single tools: [combinr · InGenAnnot (combiners)](../docs/notes/combinr_ingenannot.md); [NCBI EGAPx / Gnomon (institutional)](../docs/notes/egapx_gnomon.md); [EviAnn (Evidence Annotation)](../docs/notes/eviann.md); [FINDER](../docs/notes/finder.md); [funannotate2](../docs/notes/funannotate2.md); [GETA](../docs/notes/geta.md); [MAKER / MAKER2 (mainstream, high citation)](../docs/notes/maker2.md); [MoGAAAP](../docs/notes/mogaaap.md)
- Tool cards: [EGAPx — NCBI’s annotation pipeline (optional parallel)](../docs/tools/egapx.md); [EviAnn — evidence-driven annotation (Iso-seq friendly)](../docs/tools/eviann.md); [EVidenceModeler (EVM) — merge competing gene predictions](../docs/tools/evm.md); [MAKER-P — classical plant annotation engine](../docs/tools/maker_p.md); [Mikado — pick best transcripts at overlapping loci](../docs/tools/mikado.md); [TSEBRA — combine two BRAKER-family GTFs](../docs/tools/tsebra.md)
- First-pass step cards: [A4 — aggregation (A4a TSEBRA, A4b Mikado, A4c–A4d EVM, A4e PASA update)](../catalog/A4_aggregation/README.md)
- Other pages: [EGAPx / S8 — optional 对照 & GenBank door (not default)](../docs/EGAPX_COMPARE.md)
- Example code and data: [A2d — Optional: NCBI EGAPx (eudicot / rosids)](../pipeline/A2d_egapx_optional.md); [A4 multi-source aggregation (EVM main path, TSEBRA / Mikado / PASA optional)](../pipeline/A4_aggregation.md); [`A4_merge_sets.sh`](../pipeline/A4_merge_sets.sh); [`A4a_tsebra_optional.sh`](../pipeline/A4a_tsebra_optional.sh); [`A4b_mikado_optional.sh`](../pipeline/A4b_mikado_optional.sh); [`A4c_evm_inputs.py`](../pipeline/A4c_evm_inputs.py); [`A4d_evm_run.sh`](../pipeline/A4d_evm_run.sh); [`A4e_pasa_update.sh`](../pipeline/A4e_pasa_update.sh); [Aggregation toy data (simulated) (`examples/aggregation_toy/`)](../examples/aggregation_toy/README.md)

### 9. Non-coding RNA and pseudogene loci

- Book: [Chapter 10. Non-coding RNA and pseudogene loci](../book/chapters/10-non-coding-rna-and-pseudogene-loci.md)
- Catalogue: [section 9 of the Methods catalog](../catalog/METHODS_CATALOG.md#section-9)
- Notes on single tools: [ncRNA + TE classification side-lanes](../docs/notes/ncrna_tesorter.md)

### 10. Gene-model QC

- Book: [Chapter 11. Gene-model QC](../book/chapters/11-gene-model-qc.md)
- Catalogue: [section 10 of the Methods catalog](../catalog/METHODS_CATALOG.md#section-10)
- Notes on single tools: [OMArk · compleasm (annotation/assembly QC)](../docs/notes/omark_compleasm.md); [PSAURON · GAQET2 · AnnoAudit (QC packs)](../docs/notes/psauron_gaqet_annoaudit.md)
- Tool cards: [BUSCO — completeness](../docs/tools/busco.md); [OMArk + Compleasm — extra proteome / assembly QC](../docs/tools/omark_compleasm.md); [PSAURON — protein coding-likelihood scores](../docs/tools/psauron.md)
- First-pass step cards: [A5 — structure QC (A5b–A5e, structure_qa qa01–qa10)](../catalog/A5_structure_qc/README.md); [Last mile 01 — BUSCO / PSAURON QC](../catalog/LM01_qc_busco_psauron/README.md)
- Other pages: [Recommended BUSCO / Compleasm lineages (plants)](../docs/LINEAGES.md)
- Example code and data: [`A5_agat_stats.sh`](../pipeline/A5_agat_stats.sh); [`A5b_omark_compleasm.sh`](../pipeline/A5b_omark_compleasm.sh); [A5c — Expression + domain filter (GetaFilter idea)](../pipeline/A5c_expression_pfam_filter.md); [`A5d_stage_counts.sh`](../pipeline/A5d_stage_counts.sh); [`A5e_filter_proteins.sh`](../pipeline/A5e_filter_proteins.sh); [`01_qc_busco_psauron.sh`](../pipeline/01_qc_busco_psauron.sh); [`protein_stop_check.py`](../pipeline/protein_stop_check.py); [Structure QA step / 结构注释质量评估 (`pipeline/structure_qa/`)](../pipeline/structure_qa/README.md); [Simulated example for the structure QA step / 结构质量评估模拟示例 (`examples/structure_qa_sim/`)](../examples/structure_qa_sim/README.md)

### 11. Curation and browsers

- Book: [Chapter 12. Curation and browsers](../book/chapters/12-curation-and-browsers.md)
- Catalogue: [section 11 of the Methods catalog](../catalog/METHODS_CATALOG.md#section-11)
- Tool cards: [GSAman — manual gene-structure curation](../docs/tools/gsaman.md)
- First-pass step cards: [Last mile 02 — priority loci (02, 02b)](../catalog/LM02_priority_loci/README.md); [Last mile 03 — evidence pack](../catalog/LM03_evidence_pack/README.md); [Last mile 04 — GSAman / manual curation](../catalog/LM04_gsaman_curation/README.md)
- Other pages: [Four structural error classes (from GSAman)](../docs/ERROR_CLASSES.md)
- Example code and data: [`02_priority_loci.py`](../pipeline/02_priority_loci.py); [`02b_merge_priority_r2.py`](../pipeline/02b_merge_priority_r2.py); [03 — Evidence pack for GSAman (detailed)](../pipeline/03_evidence_checklist.md); [04 — GSAman curation (detailed)](../pipeline/04_gsaman_curation.md)

### 12. GFF3 cleanup and release

- Book: [Chapter 13. GFF3 cleanup and release](../book/chapters/13-gff3-cleanup-and-release.md)
- Catalogue: [section 12 of the Methods catalog](../catalog/METHODS_CATALOG.md#section-12)
- Tool cards: [AGAT + gffread — GFF hygiene and proteins](../docs/tools/agat_gffread.md)
- First-pass step cards: [A3 — proteins from GFF](../catalog/A3_proteins/README.md); [A6 / A6b — hand-off to function](../catalog/A6_handoff_to_function/README.md); [Last mile 06 — release](../catalog/LM06_release/README.md)
- Example code and data: [`A3_proteins_from_gff.sh`](../pipeline/A3_proteins_from_gff.sh); [A6 — Hand-off to function (FA is NEVER a product of this repo)](../pipeline/A6_handoff_to_function.md); [`A6b_rename_gff.py`](../pipeline/A6b_rename_gff.py); [06 — Release qualified GFF (detailed)](../pipeline/06_release_gff.md); [`longest_isoform.py`](../pipeline/longest_isoform.py); [Golden pack (EXAMPLE checklist) — structure L0 / L1 (`examples/golden_pack/`)](../examples/golden_pack/README.md)

### 13. Reference databases

- Book: [Chapter 14. Reference databases](../book/chapters/14-reference-databases.md)
- Catalogue: [section 13 of the Methods catalog](../catalog/METHODS_CATALOG.md#section-13)
- First-pass step cards: [Database index](../catalog/_databases.md)

### 14. Standards and overview papers

- Book: [Chapter 15. Standards and overview papers](../book/chapters/15-standards-and-overview-papers.md)
- Catalogue: [section 14 of the Methods catalog](../catalog/METHODS_CATALOG.md#section-14)
- Notes on single tools: [Dario Copetti — practical plant annotation scheme](../docs/notes/copetti.md)
- First-pass step cards: [Cross-stage: whole pipelines, overview papers and standards](../catalog/X_cross_stage/README.md)

### 15. Ideas not yet tied to one tool

- Book: [Chapter 16. Ideas not yet tied to one tool](../book/chapters/16-ideas-not-yet-tied-to-one-tool.md)
- Catalogue: [section 15 of the Methods catalog](../catalog/METHODS_CATALOG.md#section-15)

### Visualization tools

- Book: [Chapter 17. Visualization tools](../book/chapters/17-visualization-tools.md)
- Catalogue: [Visualization tools in the Methods catalog](../catalog/METHODS_CATALOG.md#visualization)

### Choosing tools

- Book: [Chapter 18. Choosing tools](../book/chapters/18-choosing-tools.md)
- First-pass step cards: [Branch view (S1–S14)](../catalog/_branches.md)

### Pitfalls and quality control

- Book: [Chapter 19. Pitfalls and quality control](../book/chapters/19-pitfalls-and-qc.md)

### Worked example: a grapevine genome on route S1

- Book: [Chapter 20. Worked example: a grapevine genome on route S1](../book/chapters/20-worked-example.md)
- Other pages: [Case: *Vitis* T2T assembly → publication-grade structure (S1 engine + S5 bar)](../docs/cases/vitis-t2t-s1-s5.md)
- Example code and data: [Plant simulation trio (`examples/plant_sim/`)](../examples/plant_sim/README.md)

### Glossary

- Book: [Appendix A. Glossary](../book/chapters/appendix-a-glossary.md)

<a id="learn"></a>
## Learn

- Book: [Plant gene structure annotation: a study guide with grapevine as the example](../book/README.md); [Plant gene structure annotation: a study guide with grapevine as the example](../book/BOOK_full.md); [Book file index · 全书文件索引](../book/INDEX.md); [Preface](../book/chapters/00-preface.md)
- Bilingual pages: [Bilingual teaching track](../docs/BILINGUAL.md)
- Chinese teaching pages (34):
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
## Reference workflow

These pages give one reference route, how to choose a branch and how to check the result. They are part of the knowledge base, not a maintained software package.

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
## Software lists and sources

- [Software guide by analysis step](../docs/software/README.md)
- [`SOFTWARE_AUTHORITY.tsv`](../catalog/SOFTWARE_AUTHORITY.tsv)
- [Catalog — new structural tools, databases and ideas by stage (2026-11)](../catalog/README.md)
- [Tools — gene structure (this repo)](../docs/TOOLS.md)
- [Related software (structural)](../docs/RELATED_SOFTWARE.md)
- [Peer structural pipelines (biology-wide)](../docs/PEER_PIPELINES.md)
- [Annotation quality — methods, papers, repos](../docs/QUALITY_SOURCES.md)
- [Overview papers and benchmarks behind these pages](../docs/REVIEWS.md)
- [External tutorials & meetings — gene structure](../docs/TUTORIALS_AND_MEETINGS.md)

<a id="example-code"></a>
## Example code and test data

The example code shows how each step is done. It is small and tested on toy data. Step scripts are listed under their topic above; this list has the shared parts.

- [Pipeline folder overview](../pipeline/00_overview.md)
- [flow_tool (structure) — step 1 (`pipeline/flow_tool/`)](../pipeline/flow_tool/README.md) · 3 files
- [`preflight.py`](../pipeline/preflight.py)
- [`print_qc_commands.py`](../pipeline/print_qc_commands.py)
- [`check_release_pack.py`](../pipeline/check_release_pack.py)
- [`_env_guards.sh`](../pipeline/_env_guards.sh)
- [`sbatch_s1_examples.sh`](../pipeline/sbatch_s1_examples.sh)
- [`sbatch_s11_examples.sh`](../pipeline/sbatch_s11_examples.sh)
- [config/ (`config/`)](../config/) · 6 files
- [envs/ (`envs/`)](../envs/) · 3 files
- [scripts/ (`scripts/`)](../scripts/) · 2 files
- [Tests (`tests/`)](../tests/README.md) · 22 files
- [testdata/ (`testdata/`)](../testdata/) · 12 files
- [skills/ (`skills/`)](../skills/) · 1 files

<a id="figures"></a>
## Figures

- [Figures](../docs/figures/README.md); [Figures for the guide](../docs/figures/guide/README.md) · 53 files

<a id="older-pages"></a>
## Older pages and corrections

These pages are kept as a record and are unchanged. The sections above hold the current material.

| Page | Note |
|---|---|
| [Audit 2026-09-14 — gene-structure-annotation](../docs/AUDIT_2026-09-14.md) | A check of these pages against the literature, dated 2026-09-14. |
| [Self-audit — gene-structure-annotation](../docs/SELF_AUDIT.md) | A self-check of the branch chooser and peer list, dated 2026-09-14. |
| [Software, databases and ideas by type (structural) — 2026-11](../docs/CATALOG_BY_TYPE_2026-11.md) | The first 2026-11 list by type. The current catalogue is the Methods catalog on the home page and catalog/SOFTWARE_AUTHORITY.tsv. |
| [New tools, databases and ideas by stage (structural) — 2026-11 survey](../docs/CATALOG_NEW_TOOLS_2026-11.md) | The first 2026-11 list by stage. The current catalogue is the same as above. |
| [Erratum to gene-function-annotation catalog v4 (NLR-Annotator, NLRSeek, plantiSMASH 2.0)](../docs/CATALOG_NEW_TOOLS_2026-11_ERRATUM_NLR_PLANTISMASH.md) | A correction to the 2026-11 list (NLR-Annotator, NLRSeek, plantiSMASH 2.0). |
| [Erratum: GSAman tool paper vs last-mile opinion DOI](../docs/GSAMAN_DOI_ERRATUM.md) | A correction on which DOI belongs to the GSAman tool paper. |
| [Classroom tonight (structure) — offline mirror](../docs/CLASSROOM_TONIGHT.md) | An offline copy of a one-evening class checklist from the wiki. The current start page is docs/START_HERE.md. |
| [Wiki page Start-tonight](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Start-tonight) | A wiki page for a first evening, not in the clone. |
| [Annotation board (Project #2)](https://github.com/users/Xuzhen-Li/projects/2) | A task board for the annotation repositories. |

<a id="other-files"></a>
## Other repository files

- `.github/` · 5 files
- `.gitignore`
- `CONTRIBUTING.md`
- `README.md`
- `README.zh.md`
- `CHANGELOG.md`
- `LICENSE`
- `NOTICE.md`
