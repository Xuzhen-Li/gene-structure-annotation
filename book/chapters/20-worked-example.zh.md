# 第 20 章 实例：葡萄基因组走 S1 路线

本章按 [`examples/plant_sim/01_vitis_s1_s7/plan.md`](../../examples/plant_sim/01_vitis_s1_s7/plan.md) 的教学计划走一遍。基因组是模拟的（Vitis_vinifera_sim），重点是决策顺序，不是真实数字。计划由 `pipeline/flow_tool/flow.py` 生成。

## 20.1 路线选择

回答是：有 RNA 和蛋白，没有近缘人工注释，没有深度 Iso-Seq，不做 GPU 对比，也不用 EVM 组合，项目关注串联抗病基因窗口。于是流程工具选 S1 为主草稿，加上 S7 叠加层处理串联和抗病窗口，目标等级 L1。这与第 18 章一致：没有近缘参考时，用 RNA 加蛋白的 BRAKER 是默认（[doi:10.1101/gr.278090.123](https://doi.org/10.1101/gr.278090.123)）。

## 20.2 各阶段

| 序号 | 阶段 | 工具 | 要记录什么 | 为什么 |
|---|---|---|---|---|
| 1 | Asm0 组装或接收现成 FASTA | hifiasm 或给定基因组 | 来源、版本、倍性、稳定的序列名 | 后续步骤依赖稳定的序列名 |
| 2 | Asm1 组装质控 | BUSCO 基因组模式、seqkit | 谱系名（viridiplantae_odb12）、ASSEMBLY_OK | 谱系须与类群匹配（`docs/LINEAGES.md`） |
| 3 | A0 soft-mask | RepeatMasker -xsmall 加可信库 | 库版本和 sha256 | 只做 soft-mask；屏蔽比例不是基因组 TE%（第 1.4 节） |
| 4 | A1b RNA 比对 | HISAT2 或 STAR；长读长用 minimap2 | 链特异 BAM | 作为 BRAKER 和 StringTie 的证据 |
| 5 | S1 草稿 | BRAKER4/3，StringTie 加 TransDecoder 作对照轨道 | DRAFT_GFF 和对照轨道 | 对照不是给 EVM 的第二套基因 |
| 6 | 跳过 A4 合并 | 无 | MERGED_GFF 设为 DRAFT_GFF | 只有一套主草稿时不需要 EVM 或 TSEBRA |
| 7 | A5 计数 | AGAT | 基因、mRNA、CDS 数 | 与近缘物种比较 |
| 8 | A3 提取蛋白 | gffread 或 AGAT | 每个基因一条代表蛋白及异构体规则 | 用于质控和功能仓库 |
| 9 | 质控 | BUSCO 蛋白模式、PSAURON；L2 时加 OMArk | C/D/F/M 与谱系；PSAURON 表 | 完整度和可疑蛋白筛查（[doi:10.1093/nargab/lqae189](https://doi.org/10.1093/nargab/lqae189)） |
| 10 至 12 | S7 叠加层 | families.tsv、`pipeline/02_priority_loci.py --families`、GSAman | 优先级表；人工校对窗口 | 串联 NLR 和 QTL 窗口需要人工校对（[doi:10.1016/j.xinn.2026.101471](https://doi.org/10.1016/j.xinn.2026.101471)） |
| 13 | 发布 | gffread 校验、发布目录、METHODS | 发布标签和质控快照 | 门槛见 `docs/EVALUATION.md` |
| 14 | A6 交接 | gene-function-annotation，F1 框架 | RELEASE_TAG 和蛋白 | 功能标签在姊妹仓库中添加 |

## 20.3 要点

- 路线由数据决定，每个叠加层都写在主路线旁边。
- 对照轨道（这里是 StringTie）用于检查，不悄悄合并。
- 人工校对只做对项目重要的窗口；其余可以保持草稿，但要在 METHODS 中写明。
- T2T 葡萄基因组的真实案例见 [`docs/cases/vitis-t2t-s1-s5.md`](../../docs/cases/vitis-t2t-s1-s5.md)。
