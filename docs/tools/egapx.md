# EGAPx — NCBI’s annotation pipeline (optional parallel)

**Role:** **S8** — external comparison / NCBI-oriented path.

## Get it
- https://github.com/ncbi/egapx  

## How we use it
1. Keep lab S1/S3 as primary.  
2. Run EGAPx with correct *Vitis* taxid + RNA config YAML.  
3. AGAT + BUSCO both GFFs; spot-check NLR in GSAman.  
4. Document which one you release.

## Pitfalls
- Letting EGAPx silently replace curated NLR models without a diff table.  
- Wrong taxonomy / RNA YAML → empty or generic models.
