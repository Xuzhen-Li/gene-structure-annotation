# 入门 FAQ（稍有基础、第一次跟最短路径）

配合 [README 今天最短路径](README.md)。英文细则仍以 `docs/EVALUATION.md` / `docs/tools/` 为准。

---

## TE / soft-mask

**Q：A0 打印的 softmasked_fraction 是不是基因组 TE%？**  
A：**不是。** 那是「相对**这份 trusted 库**被打成小写的碱基比例」（同源覆盖），不是全基因组 TE 含量。瘦 trusted（例如主要是有名 Copia/Gypsy/hAT）占比偏低可以是预期；葡萄真实 TE 碱基常很高。**禁止**为刷高数字改用整份 working / 生 EDTA 当 `-lib`（正好踩红线）。

**Q：soft-mask 会弄丢抗病基因吗？**  
A：正确 soft-mask 是改**小写**（碱基还在），不是改成 N。Hard-mask / 假 curatedlib 才会毁掉 NLR。A0 的 softmasked_fraction **不是**「基因组 TE%」，只是相对这份 trusted 的同源覆盖（见上一问）。  

**Q：命令行弱，能不能 Galaxy？**  
A：可先只要到 trusted FASTA；soft-mask 可请人按 A0 跑。Galaxy RepeatMasker 见 [17](17_外部教程与会议.md)。

**Q：trusted TE 长什么样？**  
A：通常是**一个** FASTA（共识序列库），例如 `grape_TElib_trusted_v1.1.fa`。METHODS 写：**文件名 + 版本 + sha256**。不是「一堆原始 EDTA 目录」。

**Q：怎么判断手里是 trusted 还是 working？**  
A：看**门控是否做过、文件名/标签是否写 trusted/curatedlib**。整份 working、生 EDTA、`cat`+CD-HIT **都不算** trusted。说不清就向实验室要现行 trusted；不要自己用生 EDTA 顶上 soft-mask。

**Q：只有生 EDTA，最短路径第 3 步是不是卡死？**  
A：对基因 A0 来说，**没有 trusted 就不要宣称 L1 soft-mask 诚实（G2）**。中间态可以：先做发现、METHODS 写明「仅 EDTA discovery，尚未 emit trusted；基因预测暂缓 / 或仅用外部 trusted」。日常注释不必先读完课 18；建库深链见 [18](18_TE流程课_借鉴实验室03_TE.md) / [vitis-te](https://github.com/Xuzhen-Li/vitis-te)。

**Q：没实验室 trusted、又不想现在啃 vitis-te——能用近缘物种的 trusted 做 soft-mask 吗？**  
A：**可以作权宜**，但必须在 METHODS 写清：来源物种/文件名/版本/sha256、以及「非本物种自建门控」。风险是近缘库可能漏本物种特有 TE 或过 mask。更稳的两档：(1) 暂缓基因预测直到本面板 emit trusted；(2) 用近缘 trusted 先出 **L0/provisional** 草稿，待本库就绪再 remask（S10）升档。**不要**用近缘 raw EDTA 冒充 trusted。

**Q：R1≈240 要不要懂？**  
A：最短路径**可以先当没看见**。那是葡萄面板档案/教学数字，不是你物种的配额。

**Q：TOOLS 写 EDTA *(or curated lib)*——有 trusted 能跳过 EDTA 吗？**  
A：**可以。** 基因 soft-mask 优先用现成 **trusted**；EDTA 是「还没有库」时的 de novo 起点，不是每天必跑。

**Q：不是葡萄，`--species` / `--cds` / 长 contig 名怎么办？**  
A：见 [`../tools/edta.md`](../tools/edta.md)：多数非稻/玉米用 `--species others`；`--cds` 按你的门控方案；contig 名过长须**先改短名并自备 id_map**（EDTA 要求 ≤13 字符）。本仓 A0 只接到 trusted→RepeatMasker；TEtrimmer 等在 TE 专题/vitis-te。

---

## flow / answers / 三种「打印」

**Q：answers 填错会怎样？**  
A：会选**错分支**。flow 只根据你勾的证据选路，不会核对你磁盘上真有没有 RNA。填完对照 plan 里的 Reason；不对就改 yaml 重跑。

**Q：`goal: qualified` 是 L1 吗？**  
A：是。对照：`provisional`→L0，`qualified`→L1，`paper_t2t`→L2/S5。见 `answers.example.yaml` 注释。

**Q：`close_curated_ref` 多近才算？我有半成品 Liftoff？**  
A：指**可信任的近缘/同种已策展 GFF** 适合当投影主路径（S11）。「半成品 Liftoff」通常仍勾 false，主草稿走 S1，Liftoff 当对照轨——METHODS 写清**一个 primary draft**。

**Q：`plant_tandem_focus: true` 会怎样？先 false？**  
A：true 时 plan 会出现 overlay **S7**（植物串联/抗病/QTL 窗口关注），验收硬门槛 **G9** 适用。example 默认 **false**（动物/普通教学勿照抄 true）。做植物抗病再 true；本科不确定先 false 并问导师。

**Q：plan 里 Overlays: S7 是什么？**  
A：**不是**另一条主草稿支（主草稿仍是 S1/S11…）。S7 = 因 `plant_tandem_focus` 打开而附加的「串联/抗病窗口」关注层，和 G9 同一件事。动物基因组不应默认出现。

**Q：手里已有老师给的基因组，plan 还从 Asm0 讲起？**  
A：把 Asm0/Asm1 当**检查清单**：接受成品 FASTA、写来源、跑/抄基因组 BUSCO、设 `ASSEMBLY_OK=yes`。**不必**自己再跑 hifiasm。宿舍只有 conda、没有集群：最短路径停在「读懂 plan + 填好将需要的路径清单」也算诚实进度；BRAKER 等到有 HPC/容器再跑。

**Q：怎么一次看齐「三种打印」？**  
A：```bash
python3 pipeline/flow_tool/flow.py --answers my_answers.yaml -o my_plan.md --emit-commands
python3 pipeline/print_qc_commands.py --env config/example.env
```
同一份 plan 里会带阶段助手草稿；QC 打印是另一个命令。

**Q：近缘 trusted 同科可以、跨纲不行？**  
A：没有硬尺子。越近缘越好；跨纲风险大。METHODS 必须写来源；更稳是 L0/暂缓或等本物种 trusted。问导师。

**Q：plan 全英文，本科生怎么读？**  
A：先看 Chooser（Primary draft / Target grade / Reason）和文末 After this plan；阶段名用 [99_术语表](99_术语表.md) 对照。不必第一天读懂每一段 BRAKER 旗标。

**Q：非葡萄 / 动物用户？**  
A：示例常带葡萄/eudicots 教学味。换你的：`BUSCO_LINEAGE`（动物常见 `metazoa_odb*`）、`PROTEIN_DB`、trusted TE、关掉 `plant_tandem_focus`。勿照抄 OMARK_TAXID=29760 或 viridiplantae。

**Q：`my_answers.yaml` 和 `answers.yaml`？**  
A：都行；仓库约定示例用根目录 **`my_answers.yaml`**（已在 `.gitignore` 思路上：勿提交私有答案）。不要提交填了路径的答案文件。

**Q：plan、`--emit-commands`、`print_qc_commands.py` 三个什么关系？**  
A：
1. **`my_plan.md`**：选哪条支 + 每步讲解（主学习文件）。  
2. **`flow.py --emit-commands`**：在 plan 里附带**阶段助手**命令草稿（仍常含占位）。  
3. **`print_qc_commands.py`**：按**验收勾选表**打印 QC 命令（AGAT/BUSCO/PSAURON…）。可先：`python3 pipeline/print_qc_commands.py --env config/example.env` 看样例——**此时出现 `[STOP]` 属预期**（占位/`YOUR_*`/裸 eukaryota）；填好 `local.env` 后再求绿。

**Q：没集群 / 没 Singularity，plan 里的命令？**  
A：plan 是**模板**；装法见各 `docs/tools/*.md`（常推荐容器）。笔记本可先跑通 flow + 读 plan，BRAKER 等到有环境再贴。

**Q：没有 GPU 还要看 S13/Helixer 吗？**  
A：默认 S1 **不需要**。Helixer 可 CPU（很慢）或跳过；有 RNA+蛋白时 **禁止用 S13 静默顶替 S1**（自动不合格）。

---

## local.env / 目录

**Q：`WORK_DIR` 下那些子目录谁建？**  
A：`mkdir` 那行是**你先建骨架**；FASTQ/BAM/基因组由你放进约定位置；许多脚本也会再 `mkdir -p` 自己的输出子目录。输入不会从天而降。

**Q：RNA / 蛋白变量到底叫什么？**  
A：打开 [`../../config/example.env`](../../config/example.env) 对照键名。常见：`GENOME_FA`、`GENOME_SOFT`、`RNA_BAM`、`PROTEIN_DB`、`BUSCO_LINEAGE`、`WORK_DIR`、`THREADS`、`DRAFT_GFF`、`PROTEINS_FA`、`RELEASE_TAG`。

---

## 验收勾选

**Q：基因组是别人组装的，G1 还能勾吗？**  
A：**能**，前提是你在 Asm1/METHODS 写清：来源、谱系 BUSCO、N50/倍性判断，并设 `ASSEMBLY_OK=yes`。G1 考的是「声明可注」，不是「必须你亲自 hifiasm」。

**Q：trusted 没有现成 sha256？**  
A：你自己 `sha256sum that.fa` 写入 METHODS **算数**（写清你算的、对应哪一版文件）。

**Q：BUSCO Completeness 要到多少？谱系用哪个？**  
A：本 playbook **不设全球数字门槛**（见 EVALUATION 软指标）。植物常见起点 `viridiplantae_odb12`，更细谱系按物种/课题组定，但**必须写出谱系全名**。百分比在 Asm1/S5 事先自定。

**Q：PSAURON「最差」怎么排？**  
A：用仓内 `pipeline/02_priority_loci.py`（及 S5 的 merge 脚本）从分数生成优先表；修不完就在 METHODS **显式暂缓**。

**Q：跑了 S1 又跑 Liftoff，primary draft 填啥？**  
A：只填**一条主草稿 ID**（通常 S1）；Liftoff 写「对照/次要证据」，不要两个都自称 primary。

**Q：Helixer GFF 算不算注释完成？**  
A：最多算 **S13 草稿/对照**；默认有 RNA+蛋白时应走 S1。只交 Helixer 就写「完成」→ 不合格叙事。

**Q：isoform 政策写哪？**  
A：**METHODS 一句话即可**（例如「每基因取最长 CDS 为代表蛋白」）；不强制改 GFF 全套 attribute。

**Q：A6b 改 gene ID 算结构还是功能？**  
A：**结构仓**（坐标/ID 体系仍属结构放行）。GO/名字释义才是功能仓。

**Q：走完中文最短路径还要不要读英文 QUICKSTART？**  
A：**卡住再翻**。START_HERE 是英文门牌；日常跟 `docs/zh` + plan + 勾选表即可。

**Q：完整课表 02/04/05 第一天要读吗？**  
A：**卡了再查**。最短路径故意只钉 01→03→跑→验收；02/05 是 TE/soft-mask 卡住时再打开。
