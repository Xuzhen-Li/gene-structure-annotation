# AGAT + gffread — GFF hygiene and proteins

**Role:** After every draft/merge/curation; protein FASTA for BUSCO/PSAURON.

## Get them
- bioconda `agat`, `gffread` (or cufflinks gffread)

## AGAT stats (structural sanity)
```bash
bash pipeline/A5_agat_stats.sh path/to/genes.gff3
# wraps agat_sp_statistics.pl — gene/mRNA/exon counts
```

## Proteins (representative CDS → AA)
```bash
# pipeline/A3_proteins_from_gff.sh uses gffread -y / similar
export DRAFT_GFF=... GENOME_FA=... PROTEINS_FA=...
bash pipeline/A3_proteins_from_gff.sh
```

## Manual gffread checks
```bash
gffread genes.gff3 -g "$GENOME_FA" -y proteins.faa
# Errors often mean bad phase / missing stop — fix before release
```

## Pitfalls
- BUSCO on wrong protein set (all isoforms vs one per gene).  
- Releasing GFF that fails `gffread`.
