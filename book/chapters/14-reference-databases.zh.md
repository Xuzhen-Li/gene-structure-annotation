# 第 14 章 参考数据库

*本章收录[主页第 13 节](../../README.zh.md#section-13)：该节说明、含论文、实验室、权威度和评价的完整工具表，以及评测要点。链接指回仓库。*

用作证据或近缘 GFF 的参考基因组与注释库。

**需要：** 无需额外测序——这里收录的是用作证据或近缘 GFF 的参考基因组与注释。请核对所用版本是否与 METHODS 中记录的一致。[按场景列出的数据需求](../../README.zh.md#data-needs)

**分组：**
- *蛋白证据集*（互补）：OrthoDB v12、UniProt 2025。BRAKER3/BRAKER4 的标准蛋白集是 OrthoDB 的绿色植物分区；GALBA2 则要用一到数个近缘物种的蛋白组；需要小而干净的集合时加 Swiss-Prot。
- *比较用基因集*（互补）：Phytozome、Ensembl Plants (Ensembl Genomes 2022)、PLAZA 5.0、NCBI RefSeq、Araport11、PN40024 reference annotation (PN_T2T / v5)。用于同近缘物种及葡萄参考基因组对比基因数量与结构。
- *ncRNA 参考*（互补）：Rfam 15、RNAcentral。Infernal 搜索使用 Rfam 模型；命中结果的命名使用 RNAcentral。


| 工具 | 角色 | 用途 / 何时用 | 原始论文 | 实验室（通讯作者，机构） | 权威度（档位 · 被引） | 评价（出处） |
|---|---|---|---|---|---|---|
| [RNAcentral](https://rnacentral.org/) | 资源 | 综合性的非编码 RNA 序列数据库。 | [Nucleic Acids Research 2020](https://doi.org/10.1093/nar/gkaa921) | Zasha Weinberg | 成熟 · 441 次 | 无摘要或仓库说明可引；见原文 |
| [Phytozome](https://phytozome-next.jgi.doe.gov/) | 资源 | JGI 维护的植物基因组与注释门户数据库。 | [Nucleic Acids Research 2011](https://doi.org/10.1093/nar/gkr944) | David M. Goodstein (Joint Genome Institute) | 标准 · 6177 次 | 无摘要或仓库说明可引；见原文 |
| [Ensembl Plants (Ensembl Genomes 2022)](https://plants.ensembl.org/) | 资源 | 收录植物基因组、基因模型与比较基因组学数据的综合数据库。 | [Nucleic Acids Research 2021](https://doi.org/10.1093/nar/gkab1007) | Andrew D. Yates (European Bioinformatics Institute) | 成熟 · 498 次 | 作者摘要原句：“Here, we present our largest increase in plant, metazoan and fungal genomes since the project's inception creating one of the world's most comprehensive genomic resources and describe our efforts to reduce genome redundancy in our Bacteria portal.” |
| [Araport11](https://www.arabidopsis.org/) | 资源 | 拟南芥 Col-0 基因组的重注释参考版本。 | [The Plant Journal 2017](https://doi.org/10.1111/tpj.13415) | Christopher D. Town (J. Craig Venter Institute) | 标准 · 1521 次 | 无摘要或仓库说明可引；见原文 |
| [Rfam 15](https://rfam.org) | 资源 | RNA 家族协方差模型数据库；可配合 Infernal cmscan 扫描 rRNA、snoRNA 与核糖体开关（riboswitch）等位点。 | [Nucleic Acids Research 2024](https://doi.org/10.1093/nar/gkae1023) | Blake Sweeney (European Bioinformatics Institute) | 成熟 · 279 次 | 作者摘要原句：“This paper introduces major improvements, including the expansion of Rfamseq to 26 106 genomes, a 76% increase, incorporating the latest UniProt reference proteomes and additional viral genomes.” |
| [OrthoDB v12](https://www.orthodb.org/) | 资源 | 直系同源目录，其绿色植物蛋白分区是 BRAKER3/BRAKER4 的标准蛋白证据（GALBA/GALBA2 则应使用一到数个近缘物种的蛋白组）；同一次更新也刷新了 BUSCO 谱系。 | [Nucleic Acids Research 2024](https://doi.org/10.1093/nar/gkae987) | Evgeny M. Zdobnov (University of Geneva) +1 | 标准 · 592 次 | 无摘要或仓库说明可引；见原文 |
| [UniProt 2025](https://www.uniprot.org/) | 资源 | 经人工审校的 Swiss-Prot 植物蛋白集，可为蛋白提示和 GeneValidator 质控提供精简干净的证据。 | [Nucleic Acids Research 2024](https://doi.org/10.1093/nar/gkae1010) | Jian Zhang | 标准 · 3617 次 | 论文摘要：“In this publication, we describe ongoing changes to our production pipeline to limit the sequences available in UniProtKB to high-quality, non-redundant reference proteomes.” |
| [PLAZA 5.0](https://bioinformatics.psb.ugent.be/plaza/) | 资源 | 植物比较基因组学平台，提供基因家族与共线性信息；适合跨物种核对基因数量及错误拆分或合并的模型。 | [Nucleic Acids Research 2021](https://doi.org/10.1093/nar/gkab1024) | Klaas Vandepoele (Ghent University) | 成熟 · 281 次 | 作者摘要原句：“This latest release also comes with a set of new and updated features: a new BED import functionality for the workbench, improved interactive visualizations for functional enrichments and genome-wide mapping of gene sets, and a fully redesigned and extended …” |
| [NCBI RefSeq](https://www.ncbi.nlm.nih.gov/refseq/) | 资源 | 经审校的转录本与蛋白集及 Gnomon 预测结果；运行 S8 EGAPx 路线时作为对照数据集。 | [Nucleic Acids Research 2015](https://doi.org/10.1093/nar/gkv1189) | Kim D. Pruitt (National Institutes of Health) | 标准 · 7254 次 | 作者摘要原句：“This paper summarizes the current status of the viral, prokaryotic, and eukaryotic branches of the RefSeq project, reports on improvements to data access and details efforts to further expand the taxonomic representation of the collection.” |
| [PN40024 reference annotation (PN_T2T / v5)](https://grapedia.org/) | 资源 | 葡萄 PN_T2T（v5）现行参考基因集，并含早期 v4（doi:10.1093/g3journal/jkad067）及 12X.v2 上的 VCost.v3（doi:10.1016/j.gdata.2017.09.002）；是所有新葡萄属注释的对照集。 | [Horticulture Research 2023](https://doi.org/10.1093/hr/uhad061) | Camille Rustenholz (Institut National de Recherche pour l'Agriculture, l'Alimentation et l'Environnement) +3 | 成熟 · 294 次 | 作者摘要原句：“Even though PN40024 derives from nine generations of selfing, we still found nine genomic hotspots of heterozygous sites associated with biological processes, such as the oxidation-reduction process and protein phosphorylation.” |
| [Gramene 2021](https://www.gramene.org/) | 备选 | 与 Ensembl Plants 整合的植物比较基因组与通路门户。 | [Nucleic Acids Research 2020](https://doi.org/10.1093/nar/gkaa979) | Doreen Ware (Agricultural Research Service) | 成熟 · 136 次 | 无摘要或仓库说明可引；见原文 |
