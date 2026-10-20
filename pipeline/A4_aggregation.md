# A4 multi-source aggregation (EVM main path, TSEBRA / Mikado / PASA optional)

Step A4 combines several gene sets and evidence into one gene set using EVidenceModeler (EVM), a tool that merges different gene predictions and alignments into one consensus set. It runs optional A4a TSEBRA (a combiner for BRAKER runs) and optional A4b Mikado (a tool that picks the best transcript per locus, or gene position, from several transcript assemblies to use as transcript evidence), then A4c makes EVM input files, A4d runs EVM, and optional A4e runs PASA update (a tool that adds untranslated regions and alternative isoforms). The final output goes to step A5 AGAT (a toolkit that checks and formats gene annotation files) as `MERGED_GFF`.

## Steps

| Step | File | In | Out |
|------|------|----|-----|
| A4a (optional) | [`A4a_tsebra_optional.sh`](A4a_tsebra_optional.sh) | BRAKER1 + BRAKER2 `augustus.hints.gtf`, `hintsfile.gff` | `$AGG_DIR/tsebra/tsebra.gtf` |
| A4b (optional) | [`A4b_mikado_optional.sh`](A4b_mikado_optional.sh) | `MIKADO_LIST` (transcript assemblies) | `$AGG_DIR/mikado/mikado.loci.gff3` |
| A4c | [`A4c_evm_inputs.py`](A4c_evm_inputs.py) | BRAKER/AUGUSTUS, GeMoMa, StringTie, PASA, Mikado, miniprot | `gene_predictions.gff3`, `transcript_alignments.gff3`, `protein_alignments.gff3`, `weights.txt`, `summary.tsv` |
| A4d | [`A4d_evm_run.sh`](A4d_evm_run.sh) | A4c outputs + genome | `$AGG_DIR/evm/evm.EVM.gff3` |
| A4e (optional) | [`A4e_pasa_update.sh`](A4e_pasa_update.sh) | `evm.EVM.gff3` + PASA DB/configs | `$AGG_DIR/pasa_update/pasa_updated.gff3` |

Weights: [`../config/evm_weights_aggregate.txt`](../config/evm_weights_aggregate.txt)

The weights file sets score multipliers for each evidence class: ab initio prediction (genes predicted from genome sequence alone), other prediction, protein, and transcript. Its starting values come from the EVM wiki and Haas et al. 2008 (ab initio 1, protein 2 to 5, transcript 8 to 10, PASA 10). Only the ratios between numbers matter, so you should tune them per species on a few manually curated genes and never copy a tuned file across species. Step A4d saves the exact weights used as `weights.used.txt`.

## Evidence classes

| A4c option | EVM class | SOURCE (column 2) | Default weight |
|------------|-----------|-------------------|----------------|
| `--braker` | ABINITIO_PREDICTION | BRAKER | 1 |
| `--tsebra` | ABINITIO_PREDICTION | TSEBRA | 1 |
| `--augustus` | ABINITIO_PREDICTION | AUGUSTUS | 1 |
| `--gemoma` | OTHER_PREDICTION | GeMoMa | 2 |
| `--miniprot` | PROTEIN | miniprot | 3 |
| `--stringtie` | TRANSCRIPT | StringTie | 8 |
| `--mikado` | TRANSCRIPT | Mikado | 8 |
| `--pasa` | TRANSCRIPT | PASA | 10 |

In GFF3 (a standard nine-column text format for gene features), column 2 is the `SOURCE` name, and it must match the weights file exactly; step A4c writes these names and fails if an input source has no row in the weights file. Run step A4a only when combining separate BRAKER1 (a predictor using RNA-seq, which is sequenced RNA reads) and BRAKER2 (a predictor using protein data) runs; BRAKER3 already runs TSEBRA inside, so setting `BRAKER_VERSION=3` skips step A4a. Pass `--tsebra` instead of `--braker` to step A4c when you have TSEBRA output, and never use both options together.

## Commands

```bash
# all steps print first; RUN=1 executes
export WORK_DIR=/path/to/work GENOME_FA=/path/to/genome.fa
export AGG_DIR="$WORK_DIR/aggregate"

# A4a (only for separate BRAKER1 + BRAKER2 runs; BRAKER_VERSION=3 skips)
BRAKER_VERSION=1+2 BRAKER1_DIR=/path/to/braker1 BRAKER2_DIR=/path/to/braker2 \
  TSEBRA_HOME=/path/to/TSEBRA RUN=1 bash pipeline/A4a_tsebra_optional.sh

# A4b (optional)
MIKADO_LIST=/path/to/list.tsv MIKADO_SCORING=plant.yaml RUN=1 bash pipeline/A4b_mikado_optional.sh

# A4c
python3 pipeline/A4c_evm_inputs.py -o "$AGG_DIR/evm_inputs" \
  -w config/evm_weights_aggregate.txt --genome "$GENOME_FA" \
  --braker braker.gtf --gemoma gemoma.gff3 --miniprot miniprot.gff \
  --stringtie stringtie.gtf --pasa pasa_assemblies.gff3

# A4d
EVM_HOME=/path/to/EVidenceModeler THREADS=16 RUN=1 bash pipeline/A4d_evm_run.sh

# A4e (optional; PASA_ROUNDS defaults to 2)
PASA_HOME=/path/to/PASApipeline PASA_ALIGN_CONFIG=alignAssembly.config \
  PASA_ANNOT_CONFIG=annotCompare.config PASA_TRANSCRIPTS=transcripts.fasta.clean \
  RUN=1 bash pipeline/A4e_pasa_update.sh
```

To run these commands, open a terminal (Mac: Terminal app; Linux: a terminal window; cluster: your login shell) inside the gene-structure-annotation folder. Every shell step only prints its commands by default, so add `RUN=1` to execute them. Step A4c uses only Python with no extra tools, needs at least one gene prediction input, and writes `gene_predictions.gff3`, `transcript_alignments.gff3`, `protein_alignments.gff3`, `weights.txt`, and `summary.tsv` (which lists feature counts per source and dropped records). Step A4c drops unstranded transcripts (transcripts without a known DNA strand direction) and UTRs (untranslated regions at the ends of a transcript); step A4d checks the inputs again before running EVM, and step A4e adds UTRs and alternative isoforms (different transcript versions from the same gene) back from PASA in 2 rounds by default.

## Environment keys

| Step | Required | Optional (default) |
|------|----------|--------------------|
| A4a | `BRAKER_VERSION`, `WORK_DIR`, `BRAKER1_DIR`, `BRAKER2_DIR`, `TSEBRA_CFG` or `TSEBRA_HOME` | `TSEBRA_GTFS`, `TSEBRA_HINTS`, `TSEBRA_OUT`, `TSEBRA_EXTRA` |
| A4b | `WORK_DIR`, `GENOME_FA`, `MIKADO_LIST` | `MIKADO_BIN` (mikado), `MIKADO_SCORING` (plant.yaml), `MIKADO_MODE` (permissive), `MIKADO_JUNCTIONS`, `MIKADO_BLAST_TARGETS`, `MIKADO_BLAST_TSV`, `MIKADO_ORFS` |
| A4d | `WORK_DIR`, `GENOME_FA` or `EVM_GENOME` | `EVM_HOME`, `EVM_INPUT_DIR`, `EVM_DIR`, `EVM_SAMPLE_ID` (evm), `EVM_GFF`, `EVM_SEGMENT_SIZE` (100000), `EVM_OVERLAP_SIZE` (10000), `REPEATS_GFF`, `THREADS` (4) |
| A4e | `WORK_DIR`, `PASA_HOME`, `GENOME_FA`, `PASA_ALIGN_CONFIG`, `PASA_ANNOT_CONFIG`, `PASA_TRANSCRIPTS` | `EVM_GFF`, `PASA_ROUNDS` (2), `PASA_UPDATE_DIR`, `PASA_UPDATED_GFF` |

## Example and tests

- Toy data: [`../examples/aggregation_toy/`](../examples/aggregation_toy/)
- Tests: `python3 -m unittest discover -s tests -v`

Open a terminal (Mac: Terminal app; Linux: a terminal window; cluster: your login shell) inside the gene-structure-annotation folder to run `python3 -m unittest discover -s tests -v`. These tests use only the Python standard library (built-in code that comes with Python) and check that the committed toy files equal the output of `make_toy.py` and that output files have the right structure. They run without the real tools installed by using mocks (small stand-in scripts that imitate the real programs), and a full run of 24 tests takes about 1 second.

## References

- EVidenceModeler wiki (v2.1.0): https://github.com/EVidenceModeler/EVidenceModeler/wiki
- Haas et al. 2008, Genome Biology 9:R7, doi:10.1186/gb-2008-9-1-r7
- TSEBRA: https://github.com/Gaius-Augustus/TSEBRA
- Mikado tutorial: https://mikado.readthedocs.io/en/stable/Tutorial/
- PASA annotation updates: https://github.com/PASApipeline/PASApipeline/wiki/PASA_genome_annotation
