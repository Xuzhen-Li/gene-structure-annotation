# Scenarios — how to annotate in each situation

**Tool how-tos:** [`TOOLS.md`](TOOLS.md).


**Command-level spine (read first):** [`DETAILED_GUIDE.md`](DETAILED_GUIDE.md)  
**Checklist:** [`PLAYBOOK.md`](PLAYBOOK.md) · **Peers:** [`RELATED_SOFTWARE.md`](RELATED_SOFTWARE.md)

Every scenario below is a full recipe. Shared early steps always mean:  
**Asm0 → Asm1 → soft-mask (A0+A0b)** unless the scenario says otherwise.

---

## S1 — Default: RNA-seq + proteins → qualified GFF

**When:** Illumina RNA from the same (or very close) genotype + OrthoDB / grape proteins.

### Steps (do in order)

1. **Assemble** — HiFi (+ Hi-C if available) → `GENOME_FA`. Dual-hap? Decide now (else S4 later).  
   Details: [`DETAILED_GUIDE.md`](DETAILED_GUIDE.md) Step 1 · [`../pipeline/Asm0_assembly.md`](../pipeline/Asm0_assembly.md)

2. **Assembly QC** — genome BUSCO + contig stats. Set `ASSEMBLY_OK=yes` only if pass.  
   Step 2 · [`../pipeline/Asm1_assembly_qc.md`](../pipeline/Asm1_assembly_qc.md)

3. **Soft-mask** — curated TE lib → ProtExcluder clean → RepeatMasker `-xsmall` → `GENOME_SOFT`.  
   Step 3 · [`../pipeline/A0_softmask.md`](../pipeline/A0_softmask.md)

4. **Align RNA** — HISAT2 or STAR → `RNA_BAM` + index.  
   Step 4 · [`../pipeline/A1b_rna_align.md`](../pipeline/A1b_rna_align.md)

5. **Primary draft** — **prefer [BRAKER4](notes/braker4.md) ETP** if Singularity works; else BRAKER3 `braker.pl`.  
   ```bash
   # BRAKER4: see docs/tools/braker4.md (samples.csv mode=ETP)
   DRAFT_ENGINE=braker3 bash pipeline/A2_run_draft.sh   # classic fallback
   ```
   Step 5

6. **Second draft** — GeMoMa or Liftoff from PN40024 → `DRAFT_GFF_B`.  
   Step 6 · [`../pipeline/A2b_second_predictor.md`](../pipeline/A2b_second_predictor.md) · [`../pipeline/A2c_liftoff.md`](../pipeline/A2c_liftoff.md)

7. **Merge** — EVM (or TSEBRA if two BRAKER-family sets) → `MERGED_GFF`.  
   ```bash
   MERGE_MODE=evm bash pipeline/A4_merge_sets.sh
   bash pipeline/A5_agat_stats.sh "$MERGED_GFF"
   ```
   Step 7

8. **Proteins** — representative `PROTEINS_FA` from merged GFF.  
   ```bash
   DRAFT_GFF="$MERGED_GFF" bash pipeline/A3_proteins_from_gff.sh
   ```

9. **QC** — BUSCO proteins + PSAURON (+ OMArk/Compleasm if available).  
   ```bash
   bash pipeline/01_qc_busco_psauron.sh
   ```

10. **Priority** — low PSAURON + NLR/stilbene boost → `priority.tsv`.  
    ```bash
    python3 pipeline/02_priority_loci.py -i "$PSAURON_TSV" -o curate/priority.tsv --threshold 90
    ```

11. **GSAman** — load genome, GFF, BAM, homologs; fix priority loci; tag [`ERROR_CLASSES.md`](ERROR_CLASSES.md); export `CURATED_GFF`.  
    [`../pipeline/03_evidence_checklist.md`](../pipeline/03_evidence_checklist.md) · [`../pipeline/04_gsaman_curation.md`](../pipeline/04_gsaman_curation.md)

12. **Re-QC + release** — proteins/BUSCO/AGAT again; pass qualification checklist; freeze `RELEASE_TAG`.  
    Step 13 · [`../pipeline/06_release_gff.md`](../pipeline/06_release_gff.md)

**Stop early?** See S12.

---

## S2 — Proteins only (no usable RNA)

**When:** No RNA, or RNA is distant / bad mapping.

### Steps

1–3. Same as S1 (assembly, QC, soft-mask).

4. **Skip RNA** — `RNA_BAM=none` in `config/local.env`.

5. **Primary** — GALBA (close proteins) **or** GeMoMa as primary. Prefer GALBA if proteins are diverse; GeMoMa if one excellent grape GFF+FA exists.  
   ```bash
   DRAFT_ENGINE=galba bash pipeline/A2_run_draft.sh
   # or DRAFT_ENGINE=gemoma ...
   ```

6. **Second** — Liftoff PN40024 → `DRAFT_GFF_B` (always useful without RNA).

7. **Merge** — EVM with **higher weights on homology / Liftoff** than ab initio.  
   Document weights in METHODS.

8–10. Same as S1 (proteins, BUSCO/PSAURON, priority).  
   Expect more low-PSAURON splice issues.

11. **GSAman** — emphasize splice-site and start/stop fixes; use protein alignments heavily.

12. **Release** — if no RNA ever: set `status=provisional` unless S5 bar and heavy curation met.

---

## S3 — Deep Iso-seq / full-length transcripts

**When:** PacBio Iso-seq or equivalent FLNC depth is high.

### Steps

1–3. Same as S1.

4. **Map Iso-seq**  
   ```bash
   minimap2 -t "$THREADS" -ax splice:hq -uf "$GENOME_FA" flnc.fq.gz \
     | samtools sort -o "$WORK_DIR/rna/isoseq.bam"
   samtools index "$WORK_DIR/rna/isoseq.bam"
   export ISOSEQ_BAM="$WORK_DIR/rna/isoseq.bam"
   ```
   Optional: also keep Illumina BAM for coverage.

5. **Primary** — EviAnn with Iso-seq + proteins → evidence GFF as backbone candidate.  
   ```bash
   DRAFT_ENGINE=eviann bash pipeline/A2_run_draft.sh
   ```

6. **Secondary** — BRAKER3 (RNA short-read BAM if any, else proteins) → `DRAFT_GFF`.

7. **Merge** — EviAnn backbone; add BRAKER-only orphans after AGAT/overlap filter.  
   ```bash
   MERGE_MODE=evi_backbone bash pipeline/A4_merge_sets.sh
   ```

8–12. Same as S1.  
   GSAman: resolve backbone vs orphan conflicts first; Iso-seq tracks are ground truth for exons.

---

## S4 — Multi-haplotype / pangenome panel

**When:** Two+ phased haplotypes or cultivar panel.

### Steps

1. Pick **reference haplotype**. Run **full S1 (or S3)** through qualified `CURATED_GFF` on that hap.

2. For each other haplotype `H`:  
   ```bash
   # Liftoff curated ref GFF onto H (see A2c)
   liftoff -g "$CURATED_GFF" -o "draft/${H}.liftoff.gff3" -polish \
     -p "$THREADS" "asm/${H}.fa" "$GENOME_FA"
   ```

3. **SynGAP** (or equivalent) ref vs each `H` → conflict / presence-absence list.  
   [`../pipeline/05_syngap_polish.md`](../pipeline/05_syngap_polish.md)

4. **GSAman** on each hap: only SynGAP conflicts + NLR/QTL priority — not whole genome again.

5. **Release** a set:  
   - `ref.${RELEASE_TAG}.gff3`  
   - `hap2.${RELEASE_TAG}.gff3` …  
   - SynGAP reports + METHODS naming which hap is reference

---

## S5 — T2T / publication-grade

**When:** Paper or database release needs “qualified,” not provisional.

### Steps

1. **Asm1 stricter** — write numeric pass criteria into METHODS before annotating (BUSCO-C, N50, #chr).

2. Run **complete S1** through first GSAman pass (or S3 if Iso-seq exists).

3. **Mandatory** OMArk + Compleasm (`A5b`); save tables under `qc/`.

4. **Expand priority** — all fragmented BUSCO genes + genome-wide tandem arrays (not only PSAURON < 90).

5. **Second GSAman round** on expanded list.

6. Apply **S12** — stop when BUSCO-C stable and priority empty.

7. Optional: **S8** EGAPx side-by-side table in METHODS.

8. Release only if [`PLAYBOOK.md`](PLAYBOOK.md) checklist is 100% — no `provisional`.

---

## S6 — Thin evidence

**When:** Distant proteins only; little/no RNA; assembly OK but evidence weak.

### Steps

1–3. Same (do not skip soft-mask).

4. **No RNA** (or ignore low-mapping RNA).

5. **Draft** — Liftoff and/or GeMoMa only. Optional weak BRAKER protein-only for orphans.

6. **Light merge** — prefer homology GFF; do not over-trust ab initio.

7–10. Proteins + QC + priority (families only if known).

11. **GSAman** — **only** NLR / stilbene / QTL windows. Do not pretend genome-wide polish.

12. Release `status=provisional`. Plan Iso-seq → re-enter **S3**.

---

## S7 — Family / QTL-first

**When:** Science question is a locus or gene family, not whole-genome polish.

### Steps

1. Run S1 Steps 1–10 **genome-wide automated** (through priority).

2. Build `families.tsv`:  
   `gene_id<TAB>family_or_window` for Orthogroups / QTL interval genes.  
   For NLR: run [HRP](../tools/hrp.md) / nf-annotate `--r_genes` and add those IDs.

3. Re-rank:  
   ```bash
   python3 pipeline/02_priority_loci.py -i "$PSAURON_TSV" -o curate/priority.tsv \
     --threshold 90 --families curate/families.tsv
   ```

4. **GSAman** only those windows (±100 kb for tandems). Leave rest as draft.

5. Release options:  
   - Dual tracks (`full.gff3` + `curated_windows.gff3`), or  
   - One GFF with `curated=yes` attributes on edited genes  

   METHODS must state curation scope.

---

## S8 — NCBI EGAPx parallel

**When:** You want an external NCBI-style annotation for comparison or NCBI submission path.

### Steps

1. Keep **S1 (or S3)** as the lab primary through merge (do not replace it).

2. Install/run [ncbi/egapx](https://github.com/ncbi/egapx) with *Vitis* taxonomy + RNA YAML.  
   [`../pipeline/A2d_egapx_optional.md`](../pipeline/A2d_egapx_optional.md)

3. AGAT + protein BUSCO on **both** lab merge and EGAPx GFF.

4. Spot-check NLR / known genes in GSAman on both; table differences in METHODS.

5. **Primary release = lab branch** unless EGAPx clearly wins documented metrics — then say so and release EGAPx (or a curated hybrid).

---

## S9 — High BUSCO-D / suspected polyploid collapse

**When:** Asm1 genome BUSCO shows high Duplicate; or known tetraploid / collapsed haplotigs.

### Steps

1. At Asm1: **do not purge** until ploidy / haplotig status is known.

2. Prefer **phased hap1+hap2** and follow **S4**, rather than annotating one collapsed primary.

3. If you must annotate collapsed primary:  
   - Still soft-mask + S1/S2 draft  
   - GSAman heavily for **fusion vs split** (error classes)  
   - Report BUSCO-D and warn users in METHODS  

4. Do not claim “haplotype-resolved annotation” if assembly is collapsed.

---

## S10 — TE / ORF inflation

**When:** AGAT gene count ≫ near relatives × ploidy, or many tiny proteins / TE-like ORFs.

### Steps

1. **Stop** further curation on the inflated GFF.

2. Rebuild TE library; run **ProtExcluder** (`A0b`); re-soft-mask (`A0`).

3. **Re-enter S1 from draft** (Step 5) — do not merge old TE-inflated models forward.

4. Optional filter (`A5c`): drop loci that fail **RNA ∩ Pfam ∩ homolog** all three — never FPKM-only kill of NLR.

5. Re-run AGAT; gene count should drop toward clade norms before GSAman.

---

## S11 — Lift-only (quick transfer)

**When:** Need a fast working GFF for another cultivar / close assembly; not a publication annotation.

### Steps

1. Asm1 light check (stats + optional BUSCO). Soft-mask recommended.

2. **Only Liftoff** from best grape GFF — no BRAKER required.  
   [`../pipeline/A2c_liftoff.md`](../pipeline/A2c_liftoff.md)

3. AGAT (+ optional protein BUSCO). Flag `valid_ORF=False` for later.

4. METHODS: `status=provisional`, `method=liftoff-only`.

5. **Do not** claim qualified / last-mile complete.

---

## S12 — Stop rules (when to freeze)

Apply after any GSAman round:

| Observation | Action |
|-------------|--------|
| `priority.tsv` empty at your threshold | Freeze GFF → S1 Step 12 / DETAILED Step 13 |
| Protein BUSCO-C unchanged after round 2 | Stop genome-wide GSAman |
| Remaining issues are TE-like only | Document in METHODS; freeze |
| New deep Iso-seq arrives | Re-open **S3** on chromosomes that change |

Do not endless-polish for a 0.1% BUSCO bump.

---



---

## S13 — Helixer + Mikado (RAGNAROK-style)

**When:** GPU available; want a BRAKER-alternative automated draft, or second opinion beside S1.

### Steps

1–5. Asm0 → Asm1 → EDTA/ProtExcluder soft-mask → RNA (HISAT/STAR and/or Iso-seq minimap2).

6. **Helixer** `land_plant` on soft-masked or raw genome (follow Helixer docs) → Helixer GFF.

7. **StringTie** (+ optional TransDecoder) and **miniprot** proteins → evidence tracks.

8. **Mikado** pick with plant scoring (penalize Helixer microexons; see RAGNAROK YAML note) → `MERGED_GFF`.  
   Or run upstream [RAGNAROK](https://github.com/ryandkuster/ragnarok) end-to-end and import its GFF here.

9–12. Same as S1 from proteins / BUSCO / PSAURON / priority / GSAman / release.  
    Still apply Copetti stage QC if you also have a BRAKER set for comparison.

Peers: [`notes/ragnarok.md`](notes/ragnarok.md).

---

## S1 add-on — Copetti diagnostics (always after BRAKER)

After Step 5 (BRAKER), before trusting the merge:

```bash
# Point at GeneMark / Augustus / braker GTFs inside the BRAKER working dir + optional StringTie:
bash pipeline/A5d_stage_counts.sh \
  "$WORK_DIR/draft/braker3/GeneMark-ETP/.../genemark.gtf" \
  "$WORK_DIR/draft/braker3/Augustus/augustus.hints.gtf" \
  "$WORK_DIR/draft/braker3/braker.gtf" \
  "$WORK_DIR/rna/stringtie.gtf"
```

If BRAKER << other sets: TSEBRA rescue ([`tools/tsebra.md`](tools/tsebra.md)) before EVM. Full write-up: [`notes/copetti.md`](notes/copetti.md).



---

## S14 — EVM consensus path

**Merged runbook:** [`steps/dclab/`](steps/dclab/).  
**When:** You want the published Cantu Lab structural-annotation path (PASA → train Augustus/GeneMark → EVM → PASA polish), (further reading: [AnnotationPipeline2-EVM_based-DClab](https://github.com/CantuLab/AnnotationPipeline2-EVM_based-DClab).

### Steps (follow upstream docs for full flags)

1. **Asm0–Asm1** as usual; set vars per their `00-Setup.md` (`GENOME_FASTA`, `REPEAT_LIB`, `GENOME_PREFIX`, …).

2. **01 External evidences** — Iso-Seq HQ and/or related CDS / RNA assemblies.

3. **02 Repeats** — RepeatMasker `-xsmall`; build `repeats.gff3` for EVM ([`../tools/repeatmasker.md`](../tools/repeatmasker.md)).

4. **03–04 PASA training set → train Augustus + GeneMark-ET** ([`../tools/pasa.md`](../tools/pasa.md)).

5. **05–06** Genome-wide ab initio + transcript alignment tracks.

6. **07 EVM** with [`../config/evm_weights_cantulab.txt`](../config/evm_weights_cantulab.txt); then **PASA polish**.  
   Notes: [`notes/cantulab_evm.md`](notes/cantulab_evm.md).

7. **08 Filter** — no stop / &lt;50 aa:  
   ```bash
   bash pipeline/A5e_filter_proteins.sh path/to/gene_models.gff3 50
   ```

8. **09 Rename** (optional):  
   ```bash
   python3 pipeline/A6b_rename_gff.py VitisVinifera 1 chr models.checked.gff3 > models.named.gff3
   ```

9. **QC + last mile** — AGAT, BUSCO, PSAURON, priority, GSAman (S1 steps 9–12). Still apply Copetti `A5d` if you also have BRAKER.

**Do not copy** their absolute tool paths; clone upstream and point `SCRIPTS_DIR` / `EVM_TOOLS` at your install.

## Choosing a branch (one-liner)

| Evidence / goal | Branch |
|-----------------|--------|
| RNA + proteins, normal release | **S1** (BRAKER4 ETP if possible) |
| No RNA | **S2** |
| Deep Iso-seq | **S3** |
| Multiple haps | **S4** |
| Paper T2T bar | **S5** |
| Almost no evidence | **S6** |
| One family/QTL | **S7** |
| Want NCBI parallel | **S8** |
| High BUSCO-D | **S9** |
| Gene count exploded | **S10** |
| Quick lift | **S11** |
| Done polishing | **S12** |
