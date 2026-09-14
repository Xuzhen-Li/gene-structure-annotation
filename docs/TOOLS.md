# Tools — gene **structure** (this repo)

How to install/run each **structure** program. Workflow order: [`DETAILED_GUIDE.md`](DETAILED_GUIDE.md) · auto-plan: [`../pipeline/flow_tool/`](../pipeline/flow_tool/).

Functional tools → [gene-function-annotation](https://github.com/Xuzhen-Li/gene-function-annotation).

Workflow order lives in [`DETAILED_GUIDE.md`](DETAILED_GUIDE.md).  
This page is **tool literacy**: what each program is for, how to get it, a minimal working command, outputs, and common failures.

Prefer **containers** (Docker / Singularity / Apptainer) over compiling by hand. Paths below are templates — put your image tags and module names in `config/local.env`.

## Functional tools

**Not in this repo.** After `proteins.faa` exists, use [gene-function-annotation](https://github.com/Xuzhen-Li/gene-function-annotation) (`docs/TOOLS.md` / F1). Do not look for eggNOG / InterProScan / AHRD pages here.

---
## Order (upstream structural S1 — do not skip around)

Use tools **in this sequence**. Later steps assume earlier outputs exist.

| # | Tool | Makes | Next needs |
|---|------|-------|------------|
| 1 | [hifiasm](tools/hifiasm.md) | contigs | scaffolding / QC |
| 2 | [YaHS](https://github.com/c-zhou/yahs) *(external; optional Hi-C scaffold)* *(if you have Hi-C)* | chrom-scale `GENOME_FA` | Asm1 |
| 3 | [BUSCO](tools/busco.md) *(genome mode)* | Asm1 pass/fail | soft-mask only if pass |
| 4 | [EDTA](tools/edta.md) *(or curated lib)* + [ProtExcluder](tools/protexcluder.md) | TE lib / anno | soft-mask |
| 5 | [RepeatMasker](tools/repeatmasker.md) / EDTA `make_masked.pl` | `GENOME_SOFT` | RNA + drafts |
| 6 | [HISAT2 / STAR](tools/hisat2_star.md) (+ optional [StringTie](tools/stringtie.md)) | `RNA_BAM` | BRAKER3, GSAman, Mikado |
| 7 | [BRAKER4](tools/braker4.md) *(preferred)* or [BRAKER3](tools/braker3.md) | primary `DRAFT_GFF` | second predictor |
| 8 | [GeMoMa](tools/gemoma.md) *or* [Liftoff](tools/liftoff.md) *(or [miniprot](tools/miniprot.md) evidence)* | `DRAFT_GFF_B` | merge |
| 8b | *(S13)* [Helixer](tools/helixer.md) | ab initio GFF | Mikado |
| 9 | [EVM](tools/evm.md) *or* [TSEBRA](tools/tsebra.md) *or* [Mikado](tools/mikado.md) | `MERGED_GFF` | proteins |
| 9b | [A5d stage counts](../pipeline/A5d_stage_counts.sh) (Copetti) | mono:multi table | catch TSEBRA collapse |
| 10 | [AGAT + gffread](tools/agat_gffread.md) | stats + `PROTEINS_FA` | QC |
| 11 | [BUSCO](tools/busco.md) *(protein)* + [PSAURON](tools/psauron.md) | scores | priority list |
| 12 | *(optional S5)* [OMArk / Compleasm](tools/omark_compleasm.md) | extra QC tables | curation |
| 13 | [GSAman](tools/gsaman.md) | `CURATED_GFF` | re-QC + release |
| 14 | AGAT / gffread / BUSCO again | release package | freeze `RELEASE_TAG` |

**Branch inserts (only when that scenario applies):**

| When | Insert / replace |
|------|------------------|
| No RNA (**S2**) | Skip #6; use [GALBA](tools/galba.md) at #7 instead of BRAKER3 |
| Deep Iso-seq (**S3**) | Add [minimap2](tools/minimap2.md) after #5; [EviAnn](tools/eviann.md) as #7; BRAKER as secondary; EviAnn-backbone merge |
| Multi-hap (**S4**) | After #13 on ref: Liftoff each hap → [SynGAP](tools/syngap.md) → GSAman conflicts only |
| NCBI parallel (**S8**) | Run [EGAPx](tools/egapx.md) beside #7–#11; compare, do not auto-replace |
| TE inflation (**S10**) | Stop; go back to #4–#5; restart from #7 |
| Lift-only (**S11**) | After #3 (light): only Liftoff → AGAT; skip BRAKER/EVM/GSAman claim |
| Helixer path (**S13**) | #8b Helixer → #9 Mikado instead of BRAKER+EVM |
| EVM consensus (**S14**) | Repeats → [PASA](tools/pasa.md) train Augustus/GeneMark → EVM (cantulab weights) → PASA polish → A5e filter → A6b rename |
| BRAKER gene collapse | After #7 run #9b; TSEBRA `-k` rescue (Copetti) |

**Install order on a new machine** (so you can actually run the sequence above):

1. `samtools`, `seqkit`, `gffread`, `agat`  
2. `busco` + download `viridiplantae_odb12` once  
3. `hisat2` or `STAR`, `minimap2`  
4. `RepeatMasker` + TE lib  
5. BRAKER3 container (largest)  
6. Liftoff → EVM / GeMoMa → PSAURON → GSAman as needed  

## Map: stage → tool pages

| Stage | Tools |
|-------|--------|
| Assembly | [`tools/hifiasm.md`](tools/hifiasm.md), [YaHS](https://github.com/c-zhou/yahs) |
| Soft-mask | [`tools/edta.md`](tools/edta.md), [`tools/repeatmasker.md`](tools/repeatmasker.md), [`tools/protexcluder.md`](tools/protexcluder.md) |
| RNA / Iso-seq | [`tools/hisat2_star.md`](tools/hisat2_star.md), [`tools/stringtie.md`](tools/stringtie.md), [`tools/minimap2.md`](tools/minimap2.md) |
| Draft genes | [`tools/braker4.md`](tools/braker4.md), [`tools/braker3.md`](tools/braker3.md), [`tools/galba.md`](tools/galba.md), [`tools/gemoma.md`](tools/gemoma.md), [`tools/eviann.md`](tools/eviann.md), [`tools/liftoff.md`](tools/liftoff.md), [`tools/helixer.md`](tools/helixer.md), [`tools/maker_p.md`](tools/maker_p.md), [`tools/miniprot.md`](tools/miniprot.md) |
| Merge | [`tools/evm.md`](tools/evm.md), [`tools/tsebra.md`](tools/tsebra.md), [`tools/mikado.md`](tools/mikado.md), [`tools/pasa.md`](tools/pasa.md) |
| GFF / proteins | [`tools/agat_gffread.md`](tools/agat_gffread.md) |
| QC | [`tools/busco.md`](tools/busco.md), [`tools/psauron.md`](tools/psauron.md), [`tools/omark_compleasm.md`](tools/omark_compleasm.md) |
| Curation | [`tools/gsaman.md`](tools/gsaman.md), [`tools/syngap.md`](tools/syngap.md), [HRP (FA repo)](https://github.com/Xuzhen-Li/gene-function-annotation/blob/main/docs/tools/hrp.md) |
| Optional NCBI | [`tools/egapx.md`](tools/egapx.md) |

## Shared habits

1. **Soft-masked genome** for BRAKER / GALBA (`-xsmall` / lowercase), not hard `N` mask.  
2. **One working directory per tool** under `$WORK_DIR/...` so logs are recoverable.  
3. **Record versions** in METHODS (`braker.pl --version`, `busco -v`, …).  
4. After every structural step: `bash pipeline/A5_agat_stats.sh that.gff3`.  
5. If a script prints `[STOP]`, it printed the command for *you* to run in your container — that is expected until you wire the image.

Protein DB: OrthoDB Viridiplantae / eudicots for BRAKER; PN40024 FA+GFF for Liftoff/GeMoMa.
