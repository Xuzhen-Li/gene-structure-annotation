# Tiberius

- GitHub: https://github.com/Gaius-Augustus/Tiberius  
- Papers: Gabriel et al. *Bioinformatics* 2024 (end-to-end DL + differentiable HMM); multi-clade extension (bioRxiv / Methods Mol Biol lineage — Mesangiospermae, Fungi, Vertebrata, Insecta, Chlorophyta, Bacillariophyta).  
- Web server: https://bioinf.uni-greifswald.de/tiberius  
- Same lab lineage as AUGUSTUS/BRAKER; often stronger than Helixer on mammals; multi-clade models aim near BRAKER3 accuracy without evidence in several groups, much faster on GPU.  
- Modes: ab initio; optional evidence combination; Nextflow parallelization.

**Our mapping:** AI ab initio peer for S13-class runs; natural compare/combine with BRAKER4 (same ecosystem). Prefer Tiberius when GPU throughput matters and RNA is absent; prefer BRAKER ETP when BAM+proteins exist.
