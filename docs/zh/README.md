# 中文教学入口 — 基因**结构**注释

> 本目录用中文讲清「是什么、**为什么**、怎么选路、怎么验收」。  
> **真正跑命令、写 METHODS、工具安装**仍以英文文档为准（国际可引用）。

[English bilingual policy](../BILINGUAL.md) · [仓库首页](../../README.md)

---

## 完整课程（建议按序）

| 顺序 | 文档 | 你学到什么 |
|------|------|------------|
| 0 | [00_为什么要做结构注释.md](00_为什么要做结构注释.md) | **WHY**：结构作为一层；跳过的代价；预测≠注释；结构≠功能 |
| 1 | [01_什么是结构注释.md](01_什么是结构注释.md) | 结构 ≠ TE ≠ 功能；GFF 里有什么 |
| 2 | [02_TE与基因的关系.md](02_TE与基因的关系.md) | 为什么要 soft-mask；trusted lib |
| 3 | [03_怎么开始跑.md](03_怎么开始跑.md) | 三步上手 + flow 工具 |
| 4 | [04_分支怎么选.md](04_分支怎么选.md) | S11/S1/S2… 对照表 |
| 5 | [05_softmask与A0.md](05_softmask与A0.md) | soft vs hard；trusted vs working；A0/A0b |
| 6 | [06_质控课.md](06_质控课.md) | BUSCO/PSAURON/OMArk/AGAT；为何单靠 BUSCO 不够 |
| 7 | [07_S1精讲_BRAKER路线.md](07_S1精讲_BRAKER路线.md) | 默认草稿支逐步讲 |
| 8 | [08_S11精讲_liftover优先.md](08_S11精讲_liftover优先.md) | 近缘参考时先投影再补洞 |
| 9 | [09_S2_S3_S13_S14速览.md](09_S2_S3_S13_S14速览.md) | 其他草稿支一张课 |
| 10 | [10_合并与GSAman.md](10_合并与GSAman.md) | 合并、优先表、策展、S12 停手 |
| 11 | [11_验收L0L1L2.md](11_验收L0L1L2.md) | L0/L1/L2 门禁（指针到英文 EVALUATION） |
| 12 | [12_flow工具怎么用.md](12_flow工具怎么用.md) | answers → plan；print-first 边界 |
| 13 | [13_常见翻车.md](13_常见翻车.md) | Helixer 过召、hard-mask、假 curatedlib… |
| 14 | [14_为什么这样选证据.md](14_为什么这样选证据.md) | **WHY**：证据→方法；S11；StringTie；S13≠静默 S1 |
| 15 | [15_为什么质控是这些指标.md](15_为什么质控是这些指标.md) | **WHY**：BUSCO 盲区；谱系；PSAURON/OMArk；S12 |
| 16 | [16_为什么TE要trusted.md](16_为什么TE要trusted.md) | **WHY**：禁生 EDTA / cat+CD-HIT / hard-mask |
| 99 | [99_术语表.md](99_术语表.md) | GFF / BUSCO / soft-mask / curatedlib… |

> 课 00 / 14–16 是 **WHY 层**；课 01–13 正文里也有短 `## 为什么`（含反例）。操作与门禁仍以英文为准。

## 英文操作文档（跑起来时打开）

| 需要 | 打开 |
|------|------|
| 自动选路 + 逐步讲解 | [`../../pipeline/flow_tool/`](../../pipeline/flow_tool/) |
| 阶段输入/输出 | [`../STAGE_IO.md`](../STAGE_IO.md) |
| 合不合格 | [`../EVALUATION.md`](../EVALUATION.md) |
| 完整路线图 | [`../ROADMAP.md`](../ROADMAP.md) |
| 综述与证据选择 | [`../REVIEWS.md`](../REVIEWS.md) |
| TE 方案（英文） | [`../TE_LIBRARY.md`](../TE_LIBRARY.md) |
| 上手长文 | [`../QUICKSTART.md`](../QUICKSTART.md) |

## 一句话自测

> 这一步改的是**外显子坐标**，还是只改**蛋白的名字/GO**？  
> 改坐标 → 本仓库。改名字/GO → [功能注释仓](https://github.com/Xuzhen-Li/gene-function-annotation)。
