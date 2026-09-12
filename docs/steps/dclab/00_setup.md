# S14 / 00 — Setup

Setup for the S14 EVM consensus path.

```bash
# After: cp config/example.env config/local.env && source it
mkdir -p "${EXTERNAL_DIR}" "${REPEAT_DIR}" "${TRAINING_DIR}" \
  "${AUGUSTUS_TRAIN_DIR}" "${GENEMARK_TRAIN_DIR}" \
  "${AUGUSTUS_PRED_DIR}" "${GENEMARK_PRED_DIR}" \
  "${EVM_DIR}" "${POLISHING_DIR}" "${FILTERING_DIR}"
```

Required tools (versions as in upstream README): RepeatMasker, GMAP, pblat, PASA, Augustus, GeneMark-ET (+ `~/.gm_key`), EVM, gffread, parallel, samtools.

Set `GENOME_FASTA`, `GENOME_PREFIX`, `REPEAT_LIB`, `THREADS`, `MAX_INTRON`, and all `*_DIR` / tool roots in `config/local.env`.
