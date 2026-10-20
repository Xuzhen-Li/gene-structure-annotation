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

Open a terminal (Mac: Terminal app; Linux: a terminal window; cluster: your login shell) inside the gene-structure-annotation folder (the repo root, which is the top-level directory of the project) to run `python3 -m unittest discover -s tests -v` or `GSA_FORCE_MOCKS=1 python3 -m unittest discover -s tests -v`. Mocks are small stand-in scripts in `tests/mock_bin` and `tests/mock_pasa_home` that replace EVidenceModeler, `tsebra.py`, `mikado`, or PASA when those tools are not installed. When you run `GSA_FORCE_MOCKS=1 python3 -m unittest discover -s tests -v`, the mocks are always used even if the real programs are present. Because the 24 tests only check the structure of outputs and run in about 1 second using only the Python standard library, a real tool installation also passes.
