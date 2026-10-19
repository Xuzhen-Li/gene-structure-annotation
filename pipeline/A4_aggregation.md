# A4 multi-source aggregation (EVM main path, TSEBRA / Mikado / PASA optional)

[[TODO-TEXT]]

## Steps

| Step | File | In | Out |
|------|------|----|-----|
| A4a (optional) | [`A4a_tsebra_optional.sh`](A4a_tsebra_optional.sh) | BRAKER1 + BRAKER2 `augustus.hints.gtf`, `hintsfile.gff` | `$AGG_DIR/tsebra/tsebra.gtf` |
| A4b (optional) | [`A4b_mikado_optional.sh`](A4b_mikado_optional.sh) | `MIKADO_LIST` (transcript assemblies) | `$AGG_DIR/mikado/mikado.loci.gff3` |
| A4c | [`A4c_evm_inputs.py`](A4c_evm_inputs.py) | BRAKER/AUGUSTUS, GeMoMa, StringTie, PASA, Mikado, miniprot | `gene_predictions.gff3`, `transcript_alignments.gff3`, `protein_alignments.gff3`, `weights.txt`, `summary.tsv` |
| A4d | [`A4d_evm_run.sh`](A4d_evm_run.sh) | A4c outputs + genome | `$AGG_DIR/evm/evm.EVM.gff3` |
| A4e (optional) | [`A4e_pasa_update.sh`](A4e_pasa_update.sh) | `evm.EVM.gff3` + PASA DB/configs | `$AGG_DIR/pasa_update/pasa_updated.gff3` |

Weights: [`../config/evm_weights_aggregate.txt`](../config/evm_weights_aggregate.txt)

[[TODO-TEXT]]

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

[[TODO-TEXT]]

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

[[TODO-TEXT]]

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

[[TODO-TEXT]]

## References

- EVidenceModeler wiki (v2.1.0): https://github.com/EVidenceModeler/EVidenceModeler/wiki
- Haas et al. 2008, Genome Biology 9:R7, doi:10.1186/gb-2008-9-1-r7
- TSEBRA: https://github.com/Gaius-Augustus/TSEBRA
- Mikado tutorial: https://mikado.readthedocs.io/en/stable/Tutorial/
- PASA annotation updates: https://github.com/PASApipeline/PASApipeline/wiki/PASA_genome_annotation
