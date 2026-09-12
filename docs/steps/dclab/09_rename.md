# S14 / 09 — Standard gene names

```bash
python3 "${REPO_ROOT}/pipeline/A6b_rename_gff.py" \
  "${GENOME_PREFIX}" 1 chr \
  "${FILTERING_DIR}/gene_models.checked.gff3" \
  > "${FILTERING_DIR}/${GENOME_PREFIX}.renamed.gff3"
```

Then **return to main spine**: AGAT, proteins, BUSCO, PSAURON, GSAman, release.
