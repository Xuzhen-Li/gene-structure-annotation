# 为什么 TE 库必须是 trusted？

> WHY 深课。操作见 [02](02_TE与基因的关系.md) · [05](05_softmask与A0.md)；英文 [`../TE_LIBRARY.md`](../TE_LIBRARY.md)。

## 1. Soft-mask 信任的是「库」，不是「有个 FASTA」

RepeatMasker `--curatedlib` / `-lib` 会把库里的序列当作**高信任重复**来 mask。  
若库里混进宿主基因片段、未知垃圾、或未门控的 ORF：

- **基因 wipe：** 真基因（尤其嵌在重复区的 NLR 等）被当成 TE → soft-mask 后预测器绕开或截断；  
- **TE inflation：** 库太松 → 假基因仍在，基因数爆炸。

所以本仓只认 **trusted curatedlib** 当 soft-mask 金标准。

## 2. 为什么不能用生 EDTA 整锅端？

EDTA 等自动化流水线产出的粗库含大量 unknowns / 片段，**未经「这不是宿主基因」的门控**。  
整份当 `--curatedlib` → 把不确定性抬成 100% 信任。  
EVALUATION：**自动不合格**。

**反例：** 「EDTA 跑完就 soft-mask」→ 宿主抗病基因成片消失，BUSCO 却可能还行。

## 3. 为什么 `cat` + CD-HIT ≠ curatedlib？

多个 haplotype / 样本的 TElib 拼起来再去重，只是 **dedup**。  
去重不回答：「这条共识序列是不是宿主 CDS？」  
Ou panEDTA / 实验室红线：**禁止**幼稚 concatenate 冒充 curated。

口诀：**Dedup ≠ curation。**

**反例：** 四套 haplotype TElib `cat | cd-hit` 写进 METHODS 当「我们的 curated TE library」。

## 4. 为什么禁止 hard-mask 喂 BRAKER/GALBA？

Hard-mask 把重复区改成 `N` — **序列没了**。  
嵌在重复景观里的真基因无法被正确跨越；部分家族系统性受损。  
本 playbook：ab initio / 证据训练路径只用 **`-xsmall` soft-mask**。

**反例：** 为「让预测器干净一点」先 hard-mask，再抱怨 NLR 注释差。

## 5. Working lib 为什么只能当档案？

| 产品 | 角色 |
|------|------|
| Working（TEtrimmer+CD-HIT 等） | 敏感工作集 / 后续人工门控的原料 |
| Family catalog | 目录与命名 |
| **Trusted curatedlib** | **唯一** soft-mask / curatedlib 金标准 |
| panEDTA combine | 泛基因组 TE **轨道**，不是 `cat` 替代品 |

基因数因 TE 爆炸 → 叠加支 **S10**（回炉 remask），不是改用更松的库「多找回基因」。

## 挂钩

地板课 → [05](05_softmask与A0.md)  
翻车清单 → [13](13_常见翻车.md)  
英文四层产品 → [`../TE_LIBRARY.md`](../TE_LIBRARY.md)

下一课建议回到主干 [06](06_质控课.md)，或查术语 [99](99_术语表.md)。
