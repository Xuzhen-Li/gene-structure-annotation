# 03 — Evidence pack for GSAman (detailed)

Load into the browser (paths absolute):

| Track | Why |
|-------|-----|
| Soft-masked FASTA | Sequence + TE context |
| Current GFF (`MERGED_GFF` or curated) | Models to edit |
| Illumina RNA BAM | Intron / coverage |
| Iso-seq BAM (if any) | Exon truth |
| Miniprot / GenomeThreader proteins | ORF support |
| Homolog GFF (PN40024 Liftoff) | Conserved structure |
| `priority.tsv` | Work order |

## Per locus before you click “fixed”
- [ ] Start codon / stop agree with protein evidence  
- [ ] Splice sites match RNA or Iso-seq  
- [ ] Not a TE ORF (check soft-mask + domains)  
- [ ] Tandem copy not collapsed into neighbor ([`ERROR_CLASSES.md`](../docs/ERROR_CLASSES.md))  
- [ ] Changelog row written  

Next: [`04_gsaman_curation.md`](04_gsaman_curation.md)
