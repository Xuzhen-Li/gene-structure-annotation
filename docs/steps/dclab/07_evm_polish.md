# S14 / 07 — EVM consensus + PASA polish

## EVM

```bash
cd "${EVM_DIR}"
cp "${GENOME_FASTA}" .
GENOME=$(basename "${GENOME_FASTA}")
cat prediction.*.gff3 > predictions.gff3
cat transcript_alignment.*.gff3 > transcript_alignments.gff3
cp "${REPO_ROOT}/config/evm_weights_cantulab.txt" weights.txt
# partition_EVM_inputs.pl → write_EVM_commands.pl → parallel → recombine → convert
# Exact flags: upstream 07-EVM_consensus.md
# → EVM.all.gff3 → filter incomplete → EVM.filtered.gff3
```

## PASA polish

Load `EVM.filtered.gff3` + `all_transcripts.fasta` into a polishing PASA DB; run `cDNA_annotation_comparer.dbi` + `dump_valid_annot_updates.dbi` (upstream 7.3).  

Then continue to [`08_filter.md`](08_filter.md).
