# Simulated example for the structure QA step / 结构质量评估模拟示例

<!-- All prose on this page is a placeholder. Replace each [[TODO-TEXT]] with reviewed text. -->

[[TODO-TEXT: what this example is (10 simulated genes on 2 short chromosomes; not real data) and how to run it.]]

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

[[TODO-TEXT: what each planted case shows in qc_summary.tsv; note that gene_count and exons_per_gene_mean WARN only because the example is tiny.]]

## 中文

[[TODO-TEXT: 中文说明，内容与英文部分对应。]]
