# Stage I/O — what goes in, what comes out

Use this while you run the playbook so each folder on disk has a meaning.  
Beginner path: [`QUICKSTART.md`](QUICKSTART.md). Branch IDs: [`steps/MAIN.md`](steps/MAIN.md).

Paths assume `WORK_DIR` from `config/local.env`. Names can vary; **role** matters more than exact filename.

## Big picture

| Layer | Repo | Primary product |
|-------|------|-----------------|
| Structure | **this repo** | Qualified GFF + `proteins.faa` + METHODS |
| Function | [`gene-function-annotation`](https://github.com/Xuzhen-Li/gene-function-annotation) | `functional_master.tsv` (+ METHODS) |

```text
reads / assembly
    → GENOME_FA (+ softmask)
    → draft GFF(s)  → merged GFF
    → proteins.faa
    → curated / release GFF + proteins
    → (optional) FA tables in sibling repo
```

## Shared early stages (every branch)

| Stage | You provide | You run / read | You should get | How you know it worked |
|-------|-------------|----------------|----------------|------------------------|
| **Asm0** | Raw HiFi / Hi-C / … | [`../pipeline/Asm0_assembly.md`](../pipeline/Asm0_assembly.md) | `GENOME_FA` (haplotype decision documented) | Contigs exist; ploidy choice written down |
| **Asm1** | `GENOME_FA` | [`../pipeline/Asm1_assembly_qc.md`](../pipeline/Asm1_assembly_qc.md) | QC notes; set `ASSEMBLY_OK=yes` | Genome BUSCO + N50 acceptable for *your* clade |
| **A0 / A0b** | Genome + **curated** TE lib | [`TE_LIBRARY.md`](TE_LIBRARY.md) + softmask notes | `GENOME_SOFT` + curated lib + exclusion list | Softmask file exists; raw EDTA not used as gold; NLR not in TE lib |
| **A1b** (if RNA) | RNA FASTQ | HISAT2/STAR | `RNA_BAM` (+ index) | Align rate sane; BAM indexes present |

## Draft → merge (branch-dependent; S1 shown)

| Stage | You provide | Helper | You should get | Check |
|-------|-------------|--------|----------------|-------|
| **A2** primary draft | `GENOME_SOFT`, proteins, optional `RNA_BAM` | `A2_run_draft.sh` | `DRAFT_GFF` (e.g. BRAKER) | Gene/mRNA counts non-zero (`A5_agat_stats.sh`) |
| **A2b / A2c** second set | Same genome + ref or GeMoMa | notes / Liftoff | `DRAFT_GFF_B` | Second track exists; not a duplicate empty file |
| **StringTie compare** (recommended if RNA) | `RNA_BAM` | your StringTie→TransDecoder | ORF/transcript GFF or FA for compare | Kept as **compare**, not silent replace of BRAKER |
| **A4** merge | Two (or more) drafts | `A4_merge_sets.sh` | `MERGED_GFF` | AGAT counts between the two parents; weights logged |
| **A5** structure QC | Merged GFF | `A5_agat_stats.sh` | `$AGAT_OUT/*.counts.txt` | Gene count vs related species × ploidy |
| **A3** proteins | GFF + genome | `A3_proteins_from_gff.sh` | `PROTEINS_FA` | One protein/gene (or documented isoform rule); FASTA headers match IDs |

## Last mile → release

| Stage | You provide | Helper | You should get | Check |
|-------|-------------|--------|----------------|-------|
| **01** | `PROTEINS_FA` | `01_qc_busco_psauron.sh` | BUSCO summary + `PSAURON_TSV` | BUSCO-C reported **with lineage name** |
| **02** | PSAURON (+ optional families) | `02_priority_loci.py` | `PRIORITY_TSV` | Worst-scoring loci listed for curation |
| **04** | Evidence + priority | GSAman notes | Edits in browser / curated GFF | Priority windows reviewed or explicitly deferred |
| **05** (multi-hap) | Dual hap GFFs | SynGAP notes | Polished models | Optional |
| **06** | Curated GFF | release notes | `RELEASE_TAG` folder: GFF + proteins + METHODS | [`PLAYBOOK.md`](PLAYBOOK.md) checklist all ticked |
| **A6** | Released proteins | — | Hand-off to FA repo | Do **not** invent GO in this repo |

## Liftover-first path (S11)

| Stage | In | Out | Check |
|-------|----|-----|-------|
| Liftoff / LiftOn / CAT | `REF_FA` + `REF_GFF` + target genome | Lifted GFF | Coverage of conserved genes; mark `status=provisional` until QC |
| Fill gaps | Same as S1/S2 as needed | Merged improved GFF | Document what was lifted vs de novo |

## What *not* to expect from this repo

- GO / KEGG / InterPro tables → sibling FA repo  
- Automatic write-back of function into GFF column 9 → not claimed  
- Private BAM/FASTQ in git → never  

## Suggested `WORK_DIR` layout

```text
$WORK_DIR/
  genome/           # GENOME_FA, GENOME_SOFT
  rna/              # BAM + index
  draft/            # DRAFT_GFF, DRAFT_GFF_B, MERGED_GFF
  agat/             # count + stats dumps
  qc/               # BUSCO, PSAURON, stage_qc
  curated/          # after GSAman
  release/<TAG>/    # public products only
```
