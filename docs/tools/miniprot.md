# miniprot — fast protein-to-genome alignment

**Role:** Related-species proteins / genes as hints (Copetti); RAGNAROK protein track; GSAman evidence.

```bash
miniprot -t "$THREADS" --gff "$GENOME_FA" related_proteins.faa \
  > "$WORK_DIR/draft/miniprot.gff"
# or align CDS/proteins per miniprot docs
```

**Pitfall:** Sparse hits from a distant genus look like “failed annotation” — still useful as partial evidence, not as sole draft.
