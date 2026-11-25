# Chapter 12. Curation and browsers

*This chapter reproduces [README section 11](../../README.md#section-11): the section notes, the full tool table with paper, lab, tier and evaluation, and the benchmark notes. Links point back into the repository.*

Evidence packs, browsers and editors used in last-mile curation (LM03–LM04).

**Needs:** the draft GFF, genome, and an evidence pack (BAM, protein alignments, RNA coverage) before GSAman or a browser session. [Data needs by scenario](../../README.md#data-needs)

**Clusters:**
- *Collaborative web curation* (complementary): Apollo 3, JBrowse 2. Apollo 3 runs as a plugin on JBrowse 2; use the two together for team curation.
- *Desktop and manual curators* (alternatives): IGV, Artemis / ACT, GSAman, TBtools-II. Use for local inspection of a few loci; GSAman handles LM04 edits.


| Tool | Role | What it does / when to use | Paper | Lab (corresponding author, institution) | Tier · citations | Evaluation (source) |
|---|---|---|---|---|---|---|
| [IGV](https://github.com/igvteam/igv) | alternative, general-purpose | Desktop genome viewer for alignments and annotations. | [Nature Biotechnology 2011](https://doi.org/10.1038/nbt.1754) | James T Robinson (Broad Institute) +1 | standard · 16992 | GitHub last push 2026-11 |
| [igv.js / igv-reports](https://github.com/igvteam/igv-reports) | alternative, general-purpose | Embeddable IGV; igv-reports builds self-contained HTML pages of loci with tracks. | [Bioinformatics 2022](https://doi.org/10.1093/bioinformatics/btac830) | James T Robinson (University of California San Diego) | standard · 648 | GitHub last push 2026-11 |
| [Artemis / ACT](https://github.com/sanger-pathogens/Artemis) | alternative, general-purpose | Genome browser/annotation editor and comparison tool. | [Bioinformatics 2011](https://doi.org/10.1093/bioinformatics/btr703) | Tim J. Carver (Wellcome Sanger Institute) | standard · 1410 | Paper: “We present Artemis as a tool for integrated visualization and computational analysis of different types of HTS datasets in the context of a reference genome and its corresponding annotation.”; GitHub last push 2025-12 |
| [Apollo 3](https://github.com/GMOD/Apollo3) | alternative | Collaborative gene-model editor built on JBrowse 2 for local or server deployment. Apollo 2 (2019 paper, doi:10.1371/journal.pcbi.1006790) is the older server release; use it only when a community portal still runs it. | [bioRxiv (Cold Spring Harbor Laboratory) 2026](https://doi.org/10.64898/2026.06.08.730970) | Ian H Holmes (University of California, Berkeley) | newer · 1 | Authors: “Its functionality is inspired by existing manual genome annotation tools such as Apollo, Artemis, and Otter, combining features from those tools with an updated and more scalable architecture and technology stack.”; GitHub last push 2026-11 |
| [JBrowse 2](https://github.com/GMOD/jbrowse-components) | alternative, general-purpose | Genome browser with synteny and SV views; host evidence tracks for curation. | [Genome biology 2023](https://doi.org/10.1186/s13059-023-02914-z) | Ian H Holmes (University of California, Berkeley) | standard · 907 | Authors: “These improvements are enabled by a ground-up redesign using modern web technology.”; GitHub last push 2026-11 |
| GSAman | alternative | Desktop curator for editing gene-structure models against aligned evidence; serves as the LM04 manual curation tool. | [The Innovation 2026](https://doi.org/10.1016/j.xinn.2026.101471) | Chengjie Chen (South China Agricultural University) +2 | newer · 5 | Authors: “In contrast to web-based platforms such as Apollo2, which generally require server deployment and do not provide full offline functionality, GSAman delivers a fully local, responsive interface for real-time annotation refinement, thereby improving …” |
| [TBtools-II](https://github.com/CJ-Chen/TBtools-II) | alternative, general-purpose | Plant-focused desktop toolkit for GFF viewing, sequence extraction and gene-structure plotting; convenient for quick checks on a few loci. | [Molecular Plant 2023](https://doi.org/10.1016/j.molp.2023.09.010) | Chengjie Chen (South China Agricultural University) +1 | standard · 4462 | GitHub last push 2026-10 |
| ORCAE | alternative | Wiki-style web resource for community curation of gene models. | [Nature Methods 2012](https://doi.org/10.1038/nmeth.2242) | Lieven Sterck (Ghent University) | established · 226 | no abstract or repo text available; see paper |
