# OMArk · compleasm (annotation/assembly QC)

- OMArk: Nevers et al. *Nat Biotechnol* 2024 doi:10.1038/s41587-024-02147-w — proteome completeness **and** consistency vs OMA families; flags contamination/dubious proteins (beyond BUSCO-only).  
- compleasm: https://github.com/huangnengCSU/compleasm — miniprot+BUSCO orthologs; often faster/more accurate completeness than BUSCO genome mode.  
- Already hooked via `pipeline/A5b_omark_compleasm.sh`.  
- **Our mapping:** qualify checklist — report BUSCO **and** OMArk/compleasm before release.
