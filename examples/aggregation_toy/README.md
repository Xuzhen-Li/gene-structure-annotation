# Aggregation toy data (simulated)

[[TODO-TEXT]]

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

[[TODO-TEXT]]
