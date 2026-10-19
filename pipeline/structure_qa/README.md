# Structure QA step / 结构注释质量评估

<!-- All prose on this page is a placeholder. Replace each [[TODO-TEXT]] with reviewed text. -->

## English

[[TODO-TEXT: what this step is for, where it sits (after the consensus merge step, before release / handoff), and that a WARN means "look", not "delete".]]

### Inputs

| Input | Flag | Required |
|---|---|---|
| Consensus GFF3 from the merge step | `--gff` | yes |
| Genome FASTA | `--genome` | yes |
| Protein FASTA (IDs = mRNA IDs) | `--proteins` | no |
| Evidence models, `NAME=PATH` (GTF/GFF3) | `--evidence` | no |
| RNA-seq BAM, or junction table | `--bam` / `--junctions` | no |
| TE annotation (GFF3 / BED / RepeatMasker `.out`) | `--te` | no |
| Settings and thresholds | `--config` (default `config/structure_qa.ini`) | no |

[[TODO-TEXT: one line per input on where it comes from.]]

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

[[TODO-TEXT: short explanation of each check and how to read it.]]

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

[[TODO-TEXT: what RUN=1 changes; that results already under --out are reused; how to set BUSCO lineages and the OMAmer database in the config.]]

### Output: `qc_summary.tsv`

Columns: `metric`, `value`, `threshold`, `status` (PASS / WARN / INFO), `basis`, `step`, `note`.

[[TODO-TEXT: how to read PASS / WARN / INFO; a missing value is WARN; all thresholds are rules of thumb to compare with a close relative.]]

### Try it on the simulated example

```bash
bash examples/structure_qa_sim/run_example.sh
python3 -m unittest discover -s tests -v
```

[[TODO-TEXT: expected result of the example and which WARN rows are planted on purpose.]]

## 中文

[[TODO-TEXT: 中文说明，内容与英文部分对应。]]
