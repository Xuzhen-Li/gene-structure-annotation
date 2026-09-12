# S14 / 05 — Genome-wide Augustus + GeneMark + PASA tracks

Upstream: https://github.com/CantuLab/AnnotationPipeline2-EVM_based-DClab/blob/main/05-Ab_initio_prediction.md

1. Split genome per sequence; `parallel` Augustus → `prediction.augustus.gff3` → copy to `EVM_DIR`  
2. Same splits; GeneMark `gmhmme3 -m ${GENOME_PREFIX}.genemark.mod` → `prediction.genemark.gff3`  
3. PASA TransDecoder clean GFF → `prediction.pasa.gff3` in `EVM_DIR`
