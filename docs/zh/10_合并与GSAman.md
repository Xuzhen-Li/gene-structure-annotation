# 合并、优先表、GSAman 与 S12 停手

英文：[`../STAGE_IO.md`](../STAGE_IO.md) · [`../ERROR_CLASSES.md`](../ERROR_CLASSES.md) · EVALUATION「Stop rules」

## 为什么

1. 多套草稿坐标会打架 — 无合并权重就**不可复现**。  
2. 坏父本权重过高会污染终稿；AGAT 计数是第一道 sanity。  
3. 蛋白不同步 = 用旧序列做 BUSCO/FA。  
4. 优先表把有限人工对准**最差点**（碎裂/融合/剪接/串联）。  
5. **S12** 防止无限打磨成为不交付。

**反例：** 合并后基因数翻倍却不查父本，仍写 L1。
## 合并（A4）在解决什么

多套草稿（BRAKER + GeMoMa、lift + de novo、StringTie ORF…）坐标会打架。合并器（EVM / TSEBRA / Mikado 等）按**权重**挑一套共识。

教学要求：

1. 合并前后都跑 **AGAT counts**，数量应合理，不是爆炸。
2. **权重路径写入 METHODS** — 否则不可复现。
3. 合并不是「平均一下就科学」；坏父本权重过高会污染终稿。

## 蛋白必须从本轮 GFF 重抽（A3 / G5）

功能注释和蛋白 BUSCO 看的是**序列**。若 `proteins.faa` 还是上一轮 curation 前的，你在给幽灵注释做 QC。  
Isoform 政策写死：一基因一代表，或明确保留多 isoform（并告诉 FA 仓）。

## 优先表（02）

```text
PSAURON 低分
  + BUSCO 碎裂直系同源
  + 串联阵列邻域
        ↓
   PRIORITY_TSV
        ↓
   GSAman / 浏览器逐窗看
```

四种结构错误标签（GSAman 用语）：**碎裂 / 邻位融合 / 外显子·剪接错 / 串联塌缩**。  
植物免疫、次生代谢阵列（NLR、stilbene…）是高发区 — 适用时构成 G9 门槛。

## GSAman（04）深度看目标

| 目标 | 人工深度 |
|------|----------|
| L1 合格 | 优先表清空或**显式暂缓**写进 METHODS |
| L2 / S5 | 第二轮 curation + OMArk 旗标窗口 |

「看过但决定暂缓」合法；「假装没看见」不合法。

## S12 — 什么时候停手

满足任一即可冻结当前等级放行：

1. 优先表在你声明的阈值下已空  
2. 一整轮 curation 后蛋白 BUSCO-C **几乎不动**  
3. 剩下只是剪接位点口味分歧（组合器之间常见）  
4. 在追 <0.1% BUSCO

METHODS 写一句冻结理由。无限打磨不是交付标准。

下一页：[11_验收L0L1L2.md](11_验收L0L1L2.md)
