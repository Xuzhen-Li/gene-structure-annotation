# Structure flow plan — Solanum_lycopersicum_sim

Generated: 2026-09-16 03:11 UTC  
Tool: `pipeline/flow_tool/flow.py` (plan + explain; print-first execution).

## Chooser decision

- **Primary draft:** `S11`
- **Overlays:** (none)
- **Target grade:** `L1` (see docs/EVALUATION.md)
- **Reason:** Close curated reference → liftover first (Ji NRG 2026).

### Answers snapshot

- `close_curated_ref`: `True`
- `has_rna`: `True`
- `has_proteins`: `True`
- `deep_isoseq`: `False`
- `want_gpu_abinitio_compare`: `False`
- `want_evm_pasa`: `False`
- `goal`: `qualified`
- `multi_hap`: `False`
- `plant_tandem_focus`: `False`
- notes: Simulates S11 when a trusted near-species curated GFF exists. Gap-fill with S1/S2 later; do not force A4 on single lift.

---

## Narrated stages

### 1. Asm0 — Assembly / haplotype decision

**Input:** Raw HiFi / Hi-C / ONT (or an already-finished genome FASTA).

**Software & purpose:** Assembler stack you already trust (hifiasm, etc.) — see pipeline/Asm0_assembly.md.

**Process:** Build or accept GENOME_FA; write down ploidy / hap choice. If the FASTA was given to you, skip assembling — document source for G1. Finished-genome checklist: (1) source/version, (2) BUSCO lineage name for Asm1, (3) N50/ploidy note, (4) ASSEMBLY_OK gate, (5) stable headers.

**Output:** GENOME_FA with stable headers.

**Helper:** `pipeline/Asm0_assembly.md`

### 2. Asm1 — Assembly QC gate

**Input:** GENOME_FA

**Software & purpose:** BUSCO (genome mode), seqkit/QUAST-style stats.

**Process:** Decide ASSEMBLY_OK for your clade; set lineage name explicitly.

**Output:** Asm1 notes; ASSEMBLY_OK=yes|no.

**Helper:** `pipeline/Asm1_assembly_qc.md`

### 3. A0 — Soft-mask with trusted TE library

**Input:** GENOME_FA + trusted curatedlib (not raw EDTA / not full working lib).

**Software & purpose:** RepeatMasker -xsmall; TE scheme in docs/TE_LIBRARY.md; optional ProtExcluder (A0b).

**Process:** Soft-mask only; never hard-mask for BRAKER/GALBA.

**Output:** GENOME_SOFT (+ lib version/sha in METHODS).

**Helper:** `pipeline/A0_softmask.md`

**Also see:** docs/TE_LIBRARY.md

### 4. S11 — Liftover-first draft

**Input:** REF_FA + REF_GFF + target GENOME_SOFT

**Software & purpose:** Liftoff / LiftOn / CAT (± TOGA2 if WGA).

**Process:** Transfer models; mark provisional until QC; plan gap-fill with S1/S2.

**Output:** Lifted DRAFT_GFF (status=provisional until G7).

**Helper:** `pipeline/A2c_liftoff.md`

**Also see:** No one-liner bash yet — follow the md (Liftoff/LiftOn). Do not hunt for a missing bash block.

### 5. A4skip — Merge skipped (single draft / compare-only)

**Input:** Primary DRAFT_GFF only

**Software & purpose:** N/A — set MERGED_GFF=$DRAFT_GFF or enable dual_draft_merge / has_second_predictor / DRAFT_ENGINE_B

**Process:** Single primary draft (S11) does not require EVM/TSEBRA. Promote that GFF forward; run A4 only with a true second predictor / dual Liftoff set / S14 combiner. StringTie compare alone is not a second gene set.

**Output:** Use DRAFT_GFF as release-candidate input to AGAT/proteins

**Also see:** pipeline/A4_merge_sets.sh (optional if dual track later)

### 6. A5 — AGAT structure counts

**Input:** MERGED_GFF or primary GFF

**Software & purpose:** AGAT

**Process:** Gene/mRNA/CDS counts for METHODS and sanity vs related species.

**Output:** AGAT_OUT counts

**Helper:** `pipeline/A5_agat_stats.sh`

```bash
# Print-first: DRY unless RUN=1 (see script header).
bash pipeline/A5_agat_stats.sh          # dry
RUN=1 bash pipeline/A5_agat_stats.sh    # execute on cluster after review
```

### 7. A3 — Proteins from GFF

**Input:** Release-candidate GFF + genome

**Software & purpose:** gffread / AGAT extract

**Process:** One representative protein per gene (state isoform rule).

**Output:** PROTEINS_FA

**Helper:** `pipeline/A3_proteins_from_gff.sh`

```bash
# Print-first: DRY unless RUN=1 (see script header).
bash pipeline/A3_proteins_from_gff.sh          # dry
RUN=1 bash pipeline/A3_proteins_from_gff.sh    # execute on cluster after review
```

### 8. 01 — Protein BUSCO + PSAURON

**Input:** PROTEINS_FA

**Software & purpose:** BUSCO (protein), PSAURON; optional OMArk (required if S5/L2).

**Process:** Report C/D/F/M + lineage; triage low-quality loci.

**Output:** BUSCO summary + PSAURON_TSV (+ OMArk if L2)

**Helper:** `pipeline/01_qc_busco_psauron.sh`

**Also see:** pipeline/A5b_omark_compleasm.sh (optional / L2)

```bash
# Print-first: DRY unless RUN=1 (see script header).
bash pipeline/01_qc_busco_psauron.sh          # dry
RUN=1 bash pipeline/01_qc_busco_psauron.sh    # execute on cluster after review
```

### 9. 02 — Priority loci list (G7)

**Input:** PSAURON_TSV (± family boost TSV)

**Software & purpose:** pipeline/02_priority_loci.py (± 02b_merge_priority_r2.py)

**Process:** Rank worst models; expand for tandems/BUSCO fragments on L2.

**Output:** PRIORITY_TSV

**Helper:** `pipeline/02_priority_loci.py`

**Also see:** docs/EVALUATION.md G7 · docs/EVALUATION_CHECKLIST.md · docs/SCENARIOS.md

```bash
# Print-first emit (review; may still need RUN=1 for .sh helpers):
python3 pipeline/02_priority_loci.py -i "$PSAURON_TSV" -o "$PRIORITY_TSV"
```

### 10. 04 — GSAman / manual curation

**Input:** Priority windows + evidence tracks

**Software & purpose:** GSAman (browser curation)

**Process:** Fix or defer each priority locus (no S7 overlay on this plan — genome-wide or PSAURON-priority only).

**Output:** CURATED_GFF

**Helper:** `pipeline/04_gsaman_curation.md`

### 11. 06 — Qualify + package release

**Input:** Curated GFF + proteins + qc/

**Software & purpose:** gffread validate; copy to release/<TAG>/; fill METHODS

**Process:** Tick docs/EVALUATION.md gates for target grade; freeze tag.

**Output:** release/<TAG>/ GFF + proteins + METHODS + qc snapshot

**Helper:** `pipeline/06_release_gff.md`

**Also see:** docs/EVALUATION.md

### 12. A6 — Hand-off to functional annotation

**Input:** Released PROTEINS_FA

**Software & purpose:** Sibling gene-function-annotation flow tool (F1 default).

**Process:** Do not invent GO here; point FA at this RELEASE_TAG.

**Output:** FA functional_master.tsv (next repo)

**Helper:** `pipeline/A6_functional_optional.md`

---

## After this plan

1. Copy `config/example.env` → `config/local.env` and fill paths.
2. Walk stages in order; tick `docs/EVALUATION_CHECKLIST.md` (Chinese: `docs/zh/验收勾选表.md`; full rules: `docs/EVALUATION.md`).
3. Optional QC command print: `python3 pipeline/print_qc_commands.py` (try `--env config/example.env`, or after `source config/local.env`).
   Re-run with `--emit-commands` to embed stage helper stubs in this plan.
   Already have GENOME_FA from someone else: treat Asm0/Asm1 as a checklist (document source + `ASSEMBLY_OK`), do not re-assemble.
4. Hand proteins to `gene-function-annotation` (`pipeline/flow_tool/flow.py` there).

This tool does **not** claim one-click BRAKER on your HPC yet — helpers often print commands.
