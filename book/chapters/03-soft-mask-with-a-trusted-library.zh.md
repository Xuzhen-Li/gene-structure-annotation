# 第 3 章 用可信库做 soft-mask

*本章收录[主页第 2 节](../../README.zh.md#section-2)：该节说明、含论文、实验室、权威度和评价的完整工具表，以及评测要点。链接指回仓库。*

利用可信 TE 库屏蔽重复序列，或屏蔽低复杂度序列。本库不负责构建 TE 库。

**需要：** 一份可信的 TE 库（来自 vitis-te 或其他审定库）。本节仅做 soft-mask，不构建 TE 库。[按场景列出的数据需求](../../README.zh.md#data-needs)

**分组：**
- *库与屏蔽程序*（互补）：Dfam、RepeatMasker。默认 A0：用 RepeatMasker 跑 vitis-te 的库（已知家族由 Dfam 补充）。
- *串联与卫星重复*（互补）：Tandem Repeats Finder (TRF)、ULTRA、TRASH。存在着丝粒或长卫星重复时并入屏蔽结果；TRASH 还能对着丝粒阵列进行分类。
- *无库屏蔽与建库（仅作对照）*（可替代）：WindowMasker、Red、Earl Grey。WindowMasker 和 Red 不用库直接屏蔽；Earl Grey 会自建库再屏蔽。三者都只用于和 A0 的屏蔽结果比较，在默认路径上不能替代 vitis-te 的库。


| 工具 | 角色 | 用途 / 何时用 | 原始论文 | 实验室（通讯作者，机构） | 权威度（档位 · 被引） | 评价（出处） |
|---|---|---|---|---|---|---|
| [RepeatMasker](https://github.com/Dfam-consortium/RepeatMasker) | 默认（A0） | 利用给定的重复序列库（Dfam 或经审定的物种专有库）屏蔽重复序列；`-xsmall` 参数输出 soft-masking 结果。 | 无文章 | — | 无论文 | 仓库简介：“RepeatMasker is a program that screens DNA sequences for interspersed repeats and low complexity DNA sequences.”；GitHub 最后提交 2026-10 |
| [Dfam](https://www.dfam.org/) | 资源 | RepeatMasker 所用的转座子（TE）家族与隐马尔可夫模型（profile HMM）公开数据库。 | [Mobile DNA 2021](https://doi.org/10.1186/s13100-020-00230-y) | Jessica M. Storer (Institute for Systems Biology) +2 | 标准 · 838 次 | 作者摘要原句：“This expansion demonstrates the utility of many of Dfam's new features and provides insight into the long term challenges ahead for improving de novo generated transposable element datasets.” |
| [Tandem Repeats Finder (TRF)](https://github.com/Benson-Genomics-Lab/TRF) | 备选 | 检测串联重复序列。 | [Nucleic Acids Research 1999](https://doi.org/10.1093/nar/27.2.573) | Gary Benson (Icahn School of Medicine at Mount Sinai) | 标准 · 10371 次 | 论文摘要：“In this paper, we present a new algorithm for finding tandem repeats which works without the need to specify either the pattern or pattern size.”；GitHub 最后提交 2023-01 |
| [WindowMasker](https://www.ncbi.nlm.nih.gov/IEB/ToolBox/CPP_DOC/lxr/source/src/app/winmasker/) | 备选 | 无需重复序列库，直接基于高频 k-mer 做序列屏蔽的工具（NCBI）。 | [Bioinformatics 2005](https://doi.org/10.1093/bioinformatics/bti774) | Richa Agarwala (National Institutes of Health) | 成熟 · 354 次 | 无摘要或仓库说明可引；见原文 |
| [ULTRA](https://github.com/TravisWheelerLab/ULTRA) | 备选 | 对串联重复与低复杂度重复做概率标注；输出结果可配合可信 TE 库用于 soft-masking。 | [Bioinformatics Advances 2024](https://doi.org/10.1093/bioadv/vbae149) | Daniel R. Olson (University of Montana) | 较新 · 20 次 | 作者摘要原句：“Tools that annotate repetitive sequence are now more important than ever, so that we can better understand newly uncovered repetitive sequences, and also so that we can mitigate errors in bioinformatic software caused by those repetitive sequences.”；GitHub 最后提交 2026-11 |
| Red | 备选 | 不依赖重复库的从头重复序列检测工具，尚无可信 TE 库时可快速生成 soft-mask。仅作为对照轨道与 vitis-te 库比较。 | [BMC Bioinformatics 2015](https://doi.org/10.1186/s12859-015-0654-5) | Hani Z. Girgis (National Institutes of Health) | 成熟 · 275 次 | 作者摘要原句：“It is sensitive to both transposons and simple repeats; in contrast, available tools such as RepeatScout and ReCon are sensitive to transposons, and WindowMasker to simple repeats.” |
| [TRASH](https://github.com/vlothec/TRASH) | 备选 | 识别并分类串联重复与卫星重复阵列（如着丝粒重复）；可在基因预测前用来屏蔽或标记 T2T 组装的着丝粒。 | [Bioinformatics 2023](https://doi.org/10.1093/bioinformatics/btad308) | Ian R. Henderson (University of Cambridge) | 成熟 · 115 次 | 作者摘要原句：“TRASH analyses a fasta assembly file, identifies regions occupied by repeats and then precisely maps them and their higher order structures.”；GitHub 最后提交 2025-03 |
| [Earl Grey](https://github.com/TobyBaril/EarlGrey) | 备选 | 封装 RepeatModeler2 和 RepeatMasker 的自动化 TE 注释流程。建库工作归属 vitis-te，此处收录仅用于对比屏蔽结果。 | [Molecular Biology and Evolution 2024](https://doi.org/10.1093/molbev/msae068) | Tobias Baril (University of Exeter) +1 | 成熟 · 292 次 | 作者摘要原句：“Using nine simulated genomes and an annotation of Drosophila melanogaster, we show that Earl Grey outperforms current widely used TE annotation methodologies in ameliorating the issues mentioned above while scoring highly in benchmarking for TE annotation and …”；GitHub 最后提交 2026-11 |
| [RepeatModeler2](https://github.com/Dfam-consortium/RepeatModeler) | 备选 | 为新基因组从头构建重复序列库；RepeatMasker 所用的库通常来自它。 | [Proceedings of the National Academy of Sciences 2020](https://doi.org/10.1073/pnas.1921046117) | Arian F. A. Smit (Institute for Systems Biology) | 标准 · 4333 次 | 作者摘要原句：“This program brings substantial improvements over the original version of RepeatModeler, one of the most widely used tools for TE discovery.”；GitHub 最后提交 2026-11 |
| [EDTA](https://github.com/oushujun/EDTA) | 备选 | 整合 LTR、TIR、Helitron 等检测器并过滤去冗余，得到 TE 库；植物基因组 soft-mask 常用的库来源。 | [Genome biology 2019](https://doi.org/10.1186/s13059-019-1905-y) | Ning Jiang (Michigan State University) +2 | 标准 · 1683 次 | GitHub 最后提交 2026-11 |
| [BEDTools (maskfasta)](https://github.com/arq5x/bedtools2) | 备选，通用工具 | 通用区间工具集；maskfasta -soft 可把重复 BED/GFF 转成 soft-mask 的 FASTA。 | [Bioinformatics 2010](https://doi.org/10.1093/bioinformatics/btq033) | Aaron R. Quinlan (University of Virginia) +1 | 标准 · 30267 次 | GitHub 最后提交 2026-06 |
