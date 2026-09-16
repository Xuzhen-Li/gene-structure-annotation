# Plant simulation trio — exercise post-review defaults

Three **print-first** plant setups that stress the L1 fixes (TE honesty, lineage placeholders,
conditional A4, S7 narration, S11 chooser). Paths in `env.snippet` are placeholders — do not
commit real cluster paths.

| ID | Species | Structure chooser stress | Function stress |
|----|---------|--------------------------|-----------------|
| `01_vitis_s1_s7` | Grape | S1 + S7 overlay; `TRUSTED_TE_LIB`; no forced A4 | F1 + `want_nlr` |
| `02_oryza_s1` | Rice | S1; non-grape EDTA/lineage (no Vitis `--u`) | Plain F1 |
| `03_solanum_s11` | Tomato + close ref | **S11** liftover-first | F1 + Mercator |

## Run (structure)

```bash
cd gene-structure-annotation
for d in examples/plant_sim/01_vitis_s1_s7 examples/plant_sim/02_oryza_s1 examples/plant_sim/03_solanum_s11; do
  python3 pipeline/flow_tool/flow.py --answers "$d/answers.sim.yaml" --emit-commands -o "$d/plan.md"
done
# Optional: merge env.snippet into config/local.env, then
# python3 pipeline/print_qc_commands.py
```

## Run (function)

Same IDs under `gene-function-annotation/examples/plant_sim/`.

These sims do **not** download genomes or run BRAKER/IPS. They only show the plan/QC command surface.
