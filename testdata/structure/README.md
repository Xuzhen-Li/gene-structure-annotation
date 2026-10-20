# Toy data for the first run / 首次运行的玩具数据

This folder holds about 70 kB of simulated toy data (not a real genome) that you run by opening a terminal (on Mac: Terminal app; on Linux: a terminal window; on a cluster: your login shell) inside the `gene-structure-annotation` folder and typing `bash scripts/first_run.sh`. It contains two simulated chromosomes of 30 kb each (a chromosome is a long DNA molecule, and 1 kb is 1,000 DNA bases), 10 genes, and 11 transcripts (a transcript is an RNA copy read from a gene). It also includes protein evidence for 6 genes from a pretend close relative with about 5 % of residues changed (a residue is one amino acid building block in a protein), RNA-seq reads (short sequencing fragments from expressed RNA), transcripts, and a TE annotation (a TE, or transposable element, is a mobile DNA sequence that can copy itself around the genome). Rebuilding this dataset gives the exact same bytes every time.

| File | Stands in for |
|---|---|
| `genome.fa` | assembled genome (soft-masked copy not needed for the toy) |
| `draft.gff3` | BRAKER output `braker.gff3` |
| `protein_db.faa` | protein evidence from a close relative (6 genes, ~5 % residues changed) |
| `rnaseq.bam` | RNA-seq alignments (HISAT2/STAR) |
| `rnaseq_junctions.tsv` | junctions from `rnaseq.bam` (chrom, start, end, reads) |
| `transcripts.gtf` | StringTie transcripts |
| `te.gff3` | TE annotation (EDTA) |
| `te_lib.fa` | trusted TE library |
| `expected/first_run_files.txt` | files `scripts/first_run.sh` must produce |
| `expected/qc_summary.key.tsv` | metric, value, threshold, status expected in `qc_summary.tsv` |

Rebuild (same bytes every time): `python3 testdata/structure/make_toy.py`

The simulated genes include planted problems to test quality checks: gene `g04` has a GC-AG intron (an intron is a non-coding segment spliced out of RNA, and GC-AG is a rarer boundary pattern than standard GT-AG), `g05` has an internal stop codon (a stop codon is a three-base signal that ends protein translation early when it appears inside a gene), `g06` has no supporting evidence and gets an AED of 1 (AED, or Annotation Edit Distance, measures how much a predicted gene differs from the experimental evidence from 0 to 1), `g07` has its coding sequence (the part of a gene translated into protein) inside a TE, and `g08` has a last exon (an exon is a retained RNA segment in the final transcript) without evidence. In `qc_summary.tsv`, these planted problems trigger `WARN` rows where thresholds are rules of thumb: `splice_gt_ag_share` is 0.9412 (below 0.98), `internal_stop_share` and `protein_fasta_internal_stop_count` flag 1 stop, `aed_eq_1_share` is 0.0909 (above 0.05), `te_overlap_gene_share` is 0.1, and `te_overlap_cds_base_share` is 0.1069 (above 0.01). Other `WARN` rows come only from the tiny dataset size, including `gene_count` at 10, `exons_per_gene_mean` at 2.6, and `NA` values for every BUSCO and OMArk row (BUSCO and OMArk are tools that check annotation completeness against known gene families, and they are not run on this toy data).

## 中文

本文件夹包含约 70 kB 的模拟测试数据（并非真实基因组），请打开终端（Mac 上为 Terminal 应用，Linux 上为终端窗口，集群上为登录 shell）并进入 `gene-structure-annotation` 文件夹，输入 `bash scripts/first_run.sh` 即可运行。数据包含两条各 30 kb 的模拟染色体（染色体是长链 DNA 分子，1 kb 为 1,000 个碱基）、10 个基因和 11 条转录本（转录本是由基因转录出的 RNA 序列），并提供来自假想近缘物种的 6 个基因的蛋白证据（约 5 % 的氨基酸残基发生改变，残基即构成蛋白质的单个氨基酸单元）、RNA-seq 测序读段（来自表达 RNA 的短测序片段）、转录本以及 TE 注释（TE 即转座子，是一类可在基因组中移动或复制的 DNA 序列），每次重新生成都会得到完全相同的字节内容。这些基因内置了预设问题来测试质控检查：`g04` 含有一个 GC-AG 内含子（内含子是 RNA 剪接时被切除的非编码片段，GC-AG 是比标准 GT-AG 更少见的边界模式），`g05` 含有内部终止密码子（终止密码子是结束蛋白质翻译的三碱基信号，出现在基因内部会导致翻译提前终止），`g06` 没有支持证据因此 AED 为 1（AED 即注释编辑距离，用 0 到 1 衡量预测基因与实验证据的差异程度），`g07` 的编码序列（基因中翻译为蛋白质的部分）位于 TE 内部，`g08` 的最后一个外显子（外显子是成熟转录本中保留的 RNA 片段）缺乏证据支持。在 `qc_summary.tsv` 中，这些问题会触发基于经验阈值的 `WARN` 行，包括 `splice_gt_ag_share` 为 0.9412（低于 0.98）、`internal_stop_share` 与 `protein_fasta_internal_stop_count` 报告 1 个内部终止、`aed_eq_1_share` 为 0.0909（高于 0.05）、`te_overlap_gene_share` 为 0.1 以及 `te_overlap_cds_base_share` 为 0.1069（高于 0.01）；其余 `WARN` 行仅因测试集极小而产生，包括 `gene_count` 为 10、`exons_per_gene_mean` 为 2.6，以及所有 BUSCO 和 OMArk 行显示为 `NA`（BUSCO 和 OMArk 是基于已知基因家族评估注释完整性的工具，不会在该测试数据上运行）。
