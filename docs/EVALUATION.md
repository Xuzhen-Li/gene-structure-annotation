# Final evaluation criteria — gene structure

**What “done” means** for a release in this playbook.  
Not a second roadmap: [`ROADMAP.md`](ROADMAP.md) picks the path; **this page judges the finish**.

Sibling FA criteria: [gene-function-annotation `EVALUATION.md`](https://github.com/Xuzhen-Li/gene-function-annotation/blob/main/docs/EVALUATION.md).

Lit anchors (why these gates): Freedman & Sackton *Genome Res.* 2025 (multi-metric, RNA matters); Ji *Nat Rev Genet* 2026 (structure ≠ function); OMArk / PSAURON / MoGAAAP (BUSCO alone is not enough) — [`REVIEWS.md`](REVIEWS.md) · [`SELF_AUDIT.md`](SELF_AUDIT.md).

---

## Three finish grades

| Grade | Label in METHODS | When to claim it |
|-------|------------------|------------------|
| **L0 Provisional** | `status=provisional` | Thin evidence (S6), raw liftover (S11 before gap-fill), or open curation debt |
| **L1 Qualified** | `status=qualified` (default lab release) | Trunk checklist below — all hard gates pass |
| **L2 Paper / T2T bar** | `status=qualified` + note S5 | L1 **plus** S5 overlays (OMArk mandatory, deeper GSAman, expanded priority) — [`cases/vitis-t2t-s1-s5.md`](cases/vitis-t2t-s1-s5.md) |

Do not call an L0 package “publication-final.” Do not call L1 “S5” without OMArk + second curation round.

---

## Hard gates (L1 — fail any ⇒ not qualified)

These are **binary**. Numbers that depend on clade are filled by you in Asm1 / METHODS, but the *presence* of the artifact is mandatory.

| # | Gate | Pass looks like | Fail |
|---|------|-----------------|------|
| G1 | Assembly declared | `ASSEMBLY_OK=yes` + Asm1 note (genome BUSCO lineage **named**, N50 / ploidy decision) | Annotating a genome you would not publish |
| G2 | Soft-mask honesty | Ab initio / BRAKER-class runs used **soft**-masked genome; TE lib = **trusted** curatedlib ([`TE_LIBRARY.md`](TE_LIBRARY.md)) | Hard-mask to `N`; raw EDTA / whole working lib as curatedlib |
| G3 | Draft path named | One primary draft ID (S11/S1/S2/S3/S13/S14/S6) + tool **versions** in METHODS | “We ran annotation” with no engine |
| G4 | Models validate | `gffread` / AGAT clean on release GFF; gene/mRNA/CDS counts recorded | Coordinate errors; silent truncated GFF |
| G5 | Proteins match GFF | `proteins.faa` regenerated from **this** release GFF; one rep policy stated | Stale proteins from an older draft |
| G6 | Protein BUSCO reported | Completeness **and** lineage name (e.g. `viridiplantae_odb12`) | BUSCO-% without lineage; wrong default `eukaryota` for a plant paper |
| G7 | Beyond-BUSCO triage | PSAURON run; `PRIORITY_TSV` exists; worst loci curated **or** explicitly deferred in METHODS | BUSCO-only “QC” |
| G8 | Release pack | `release/<TAG>/` has GFF + proteins + METHODS (+ qc snapshot); no private BAM/FASTQ | Loose files in `draft/` claimed as release |

**Plant / tandem-sensitive genomes (extra hard gate when relevant):**  
G9 — NLR / stilbene / known QTL windows: no unreviewed tandem-collapse, **or** open items listed in METHODS.

---

## Soft metrics (interpret; do not fake universal cutoffs)

This playbook **does not** ship a single BUSCO-C ≥ X% for all eukaryotes. Set the bar in Asm1 / S5 **before** you annotate.

| Metric | How to use | Anti-pattern |
|--------|------------|--------------|
| Genome BUSCO-C/D/F/M | Asm1 gate; high D → S9 policy | Purging haplotypes to chase C |
| Protein BUSCO-C | Track across GSAman rounds; stop when flat (S12) | Chasing &lt;0.1% C as delivery work |
| PSAURON scores | Rank loci for curation | Treating score as orthology truth |
| OMArk | **Required for L2/S5**; optional-but-recommended for L1 plant/T2T | Skipping OMArk and still claiming S5 |
| AGAT gene count | Stability across rounds | Exploding count after Helixer-only with no filter |
| StringTie↔BRAKER compare (when RNA) | Conflict list informs merge | Ignoring transcript evidence when it exists (Freedman) |

L2 / S5 adds: OMArk tables in `qc/`; expanded priority (BUSCO fragments, tandems, OMArk flags); second GSAman; stop rules in the T2T case.

---

## Automatic fail (any grade)

- Hard-masked genome fed to BRAKER/GALBA as if soft-masked  
- Raw EDTA or full **working** TE lib used as `--curatedlib` / soft-mask gold  
- S13 (Helixer/Tiberius/ANNEVO) as **silent replace** of S1 when RNA+proteins exist  
- Claiming function (GO/KEGG) inside this repo’s release — that is FA L1 next door  
- Private reads in git / release tarball  

---

## Stop rules (S12) — when to stop polishing

Freeze and release (at current grade) when **any** of:

1. Priority list empty at your stated threshold  
2. Protein BUSCO-C unchanged after a full curation round  
3. Remaining issues are splice-site taste only (JOBIM-class: combiners disagree on details)  
4. You are chasing &lt;0.1% BUSCO  

Document the freeze reason in METHODS.

---

## Hand-off to function

Structure L1 (or L2) → set `PROTEINS_FA` → [FA `EVALUATION.md`](https://github.com/Xuzhen-Li/gene-function-annotation/blob/main/docs/EVALUATION.md).  
FA cannot upgrade a broken gene set: catastrophic F0 ⇒ fix structure first.

---

## Tick list (copy into METHODS)

```text
Grade: L0 / L1 / L2
G1 Asm1 ASSEMBLY_OK + lineage ________
G2 Soft-mask + trusted TE lib ________
G3 Draft ID + versions ________
G4 GFF validate + AGAT counts ________
G5 Proteins from this GFF ________
G6 Protein BUSCO C/D/F/M + lineage ________
G7 PSAURON + priority (curated / deferred) ________
G8 release/<TAG>/ pack ________
G9 tandems (if applicable) ________
OMArk (L2 required) ________
Stop rule used ________
```

Also: [`PLAYBOOK.md`](PLAYBOOK.md) (short checklist) · [`STAGE_IO.md`](STAGE_IO.md) stage pass column · T2T case §7 for L2 packaging.
