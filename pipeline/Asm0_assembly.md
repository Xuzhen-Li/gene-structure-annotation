# Asm0 — Genome assembly (before annotation)

Full command narrative: [`../docs/DETAILED_GUIDE.md`](../docs/DETAILED_GUIDE.md) Step 1.

## Purpose
Produce the FASTA that annotation will treat as truth. Annotation cannot fix a shattered or wrongly purged assembly.

## Typical plant inputs (example: *Vitis*)
| Data | Role |
|------|------|
| PacBio HiFi | Contigs (hifiasm / HiCanu) |
| Hi-C | Chromosome scaffolding (YaHS / 3D-DNA) |
| ONT (optional) | Gap filling / scaffolding assist |
| Illumina (optional) | Polishing / QV |

## Example path (edit for your cluster)

```bash
# 1) Contigs
hifiasm -o "$WORK_DIR/asm/genome" -t "$THREADS" hifi.fastq.gz
# Extract primary / hap1 / hap2 per hifiasm docs (gfa → fa)

# 2) Optional purge (only if clearly haplotig-inflated AND not polyploid — see S9)
# purge_dups ...

# 3) Hi-C scaffold
# bwa mem / chromap → BAM; then:
# yahs contigs.fa hic.bam -o "$WORK_DIR/asm/yahs"

# 4) Manual / juicebox review of scaffolds → GENOME_FA
```

## Decisions to record in `asm/README.txt`
- Primary only vs dual haplotype annotation  
- Chromosome naming scheme (chr01… vs scaffold)  
- Assembly software + versions  
- Whether purge was applied  

## Outputs
- `GENOME_FA` — annotation target  
- Optional `GENOME_FA_HAP2`  
- `asm/README.txt`

## Next
[`Asm1_assembly_qc.md`](Asm1_assembly_qc.md)
