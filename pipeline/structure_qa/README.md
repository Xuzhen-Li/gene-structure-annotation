# Structure QA step / 结构注释质量评估

<!-- All prose on this page is a placeholder. Replace each [[TODO-TEXT]] with reviewed text. -->

## English

This step assesses the quality of your genome structure annotation. It sits after the consensus merge step and before release or handoff. A WARN means look, not delete. The example BUSCO, OMArk and gffcompare results are simulated.

### Inputs

| Input | Flag | Required |
|---|---|---|
| Consensus GFF3 from the merge step (`MERGED_GFF`: `$AGG_DIR/evm/evm.EVM.gff3`, or `pasa_updated.gff3` after the PASA update) | `--gff` | yes |
| Genome FASTA | `--genome` | yes |
| Protein FASTA (IDs = mRNA IDs) | `--proteins` | no |
| Evidence models, `NAME=PATH` (GTF/GFF3) | `--evidence` | no |
| RNA-seq BAM, or junction table | `--bam` / `--junctions` | no |
| TE annotation (GFF3 / BED / RepeatMasker `.out`) | `--te` | no |
| Settings and thresholds | `--config` (default `config/structure_qa.ini`) | no |

The `--gff` input is the required consensus GFF3 from the merge step.
The `--genome` input is the required genome FASTA.
The `--proteins` input is an optional protein FASTA with IDs equal to mRNA IDs.
The `--evidence NAME=PATH` input provides optional evidence models in GTF or GFF3 format.
The `--bam` or `--junctions` inputs provide an optional RNA-seq BAM or a junction table.
The `--te` input provides the optional TE (transposable element) annotation as GFF3, BED or RepeatMasker .out format.
The `--config` input comes from copying config/structure_qa.ini and editing the copy.

### Steps (one file each)

| File | Checks | Main output |
|---|---|---|
| `qa01_longest_isoform.py` | one protein per gene (longest CDS, by Parent) | `longest_isoform.proteins.faa` |
| `qa02_busco.py` | BUSCO protein mode per lineage; genome mode as upper bound; gap | `busco/` |
| `qa03_omark.py` | OMArk consistent / inconsistent / contaminant / unknown | `omark/` |
| `qa04_evidence_aed.py` | gffcompare vs each evidence set; AED per transcript; AED = 1 flag list | `aed_per_transcript.tsv`, `aed1_flagged.tsv` |
| `qa05_rnaseq_junctions.py` | RNA-seq junction support | `rnaseq_junctions.tsv` |
| `qa06_gene_stats.py` | gene count, exons, introns, single-exon share | `intron_length_hist.tsv` |
| `qa07_internal_stops.py` | internal stops (`*` or `.`), terminal stop, frame | `internal_stops.tsv` |
| `qa08_te_overlap.py` | CDS inside TE features | `te_overlap_genes.tsv` |
| `qa09_splice_sites.py` | GT-AG / GC-AG / AT-AC / other | `noncanonical_introns.tsv` |
| `qa10_summary.py` | joins all metrics with thresholds | `qc_summary.tsv` |
| `run_structure_qa.py` | runs qa01 to qa10 in order | all of the above |

qa01: This check keeps one protein per gene. It groups them by Parent. It prefers isoforms without an internal stop. It then prefers the longest protein. The smallest transcript ID wins on a full tie. It writes longest_isoform.proteins.faa.
qa02: This check runs BUSCO in protein mode on the longest isoforms per lineage. The gap is genome C minus annotation C in points. BUSCO only measures completeness of conserved single copy genes. The letters C, S, D, F and M mean complete, single copy, duplicated, fragmented and missing. A high D means isoforms were not deduplicated. It can also mean genes are split or chimeric.
qa03: This check reports OMArk shares as a percent of the proteome. The shares are consistent, inconsistent, contaminant, unknown and missing.
qa04: This check runs gffcompare against each evidence set. The annotation edit distance is called AED. AED equals 1 minus the mean of sensitivity and precision on exon bases. Transcripts with AED = 1 are listed in aed1_flagged.tsv. AED = 1 is a flag. It is not a deletion. Without evidence files and without an AED attribute, AED is NA, not 1.
qa05: This check measures RNA seq junction support for the longest isoform of multi exon genes. A junction counts with at least junction_min_reads.
qa06: This check writes intron_length_hist.tsv. It reports gene count, exons per gene, intron lengths and single exon share.
qa07: This check writes internal_stops.tsv. It looks for internal stops written as * or ., terminal stops, frame issues, and missing starts or stops.
qa08: This check writes te_overlap_genes.tsv for genes whose CDS lies at least 0.5 inside TE features. Simple_repeat and Low_complexity are not treated as TE.
qa09: This check writes noncanonical_introns.tsv. It classifies intron splice sites as GT AG, GC AG, AT AC or other.
qa10: This check joins all metrics with the thresholds into qc_summary.tsv. Every threshold is a rule of thumb. You should compare your results with close relative genomes annotated the same way. A WARN means look, not delete. The thresholds for aed_eq_1_share, gene_count and exons_per_gene_mean are not from the guidance. A consensus model is not a validated gene.

### Run

```bash
python3 pipeline/structure_qa/run_structure_qa.py \
  --gff "$MERGED_GFF" --genome "$GENOME_FA" --proteins "$PROTEINS_FA" \
  --evidence transcripts=stringtie.gtf --evidence proteins=miniprot.gff3 \
  --bam "$RNA_BAM" --te TEanno.gff3 \
  --out "$WORK_DIR/qc/structure_qa"
# BUSCO / OMArk / gffcompare run only with RUN=1:
RUN=1 python3 pipeline/structure_qa/run_structure_qa.py ...
```

The default mode prints commands for the heavy tools like BUSCO, OMAmer, OMArk and gffcompare. You set RUN=1 to actually run them. The script reuses existing results found in the --out folder. You set the BUSCO lineages using busco_protein_lineages and busco_genome_lineages. You set the OMAmer database path using omamer_db. Lineage names change between dataset versions. You check your names with busco --list-datasets.

### Output: `qc_summary.tsv`

Columns: `metric`, `value`, `threshold`, `status` (PASS / WARN / INFO), `basis`, `step`, `note`.

The summary file shows PASS or WARN for metrics with a threshold. A missing value is a WARN. Every threshold is a rule of thumb. Compare your results with close relative genomes annotated the same way. A WARN means look, not delete. AED = 1 is a flag, not a deletion, and a consensus model is not a validated gene. BUSCO only measures completeness of conserved single copy genes.

### Try it on the simulated example

```bash
bash examples/structure_qa_sim/run_example.sh
python3 -m unittest discover -s tests -v
```

The example BUSCO, OMArk and gffcompare results are simulated to yield ten WARN rows. Gene g04 has a GC AG intron and gene g05 has an internal stop. Gene g06 has no evidence so its AED is 1. Gene g07 has its CDS inside a TE. A TE is a transposable element. The mock eudicotyledons BUSCO result gives two WARN rows for C 88 and a gap of 6.5 points. The gene_count and exons_per_gene_mean metrics warn only because the example is tiny.

## 中文

这个质量评估步骤位于合并共识结果之后与发布之前。流程必需 --gff 文件和 --genome 文件作为输入。可选输入包括蛋白质、证据模型、RNA-seq 序列、转座元件（TE）注释和 --config 配置文件。流程按顺序运行十个检查项目。检查内容包括提取蛋白质、BUSCO 评估、OMArk 分类和 gffcompare 比较。检查内容还包括统计剪接支持度、基因计数、终止密码子、TE 重叠和内含子类型。默认模式只打印外部软件的命令。你需要设置 RUN=1 来真正运行软件。汇总表中的缺失值会被标记为 WARN。所有阈值都是经验值。请与近缘物种用同样方法注释的基因组对比。表格中的 WARN 表示需要查看，不表示删除。这里的 AED = 1 只是标记，不是删除。共识模型不等于已验证的基因。软件 BUSCO 只衡量保守单拷贝基因的完整度。示例提供的 BUSCO 结果、OMArk 结果和 gffcompare 结果都是模拟的。
