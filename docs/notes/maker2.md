# MAKER / MAKER2 (mainstream, high citation)

- MAKER2: Holt & Yandell, *BMC Bioinformatics* 2011 (doi:10.1186/1471-2105-12-491) — extremely widely adopted eukaryotic annotation framework.  
- Combines SNAP / AUGUSTUS / GeneMark ab initio with protein and transcript evidence; **AED** quality metric; mRNA-seq support; reannotation pass-through.  
- Still the “textbook” pipeline in many core facilities and teaching courses.

**Our mapping:** alternate full stack parallel to BRAKER+EVM. We do not default to MAKER (BRAKER3/4 + optional EVM is lighter for many new genomes), but METHODS may cite MAKER2 when that is the lab standard. AED idea informs our qualify checklist (QC metrics before release).
