# S14 / 06 — Transcript alignments into EVM

Reuse GMAP/BLAT/PASA assemblies from step 03 (no new align):

```bash
sed "s:${GENOME}.gmap:gmap:" "${TRAINING_DIR}/gmap.spliced_alignments.gff3" \
  > "${EVM_DIR}/transcript_alignment.gmap.gff3"
cp "${TRAINING_DIR}/blat.spliced_alignments.gff3" \
  "${EVM_DIR}/transcript_alignment.blat.gff3"
sed 's:assembler-mRNA_training_PASA.sqlite:PASA_assemblies:' \
  "${TRAINING_DIR}/mRNA_training_PASA.sqlite.pasa_assemblies.gff3" \
  > "${EVM_DIR}/transcript_alignment.pasa.gff3"
```
