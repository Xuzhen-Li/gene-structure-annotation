# BUSCO — completeness

**Role:** Asm1 (genome mode) and protein QC after annotation.

## Get it
- https://busco.ezlab.org · bioconda `busco`  
- Download lineage once: `viridiplantae_odb12` (or eudicots) — huge, cache it.

## Genome mode (Asm1)
```bash
busco -i "$GENOME_FA" -l viridiplantae_odb12 \
  -o genome_busco --out_path "$WORK_DIR/asm" -m genome -c "$THREADS"
```

## Protein mode (annotation QC)
```bash
busco -i "$PROTEINS_FA" -l viridiplantae_odb12 \
  -o prot_busco --out_path "$WORK_DIR/qc" -m proteins -c "$THREADS"
# or: bash pipeline/01_qc_busco_psauron.sh
```

## How to read scores
| Letter | Meaning |
|--------|---------|
| C | Complete |
| D | Duplicated (high → haplotigs / polyploid / isoforms) |
| F | Fragmented |
| M | Missing |

## Pitfalls
- Comparing different lineages across papers.  
- High D on proteins because you fed **all isoforms** — use one rep per gene.  
- Ignoring genome-mode D before annotating (**S9**).
