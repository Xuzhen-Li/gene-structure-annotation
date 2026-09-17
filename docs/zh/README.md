# 中文教学入口 — 基因**结构**注释

> 中文讲清「是什么、为什么、怎么选路、怎么验收」。  
> **跑命令、写 METHODS、装工具**用英文文档（国际可引用）。

[English bilingual policy](../BILINGUAL.md) · [仓库首页](../../README.md)

![结构注释总览](../figures/structure_overview.png)

读图：本仓主线是 **genome → A0 → 一主草稿支 → GFF/蛋白**；TE trusted 是**前置地板**；功能在隔壁。选支一眼见图内 S11 vs S1；课堂换作物另见图 [`plant_sim_three_lines.png`](../figures/plant_sim_three_lines.png)。

英文 Start here：[`../START_HERE.md`](../START_HERE.md)

---

## 今天最短路径（先做这个）

**前提：** 组装已完成 → `ASSEMBLY_OK=yes`（Asm0 是清单，勿重装）。[FAQ](FAQ_入门.md)

| 步 | 打开 | 做什么 |
|----|------|--------|
| 1 | [01_什么是结构注释.md](01_什么是结构注释.md) | 找外显子，不是做 GO |
| 2 | [03_怎么开始跑.md](03_怎么开始跑.md) | `answers` → `flow.py` → `my_plan.md` |
| 3 | 填 [`../../config/example.env`](../../config/example.env) → `local.env` | 列将需要的路径；**无集群可停在「读懂 plan + 路径清单」**（勿以为今晚必须跑完 BRAKER） |
| 3b（有集群） | 按 plan `RUN=1` 执行助手 | 默认 **S1**；近缘好 GFF → **S11** |
| 4 | [**验收勾选表**](验收勾选表.md) | 认清目标 **L1**（档位认知；≠今晚必交满勾） |

**课堂最低（今晚可交）：** 读懂 plan 主草稿支 + 填好/列清 local.env 键 + 能解释勾选表在考什么。
**上集群前：** 未勾 [Done when](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Start-tonight#done-when) / `print_qc` 未绿（仍有 `[STOP]`）= **不许** `RUN=1`。

**放行交接（A6）：** 功能仓 `PROTEINS_FA` 指 `release/<TAG>/proteins.faa`（稳定别名），不要默认用 `WORK_DIR/proteins.faa` 可能过期的根副本。

<details>
<summary>卡住再查 / 可选练习（默认折叠）</summary>

- [FAQ](FAQ_入门.md) · [04 分支](04_分支怎么选.md) · [13 翻车](13_常见翻车.md) · [术语](99_术语表.md)
- 可选：[植物三种模拟](植物三种模拟.md)（葡萄抗病开 `plant_tandem_focus`）
- TE：**trusted** 库 soft-mask（小写，不是 N）；深课 [18](18_TE流程课_借鉴实验室03_TE.md)；EDTA 工具页事后再开
- 打印 QC：`python3 pipeline/print_qc_commands.py`（先 `source config/local.env`）
- 英文：[`flow_tool/`](../../pipeline/flow_tool/) · [`EVALUATION.md`](../EVALUATION.md)

</details>

---

## 完整课程（想系统学再按序）

| 顺序 | 文档 | 你学到什么 |
|------|------|------------|
| 0 | [00_为什么要做结构注释.md](00_为什么要做结构注释.md) | **WHY**：结构作为一层；跳过的代价 |
| 1 | [01_什么是结构注释.md](01_什么是结构注释.md) | 结构 ≠ TE ≠ 功能；GFF 里有什么 |
| 2 | [02_TE与基因的关系.md](02_TE与基因的关系.md) | 为什么要 soft-mask；trusted lib |
| 3 | [03_怎么开始跑.md](03_怎么开始跑.md) | 三步上手 + flow 工具 |
| 4 | [04_分支怎么选.md](04_分支怎么选.md) | S11/S1/S2… 对照表 |
| 5 | [05_softmask与A0.md](05_softmask与A0.md) | soft vs hard；trusted vs working |
| 6 | [06_质控课.md](06_质控课.md) | BUSCO/PSAURON/OMArk/AGAT |
| 7 | [07_S1精讲_BRAKER路线.md](07_S1精讲_BRAKER路线.md) | 默认草稿支 |
| 8 | [08_S11精讲_liftover优先.md](08_S11精讲_liftover优先.md) | 近缘参考时先投影 |
| 9 | [09_S2_S3_S13_S14速览.md](09_S2_S3_S13_S14速览.md) | 其他草稿支 |
| 10 | [10_合并与GSAman.md](10_合并与GSAman.md) | 合并、策展、停手 |
| 11 | [11_验收L0L1L2.md](11_验收L0L1L2.md) | L0/L1/L2 |
| 12 | [12_flow工具怎么用.md](12_flow工具怎么用.md) | answers → plan |
| 13 | [13_常见翻车.md](13_常见翻车.md) | 翻车清单 |
| 14–16 | [14](14_为什么这样选证据.md) · [15](15_为什么质控是这些指标.md) · [16](16_为什么TE要trusted.md) | WHY 深课 |
| 17 | [外部教程与会议](17_外部教程与会议.md) | Galaxy / 会议 |
| 18 | [TE流程课](18_TE流程课_借鉴实验室03_TE.md) | 四层产品·漏斗（TE 专题） |
| 99 | [99_术语表.md](99_术语表.md) | 术语 |

> 课 00 / 14–16 是 **WHY 层**。操作与门禁仍以英文为准。


## 英文助手中文指针（3–5 行）

| 指针 | 对应英文 |
|------|----------|
| [TRUSTED_TE_PATH.md](TRUSTED_TE_PATH.md) | trusted TE 借库/自建清单 |
| [LINEAGES.md](LINEAGES.md) | BUSCO/Compleasm 谱系名 |
| [A2e_s11_gapfill.md](A2e_s11_gapfill.md) | S11 补洞 |
| [golden_pack.md](golden_pack.md) | 放行包 EXAMPLE 目录 |
| [PROVISIONAL_NOT_L1.md](PROVISIONAL_NOT_L1.md) | 临时稿 ≠ L1（Liftoff/Helixer） |
| [COMPARE_HELIXER_BRAKER.md](COMPARE_HELIXER_BRAKER.md) | Helixer↔BRAKER 对照课 |
| [MERGE_AND_ENTRIES.md](MERGE_AND_ENTRIES.md) | 三种入口 + 合并 QC（无 Snakemake） |
| [EGAPX_COMPARE.md](EGAPX_COMPARE.md) | EGAPx / S8 对照与提交门（非默认） |

英文一页路径：[`../POST_ASSEMBLY.md`](../POST_ASSEMBLY.md)。

## 一句话自测

> 这一步改的是**外显子坐标**，还是只改**蛋白的名字/GO**？  
> 改坐标 → 本仓库。改名字/GO → [功能注释仓](https://github.com/Xuzhen-Li/gene-function-annotation)。
