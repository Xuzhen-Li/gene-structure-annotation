# SynGAP — haplotype / synteny annotation polish

**Role:** **S4** — compare ref vs hap annotations after Liftoff.

## Get it
- SynGAP (search current GitHub / paper from RELATED_SOFTWARE).  
- Notes in [`../../pipeline/05_syngap_polish.md`](../../pipeline/05_syngap_polish.md).

## Typical use
1. Qualified GFF on reference hap.  
2. Liftoff to hap2.  
3. SynGAP → conflict / PAV list.  
4. GSAman **only** those conflicts + priority families.

## Pitfalls
- Re-curating whole hap2 from scratch.  
- Ignoring true presence/absence as “errors.”
