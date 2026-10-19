# Tests

```bash
python3 -m unittest discover -s tests -v
GSA_FORCE_MOCKS=1 python3 -m unittest discover -s tests -v
```

| Path | Replaces |
|------|----------|
| `mock_bin/EVidenceModeler` | EVidenceModeler 2.x |
| `mock_bin/tsebra.py` | TSEBRA |
| `mock_bin/mikado` | Mikado configure / prepare / serialise / pick |
| `mock_pasa_home/` | PASA `Launch_PASA_pipeline.pl -A`, `scripts/Load_Current_Gene_Annotations.dbi`, `misc_utilities/pasa_gff3_validator.pl` |

[[TODO-TEXT]]
