# S14 / 03 — PASA training set

Full command list is long; **canonical reference:**  
https://github.com/CantuLab/AnnotationPipeline2-EVM_based-DClab/blob/main/03-Training_set.md  

Condensed intent:

1. `cat ${EXTERNAL_DIR}/*.fasta > ${TRAINING_DIR}/all_transcripts.fasta`  
2. Write `pasa_config.txt` with SQLite DB under `TRAINING_DIR` and `MAX_INTRON`  
3. GMAP+BLAT via PASA `run_spliced_aligners.pl`  
4. TransDecoder + PASA assemble → `*.pasa_assemblies.gff3`  
5. `pasa_asmbls_to_training_set.dbi` → clean GFF for Augustus/GeneMark training  

Tool notes: [`../../tools/pasa.md`](../../tools/pasa.md).  
Keep their scripts/`GFF_extract_features.py` for cleaning, or AGAT equivalents.
