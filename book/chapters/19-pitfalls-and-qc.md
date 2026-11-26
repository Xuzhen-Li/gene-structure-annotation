# Chapter 19. Pitfalls and quality control

## 19.1 Pitfalls the repository already names

These come from the README section Data needed alongside the genome and from `docs/EVALUATION.md`.

- TE library construction is a separate job in TE-Lib; this repository only soft-masks with a trusted library.
- Functional labels (GO, KEGG, domains, names, NLR and TF classes) belong in gene-function-annotation. A protein tool that says structure usually means 3D structure, not gene models.
- `grade=` and `status=` are separate fields; a provisional set is not L1.
- A close reference means the same species or cultivar (or a near-identical haplotype) with a curated GFF you trust, not any GFF from the same family.
- The BUSCO lineage must match the clade, and odb10 versus odb12 must be recorded (`docs/LINEAGES.md`). Compleasm is a useful comparison, not an automatic replacement.
- High BUSCO duplication can be real haplotypes (S9); do not purge haplotypes only to lower it.
- If gene counts collapse after TSEBRA, run the A5d mono-exonic to multi-exonic ratio check before accepting the merge.

## 19.2 Pitfalls from the literature

- **Chimeric genes.** Adjacent genes fused into one model are common in plant annotations and persist because later work copies them; machine-learning predictors such as Helixer helped to find them ([doi:10.1186/s12864-025-11765-w](https://doi.org/10.1186/s12864-025-11765-w)).
- **RNA alone is not enough.** Transcripts from RNA alignments alone are not sufficient; combine evidence-based and ab initio prediction ([doi:10.1002/aps3.11533](https://doi.org/10.1002/aps3.11533)).
- **Isoforms are hard.** Exons are found well, but complete isoforms remain a challenge ([doi:10.1038/nmeth.2714](https://doi.org/10.1038/nmeth.2714)); with long reads, read length and accuracy matter more than depth for transcript discovery ([doi:10.1038/s41592-024-02298-3](https://doi.org/10.1038/s41592-024-02298-3)).
- **Small RNA calls.** Many plant miRNA annotations are questionable because siRNAs were called miRNAs; updated criteria require replication and small RNA sequencing ([doi:10.1105/tpc.17.00851](https://doi.org/10.1105/tpc.17.00851)).
- **Downstream effects.** Different annotation sources give markedly different orthology results ([doi:10.1093/bioinformatics/btaf365](https://doi.org/10.1093/bioinformatics/btaf365)), so record the annotation source and version in METHODS.
- **Duplicated haplotigs.** Heterozygous regions can be assembled twice, which breaks contiguity and confuses annotation ([doi:10.1093/bioinformatics/btaa025](https://doi.org/10.1093/bioinformatics/btaa025)); check this in assembly QC, not by deleting genes.

## 19.3 A quality-control checklist

| Check | Tool | What a problem looks like | Source |
|---|---|---|---|
| Genome completeness before annotation | BUSCO genome mode, compleasm | Many missing BUSCOs: fix the assembly first | [doi:10.1093/molbev/msab199](https://doi.org/10.1093/molbev/msab199), [doi:10.1093/bioinformatics/btad595](https://doi.org/10.1093/bioinformatics/btad595) |
| Proteome completeness | BUSCO protein mode | Lower than genome mode: genes were missed | [doi:10.1093/molbev/msab199](https://doi.org/10.1093/molbev/msab199) |
| Consistency and contamination | OMArk | Many proteins inconsistent with the lineage, or contaminant species | [doi:10.1038/s41587-024-02147-w](https://doi.org/10.1038/s41587-024-02147-w) |
| Per-protein plausibility | PSAURON | Low scores flag spurious proteins | [doi:10.1093/nargab/lqae189](https://doi.org/10.1093/nargab/lqae189) |
| Structure counts | AGAT, gffread | Gene, mRNA and CDS counts far from related species; invalid GFF3 | [doi:10.12688/f1000research.23297.2](https://doi.org/10.12688/f1000research.23297.2); AGAT [doi:10.5281/zenodo.3552717](https://doi.org/10.5281/zenodo.3552717) |
| Mono-exonic to multi-exonic ratio | A5d stage counts | A jump after a merge | [doi:10.1002/aps3.11533](https://doi.org/10.1002/aps3.11533); `docs/TOOLS.md` |
| Visual check of hard loci | JBrowse 2, GSAman, Apollo 3 | Fused or split models against RNA and protein tracks | [doi:10.1186/s13059-023-02914-z](https://doi.org/10.1186/s13059-023-02914-z), [doi:10.1016/j.xinn.2026.101471](https://doi.org/10.1016/j.xinn.2026.101471) |

Acceptance levels and gates are defined in [`docs/EVALUATION.md`](../../docs/EVALUATION.md) and [`docs/EVALUATION_CHECKLIST.md`](../../docs/EVALUATION_CHECKLIST.md).
