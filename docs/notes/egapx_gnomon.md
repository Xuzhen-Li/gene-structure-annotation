# NCBI EGAPx / Gnomon (institutional)

- EGAPx: https://github.com/ncbi/egapx — public eukaryotic annotation (CGR); vertebrates/arthropods/plants.  
- Core idea mirrors RefSeq EGAP: STAR/minimap2 RNA + miniprot/ProSplign proteins → **Gnomon** chaining + HMM ab initio; orthology naming; optional tRNAscan/cmsearch ncRNA.  
- 2026: GenBank accepts EGAPx ASN submissions; auto BUSCO lineage; long-read RNA support.  
- Internal RefSeq EGAP remains NCBI-side (https://www.ncbi.nlm.nih.gov/refseq/annotation_euk/process/).  
- **Our mapping:** S8-class institutional peer (`pipeline/A2d_egapx_optional.md`). Use when targeting GenBank-ready packages; still soft-mask/QC locally. Does not replace evidence-first S1 for every paper.
