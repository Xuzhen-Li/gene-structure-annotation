# S14 / 02 — RepeatMasker soft-mask + repeats GFF for EVM

```bash
cd "${REPEAT_DIR}"
cp "${GENOME_FASTA}" .
GENOME=$(basename "${GENOME_FASTA}")
"${REPEATMASKER_DIR}/RepeatMasker" -pa "${THREADS}" -s \
  -lib "${REPEAT_LIB}" -a -xsmall -gff -e ncbi "${GENOME}"
"${REPEATMASKER_DIR}/util/rmOutToGFF3.pl" "${GENOME}.out" > "${GENOME}.out.gff3"
grep -v '^#' "${GENOME}.out.gff3" > "${EVM_DIR}/repeats.gff3"
```

Also set `GENOME_SOFT` to the `*.masked` file for any BRAKER comparison runs.
