# Structure flow plan — Vitis_vinifera_sim

Generated: 2026-09-16 02:21 UTC  
Tool: `pipeline/flow_tool/flow.py` (plan + explain; print-first execution).

## Chooser decision

- **Primary draft:** `S1`
- **Overlays:** S7 — S7 = plant tandem/disease windows (G9); not a second primary draft
- **Target grade:** `L1` (see docs/EVALUATION.md)
- **Reason:** RNA + proteins, no close ref → BRAKER4/3 + StringTie compare.

### Answers snapshot

- `close_curated_ref`: `False`
- `has_rna`: `True`
- `has_proteins`: `True`
- `deep_isoseq`: `False`
- `want_gpu_abinitio_compare`: `False`
- `want_evm_pasa`: `False`
- `goal`: `qualified`
- `multi_hap`: `False`
- `plant_tandem_focus`: `True`
- notes: Simulates TE soft-mask honesty + S7/G9. Use TRUSTED_TE_LIB (not working/raw EDTA). BUSCO viridiplantae_odb12.

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

### 4. A1b — RNA alignment

**Input:** RNA FASTQ + GENOME_FA/SOFT

**Software & purpose:** HISAT2 or STAR (short); minimap2 for long reads if Iso-seq.

**Process:** Produce stranded BAM suitable for BRAKER / StringTie / PASA.

**Output:** RNA_BAM (+ index).

**Helper:** `pipeline/A1b_rna_align.md`

### 5. S1 — BRAKER draft + transcript compare

**Input:** GENOME_SOFT + PROTEIN_DB + RNA_BAM

**Software & purpose:** BRAKER4/3 (± GeMoMa); StringTie→TransDecoder as compare set.

**Process:** Train/predict with RNA+proteins; keep StringTie as compare, not silent replace. Note: StringTie compare ≠ a second gene set for EVM — do not force A4 for compare-only.

**Output:** DRAFT_GFF (+ compare track)

**Helper:** `pipeline/A2_run_draft.sh`

**Also see:** pipeline/A2b_second_predictor.md

```bash
# Print-first helper (review before running on cluster):
bash pipeline/A2_run_draft.sh
```

### 6. A4skip — Merge skipped (single draft / compare-only)

**Input:** Primary DRAFT_GFF only

**Software & purpose:** N/A — set MERGED_GFF=$DRAFT_GFF or enable dual_draft_merge / has_second_predictor / DRAFT_ENGINE_B

**Process:** Single primary draft (S1) does not require EVM/TSEBRA. Promote that GFF forward; run A4 only with a true second predictor / dual Liftoff set / S14 combiner. StringTie compare alone is not a second gene set.

**Output:** Use DRAFT_GFF as release-candidate input to AGAT/proteins

**Also see:** pipeline/A4_merge_sets.sh (optional if dual track later)

### 7. A5 — AGAT structure counts

**Input:** MERGED_GFF or primary GFF

**Software & purpose:** AGAT

**Process:** Gene/mRNA/CDS counts for METHODS and sanity vs related species.

**Output:** AGAT_OUT counts

**Helper:** `pipeline/A5_agat_stats.sh`

```bash
# Print-first helper (review before running on cluster):
bash pipeline/A5_agat_stats.sh
```

### 8. A3 — Proteins from GFF

**Input:** Release-candidate GFF + genome

**Software & purpose:** gffread / AGAT extract

**Process:** One representative protein per gene (state isoform rule).

**Output:** PROTEINS_FA

**Helper:** `pipeline/A3_proteins_from_gff.sh`

```bash
# Print-first helper (review before running on cluster):
bash pipeline/A3_proteins_from_gff.sh
```

### 9. 01 — Protein BUSCO + PSAURON

**Input:** PROTEINS_FA

**Software & purpose:** BUSCO (protein), PSAURON; optional OMArk (required if S5/L2).

**Process:** Report C/D/F/M + lineage; triage low-quality loci.

**Output:** BUSCO summary + PSAURON_TSV (+ OMArk if L2)

**Helper:** `pipeline/01_qc_busco_psauron.sh`

**Also see:** pipeline/A5b_omark_compleasm.sh (optional / L2)

```bash
# Print-first helper (review before running on cluster):
bash pipeline/01_qc_busco_psauron.sh
```

### 10. S7a — S7 / G9 — build families.tsv

**Input:** OrthoGroups / QTL / NLR ID lists (from FA HRP / nf-annotate --r_genes or curated windows)

**Software & purpose:** Lab tables → families.tsv (gene_id	family_or_window)

**Process:** Mirror docs/SCENARIOS.md S7: list tandem/disease/QTL genes for boost; G9 applies when these windows matter. (Replaces the generic stage-02 priority pass — do not run 02 without --families first.)

**Output:** curate/families.tsv

**Helper:** `docs/SCENARIOS.md S7`

**Also see:** docs/EVALUATION.md G9

### 11. S7b — S7 / G9 — re-rank priority with --families (G7)

**Input:** PSAURON_TSV + curate/families.tsv

**Software & purpose:** pipeline/02_priority_loci.py --families

**Process:** Build PRIORITY_TSV with family boosts; this is the G7 command for S7 runs.

**Output:** PRIORITY_TSV with family:… reasons

**Helper:** `pipeline/02_priority_loci.py`

**Also see:** docs/SCENARIOS.md S7

```bash
# Print-first (review before running on cluster):
python3 pipeline/02_priority_loci.py -i "$PSAURON_TSV" -o "$PRIORITY_TSV" --threshold 90 --families curate/families.tsv
```

### 12. S7c — S7 / G9 — window curation (±100 kb tandems)

**Input:** Priority windows + evidence tracks

**Software & purpose:** GSAman on family/QTL windows only (rest may stay draft)

**Process:** Curate NLR/stilbene/QTL tandems; no unreviewed collapse, or list open items in METHODS (G9).

**Output:** CURATED_GFF (± curated_windows track / curated=yes attrs)

**Helper:** `pipeline/04_gsaman_curation.md`

**Also see:** docs/SCENARIOS.md S7 · G9

### 13. 06 — Qualify + package release

**Input:** Curated GFF + proteins + qc/

**Software & purpose:** gffread validate; copy to release/<TAG>/; fill METHODS

**Process:** Tick docs/EVALUATION.md gates for target grade; freeze tag.

**Output:** release/<TAG>/ GFF + proteins + METHODS + qc snapshot

**Helper:** `pipeline/06_release_gff.md`

**Also see:** docs/EVALUATION.md

### 14. A6 — Hand-off to functional annotation

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
