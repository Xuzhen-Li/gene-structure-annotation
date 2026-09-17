# 06 — Release qualified GFF (detailed)

Narrative: [`../docs/DETAILED_GUIDE.md`](../docs/DETAILED_GUIDE.md) Step 13 · checklist in [`../docs/PLAYBOOK.md`](../docs/PLAYBOOK.md).  
Layout must match **G8** / [`../docs/EVALUATION.md`](../docs/EVALUATION.md) / [`../docs/STAGE_IO.md`](../docs/STAGE_IO.md) and `pipeline/check_release_pack.py`.

## 1. Freeze curated GFF
```bash
export CURATED_GFF=...   # from GSAman
export DRAFT_GFF="$CURATED_GFF"
RUN=1 bash pipeline/A3_proteins_from_gff.sh
RUN=1 bash pipeline/01_qc_busco_psauron.sh  # bare bash = DRY only
RUN=1 bash pipeline/A5_agat_stats.sh "$CURATED_GFF"
```

## 2. Validate
```bash
gffread "$CURATED_GFF" -g "$GENOME_FA" -y /dev/null   # dies on many broken CDS
# or: agat_sp_validate.md / gt gff3validator if available
```

## 3. Package — `release/<TAG>/` (not a flat release/ dump)
`check_release_pack.py` expects a **directory** `release/<TAG>/` containing GFF + proteins + METHODS (or README/*.md).

```bash
: "${RELEASE_TAG:?}"
REL="$WORK_DIR/release/${RELEASE_TAG}"
mkdir -p "$REL" "$REL/qc"

# Required public products (tagged names + stable aliases for FA hand-off)
cp "$CURATED_GFF" "$REL/${RELEASE_TAG}.gff3"
cp "$PROTEINS_FA" "$REL/${RELEASE_TAG}.proteins.faa"
# Stable names used by A6 / function plant_sim env.snippet / STAGE_IO:
cp "$REL/${RELEASE_TAG}.gff3" "$REL/genes.gff3"
cp "$REL/${RELEASE_TAG}.proteins.faa" "$REL/proteins.faa"

# METHODS — stub if you have not written one yet (edit before claiming L1)
if [[ -f "$WORK_DIR/METHODS.md" ]]; then
  cp "$WORK_DIR/METHODS.md" "$REL/METHODS.md"
else
  cat > "$REL/METHODS.md" <<EOF
# METHODS — ${RELEASE_TAG}
grade=L0
status=provisional
primary=S__
# Fill primary=S1 / S11 / … (not blank). Do not bump grade=L1 until EVALUATION gates pass.
# Fill: assembly + Asm1; TE lib + soft-mask; branch + tool versions;
# OrthoDB/ref; RNA libs; BUSCO lineage + C/D/F/M; curation scope.
# Never write status=L1 (status is only provisional or qualified).
EOF
fi

# QC snapshot (optional but recommended; not private BAM/FASTQ)
cp "$WORK_DIR/qc/"*agat* "$REL/qc/" 2>/dev/null || true
cp -r "$BUSCO_OUT" "$REL/qc/busco" 2>/dev/null || true
[[ -f "$PSAURON_TSV" ]] && cp "$PSAURON_TSV" "$REL/qc/" || true

# Smoke-check pack presence (not a full L1 judge)
python3 pipeline/check_release_pack.py "$REL"
```

## 4. METHODS.md (required fields)
- Assembly version + Asm1 metrics  
- TE lib + soft-mask (trusted lib version + sha256)  
- Branch ID (S1… / **S11-lite** if lift-only) + tool versions  
- OrthoDB / ref GFF used  
- RNA libraries  
- BUSCO lineage + C/D/F/M  
- Curation scope (genome-wide vs priority / S7 windows)  
- `grade=L0|L1|L2` and `status=provisional|qualified` (never `status=L1`)

## 5. Do not upload
Private BAM, FASTQ, unpublished sample matrices.
