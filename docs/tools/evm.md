# EVidenceModeler (EVM) — merge competing gene predictions

**Role:** Default merge in **S1** / **S2** (`MERGE_MODE=evm`).

## Get it
- https://github.com/EVidenceModeler/EVidenceModeler  
- Many plant pipelines ship a `run_EVM.sh` wrapper — steal structure, not weights blindly.

## Concept
You supply several prediction tracks + a **weights file**. EVM picks a non-overlapping consensus gene set.

## Weights (starting ideas — tune)
```text
ABINITIO_PREDICTION   BRAKER     5
OTHER_PREDICTION      GeMoMa     8
OTHER_PREDICTION      Liftoff    7
TRANSCRIPT            PASA       10
```
No RNA → raise homology weights, lower ab initio.

## Workflow sketch
1. Convert each GFF to EVM-compatible `gene_predictions.gff3`.  
2. Write `weights.txt`.  
3. Partition genome → run EVM per partition → combine.  
4. Write `MERGED_GFF` → AGAT.

`pipeline/A4_merge_sets.sh` prints this checklist and stops until you wire your install.

## Pitfalls
- Equal weights on everything → mush.  
- Feeding unfiltered TE-ORFs as predictions.  
- Skipping AGAT after merge.


## S14 EVM consensus defaults

See [`../notes/cantulab_evm.md`](../notes/cantulab_evm.md) and `config/evm_weights_cantulab.txt`.  
Upstream runbook: https://github.com/CantuLab/AnnotationPipeline2-EVM_based-DClab/blob/main/07-EVM_consensus.md
