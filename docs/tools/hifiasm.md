# hifiasm — HiFi contig assembly

**Role in this playbook:** Asm0 — build contig FASTA before annotation.

## Get it
- https://github.com/chhylp123/hifiasm  
- Often: `conda install -c bioconda hifiasm` or a site Singularity image.

## Minimal run
```bash
hifiasm -o "$WORK_DIR/asm/vitis" -t "$THREADS" hifi.fastq.gz
# Outputs: *.p_ctg.gfa / hap gfa — convert to FASTA with gfatools or hifiasm docs
```

## Inputs / outputs
| In | Out |
|----|-----|
| HiFi FASTQ | Primary / hap1 / hap2 contigs (GFA → FA) |

## How to use the result
1. Convert GFA → FASTA.  
2. Decide primary-only vs dual-hap annotation (**S4** / **S9**).  
3. Optional Hi-C scaffolding → [`yahs.md`](yahs.md).  
4. Gate with [`../DETAILED_GUIDE.md`](../DETAILED_GUIDE.md) Step 2 (Asm1).

## Common pitfalls
- Annotating before purge/scaffold review.  
- Purging a true polyploid (**S9**).  
- Mixing hap1/hap2 into one “primary” without saying so in METHODS.
