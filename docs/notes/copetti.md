# Dario Copetti — practical plant annotation scheme

**Who:** [Dario Copetti](https://genome.arizona.edu/person/dario-copetti) (Arizona Genomics Institute / formerly ETH).  
**Sources we distilled:**

1. **Rabiosa (Italian ryegrass)** release notes — MAKER-P + custom TE library + RepeatMasker for genes/repeats/ncRNA ([CyVerse dataset](https://doi.org/10.25739/1e5z-pc33), Copetti 2021).  
2. **Live BRAKER troubleshooting** on a haploid plant assembly ([BRAKER issue #949](https://github.com/Gaius-Augustus/BRAKER/issues/949), 2025) — EDTA tracks, HISAT2/StringTie, BRAKER3-style run, miniprot from a related genus, stage-wise BUSCO and mono:multi ratios, TSEBRA over-filtering.

For the EVM consensus path, see [`cantulab_evm.md`](cantulab_evm.md) → [CantuLab/AnnotationPipeline2-EVM_based-DClab](https://github.com/CantuLab/AnnotationPipeline2-EVM_based-DClab). This page keeps Copetti’s **diagnostics** (stage counts, TSEBRA rescue, TE/browser habits). 

## Pattern A — Classical MAKER-P (Rabiosa-style)

```text
Assembly curated
  → custom / species TE library
  → RepeatMasker
  → MAKER-P (homology + ab initio)
  → TE / tRNA / ncRNA as separate tracks
```

**Use in this playbook when:** you already run MAKER-P on cluster, or need a second independent draft beside BRAKER (**compare**, do not silently merge without AGAT).

See [`../tools/maker_p.md`](../tools/maker_p.md).

## Pattern B — Modern BRAKER + diagnostics (issue #949)

```text
EDTA (TE annotation visible in browser)
  → soft-mask for predictors
  → HISAT2 RNA → optional StringTie models (external check)
  → BRAKER (BAM + Viridiplantae / clade proteins)
  → optional miniprot related-species genes as extra evidence
  → STAGE QC: GeneMark vs Augustus vs BRAKER counts + BUSCO + mono:multi
  → if BRAKER << Augustus/GeneMark: re-run TSEBRA with -k / lower intron support
  → GSAman / manual IGV on empty contigs and NLR windows
```

### Stage QC table (copy this habit)

After a BRAKER run, fill:

| Set | #genes | mono | multi | mono:multi | BUSCO-C | BUSCO-D | TE-like |
|-----|--------|------|-------|------------|---------|---------|---------|
| GeneMark | | | | | | | |
| Augustus | | | | | | | |
| BRAKER (TSEBRA) | | | | | | | |
| StringTie (external) | | | | | | | |
| miniprot lift | | | | | | | |

**Red flags (from #949):**

- BRAKER gene count **much lower** than GeneMark/Augustus + BUSCO-C drop → TSEBRA discarded unsupported multi-exon models.  
- Augustus **monoexonic explosion** → TE / soft-mask / training issue.  
- Long contigs with **zero** BRAKER models but TE annotation present → no RNA/protein hints on that contig; check BAM and protein mapping, not only TSEBRA.

**Hoff reply to use:** re-run TSEBRA enforcing Augustus or GeneMark (`-k`), or relax intron evidence in the cfg when RNA is thin.

Helper script: [`../../pipeline/A5d_stage_counts.sh`](../../pipeline/A5d_stage_counts.sh).

## What we adopted into *gene-function-annotation*

| Copetti habit | Where it lives |
|---------------|----------------|
| EDTA before gene call | [`../tools/edta.md`](../tools/edta.md), A0 |
| External StringTie as sanity track | [`../tools/stringtie.md`](../tools/stringtie.md), A1b |
| miniprot related species | [`../tools/miniprot.md`](../tools/miniprot.md), evidence pack |
| Stage BUSCO + mono:multi | A5d + DETAILED_GUIDE |
| TSEBRA rescue when gene count collapses | S1 note / [`../tools/tsebra.md`](../tools/tsebra.md) |
| MAKER-P as alternate classical stack | tools/maker_p + peer row |
| TE genes counted separately | S10 / ProtExcluder |

## Citation line for METHODS

> TE and gene-annotation operating practice follows public notes from Dario Copetti (MAKER-P + custom TE library for *Lolium* Rabiosa; BRAKER stage diagnostics as discussed in Gaius-Augustus/BRAKER#949), adapted for *Vitis*.
