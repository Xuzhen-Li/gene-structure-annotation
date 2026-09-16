# Recommended BUSCO / Compleasm lineages (plants)

Use this table when filling `BUSCO_LINEAGE` and `COMPLEASM_LINEAGE` in `config/local.env`.  
Gate **G6** ([`EVALUATION.md`](EVALUATION.md)): report **completeness + full lineage name**. Bare `eukaryota` / `eukaryota_odb*` is an anti-pattern for clade-specific plant papers.

Sibling QC helpers: [`tools/busco.md`](tools/busco.md) · [`tools/omark_compleasm.md`](tools/omark_compleasm.md) · `pipeline/01_qc_busco_psauron.sh` · `pipeline/A5b_omark_compleasm.sh`.

---

## odb10 vs odb12 (do not mix)

| Generation | Typical name shape | Notes |
|------------|--------------------|-------|
| **odb10** | `viridiplantae_odb10`, `eudicots_odb10`, `poales_odb10`, … | Long-standing papers / older Compleasm defaults |
| **odb12** | `viridiplantae_odb12`, `eudicots_odb12`, `poales_odb12`, … | Prefer for **new** runs when your BUSCO install has the dataset |

**Rules**

1. Pick **one** generation for the project (Asm1 genome + protein QC + METHODS).  
2. Download that exact dataset; do **not** compare `%C` across odb10 vs odb12 as if identical.  
3. Compleasm: use a lineage name your Compleasm build actually ships (historically odb10-oriented; newer Compleasm supports odb12 — check `compleasm list` / your site docs). Put the **same clade intent** in `COMPLEASM_LINEAGE` (often short names like `eudicots`, `poales`).  
4. Never leave `YOUR_BUSCO_LINEAGE_*` or silent `eukaryota` in a release METHODS.

Official plant catalog (odb10 framing on the site; odb12 datasets follow the same clade names with `_odb12`): [BUSCO Plants](https://busco.ezlab.org/frames/plants).

---

## Recommended names (common plants)

Prefer the **most specific available** lineage that still matches your species. If an order-level set is missing on your install, step up to class/kingdom (`eudicots` / `poales` / `viridiplantae`) — never down to bare eukaryota for a plant paper.

| Organism / clade | BUSCO lineage (prefer odb12 if available) | Compleasm-style clade (typical) | Notes |
|------------------|-------------------------------------------|----------------------------------|-------|
| **Vitis** (grape) | `eudicots_odb12` or `viridiplantae_odb12` | `eudicots` | Teaching default in this repo often uses `viridiplantae_odb12`; eudicots is finer when available |
| **Oryza** (rice) | `poales_odb12` | `poales` | Do **not** copy eudicots / Vitis defaults |
| **Solanum** (tomato, potato, …) | `solanales_odb12` if present, else `eudicots_odb12` | `solanales` or `eudicots` | Confirm dataset exists on your BUSCO data dir |
| **Arabidopsis** | `brassicales_odb12` if present, else `eudicots_odb12` | `brassicales` or `eudicots` | |
| **Zea** (maize) | `poales_odb12` | `poales` | Same family story as rice |
| **Glycine** (soybean) | `fabales_odb12` if present, else `eudicots_odb12` | `fabales` or `eudicots` | |
| **Brassica** | `brassicales_odb12` if present, else `eudicots_odb12` | `brassicales` or `eudicots` | |
| General **Viridiplantae** | `viridiplantae_odb12` | `viridiplantae` | Safe broad plant start when order set unknown |
| General **eudicots** | `eudicots_odb12` | `eudicots` | Most dicot crops when order-level set unavailable |
| General **Poales** / grasses | `poales_odb12` | `poales` | Monocot grasses (rice, maize, wheat, …) |

odb10 twins: replace `_odb12` → `_odb10` if that is what you downloaded and freeze in METHODS.

---

## Warning — bare eukaryota

```text
BAD:  BUSCO_LINEAGE=eukaryota_odb10
BAD:  BUSCO_LINEAGE=eukaryota_odb12
BAD:  reporting "C=95%" with no lineage name
OK:   BUSCO_LINEAGE=viridiplantae_odb12   # + same name in METHODS / qc snapshot
```

`pipeline/_env_guards.sh` flags bare `eukaryota*` as an EVALUATION anti-pattern for clade papers.

---

## METHODS one-liners (copy)

```text
Protein BUSCO: BUSCO vFILL, lineage viridiplantae_odb12 (mode proteins); C/D/F/M = FILL.
Assembly BUSCO (Asm1): lineage FILL_odb12 (mode genome); C/D/F/M = FILL.
Compleasm (optional): lineage FILL; version FILL.
```

---

## Wiki / Evaluate later

When the lab wiki “Evaluate” page is updated, link this file under lineage / QC choices. Optional for this batch — public ops stay here.
