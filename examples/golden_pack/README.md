# Golden pack (EXAMPLE checklist) — structure L0 / L1

**This directory is a checklist + stubs only.** It does **not** ship real genomes, GFF, or protein sequences.  
Do not treat anything here as a finished annotation. Label: **EXAMPLE**.

Plant sims (`../plant_sim/`) are **print-first plans only** — they do not download data or run BRAKER/Liftoff.

Wiki twin (optional): [Evaluate · Golden pack](https://github.com/Xuzhen-Li/gene-structure-annotation/wiki/Evaluate-release#golden-pack--what-done-looks-like).

---

## What a golden L0 / L1 mini pack MUST contain

Under `work/release/<TAG>/` (or equivalent), a reviewable pack has:

| Path / artifact | L0 provisional | L1 qualified | Notes |
|-----------------|----------------|--------------|-------|
| `*.gff3` (release gene models) | required | required | Primary draft ID clear (S1 / S11 / **S11-lite** / …) |
| `proteins.faa` (one rep per gene) | required | required | Regenerated from **this** GFF (Gate G5) |
| `METHODS.md` (or `.txt`) | required | required | grade / status / primary / versions / lineages |
| `qc/` snapshot | recommended | required | BUSCO C/D/F/M **+ lineage name**; PSAURON / priority note |
| TE soft-mask provenance | required | required | trusted lib path + version + **sha256**; working ≠ curatedlib |
| `ASSEMBLY_OK` / Asm1 note | recommended | required | Or explicit “finished genome, Asm skipped” |
| Private BAM/FASTQ in git | **forbidden** | **forbidden** | Point to SRA / local path outside repo |

### L0 vs L1 (short)

| | `grade` | `status` | Typical stop |
|--|---------|----------|--------------|
| **L0** | `L0` | `provisional` | Thin evidence, **S11-lite** (lift-only), open curation debt |
| **L1** | `L1` | `qualified` | Gates G1–G8 (and G9 if tandem focus) in [`docs/EVALUATION.md`](../../docs/EVALUATION.md) |

Lift-only with no gap-fill → **S11-lite** + L0 only. Full S11 = lift + gap-fill + trunk QC.

---

## METHODS fields (minimum FILLs)

See stub: [`METHODS.stub.md`](METHODS.stub.md).

Must fill (no placeholders left in a real release):

- `grade=` · `status=` · `primary=` (e.g. `S1` or `S11` or `S11-lite`)
- Tool versions (Liftoff / BRAKER / GALBA / AGAT / …)
- `BUSCO_LINEAGE` full name (see [`docs/LINEAGES.md`](../../docs/LINEAGES.md)) — not bare eukaryota
- Trusted TE lib filename + sha256 ([`docs/TRUSTED_TE_PATH.md`](../../docs/TRUSTED_TE_PATH.md))
- Protein evidence / OrthoDB or ref GFF provenance
- Soft-mask: RepeatMasker `-xsmall` with trusted only

---

## File list for *this* EXAMPLE folder

```text
examples/golden_pack/
  README.md           # this checklist
  METHODS.stub.md     # EXAMPLE grade/status/primary FILLs — not a real release
```

No EXAMPLE `.gff3` / `.faa` on purpose — inventing fake sequences would be misleading.

---

## How to use

1. Copy `METHODS.stub.md` into your real `release/<TAG>/METHODS.md` and replace every `FILL`.  
2. Tick [`docs/EVALUATION_CHECKLIST.md`](../../docs/EVALUATION_CHECKLIST.md).  
3. For classroom without HPC: finish `plant_sim` plans + list paths in `local.env` — that is an honest stop, not a golden L1 pack.
