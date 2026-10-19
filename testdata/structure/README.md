# Toy data for the first run / 首次运行的玩具数据

<!-- Prose on this page is a placeholder. Replace each [[TODO-TEXT]] with reviewed text. -->

[[TODO-TEXT: this is simulated data (10 genes on two 30 kb chromosomes), not a real genome; used by scripts/first_run.sh.]]

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

[[TODO-TEXT: the planted cases (GC-AG intron, internal stop, gene without evidence, CDS inside a TE) and the WARN rows they cause.]]

## 中文

[[TODO-TEXT: 中文说明，内容与英文部分对应。]]
