# 中文指针 — Trusted TE 路径

英文全文（借库 / 自建 + sha256 硬门）：[`../TRUSTED_TE_PATH.md`](../TRUSTED_TE_PATH.md)。  
课内先过 [05_softmask与A0.md](05_softmask与A0.md) 的 **Soft-mask Done when**；Wiki：[Soft-mask — Done when](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Soft-mask-TE#soft-mask--done-when-before-a0--run1)。

## 硬门（两条路共用）

**没有真 `sha256` 十六进制 → 禁止 A0。**  
占位 `YOUR_SHA256`、`<paste>`、`FILL`、空字段 **都不算** provenance。在导出 `CLEAN_TE_LIB` / 跑 RepeatMasker / 宣称 Gate soft-mask 之前：

```bash
sha256sum "$TRUSTED_TE_LIB"
# METHODS 写本文件算出的 64 位 hex — 不是模板词
```

## ① 近缘借库（不自建 panel 时优先）

- [ ] 供体库 **物种 / panel**：________________
- [ ] **来源 URL**（或公开仓+tag；METHODS 勿只写私有集群绝对路径）：________________
- [ ] **文件名**（精确）：________________
- [ ] **版本 / 日期**：________________
- [ ] **sha256**（对将 soft-mask 的那份 `sha256sum` 出的 64 hex）：________________
- [ ] 许可 / 引用 OK
- [ ] 仍用 RepeatMasker `-xsmall` soft-mask（勿 hard-mask 给 BRAKER/GALBA）

缺 `来源` / `文件名` / `版本` / **真 sha256** 任一项 → **禁止 A0**。

## ② 自建（按 TE_LIBRARY 层）

- [ ] 01 发现 → 02 working → 03 分类 → 04 门控 → 05 **trusted** 产品
- [ ] 对该 trusted 文件记录 **真 sha256** → METHODS

## 禁止当 A0 `-lib` / `--curatedlib`

生 EDTA / 整份 working / `cat`+CD-HIT 冒充 / TEsorter `all.cls.lib` / hard-mask 成 `N` / **无真 sha256**（含 `YOUR_SHA256`）。
