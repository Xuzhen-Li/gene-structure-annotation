# TE library scheme → soft-mask (A0)

> **Teaching (Chinese, illustrated):** [`zh/18_TE流程课_借鉴实验室03_TE.md`](zh/18_TE流程课_借鉴实验室03_TE.md)  
> **Lab notebook:** kept private (not in git). Public stub: [vitis-te](https://github.com/Xuzhen-Li/vitis-te).

**Canonical public stub:** [vitis-te](https://github.com/Xuzhen-Li/vitis-te).  
**Lab source of truth:** private pangenome TE notebook (not vendored).  
This file is the **public hand-off** into gene soft-mask.  

This file is the **structure-annotation hand-off**: what gene prediction is allowed to soft-mask with, and which TE products must never be confused.

Sibling: [`../pipeline/A0_softmask.md`](../pipeline/A0_softmask.md) · [`../pipeline/A0b_protexcluder.md`](../pipeline/A0b_protexcluder.md) · [`tools/edta.md`](tools/edta.md).

---

## Why structure annotation cares

BRAKER / GALBA / … over-call inside repeats if you skip masking, **hard**-mask to `N`, or soft-mask with a library that still contains **host genes** or **untrusted consensi**.  
For grape pangenome work the lab already learned: **a big FASTA after `cat`+CD-HIT is not a curatedlib.**

---

## Four products (do not crush into one FASTA)

From the live grape TE pipeline (`03_TE/README.md`):

| Product | Example (R1 archive) | Allowed use |
|---------|----------------------|-------------|
| **Working lib** | `grape_TElib_v0_cdhit95.fa` (~2530) | Sensitive consensus set after TEtrimmer+CD-HIT; **not** whole-file `--curatedlib` |
| **Family catalog** | `grape_TElib_v0_tetrimmer.fa` (~812, 80-80) | Family directory; Unknowns out before treating as curated |
| **Trusted curatedlib** | R1 archive example `grape_TElib_trusted_v1.0` (~240) | **Only** trusted goes to `--curatedlib` / gene soft-mask |
| **panEDTA combine** | `grape_panEDTA_v*.fa` | Official pan combine **after** trusted; **not** `cat` of per-genome TElibs |

TEsorter `all.cls.lib` / domain table = **labels on a subset** of the working lib. **Never** replace the working FASTA with `all.cls.lib`.

Non-TE repeats (TRF, telomere, rDNA, …) are a **separate non-TE track** — **never** enter `--curatedlib`.

### Lab status note (grape panel — teaching)

- **R1 trusted v1.0 (~240)** is an **archive / teaching example**, not automatically “panel gold forever.”  
- Notebook status (2026-09): R2 working-lib draft in progress; **v1.1** trusted expected after TEsorter/gating; until then do **not** silently treat v1.0 as final curatedlib for new panel EDTA v2.  
- If you soft-mask with v1.0 anyway: METHODS must record **filename + version + sha256** and that it is R1 archive.
- **How ~240 was defined (R1):** named superfamilies from TEsorter `cls.tsv` (e.g. Copia/Gypsy/hAT classes kept) **plus** CDS (PN40024.v4.1) decontamination / emit rules — **not** “hand-clicked 240 random consensi.” Helitron/TIR motif gates and LINE-`unknown` policy follow the lab emit rules (LINE unknown stays out of curatedlib).


---

## Lab order (pangenome `03_TE`)

```text
01 discovery   per-haplotype EDTA (de novo)
02 consensus   TEtrimmer per hap → merge Perfect/Good → CD-HIT ~95% working lib
               (+ optional 80-80 family catalog; do not overwrite working)
03 classify    TEsorter (rexdb-plant) — paste domains; does not shrink the FASTA
04 curation    CDS BLAST + Helitron/TIR/LTR gates → human trusted/working/exclude
05 release     emit trusted / working FASTAs (trusted = curatedlib only)
06 pilot       EDTA v2 + --curatedlib on a few genomes (new folder; no --overwrite on 01)
07 pan anno    panEDTA combine (−c CDS −f 3 −l trusted) → panel reannotate
08 QC          K2P age, PAV, LAI  (after name-aligned pan TE GFFs)
```

Then for **gene structure** on one assembly:

```text
trusted curatedlib  →  RepeatMasker -xsmall  (± optional A0b)
                    →  GENOME_SOFT  →  BRAKER / GALBA / …
```

---

## Hard red lines (from the live notebook)

| Do not | Why |
|--------|-----|
| `cat` all haplotype TElibs → CD-HIT → `--curatedlib` | Dedup ≠ curation (guide §3.9.5); Ou et al. panEDTA forbids naive concatenate |
| Feed **entire working** lib to `--curatedlib` | Unknowns / gene fragments get 100% trust |
| Replace working FASTA with TEsorter `all.cls.lib` | Classifier output ≠ library |
| Hard-mask for BRAKER/GALBA | Use `-xsmall` soft-mask |
| Put NLR / CDS / 03b non-TE into curatedlib | Host-gene wipe / nonsense repeats |
| Treat LAI / K2P on **raw** EDTA as delivery | Only after curated / pan GFF |
| HiTE / MCHelper / Terrier / DeepTE as this project default | Explicitly out of scope in `03_TE` |

---

## EDTA discovery defaults (grape panel)

As run in `01_discovery` (provenance; do not casually `--overwrite`):

```bash
EDTA.pl \
  --genome genome_mod.fa \
  --species others \
  --sensitive 1 \
  --anno 1 \
  --u 5.4e-9 \
  --threads "$THREADS"
# First grape round: no --cds (CDS locked later for gating / panEDTA)
# Sequence names: ≤13 chars (EDTA requirement); keep id_map.tsv
```

μ `5.4e-9`: Zhou et al. 2019 (population-calibrated; document in METHODS).  
CDS for gating / panEDTA: **PN40024.v4.1** (lab freeze — not an arbitrary newer T2T CDS unless you reopen the gate).

---

## TEtrimmer → working lib (consensus layer)

- Run **per haplotype**, not one mega-`cat` of raw EDTA TElibs (strategy A abandoned).  
- Keep Perfect/Good (and gated check bins per SOP); CD-HIT ~**95%** → **working** lib.  
- Optional second cut ~**80-80** → **family** catalog; **do not delete** the working lib.  
- Genome TE% is read from **annotation GFF**, not from consensus counts.

---

## TEsorter (classification layer)

```bash
# Example: TEsorter 1.4.x -db rexdb-plant on the WORKING fasta
# Domains land in cls.tsv for a minority of consensi; the rest stay in the FASTA unlabeled
```

Use domain calls in the **04 gate**, not as a replacement library.

---

## Curation gate → trusted (what soft-mask may trust)

Lab gate (public summary): **CDS BLAST** (frozen reference CDS for the panel) + **TEsorter class filters** + emit rules (optional motif gates as the notebook evolves).  
Emit:

- `grape_TElib_trusted_vX.fa` → **`--curatedlib` + gene soft-mask** (record sha256)  
- `grape_TElib_working_vX.fa` → sensitive archive, **not** curatedlib  

Prefer an existing **current** trusted lib for A0 over inventing raw EDTA gold. For the grape panel, check whether you need **v1.1+** rather than R1 v1.0 archive — see status note above.

---

## Soft-mask for gene structure (A0)

```bash
# CLEAN_TE_LIB = trusted curatedlib (host-gene purged)
RepeatMasker -lib "$CLEAN_TE_LIB" -xsmall -pa "$THREADS" \
  -dir "$WORK_DIR/mask" "$GENOME_FA"
cp "$WORK_DIR/mask/"*.masked "$GENOME_SOFT"
```

Optional: EDTA `--curatedlib "$CLEAN_TE_LIB"` in a **new** output directory for a TE track (S10 / METHODS) — never `--overwrite` the frozen discovery tree.

Verify soft-mask fraction (`pipeline/A0_softmask.md`). Extreme 0% or absurd wipe → check lib / A0b.

---

## Pangenome TE (after structure soft-mask path)

When the goal is panel TE GFFs (not only gene soft-mask):

1. Freeze trusted.  
2. Pilot EDTA v2 + curatedlib on a few genomes (`06_pilot`).  
3. **panEDTA** combine with `-c` CDS `-f 3` `-l` trusted — then reannotate keep genomes (`07_pan_annotation`).  
4. K2P / PAV / LAI (`08_qc_downstream`) only with aligned names.

This is owned by the pangenome TE notebook; structure playbook only needs the **trusted → GENOME_SOFT** cut.

---

## Products gene-structure must record

| Artifact | Role |
|----------|------|
| `GENOME_SOFT` | Predictor input |
| Trusted lib path + version / sha256 | METHODS |
| Note: working ≠ curatedlib | METHODS |
| Host-gene exclusion list (if A0b re-run) | METHODS / S10 |

---

## METHODS bullets (copy)

```text
TE library: EDTA (others/sensitive/anno; document --u) → TEtrimmer → CD-HIT~95% working →
TEsorter labels → CDS-gated trusted curatedlib.
Soft-mask lib example: grape_TElib_trusted_v1.0.fa
  sha256:<paste>   (R1 archive — replace with current emit when available)
Soft-mask: RepeatMasker -xsmall with that trusted file only.
working ≠ curatedlib; raw EDTA / cat+CD-HIT / all.cls.lib / non-TE repeats ≠ curatedlib.
Optional A0b ProtExcluder; optional panEDTA/LAI after trusted (TE track, not gene A0).
Do not cite private notebook or cluster absolute paths in METHODS.
```

---

## Pointers

| Need | Where |
|------|--------|
| Public stub / summary | [vitis-te](https://github.com/Xuzhen-Li/vitis-te) |
| Chinese teaching funnel | [`zh/18_TE流程课_借鉴实验室03_TE.md`](zh/18_TE流程课_借鉴实验室03_TE.md) |
| Lab detailed notebook | Private (not in git); do not paste cluster paths into METHODS |
