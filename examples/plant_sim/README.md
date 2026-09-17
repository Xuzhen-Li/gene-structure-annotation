# Plant simulation trio — exercise post-review defaults

![Three plant sims at a glance](../../docs/figures/plant_sim_three_lines.png)

Three **print-first** plant setups that stress the L1 fixes (TE honesty, lineage placeholders,
conditional A4, S7 narration, S11 chooser). Paths in `env.snippet` are placeholders — do not
commit real cluster paths.

**TE honesty (01 especially):** soft-mask lib = trusted FASTA (`TRUSTED_TE_LIB`); `softmasked_fraction` ≠ genome TE%. Never paste a comment *between* bash `\` continuations (see `docs/TE_LIBRARY.md` grape EDTA — comments go *above* `EDTA.pl`).

| ID | Species | Structure chooser stress | Function stress |
|----|---------|--------------------------|-----------------|
| `01_vitis_s1_s7` | Grape | S1 + S7 overlay; `TRUSTED_TE_LIB`; no forced A4 | F1 + `want_nlr` |
| `02_oryza_s1` | Rice | S1; non-grape EDTA/lineage (no Vitis `--u`) | Plain F1 |
| `03_solanum_s11` | Tomato + close ref | **S11** liftover-first | F1 + Mercator |


## Do not (02 / 03 red lines)

| Sim | Do not |
|-----|--------|
| **02 Oryza** | Do not treat “no close-ref in this sim” as “rice must never use S11.” Copy poales / non-grape EDTA flags — do not paste Vitis `--u`. |
| **03 Solanum** | Do not claim tomato is always S11. Need `close_curated_ref: true` **and** a trusted near curated GFF. Do not follow QUICKSTART’s default BRAKER path when plan says S11. Do not mix BUSCO odb10 with odb12. Lift-only without gap-fill = **S11-lite**, not S11/L1. |

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

**02 Oryza:** intentionally **no** close-ref (practice plain S1 + poales lineage). This does **not** teach “rice must never use S11.”

**03 Solanum:** ONLY if trusted near curated GFF; tomato ≠ always S11 — the switch is `close_curated_ref: true` + a trusted near GFF. Follow generated `plan.md` (S11 = lift **+ gap-fill**), not QUICKSTART’s default BRAKER steps. Match BUSCO odb generation (odb10 vs odb12); do not mix.
