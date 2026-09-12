# 06 — Release qualified GFF (detailed)

Narrative: [`../docs/DETAILED_GUIDE.md`](../docs/DETAILED_GUIDE.md) Step 13 · checklist in [`../docs/PLAYBOOK.md`](../docs/PLAYBOOK.md).

## 1. Freeze curated GFF
```bash
export CURATED_GFF=...   # from GSAman
export DRAFT_GFF="$CURATED_GFF"
bash pipeline/A3_proteins_from_gff.sh
bash pipeline/01_qc_busco_psauron.sh
bash pipeline/A5_agat_stats.sh "$CURATED_GFF"
```

## 2. Validate
```bash
gffread "$CURATED_GFF" -g "$GENOME_FA" -y /dev/null   # dies on many broken CDS
# or: agat_sp_validate.md / gt gff3validator if available
```

## 3. Package
```bash
mkdir -p "$WORK_DIR/release"
cp "$CURATED_GFF" "$WORK_DIR/release/${RELEASE_TAG}.gff3"
cp "$PROTEINS_FA" "$WORK_DIR/release/${RELEASE_TAG}.proteins.faa"
cp "$WORK_DIR/qc/"*agat* "$WORK_DIR/release/" 2>/dev/null || true
```

## 4. METHODS.md (required fields)
- Assembly version + Asm1 metrics  
- TE lib + soft-mask  
- Branch ID (S1…) + BRAKER/GeMoMa/EVM/Liftoff versions  
- OrthoDB / ref GFF used  
- RNA libraries  
- BUSCO lineage + C/D/F/M  
- Curation scope (genome-wide vs priority)  
- `status=qualified` or `provisional`

## 5. Do not upload
Private BAM, FASTQ, unpublished sample matrices.
