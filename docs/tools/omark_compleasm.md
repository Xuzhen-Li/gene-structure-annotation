# OMArk + Compleasm — extra proteome / assembly QC

**Role:** **S5** mandatory; optional elsewhere (`pipeline/A5b_omark_compleasm.sh`).

## Compleasm
- Fast BUSCO-like: https://github.com/huangnengCSU/Compleasm  
```bash
compleasm run -a "$GENOME_FA" -l eudicots -t "$THREADS" -o "$WORK_DIR/asm/compleasm"
```

## OMArk
- https://github.com/DessimozLab/OMArk  
- Needs OMAmer database for Viridiplantae / your clade.  
- Flags possible contamination / incomplete lineages in the **proteome**.

## Pitfalls
- Wrong OMAmer DB for plants.  
- Treating OMArk as a replacement for BUSCO — use both for papers.
