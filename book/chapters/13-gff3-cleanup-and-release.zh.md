# 第 13 章 GFF3 清理与发布

*本章收录[主页第 12 节](../../README.zh.md#section-12)：该节说明、含论文、实验室、权威度和评价的完整工具表，以及评测要点。链接指回仓库。*

GFF3 清理、格式校验与提交（last-mile 06、A6）。

**需要：** 审定后的 GFF 与基因组，外加 `docs/PLAYBOOK.md` 中列出的 METHODS 与核对表字段。[按场景列出的数据需求](../../README.zh.md#data-needs)

**分组：**
- *校验*（互补）：GenomeTools (gt gff3validator)、GFF3toolkit、gxfkit、noodles。每次发布前均需运行校验。
- *提交格式转换*（可替代）：table2asn、EMBLmyGFF3、Genome Annotation Generator (GAG)。提交 NCBI 用 table2asn，提交 ENA 用 EMBLmyGFF3。
- *辅助工具*（互补）：SeqKit 2、GTFtools、CrossMap。用于序列提取、汇总统计以及不同组装版本间的坐标转换。


| 工具 | 角色 | 用途 / 何时用 | 原始论文 | 实验室（通讯作者，机构） | 权威度（档位 · 被引） | 评价（出处） |
|---|---|---|---|---|---|---|
| [SeqKit 2](https://github.com/shenwei356/seqkit) | 备选 | FASTA/Q 序列处理工具包（统计、检索、翻译、去冗余等）。 | [iMeta 2024](https://doi.org/10.1002/imt2.191) | Wei Shen (Second Affiliated Hospital of Chongqing Medical University) | 标准 · 667 次 | 作者摘要原句：“SeqKit2 consistently outperforms its predecessor, albeit with marginally higher memory usage, while maintaining competitive runtimes against other tools.”；GitHub 最后提交 2026-11 |
| [Genome Annotation Generator (GAG)](https://github.com/genomeannotation/GAG) | 备选 | 由 GFF3 生成并校正 NCBI 提交所需的 `.tbl` 注释表。 | [GigaScience 2018](https://doi.org/10.1093/gigascience/giy018) | Scott M. Geib (Daniel K. Inouye U.S. Pacific Basin Agricultural Research Center) | 小众 · 73 次 | 作者摘要原句：“With WGS becoming commonplace, genome sequencing projects are moving away from the genome centers and into the ecology or biology lab, where fewer resources are present to support the process of genome assembly curation.”；GitHub 最后提交 2018-03 |
| [GenomeTools (gt gff3validator)](https://github.com/genometools/genometools) | 备选 | GFF3 格式校验、排序与规范化整理工具。 | [IEEE Transactions on Computational Biology and Bioinformatics 2013](https://doi.org/10.1109/TCBB.2013.68) | Stefan Kurtz (Universität Hamburg) | 标准 · 547 次 | 论文摘要：“In this paper, we present the GenomeTools, a convenient and efficient software library and associated software tools for developing bioinformatics software intended to create, process or convert annotation graphs.”；GitHub 最后提交 2026-11 |
| [EMBLmyGFF3](https://github.com/NBISweden/EMBLmyGFF3) | 备选 | 将 GFF3 与 FASTA 转换为用于 ENA 提交的 EMBL 平面文件格式。 | [BMC Research Notes 2018](https://doi.org/10.1186/s13104-018-3686-x) | Jacques Dainat (Uppsala University) | 小众 · 49 次 | 论文摘要：“Here we present EMBLmyGFF3, a robust universal converter from GFF3 format to EMBL format compatible with genome annotation submission to the European Nucleotide Archive.”；GitHub 最后提交 2025-07 |
| [table2asn](https://www.ncbi.nlm.nih.gov/genbank/table2asn/) | 备选 | NCBI 官方工具，将 GFF3/FASTA 转换为提交用的 ASN.1 格式并生成校验报告。 | 无文章 | — | 无论文 | 无摘要或仓库说明可引；见原文 |
| [GFF3toolkit](https://github.com/NAL-i5K/GFF3toolkit) | 备选 | i5k Workspace@NAL 开发的 GFF3 质控、修复与合并工具集。 | 无文章 | — | 无论文 | 仓库简介：“Python programs for processing GFF3 files”；GitHub 最后提交 2026-11 |
| [noodles](https://github.com/zaeleus/noodles) | 备选 | Rust 编写的生物信息学格式 I/O 库，包含 GFF3/GTF 读写模块。 | 无文章 | — | 无论文 | 仓库简介：“Bioinformatics I/O libraries in Rust”；GitHub 最后提交 2026-11 |
| [gxfkit](https://github.com/benngaihk/gxfkit) | 备选 | Rust 编写的 GFF3/GTF 转换工具，力求输出格式兼容 AGAT 且运行速度大幅提升。 | 无文章 | — | 无论文 | GitHub 最后提交 2026-07 |
| GTFtools | 备选 | 基于 GTF 计算基因模型特征（长度、内含子与 UTR 集合、异构体统计），用于生成发布汇总表。 | [Bioinformatics 2022](https://doi.org/10.1093/bioinformatics/btac561) | Hong‐Dong Li (Central South University) | 小众 · 33 次 | 论文摘要：“We introduce GTFtools, a stand-alone command-line software that provides a set of functions to calculate various gene features, including splice sites, independent introns, transcription start sites (TSS)-flanking regions, UTRs, isoform coordination and …” |
| [CrossMap](https://github.com/liguowang/CrossMap) | 备选 | 通过 chain 文件在不同组装版本间转换 GFF、BED、VCF 和 BAM 坐标，例如将坐标从 PN40024 v4 转换至 T2T。 | [Bioinformatics 2013](https://doi.org/10.1093/bioinformatics/btt730) | Jean‐Pierre Kocher (Mayo Clinic) +1 | 标准 · 829 次 | 论文摘要：“Here we developed CrossMap, a versatile and efficient tool for converting genome coordinates between assemblies.”；GitHub 最后提交 2026-07 |
| [GFF3sort](https://github.com/billzt/gff3sort) | 备选 | 对 GFF3 排序使父特征在子特征之前，便于 tabix 索引后上浏览器。 | [BMC Bioinformatics 2017](https://doi.org/10.1186/s12859-017-1930-3) | Sandui Guo (Chinese Academy of Agricultural Sciences) +1 | 小众 · 12 次 | 作者摘要原句：“Based on our test datasets from seven species, GFF3sort produced accurate sorting results with acceptable efficiency compared with currently available tools.”；GitHub 最后提交 2020-06 |
