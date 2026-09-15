# flow_tool (structure) — step 1

Chinese short path: [`docs/zh/`](../../docs/zh/) (今天最短路径).

**Goal:** user answers → automatic branch → full narrated plan  
(inputs · software purpose · process · outputs).

```bash
cd gene-structure-annotation
cp pipeline/flow_tool/answers.example.yaml /tmp/answers.yaml
# edit /tmp/answers.yaml
python3 pipeline/flow_tool/flow.py --answers /tmp/answers.yaml -o /tmp/structure_flow_plan.md
python3 pipeline/flow_tool/flow.py --answers /tmp/answers.yaml --emit-commands | less
```

Requires PyYAML if you want full YAML (`pip install pyyaml`); a tiny fallback parser handles the example file without it.

## Roadmap for this tool

| Step | Status |
|------|--------|
| 1 Auto-choose + narrate all stages | **this folder** |
| 2 Emit ordered print-commands from `local.env` | next |
| 3 Optional local execute for safe helpers (AGAT, gffread, BUSCO wrappers) | later |
| 4 Cluster submit hooks (user templates) | later |

Chooser logic matches [`docs/ROADMAP.md`](../../docs/ROADMAP.md).  
Finish grades: [`docs/EVALUATION.md`](../../docs/EVALUATION.md).
