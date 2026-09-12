# S14 / 04 — Train Augustus + GeneMark-ET

Upstream: https://github.com/CantuLab/AnnotationPipeline2-EVM_based-DClab/blob/main/04-Predictor_training.md

**Augustus:** `gff2gbSmallDNA.pl` → `autoAugTrain.pl --species ${GENOME_PREFIX}` → backup `AUGUSTUS_CONFIG/species/`.  

**GeneMark-ET:** intron GFF from PASA clean models → `gmes_petap.pl --ET … --training` → `${GENOME_PREFIX}.genemark.mod`.  

License: `~/.gm_key` required.
