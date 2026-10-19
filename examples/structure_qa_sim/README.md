# Simulated example for the structure QA step / 结构质量评估模拟示例

This example uses 2 simulated chromosomes of 30 kb each. It contains 10 simulated genes and is not real data. The example BUSCO, OMArk and gffcompare results are simulated. You run the test with bash examples/structure_qa_sim/run_example.sh. The script writes the output to examples/structure_qa_sim/qa_out/. The expected summary is expected_qc_summary.tsv.

```bash
bash examples/structure_qa_sim/run_example.sh          # writes examples/structure_qa_sim/qa_out/
python3 examples/structure_qa_sim/make_sim.py          # rebuilds the input files (same result every time)
```

| File | Content |
|---|---|
| `genome.fa` | 2 simulated chromosomes, 30 kb each |
| `consensus.gff3` | 10 genes, 11 mRNAs (g01 has two isoforms) |
| `proteins.faa` | proteins, stops written as `.` |
| `evidence_transcripts.gtf` | transcript evidence |
| `evidence_proteins.gff3` | protein-alignment evidence |
| `rnaseq.bam` | spliced reads |
| `te.gff3` | TE annotation |
| `mock_tool_outputs/` | mock BUSCO / OMArk / gffcompare results (not real runs) |
| `expected_qc_summary.tsv` | the summary the tests expect |

Planted cases: g04 GC-AG intron · g05 internal stop · g06 no evidence (AED 1) · g07 CDS inside a TE · g08 last exon without evidence.

The file expected_qc_summary.tsv shows ten WARN rows. Gene g04 has a GC AG intron. This triggers a WARN for splice_gt_ag_share. Gene g05 has an internal stop. This triggers a WARN for internal_stop_share and protein_fasta_internal_stop_count. Gene g06 has no evidence so its AED is 1. This triggers a WARN for aed_eq_1_share. Gene g07 has its CDS inside a TE. A TE is a transposable element. This triggers a WARN for te_overlap_gene_share and te_overlap_cds_base_share. Gene g08 has its last exon without evidence. It gives no WARN. Its AED is 0.04. Its RNA seq full chain support drops to 0.75 which is INFO. The mock eudicotyledons BUSCO result gives two WARN rows for C 88 and a gap of 6.5 points. The metrics gene_count and exons_per_gene_mean warn only because the example is tiny. Every threshold is a rule of thumb. You must compare your results with close relative genomes annotated the same way. A WARN means look. It does not mean delete. AED = 1 is a flag. It is not a deletion. A consensus model is not a validated gene. BUSCO only measures completeness of conserved single copy genes. The example BUSCO, OMArk and gffcompare results are simulated.

## 中文

文件 expected_qc_summary.tsv 显示十个 WARN 行。基因 g04 具有 GC AG 内含子。这会触发 splice_gt_ag_share 的 WARN。基因 g05 具有内部终止密码子。这会触发 internal_stop_share 和 protein_fasta_internal_stop_count 的 WARN。基因 g06 没有证据导致 AED 为 1。这会触发 aed_eq_1_share 的 WARN。基因 g07 的 CDS 位于转座元件（TE）内部。这会触发 te_overlap_gene_share 和 te_overlap_cds_base_share 的 WARN。基因 g08 的最后一个外显子没有证据。它没有产生 WARN。它的 AED 为 0.04。它的 RNA seq 全链支持度降至 0.75 并且记为 INFO。模拟的 eudicotyledons BUSCO 结果因为 C 88 和 6.5 分的差距产生两个 WARN 行。指标 gene_count 和 exons_per_gene_mean 产生 WARN 仅仅因为示例太小。每个阈值都是经验值。你必须与近缘物种用同样方法注释的基因组对比。这里的 WARN 表示需要查看。它不表示删除。这里的 AED = 1 只是标记。它不是删除。共识模型不等于已验证的基因。软件 BUSCO 只衡量保守单拷贝基因的完整度。示例中的 BUSCO、OMArk 和 gffcompare 结果是模拟的。
