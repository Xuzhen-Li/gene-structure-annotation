# PASA — transcript assemblies for training + polish

**Role:** S14 training set & polish — build training genes from aligned transcripts; polish EVM models (UTRs, splices, isoforms).

## Get it
https://github.com/PASApipeline/PASApipeline  

## Where it sits
1. Align Iso-Seq / RNA assemblies with **GMAP** (and/or pblat).  
2. PASA → high-quality transcript-derived gene models.  
3. Train Augustus / GeneMark-ET on those models (S14).  
4. After EVM: PASA **update** cycle on `EVM.filtered.gff3`.

Full command blocks: upstream [03](https://github.com/CantuLab/AnnotationPipeline2-EVM_based-DClab/blob/main/03-Training_set.md) and [07](https://github.com/CantuLab/AnnotationPipeline2-EVM_based-DClab/blob/main/07-EVM_consensus.md).

## Pitfalls
- MySQL/SQLite setup friction — follow PASA wiki for your version.  
- Polishing without enough transcripts adds little; skip to GSAman if Iso-Seq is thin.
