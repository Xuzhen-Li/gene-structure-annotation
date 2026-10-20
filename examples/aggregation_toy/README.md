# Aggregation toy data (simulated)

This folder holds simulated toy data made the same way every time with a fixed seed (a starting number that makes random generation repeatable) on one 9 kb (9,000 base pairs of DNA) contig (a continuous stretch of assembled DNA sequence) named `chr1` with three genes. Gene `g1` has all evidence types, `g2` has BRAKER, GeMoMa (a tool that predicts genes using reference proteins from related species), miniprot (a tool that aligns proteins to a genome), and StringTie (a tool that assembles transcripts from RNA reads), and `g3` has BRAKER only and no evidence. It also includes one unstranded single-exon (having only one coding segment) StringTie transcript named `STRG.9.1` that step A4c drops, and running `python3 examples/aggregation_toy/make_toy.py` regenerates every file.

| File | Used by |
|------|---------|
| `genome.fa` | all steps |
| `braker.gtf` | A4c `--braker` |
| `gemoma.gff3` | A4c `--gemoma` |
| `miniprot.gff` | A4c `--miniprot` |
| `stringtie.gtf` | A4c `--stringtie`, A4b via `mikado_list.tsv` |
| `pasa_assemblies.gff3` | A4c `--pasa` |
| `mikado_list.tsv` | A4b `MIKADO_LIST` |
| `tsebra/braker1/`, `tsebra/braker2/` | A4a `BRAKER1_DIR`, `BRAKER2_DIR` |
| `pasa/` | A4e configs and transcripts |
| `make_toy.py` | regenerates every file above |

```bash
python3 examples/aggregation_toy/make_toy.py
cd examples/aggregation_toy
python3 ../../pipeline/A4c_evm_inputs.py -o /tmp/evm_inputs -w ../../config/evm_weights_aggregate.txt \
  --genome genome.fa --braker braker.gtf --gemoma gemoma.gff3 --miniprot miniprot.gff \
  --stringtie stringtie.gtf --pasa pasa_assemblies.gff3
```

When you open a terminal (Mac: Terminal app; Linux: a terminal window; cluster: your login shell) inside the gene-structure-annotation folder and run `python3 examples/aggregation_toy/make_toy.py` and then step A4c, the run reports 3 genes from BRAKER, 2 genes from GeMoMa, 2 alignments and 1 unstranded dropped from StringTie, 1 alignment from PASA, and 2 alignments from miniprot. These counts are also saved in `summary.tsv`, and the output ends by pointing to the next step, `A4d_evm_run.sh`.
