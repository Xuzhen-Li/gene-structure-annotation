# Final evaluation criteria — gene structure

**What “done” means** for a release in this playbook.  
Not a second roadmap: [`ROADMAP.md`](ROADMAP.md) picks the path; **this page judges the finish**. One-page tick sheet: [`EVALUATION_CHECKLIST.md`](EVALUATION_CHECKLIST.md).

Sibling FA criteria: [gene-function-annotation `EVALUATION.md`](https://github.com/Xuzhen-Li/gene-function-annotation/blob/main/docs/EVALUATION.md).

Lit map: [`REVIEWS.md`](REVIEWS.md) · peer stacks: [`PEER_PIPELINES.md`](PEER_PIPELINES.md) · gaps: [`SELF_AUDIT.md`](SELF_AUDIT.md).
QC methods/repos shelf: [`QUALITY_SOURCES.md`](QUALITY_SOURCES.md).

---

## Knowledge frame (why evaluation looks like this)

Gene **structure** annotation answers *where* exons/CDS are. Classic and recent reviews agree on three points this page encodes:

1. **Prediction ≠ annotation** (Yandell & Ence *NRG* 2012; Mudge & Harrow *NRG* 2016) — a GFF is only “done” when evidence, QC, and human triage are documented, not when a predictor exits 0.
2. **Evidence chooses the method** (Ji, Pertea & Salzberg *NRG* 2026; Freedman & Sackton *Genome Res.* 2025) — liftover vs BRAKER vs GALBA vs Iso-seq vs AI ab initio are not interchangeable; METHODS must name the path.
3. **BUSCO alone is insufficient** (OMArk literature; PSAURON; MoGAAAP *NAR Genom Bioinform* 2026; JOBIM 2026 Helixer pitfalls) — completeness can look fine while gene models are fragmented, TE-inflated, or splice-wrong.

Structure and **function** are separate layers (Ji 2026): this repo stops at qualified GFF + proteins; GO/KEGG live next door.

---

## Three finish grades

| Grade | Label in METHODS | When to claim it |
|-------|------------------|------------------|
| **L0 Provisional** | `status=provisional` | Thin evidence (S6), raw liftover (S11 before gap-fill), or open curation debt |
| **L1 Qualified** | `status=qualified` (default lab release) | All hard gates G1–G8 (and G9 if applicable) |
| **L2 Paper / T2T bar** | `status=qualified` + note S5 | L1 **plus** S5 overlays — [`cases/vitis-t2t-s1-s5.md`](cases/vitis-t2t-s1-s5.md) |

Do not call an L0 package “publication-final.” Do not call L1 “S5” without OMArk + second curation round.

### Background — grades

- **L0** exists because liftover-first (Ji) and homology-thin drafts are *useful* but systematically incomplete; journals and collaborators need an honest provisional tag (same spirit as Ensembl “projection” vs full genebuild).
- **L1** is the lab’s reproducible minimum: assembly OK, honest mask, named engine, valid GFF/proteins, multi-metric QC, packagable release — aligned with Freedman’s “building better annotations” emphasis on evidence + evaluation, not a single score.
- **L2 / S5** matches how recent T2T / horticulture genome papers raise the bar: extra orthology/consistency checks (OMArk), deeper manual windows (GSAman), and explicit stop rules so polishing does not become infinite.

---

## Hard gates (L1 — fail any ⇒ not qualified)

These are **binary**. Clade-specific *numbers* are yours to set in Asm1 / METHODS; the *existence* of each artifact is mandatory.

### G1 — Assembly declared

| | |
|--|--|
| **Pass** | `ASSEMBLY_OK=yes` + Asm1 note (genome BUSCO lineage **named**, N50 / ploidy decision) |
| **Fail** | Annotating a genome you would not publish |

**Background:** Annotation cannot fix a collapsed, contaminated, or mis-phased assembly. Asm1 is the same philosophy as assembly reports in T2L/T2T papers: declare the assembly fit for gene calling *before* spending BRAKER/EVM time. High BUSCO-D without a ploidy story is a known trap (S9).

### G2 — Soft-mask honesty

| | |
|--|--|
| **Pass** | Ab initio / BRAKER-class runs used **soft**-masked genome; TE lib = **trusted** curatedlib ([`TE_LIBRARY.md`](TE_LIBRARY.md)) |
| **Fail** | Hard-mask to `N`; raw EDTA / whole working lib as curatedlib |

**Background:** Repeats harbour both real genes (e.g. NLRs) and false exons. Hard-masking to `N` deletes sequence predictors need; soft-mask (`-xsmall`) keeps bases but down-weights repeats. EDTA *de novo* libraries are not curated — gene fragments and Unknowns in a “working” lib, if trusted 100% via `--curatedlib`, wipe host genes (Ou panEDTA / lab `03_TE` red lines). Vuruputoor et al. (*Appl Plant Sci* 2023) and plant TE practice: filter before you mask for genes.

### G3 — Draft path named

| | |
|--|--|
| **Pass** | One primary draft ID (S11/S1/S2/S3/S13/S14/S6) + tool **versions** in METHODS |
| **Fail** | “We ran annotation” with no engine |

**Background:** Freedman 2025 shows method rank depends on clade and evidence; Ji 2026 frames the chooser as evidence→method. Without a named path, results are not comparable or reproducible. Version pins matter because BRAKER3/4, GALBA2, Helixer, Tiberius, EviAnn change defaults quickly (*Nat Methods* 2025–2026 wave).

### G4 — Models validate

| | |
|--|--|
| **Pass** | `gffread` / AGAT clean on release GFF; gene/mRNA/CDS counts recorded |
| **Fail** | Coordinate errors; silent truncated GFF |

**Background:** Downstream proteomes, browsers, and NCBI/Ensembl ingest assume valid GFF3 semantics. AGAT/gffread catch the boring failures (CDS not multiple of 3, missing parents, broken phase) that inflate gene counts and break translation. Counts are the first smoke test after merge/combiner steps (EVM/TSEBRA/Mikado).

### G5 — Proteins match GFF

| | |
|--|--|
| **Pass** | `proteins.faa` regenerated from **this** release GFF; one-representative-per-gene policy stated |
| **Fail** | Stale proteins from an older draft |

**Background:** FA (eggNOG/InterPro) and protein BUSCO evaluate *sequences*, not coordinates. If proteins lag the GFF by one curation round, QC and function tables describe a ghost annotation. Stating the isoform/rep rule avoids silent isoform inflation in FA.

### G6 — Protein BUSCO reported

| | |
|--|--|
| **Pass** | Completeness **and** lineage name (e.g. `viridiplantae_odb12`) |
| **Fail** | BUSCO-% without lineage; plant paper left on default `eukaryota` |

**Background:** BUSCO is still the common language for “how complete is the gene set?” but lineage choice changes the denominator. Reporting C without the odb name is not interpretable. It remains a *necessary* metric, not a *sufficient* one (see G7).

### G7 — Beyond-BUSCO triage

| | |
|--|--|
| **Pass** | PSAURON run; `PRIORITY_TSV` exists; worst loci curated **or** explicitly deferred in METHODS |
| **Fail** | BUSCO-only “QC” |

**Background:** BUSCO tracks conserved single-copy orthologs; it under-samples lineage-specific, tandem, and TE-overlapping genes. PSAURON-style scoring and priority lists operationalize “look at the worst models.” OMArk adds consistency/completeness of gene families (required at L2). MoGAAAP and AnnoCheck-class peers encode the same idea: multi-tool QC packs beat one percentage.

### G8 — Release pack

| | |
|--|--|
| **Pass** | `release/<TAG>/` has GFF + proteins + METHODS (+ qc snapshot); no private BAM/FASTQ |
| **Fail** | Loose `draft/` files claimed as release |

**Background:** A release is a *contract*: frozen tag, public products, METHODS that another lab can cite. Draft trees are for iteration. Keeping reads out of git is both legal/ethics hygiene and reproducibility (point to SRA, not a laptop path).

### G9 — Tandem / disease / QTL windows (when relevant)

| | |
|--|--|
| **Pass** | NLR / stilbene / known QTL windows: no unreviewed tandem-collapse, **or** open items listed in METHODS |
| **Fail** | Plant immune / secondary-metabolic arrays silently collapsed and called done |

**Background:** Automatic predictors systematically under-resolve tandem arrays (classic plant annotation failure mode). HRP/NLR and stilbene clusters are lab-critical for *Vitis*-class work; the gate generalizes to any genome where biology lives in arrays. Deferral is allowed — silence is not.

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
| Compleasm (optional) | Fast completeness cross-check vs BUSCO; same lineage **family** | Replacing named BUSCO lineage with Compleasm-only |
| gffcompare (when ref or 2nd draft) | Missing/novel/overlap loci for merge triage | Treating overlap % as biology truth |
| RNA exon/intron support (when RNA) | Fraction of models with coverage — AnnoAudit-style | Claiming “supported” without stating threshold |
| BRH to trusted proteome (optional) | Ortholog-ish sanity for L2 narrative | Equating BRH with function annotation |
| TE-in-genes flag (DeTEnGA / GAQET2) | Soft plant check beside G2 mask honesty | Skipping trusted lib because a TE flagger exists |

**Optional one-stop wrappers** (still tick this page): [GAQET2](https://github.com/victorgcb1987/GAQET2), [AnnoAudit](https://github.com/ERGA-consortium/AnnoAudit), [atol-qc-annotation](https://github.com/TomHarrop/atol-qc-annotation). Source shelf: [`QUALITY_SOURCES.md`](QUALITY_SOURCES.md).

### Background — soft metrics

Percentages are **clade- and assembly-dependent**. Freedman 2025: RNA evidence changes who wins; TOGA-like transfer can weaken on some monocots — so absolute cutoffs copied from a mammal paper mislead plants. JOBIM 2026: Helixer can *inflate* gene counts with short unsupported exons — rising AGAT counts are not automatically “more complete.” StringTie compare exists because transcript-derived models still catch isoforms/UTRs ab initio stacks miss when RNA is available.

L2 / S5 adds: OMArk tables in `qc/`; expanded priority (BUSCO fragments, tandems, OMArk flags); second GSAman; stop rules in the T2T case.

---

## Automatic fail (any grade)

- Hard-masked genome fed to BRAKER/GALBA as if soft-masked  
- Raw EDTA or full **working** TE lib used as `--curatedlib` / soft-mask gold  
- S13 (Helixer/Tiberius/ANNEVO/SegmentNT) as **silent replace** of S1 when RNA+proteins exist  
- Claiming function (GO/KEGG) inside this repo’s release — that is FA next door  
- Private reads in git / release tarball  

### Background — automatic fails

These are not style preferences. Hard-mask and bad curatedlib **destroy** or **bias** evidence (G2). Silent S13 replace contradicts Freedman/Ji (evidence-based methods still lead when RNA exists; AI ab initio is a *compare* lane — Hiller *Nat Methods* commentary / ANNEVO–Tiberius papers). Mixing layers confuses METHODS and review. Private data in repos breaks sharing and often licenses.

---

## Stop rules (S12) — when to stop polishing

Freeze and release (at current grade) when **any** of:

1. Priority list empty at your stated threshold  
2. Protein BUSCO-C unchanged after a full curation round  
3. Remaining issues are splice-site taste only (JOBIM-class: combiners disagree on details)  
4. You are chasing &lt;0.1% BUSCO  

Document the freeze reason in METHODS.

### Background — stop rules

Manual curation has diminishing returns. Mudge & Harrow already noted annotation as an ongoing process; GSAman / S12 make “stop” explicit so delivery exists. Splice-site disagreements between BRAKER, Helixer, and EGAPx are expected (JOBIM 2026) — infinite arbitration is not a release criterion.

---

## Hand-off to function

Structure L1 (or L2) → set `PROTEINS_FA` → [FA `EVALUATION.md`](https://github.com/Xuzhen-Li/gene-function-annotation/blob/main/docs/EVALUATION.md).  
FA cannot upgrade a broken gene set: catastrophic F0 ⇒ fix structure first.

### Background — hand-off

Ji 2026: structure and function scale differently and error modes differ (wrong locus vs wrong GO). eggNOG/InterPro on a TE-inflated or fragmented proteome produce confident-looking nonsense. Provenance (`RELEASE_TAG`) is how FA stays auditable.

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
Compleasm (optional) ________
RNA support / BRH (if applicable) ________
QC wrapper (none/GAQET2/AnnoAudit/…) ________
Stop rule used ________
```

Also: [`PLAYBOOK.md`](PLAYBOOK.md) (short checklist) · [`STAGE_IO.md`](STAGE_IO.md) · T2T case §7 for L2 packaging.
