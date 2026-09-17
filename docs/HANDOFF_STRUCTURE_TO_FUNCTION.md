# Handoff card — structure → function

Print-first. After `release/<TAG>/` is frozen, give the function repo:

| Copy | Value |
|------|--------|
| `RELEASE_TAG` | Same tag as `release/<TAG>/` |
| `PROTEINS_FA` | `…/release/<TAG>/proteins.faa` (stable alias — **not** a stale `WORK_DIR/proteins.faa` root copy) |
| `structure_grade` | Honest `grade=L0|L1|L2` and `status=provisional|qualified` (never `status=L1`). Lift-only / Helixer-only → `grade=L0` ; `status=provisional` |

```bash
# Example shape only — paths are yours
RELEASE_TAG="species_ann.v0.1"
PROTEINS_FA="/path/to/work/release/${RELEASE_TAG}/proteins.faa"
```

Details: [`../pipeline/A6_functional_optional.md`](../pipeline/A6_functional_optional.md) · [`POST_ASSEMBLY.md`](POST_ASSEMBLY.md) step 7.  
Function door: [gene-function-annotation](https://github.com/Xuzhen-Li/gene-function-annotation) · FAQ [`zh/FAQ_入门.md`](https://github.com/Xuzhen-Li/gene-function-annotation/blob/main/docs/zh/FAQ_入门.md).  
中文指针：[`zh/交接_结构到功能.md`](zh/交接_结构到功能.md).
