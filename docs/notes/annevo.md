# ANNEVO (Kai Ye / 叶凯 lab, XJTU)

- GitHub: https://github.com/xjtu-omics/ANNEVO  
- Paper: *Nat Genet* / EuropePMC record — “Highly accurate ab initio gene annotation with ANNEVO” (Ye & colleagues; MoE genomic LM).  
- Contact / license: non-commercial academic free; commercial needs license (kaiye@xjtu.edu.cn / listed contacts on repo). **Not GPL/OSI.**  
- Idea: mixture-of-experts genomic language model → ab initio gene structures from sequence; models distal context + cross-species evolutionary signal.  
- Lineages on CLI: `Mammalia`, `Insecta`, `Aves`, `Actinopteri`, `Magnoliopsida`, `Fungi`.  
- One-shot: `python annotation.py -g genome.fa -m model -l Magnoliopsida -o out.gff ...` (GPU predict + CPU decode).  
- Benchmarks claimed vs classical ab initio and competitive with evidence pipelines on diverse taxa; can patch reference gaps (e.g. BUSCO fixes validated by RNA).

**Our mapping:** AI ab initio peer beside Helixer / Tiberius / S13. Evidence-first default remains S1 (BRAKER). Use ANNEVO when GPU available and extrinsic evidence is thin, or as an independent draft to compare against BRAKER/EVM. Respect license for any public redistribution of outputs/workflows.
