# 中文教学入口 — 基因**结构**注释

> 本目录用中文讲清「是什么、为什么、怎么选路」。  
> **真正跑命令、写 METHODS、工具安装**仍以英文文档为准（国际可引用）。

[English bilingual policy](../BILINGUAL.md) · [仓库首页](../../README.md)

---

## 先建立直觉（建议按序读）

| 顺序 | 文档 | 你学到什么 |
|------|------|------------|
| 1 | [01_什么是结构注释.md](01_什么是结构注释.md) | 结构 ≠ TE ≠ 功能；GFF 里有什么 |
| 2 | [02_TE与基因的关系.md](02_TE与基因的关系.md) | 为什么要 soft-mask；trusted lib |
| 3 | [03_怎么开始跑.md](03_怎么开始跑.md) | 三步上手 + flow 工具 |
| 4 | [04_分支怎么选.md](04_分支怎么选.md) | S11/S1/S2… 对照表 |

## 英文操作文档（跑起来时打开）

| 需要 | 打开 |
|------|------|
| 自动选路 + 逐步讲解 | [`../../pipeline/flow_tool/`](../../pipeline/flow_tool/) |
| 阶段输入/输出 | [`../STAGE_IO.md`](../STAGE_IO.md) |
| 合不合格 | [`../EVALUATION.md`](../EVALUATION.md) |
| 完整路线图 | [`../ROADMAP.md`](../ROADMAP.md) |
| TE 方案（英文） | [`../TE_LIBRARY.md`](../TE_LIBRARY.md) |

## 一句话自测

> 这一步改的是**外显子坐标**，还是只改**蛋白的名字/GO**？  
> 改坐标 → 本仓库。改名字/GO → [功能注释仓](https://github.com/Xuzhen-Li/gene-function-annotation)。
