# DeepKOALA (+ BlastKOALA / GhostKOALA)

- Classic: BlastKOALA / GhostKOALA — Kanehisa et al. *JMB* 2016; KEGG KO web assignment.  
- KofamKOALA / KofamScan — HMM KO (already optional in our F1b).  
- **DeepKOALA** — https://github.com/zhaoxi120/deepkoala ; *Briefings in Bioinformatics* / GenomeNet; GRU open-set KO assignment; much faster than BlastKOALA.  
- **Our mapping:** KO depth peers beside eggNOG KEGG columns and `F1b_kofam.sh`. Prefer local KofamScan/DeepKOALA for batch genomes; Blast/GhostKOALA for small web jobs.
