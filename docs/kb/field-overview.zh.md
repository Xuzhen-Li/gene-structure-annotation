# 结构基因注释：概览

[English](field-overview.md) · [知识单元](README.zh.md)

## 1. 是什么

结构基因注释回答组装基因组的一个问题：基因在哪里，外显子和内含子怎样排布，它们编码哪些蛋白和非编码 RNA？结果是写成 GFF3 行的一套基因模型，加上预测出的蛋白（`proteins.faa`）。这些蛋白做什么（名称、GO、通路）是另一层，在 [gene-function-annotation](https://github.com/Xuzhen-Li/gene-function-annotation) 中处理。给真核生物基因组做注释，非专家也能做，但仍是一项有挑战的工作（说法 1）。植物基因组因为基因组大、转座子多、倍性多变，难度更高（说法 2）。

## 2. 问题与背后的概念

**基因组准备好做基因预测了吗？** 基因预测依赖组装：组装不完整会导致基因预测出错（说法 3）。重复序列应先标出来。**soft-mask** 把重复区写成小写字母，其余区域写成大写字母；对一些预测器来说，这比把重复区换成 `N`（hard-mask）效果更好（说法 4）。用哪个重复序列库见[用可信 TE 库做 soft-mask](trusted-softmask.zh.md)。书：第 2、3 章。

**什么证据定义一个基因模型？** 一个基因模型由[基因模型及其证据](gene-model-concepts.zh.md)中列出的几类证据构建：

- *转录本。* 短读长 RNA-seq 和长读长可以组装成转录本；StringTie2 是参考引导（reference-guided）的，IsoQuant 则有无参考注释均可（说法 5）。书：第 4 章。
- *近缘物种的蛋白。* 在一个基因组没有转录组数据时，蛋白到基因组的比对器可以驱动基因预测（说法 6）。书：第 5 章。
- *从头预测与学习型预测。* 深度学习预测器只凭 DNA 序列推断基因，但其中一个工具 Helixer 在 2021 年的论文中被描述为输出逐碱基概率，还不是完整的基因模型；另一个是在哺乳动物基因组上训练的（说法 7 和 8）。书：第 6、7 章。

任何单一证据都不够。在对五个植物基因组的比较中，只靠 RNA 读段比对得到的转录本不够，推荐把基于证据和从头预测的流程结合起来（说法 9）。

**证据冲突和已有注释怎样协调？** *合并器*把多条证据合成一套基因集。EVidenceModeler 把基因结构报告为全部证据的加权一致结果（说法 10）；TSEBRA 依据 RNA-seq 和蛋白的支持，在 BRAKER1（仅 RNA-seq）与 BRAKER2（仅蛋白）的预测之间做选择（说法 11）。当一个近缘基因组已有良好注释时，*lift-over* 把它的基因映射到新组装上：Liftoff 比对基因并保持每个外显子、转录本和基因的结构（说法 12），LiftOn 加入蛋白比对，使注释可以在更远缘的物种之间转移（说法 13）。书：第 8、9 章。

**蛋白编码基因之外还有什么？** 非编码 RNA 基因和假基因在蛋白编码集之外；MAKER-P 是为植物扩展的注释引擎，增加了非编码 RNA 注释和假基因识别（说法 14）。书：第 10 章。

**基因集够好、可以发布了吗？** 完整性可以用通用单拷贝直系同源基因（BUSCO）来衡量（说法 15）。只看完整性会漏掉其他错误：OMArk 还检验基因集相对近缘物种的一致性并报告可能的污染（说法 16），PSAURON 给每条编码序列打分，表示它是真实蛋白编码区的可能性（说法 17）。2023 年的一项比较指出，评估结构注释质量和完整性的稳健标准仍然缺乏（说法 9）。发布的文件还要遵守 GFF3 规则，例如从外显子到转录本再到基因的 `Parent` 链接，以及每条 CDS 行都有相位（说法 18）。阈值和门槛只写在 [`docs/EVALUATION.md`](../EVALUATION.md)。书：第 11 到 13 章。

## 3. 从书的哪里读起

- **刚接触结构注释：** [前言](../../book/chapters/00-preface.zh.md)和[第 1 章 概念与原理](../../book/chapters/01-concepts.zh.md)，生词查[附录 A 术语表](../../book/chapters/appendix-a-glossary.zh.md)。
- **注释前检查组装或重复序列屏蔽：** [第 2 章 组装与组装质控](../../book/chapters/02-assembly-and-assembly-qc.zh.md)和[第 3 章 用可信库做 soft-mask](../../book/chapters/03-soft-mask-with-a-trusted-library.zh.md)。
- **决定怎么用 RNA-seq、Iso-Seq 或蛋白数据：** [第 4 章 RNA 与 Iso-Seq 证据](../../book/chapters/04-rna-and-iso-seq-evidence.zh.md)和[第 5 章 蛋白证据](../../book/chapters/05-protein-evidence.zh.md)。
- **比较从头预测、深度学习、lift-over 和合并策略：** [第 6 章 从头基因预测](../../book/chapters/06-ab-initio-gene-finders.zh.md)、[第 7 章 DNA 语言模型预测](../../book/chapters/07-dna-language-model-predictors.zh.md)、[第 8 章 注释转移（lift-over）](../../book/chapters/08-lift-over-and-annotation-transfer.zh.md)、[第 9 章 合并器与注释流程](../../book/chapters/09-combiners-and-annotation-pipelines.zh.md)和[第 18 章 怎么选工具](../../book/chapters/18-choosing-tools.zh.md)。
- **非编码 RNA 与假基因位点：** [第 10 章 非编码 RNA 与假基因位点](../../book/chapters/10-non-coding-rna-and-pseudogene-loci.zh.md)。
- **评估、校对或发布基因集：** [第 11 章 基因模型质控](../../book/chapters/11-gene-model-qc.zh.md)、[第 12 章 人工校对与浏览器](../../book/chapters/12-curation-and-browsers.zh.md)、[第 13 章 GFF3 清理与发布](../../book/chapters/13-gff3-cleanup-and-release.zh.md)和[第 19 章 常见问题与质控](../../book/chapters/19-pitfalls-and-qc.zh.md)。
- **跟一个完整的植物实例：** [第 20 章 实例：葡萄基因组走 S1 路线](../../book/chapters/20-worked-example.zh.md)。

## 4. 植物和 *Vitis* 里已知什么

- 植物基因组难注释，原因是基因组大、转座子多、倍性多变（说法 2）。
- 葡萄实例见 [`docs/cases/vitis-t2t-s1-s5.md`](../cases/vitis-t2t-s1-s5.md) 和书的第 20 章。本页不给出葡萄基因模型中融合或拆分比例的一般数字。

## 5. 说法与来源

引用的句子抄自同一行所列的来源，保持原文语言。摘要读自每篇论文的 Europe PMC 记录。

| # | 说法 | 来源 | 引用原句 | 读了什么 |
|---|---|---|---|---|
| 1 | 给真核生物基因组做注释，非专家也能做，但仍是一项有挑战的工作。 | Yandell and Ence 2012, *Nat Rev Genet*, [doi:10.1038/nrg3174](https://doi.org/10.1038/nrg3174) | “Although annotating a eukaryotic genome assembly is now within the reach of non-experts, it remains a challenging task.” | 摘要（PMID 22510764） |
| 2 | 植物基因组注释之所以难，在于基因组大、转座子多、倍性多变。 | Vuruputoor et al. 2023, *Appl Plant Sci*, [doi:10.1002/aps3.11533](https://doi.org/10.1002/aps3.11533) | “The annotation of plant genomes is particularly challenging due to their large sizes, abundant transposable elements, and variable ploidies.” | 摘要（PMID 37601314） |
| 3 | 组装不完整会导致基因预测出错。 | Huang and Li 2023, *Bioinformatics*, [doi:10.1093/bioinformatics/btad595](https://doi.org/10.1093/bioinformatics/btad595) | “An incomplete assembly can lead to errors in gene predictions, annotation, and other downstream analyses.” | 摘要（PMID 37758247） |
| 4 | 预测前应先屏蔽重复序列；soft-mask 在某些预测器上比 hard-mask 效果更好。 | BRAKER README ([Gaius-Augustus/BRAKER](https://github.com/Gaius-Augustus/BRAKER)) | “This will avoid the prediction of false positive gene structures in repetitive and low complexitiy regions.” (spelling as in the source); “In case of GeneMark-ES/ET/EP/ETP and AUGUSTUS, softmasking (i.e. putting repeat regions into lower case letters and all other regions into upper case letters) leads to better results than hardmasking (i.e. replacing letters in repetitive regions by the letter `N` for unknown nucleotide).” | README，基因组文件一节 |
| 5 | 短读长和长读长 RNA 都能组装成转录本；IsoQuant 有无参考注释均可。 | Kovaka et al. 2019, *Genome Biol*, [doi:10.1186/s13059-019-1910-1](https://doi.org/10.1186/s13059-019-1910-1); Prjibelski et al. 2023, *Nat Biotechnol*, [doi:10.1038/s41587-022-01565-y](https://doi.org/10.1038/s41587-022-01565-y) | “Here we present StringTie2, a reference-guided transcriptome assembler that works with both short and long reads.”; “Here we present IsoQuant-a computational tool using intron graphs that accurately reconstructs transcripts both with and without reference genome annotation.” | 摘要（PMID 31842956; PMID 36593406） |
| 6 | 在没有转录组数据的基因组上，蛋白到基因组的比对器可以驱动基因预测。 | Brůna et al. 2023, *BMC Bioinformatics*, [doi:10.1186/s12859-023-05449-z](https://doi.org/10.1186/s12859-023-05449-z) | “In addition, no transcriptome data is available for some genomes.”; “Here, we introduce GALBA, a fully automated pipeline that utilizes miniprot, a rapid protein-to-genome aligner, in combination with AUGUSTUS to predict genes with high accuracy.” | 摘要（PMID 37653395） |
| 7 | 深度学习可以只凭 DNA 序列预测基因，但 Helixer 在 2021 年的论文中被描述为输出逐碱基概率，还不是完整的基因模型。 | Stiehler et al. 2021, *Bioinformatics*, [doi:10.1093/bioinformatics/btaa1044](https://doi.org/10.1093/bioinformatics/btaa1044) | “Here, we set out to improve the cross-species annotation of genes from DNA sequence alone with the help of deep learning.”; “Our method does not yet produce comprehensive gene models but rather outputs base pair wise probabilities.” | 摘要（PMID 33325516） |
| 8 | Tiberius 是在哺乳动物基因组上训练的深度学习从头预测器。 | Gabriel et al. 2024, *Bioinformatics*, [doi:10.1093/bioinformatics/btae685](https://doi.org/10.1093/bioinformatics/btae685) | “We present Tiberius, a novel deep learning-based ab initio gene predictor that end-to-end integrates convolutional and long short-term memory layers with a differentiable HMM layer.”; “Tiberius uses a custom gene prediction loss and was trained for prediction in mammalian genomes and evaluated on human and two other genomes.” | 摘要（PMID 39558581） |
| 9 | 只靠 RNA 读段比对不够；推荐把基于证据和从头预测的方法结合；缺少稳健的质量标准。 | Vuruputoor et al. 2023, 同说法 2 | “Transcripts derived from RNA-read alignments alone are not sufficient for genome annotation.”; “Gene prediction workflows that combine evidence-based and ab initio approaches are recommended, and a combination of short and long reads can improve genome annotation.”; “Robust standards to evaluate quality and completeness are lacking in eukaryotic structural genome annotation, as genome annotation software is developed using model organisms and typically lacks benchmarking to comprehensively evaluate the quality and accuracy of the final predictions.” | 摘要（PMID 37601314） |
| 10 | EVidenceModeler 把各种证据合成加权一致结果。 | Haas et al. 2008, *Genome Biol*, [doi:10.1186/gb-2008-9-1-r7](https://doi.org/10.1186/gb-2008-9-1-r7) | “EVidenceModeler (EVM) is presented as an automated eukaryotic gene structure annotation tool that reports eukaryotic gene structures as a weighted consensus of all available evidence.” | 摘要（PMID 18190707） |
| 11 | TSEBRA 依据证据支持度，在 BRAKER1（仅 RNA-seq）与 BRAKER2（仅蛋白）的预测之间做选择。 | Gabriel et al. 2021, *BMC Bioinformatics*, [doi:10.1186/s12859-021-04482-0](https://doi.org/10.1186/s12859-021-04482-0) | “BRAKER1 uses only RNA-seq data while BRAKER2 uses only a database of cross-species proteins.”; “TSEBRA uses a set of rules to compare scores of overlapping transcripts based on their support by RNA-seq and homologous protein evidence.” | 摘要（PMID 34823473） |
| 12 | Liftoff 在同一物种或近缘物种的组装之间映射基因，并保持其结构。 | Shumate and Salzberg 2021, *Bioinformatics*, [doi:10.1093/bioinformatics/btaa1016](https://doi.org/10.1093/bioinformatics/btaa1016) | “Liftoff aligns genes from a reference genome to a target genome and finds the mapping that maximizes sequence identity while preserving the structure of each exon, transcript and gene.” | 摘要（PMID 33320174） |
| 13 | 加入蛋白比对后，lift-over 可用于更远缘的物种。 | Chao et al. 2025, *Genome Res*, [doi:10.1101/gr.279620.124](https://doi.org/10.1101/gr.279620.124) | “DNA-based mapping tools help to address this challenge, but they are only able to transfer annotation between closely related species.”; “Here we introduce LiftOn, a homology-based software tool that integrates DNA and protein alignments to enhance the accuracy of genome-scale annotation and to allow mapping between relatively distant species.” | 摘要（PMID 39730188） |
| 14 | MAKER-P 为植物增加了非编码 RNA 注释和假基因识别。 | Campbell et al. 2014, *Plant Physiol*, [doi:10.1104/pp.113.230144](https://doi.org/10.1104/pp.113.230144) | “New features include better parallelization for large repeat-rich plant genomes, noncoding RNA annotation capabilities, and support for pseudogene identification.” | 摘要（PMID 24306534） |
| 15 | BUSCO 依据通用单拷贝直系同源基因估计完整性和冗余度。 | Manni et al. 2021, *Mol Biol Evol*, [doi:10.1093/molbev/msab199](https://doi.org/10.1093/molbev/msab199) | “BUSCO estimates the completeness and redundancy of processed genomic data based on universal single-copy orthologs.” | 摘要（PMID 34320186） |
| 16 | 完整性工具发现不了过度预测和污染；OMArk 还检验一致性。 | Nevers et al. 2025, *Nat Biotechnol*, [doi:10.1038/s41587-024-02147-w](https://doi.org/10.1038/s41587-024-02147-w) | “State-of-the-art tools to assess genome annotations measure the completeness of a gene repertoire but are blind to other errors, such as gene overprediction or contamination.”; “OMArk assesses not only the completeness but also the consistency of the gene repertoire as a whole relative to closely related species and reports likely contamination events.” | 摘要（PMID 38383603） |
| 17 | PSAURON 给出序列是真实蛋白编码区的可能性得分。 | Sommer, Zimin and Salzberg 2025, *NAR Genom Bioinform*, [doi:10.1093/nargab/lqae189](https://doi.org/10.1093/nargab/lqae189) | “PSAURON assigns a score to coding DNA or protein sequence that reflects the likelihood that the sequence is a genuine protein-coding region.” | 摘要（PMID 39781514） |
| 18 | GFF3 用 `Parent` 把外显子、转录本和基因连起来，并要求每条 CDS 行都有相位。 | GFF3 规范，Sequence Ontology ([gff3.md](https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md)) | “A parent ID can be used to group exons into transcripts, transcripts into genes, an so forth.” (spelling as in the source); “The phase is REQUIRED for all CDS features.” | 规范正文，`Parent` 属性和第 8 列 |
| 19 | 蛋白以 `proteins.faa` 放在发布目录里，交给功能注释。 | [`docs/HANDOFF_STRUCTURE_TO_FUNCTION.md`](../HANDOFF_STRUCTURE_TO_FUNCTION.md)（本仓库） | `PROTEINS_FA` is `…/release/<TAG>/proteins.faa` | 页首的表格 |

## 6. 另见

- 书：[前言](../../book/chapters/00-preface.zh.md)；[第 1 章 概念与原理](../../book/chapters/01-concepts.zh.md)；[第 20 章 实例](../../book/chapters/20-worked-example.zh.md)
- 知识单元：[基因模型及其证据](gene-model-concepts.zh.md)；[用可信 TE 库做 soft-mask](trusted-softmask.zh.md)；[基因集够不够好？（判据）](model-qc-criteria.zh.md)
- 按步骤的软件：[`catalog/README.by-type.zh.md`](../../catalog/README.by-type.zh.md)
- 结构、功能与 TE 工作的边界：[`docs/BOUNDARY.md`](../BOUNDARY.md)
