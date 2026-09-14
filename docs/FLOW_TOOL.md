# Flow tool — progressive automation

**Step 1 (now):** fill answers → automatic S-branch → Markdown plan with **input / software purpose / process / output** per stage.

```bash
cp pipeline/flow_tool/answers.example.yaml answers.yaml
# edit answers.yaml
python3 pipeline/flow_tool/flow.py --answers answers.yaml -o structure_flow_plan.md
```

Details: [`../pipeline/flow_tool/README.md`](../pipeline/flow_tool/README.md).

**Not yet:** one-click BRAKER/EVM on your cluster. Helpers remain print-first; step 2 will emit ordered commands from `local.env`.

FA sibling: [gene-function-annotation flow_tool](https://github.com/Xuzhen-Li/gene-function-annotation/tree/main/pipeline/flow_tool).
