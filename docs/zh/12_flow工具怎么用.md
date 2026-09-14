# flow 工具怎么用（结构）

英文：[`../FLOW_TOOL.md`](../FLOW_TOOL.md) · [`../../pipeline/flow_tool/README.md`](../../pipeline/flow_tool/README.md)

## 它现在能做什么（Step 1）

填一份「你有什么证据」的答案 → 自动选 **S 支** → 生成 Markdown 计划：每个阶段写清 **输入 / 软件目的 / 流程 / 输出**。

```bash
git clone https://github.com/Xuzhen-Li/gene-structure-annotation.git
cd gene-structure-annotation
cp pipeline/flow_tool/answers.example.yaml my_answers.yaml
# 编辑 true/false：RNA、蛋白、近缘参考、论文档…
python3 pipeline/flow_tool/flow.py --answers my_answers.yaml -o my_plan.md
# 可选：打印命令骨架
python3 pipeline/flow_tool/flow.py --answers my_answers.yaml --emit-commands | less
```

需要 PyYAML 时：`pip install pyyaml`（示例 YAML 也有微型回退解析）。

## 诚实边界（print-first）

| 已有 | 还没有 |
|------|--------|
| 选路 + 分阶段讲解 | 一键在你的集群上跑完 BRAKER/EVM |
| 与 ROADMAP 一致的 chooser | 从 `local.env` 自动投递作业（规划中的 Step 2+） |

助手脚本（`A2_run_draft.sh` 等）常常**先打印**命令，让你按本机 module/路径改完再跑。这是设计，不是半成品借口——集群环境差太多，黑盒 `conda install && go` 会害人。

## 和 config 的配合

1. flow 选出 S 支、写出 plan。  
2. `cp config/example.env config/local.env`，填 `GENOME_FA`、`BUSCO_LINEAGE`、`RNA_BAM` / `PROTEIN_DB`、TE 库、`WORK_DIR`、`THREADS`…  
3. 按 plan + [`../STAGE_IO.md`](../STAGE_IO.md) 做到 [`../EVALUATION.md`](../EVALUATION.md) 放行。

下一页：[13_常见翻车.md](13_常见翻车.md)
