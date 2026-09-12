# Asm1 — Assembly QC gate

Narrative: [`../docs/DETAILED_GUIDE.md`](../docs/DETAILED_GUIDE.md) Step 2.

## Why a hard gate
Annotating a fragmented or collapsed genome wastes months of GSAman time and freezes wrong gene counts into papers.

## Required commands

```bash
busco -i "$GENOME_FA" -l viridiplantae_odb12 \
  -o genome_busco --out_path "$WORK_DIR/asm" -m genome -c "$THREADS"

seqkit stats -a "$GENOME_FA" | tee "$WORK_DIR/asm/seqkit_stats.txt"
```

## Recommended extras

```bash
# Compleasm (fast BUSCO-like)
# compleasm run -a "$GENOME_FA" -l eudicots -t "$THREADS" -o "$WORK_DIR/asm/compleasm"

# Merqury QV if you have Illumina / HiFi k-mers
# merqury.sh reads.meryl "$GENOME_FA" "$WORK_DIR/asm/merqury"
```

## Metrics to write down

| Metric | Meaning for annotation |
|--------|-------------------------|
| BUSCO Complete (C) | Completeness of gene space in DNA |
| BUSCO Duplicated (D) | High D → haplotigs or polyploid; see **S9** |
| BUSCO Fragmented / Missing | May need better assembly before annotation |
| N50 / #scaffolds | Contiguity; chr-scale preferred when claiming chromosome-level assemblies |
| Gap % | Soft-mask still OK; many gaps hurt gene models |

## Pass / fail (set your paper bar in METHODS)

**Pass examples (edit):**  
- *V. vinifera*-like: ~19 chromosomes, BUSCO-C in clade-typical range  
- Draft contig set for methods-only: document lower bar and use **S6/S11**

**Fail → stop annotation:**  
- Catastrophic BUSCO-M  
- Unexplained extreme BUSCO-D without a haplotype plan  
- Assembly still in thousands of tiny contigs for a “reference” claim

```bash
# when pass:
# ASSEMBLY_OK=yes
```

## Next
Soft-mask [`A0_softmask.md`](A0_softmask.md) then choose branch in [`../docs/SCENARIOS.md`](../docs/SCENARIOS.md).
