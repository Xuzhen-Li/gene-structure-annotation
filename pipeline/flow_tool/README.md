# flow_tool (structure) — step 1

Chinese short path: [`docs/zh/`](../../docs/zh/) (今天最短路径).

**Goal:** user answers → automatic branch → full narrated plan  
(inputs · software purpose · process · outputs).

```bash
cd gene-structure-annotation
cp pipeline/flow_tool/answers.example.yaml my_answers.yaml
# edit my_answers.yaml
python3 pipeline/flow_tool/flow.py --answers my_answers.yaml -o my_plan.md
python3 pipeline/flow_tool/flow.py --answers my_answers.yaml --emit-commands | less
```

Requires PyYAML if you want full YAML (`pip install pyyaml`); a tiny fallback parser handles the example file without it.

## Roadmap for this tool

| Step | Status |
|------|--------|
| 1 Auto-choose + narrate all stages | **this folder** |
| 2 Emit ordered print-commands from `local.env` | next (stage helpers) |
| 2b QC print spine | **done** — `pipeline/print_qc_commands.py` |
| 3 Optional local execute for safe helpers (AGAT, gffread, BUSCO wrappers) | later |
| 4 Cluster submit hooks (user templates) | later |

Chooser logic matches [`docs/ROADMAP.md`](../../docs/ROADMAP.md).  
Finish grades: tick [`docs/EVALUATION_CHECKLIST.md`](../../docs/EVALUATION_CHECKLIST.md) (Chinese [`docs/zh/验收勾选表.md`](../../docs/zh/验收勾选表.md); full [`docs/EVALUATION.md`](../../docs/EVALUATION.md)).
QC command printer (side path, not inside `flow.py`): `python3 pipeline/print_qc_commands.py`.

Also: [`../../docs/START_HERE.md`](../../docs/START_HERE.md). Prefer `my_answers.yaml` in the repo root (same as root README).
