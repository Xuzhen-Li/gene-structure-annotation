**Primary checklist:** qualification list below. Functional FA → [gene-function-annotation](https://github.com/Xuzhen-Li/gene-function-annotation).

# Gene **structure** playbook — assembly to qualified GFF

Biology-general spine (eukaryotes). *Vitis* / PN40024 / plant-only tools in linked notes are examples or optional modules.

**Main spine:** [`steps/MAIN.md`](steps/MAIN.md). **AI assist:** [`AI_ASSIST.md`](AI_ASSIST.md). **S14:** [`steps/dclab/`](steps/dclab/).

**Tool how-tos:** [`TOOLS.md`](TOOLS.md).

**Reviews / benchmarks (chooser):** [`REVIEWS.md`](REVIEWS.md) — Freedman & Sackton *Genome Res.* 2025; Nature Methods Helixer / ANNEVO / EviAnn.

**Homepage flowchart:** see repository [`README.md`](../README.md).  
**Branch recipes:** [`SCENARIOS.md`](SCENARIOS.md) (S1–S12, step-by-step).  
**Stage list:** [`FULL_PIPELINE.md`](FULL_PIPELINE.md).

---

## End-to-end spine (every branch rejoins here)

```text
Asm0  Assemble / phase / purge / scaffold
Asm1  Assembly QC gate (genome BUSCO, N50, ploidy decision)
A0    Soft-mask repeats (ProtExcluder: keep genes out of TE lib)
  │
  ├─► branch by evidence / goal  (SCENARIOS S1–S11)
  │
A4/A5 Merge + AGAT (if dual draft)
A3    Proteins from GFF
01    BUSCO proteins + PSAURON (+ optional OMArk)
02    Priority loci
04    GSAman (depth depends on scenario)
05    SynGAP if multi-haplotype
06    Re-QC → qualified release checklist
A6    Optional: hand proteins to gene-function-annotation (F1)
```

---

## Qualification checklist (release = “合格”)

A release is **qualified** for this lab when:

- [ ] `ASSEMBLY_OK` documented (Asm1)
- [ ] Soft-masked genome used for ab initio (A0)
- [ ] Draft path named (S1–S11) + tool versions in METHODS
- [ ] AGAT gene/mRNA counts recorded
- [ ] Protein BUSCO-C reported (lineage named)
- [ ] PSAURON triage run; priority loci curated or explicitly deferred
- [ ] NLR / stilbene / QTL windows: no known tandem-collapse left unreviewed (or listed as open)
- [ ] GFF validates (`gffread` / AGAT); proteins regenerated
- [ ] Tag `RELEASE_TAG`; no private BAM/FASTQ in the repo

Provisional releases (S6, S11) must say `status=provisional` in METHODS.

---

## How to use the branches

1. Finish **Asm0 → Asm1 → A0**.  
2. Pick **one** scenario in [`SCENARIOS.md`](SCENARIOS.md).  
3. Follow that scenario’s numbered steps to a merged draft.  
4. Rejoin spine at **A3 → 01 → 02 → 04 → 06**.  
5. Tick the qualification checklist above.

Default if unsure: **S1** (RNA + proteins → BRAKER4/3).

When RNA exists, also keep a **StringTie → TransDecoder** compare set (GR 2025 top performer). WGA+close reference → consider **TOGA2** (check monocot BUSCO). Thin evidence / GPU → **S13**. Traceable evidence-only → **EviAnn** under **S3**.
