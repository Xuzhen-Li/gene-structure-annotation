# 第 19 章 常见问题与质控

## 19.1 仓库已列出的问题

来自主页“基因组之外还需要的数据”一节和 `docs/EVALUATION.md`。

- TE 库构建是 TE-Lib 的工作；本仓库只用可信库做 soft-mask。
- 功能标签（GO、KEGG、结构域、名称、NLR 和转录因子分类）属于 gene-function-annotation。蛋白工具说的 structure 通常指三维结构，不是基因模型。
- `grade=` 和 `status=` 是两个字段；临时版本不是 L1。
- 近缘参考指同种或同品种（或几乎相同的单倍型）且有你信任的人工 GFF，不是同科里随便一个 GFF。
- BUSCO 谱系要与类群匹配，并记录 odb10 还是 odb12（`docs/LINEAGES.md`）。compleasm 是有用的对照，不能自动替代 BUSCO。
- BUSCO 重复率高可能是真实单倍型（S9）；不要只为降低重复率去掉单倍型。
- TSEBRA 后基因数骤降时，先做 A5d 单外显子与多外显子比例检查，再接受合并结果。

## 19.2 文献中的问题

- **嵌合基因。** 相邻基因被合成一个模型，在植物注释中常见，并因后续工作沿用而持续存在；Helixer 等机器学习预测有助于发现（[doi:10.1186/s12864-025-11765-w](https://doi.org/10.1186/s12864-025-11765-w)）。
- **只靠 RNA 不够。** 仅由 RNA 比对得到的转录本不够，应结合证据预测与从头预测（[doi:10.1002/aps3.11533](https://doi.org/10.1002/aps3.11533)）。
- **异构体难。** 外显子找得准，完整异构体仍难（[doi:10.1038/nmeth.2714](https://doi.org/10.1038/nmeth.2714)）；长读长发现转录本时，读长和准确度比深度更重要（[doi:10.1038/s41592-024-02298-3](https://doi.org/10.1038/s41592-024-02298-3)）。
- **小 RNA。** 许多植物 miRNA 注释可疑，原因是把 siRNA 当成了 miRNA；新标准要求重复实验和小 RNA 测序（[doi:10.1105/tpc.17.00851](https://doi.org/10.1105/tpc.17.00851)）。
- **下游影响。** 不同注释来源给出的直系同源结果明显不同（[doi:10.1093/bioinformatics/btaf365](https://doi.org/10.1093/bioinformatics/btaf365)），所以要在 METHODS 中写明注释来源和版本。
- **重复的单倍型片段。** 杂合区域可能被组装两次，破坏连续性并干扰注释（[doi:10.1093/bioinformatics/btaa025](https://doi.org/10.1093/bioinformatics/btaa025)）；应在组装质控阶段处理，而不是删基因。

## 19.3 质控清单

| 检查 | 工具 | 出问题的表现 | 出处 |
|---|---|---|---|
| 注释前的基因组完整度 | BUSCO 基因组模式、compleasm | 缺失多：先修组装 | [doi:10.1093/molbev/msab199](https://doi.org/10.1093/molbev/msab199)、[doi:10.1093/bioinformatics/btad595](https://doi.org/10.1093/bioinformatics/btad595) |
| 蛋白组完整度 | BUSCO 蛋白模式 | 低于基因组模式：有基因漏掉 | [doi:10.1093/molbev/msab199](https://doi.org/10.1093/molbev/msab199) |
| 一致性与污染 | OMArk | 大量蛋白与谱系不一致，或出现污染物种 | [doi:10.1038/s41587-024-02147-w](https://doi.org/10.1038/s41587-024-02147-w) |
| 单个蛋白可信度 | PSAURON | 低分提示可疑蛋白 | [doi:10.1093/nargab/lqae189](https://doi.org/10.1093/nargab/lqae189) |
| 结构计数 | AGAT、gffread | 基因、mRNA、CDS 数与近缘物种差距大；GFF3 不合法 | [doi:10.12688/f1000research.23297.2](https://doi.org/10.12688/f1000research.23297.2)；AGAT [doi:10.5281/zenodo.3552717](https://doi.org/10.5281/zenodo.3552717) |
| 单外显子与多外显子比例 | A5d 阶段计数 | 合并后突变 | [doi:10.1002/aps3.11533](https://doi.org/10.1002/aps3.11533)；`docs/TOOLS.md` |
| 难点位点目视检查 | JBrowse 2、GSAman、Apollo 3 | 对照 RNA 和蛋白轨道发现合并或拆分错误 | [doi:10.1186/s13059-023-02914-z](https://doi.org/10.1186/s13059-023-02914-z)、[doi:10.1016/j.xinn.2026.101471](https://doi.org/10.1016/j.xinn.2026.101471) |

验收等级和门槛见 [`docs/EVALUATION.md`](../../docs/EVALUATION.md) 和 [`docs/EVALUATION_CHECKLIST.md`](../../docs/EVALUATION_CHECKLIST.md)。
