# EviAnn (Evidence Annotation)

**Not an NCBI product** — standalone evidence-based annotator (Zimin lab). Often confused with “EvoAnno”; NCBI’s public eukaryotic stack is **EGAPx/Gnomon**.

## Links
- Release / install: https://github.com/alekseyzimin/EviAnn_release (use release tarball `EviAnn-X.X.X.tar.gz`, not “Source code”)  
- Paper: *Nature Methods* 2026 doi:10.1038/s41592-026-03156-0  

## What it does
- **Evidence-only** gene models (no ab initio HMM/DL).  
- Inputs: RNA-seq BAM and/or transcripts + related-species (or UniProt) proteins (`miniprot`).  
- Soft-mask **not required**.  
- Outputs GFF3 (+ coding / lncRNA); evidence origin per CDS is traceable.  
- Fast: mouse-scale ~1 h on ~24 cores (with BAMs + related proteins) per authors.  
- Benchmarks in paper: competitive / better than BRAKER3, MAKER2, FINDER when evidence is strong.

## GenBank path
- GFF3 aimed at NCBI GenBank specs; submit with **table2asn** (see release README).  
- Distinct from **EGAPx ASN** submission path — both can land in GenBank, different pipelines.

## Our mapping
- Primary hook: **S3** evidence-first / deep Iso-seq+RNA backbone.  
- Typical recipe: IsoQuant|StringTie → (optional SQANTI3) → **EviAnn** (+ related proteins) → qualify; add BRAKER orphans only where evidence is thin.  
- Prefer EviAnn when you want “every CDS from data” transparency; prefer **S1 BRAKER** when you need ab initio fill for silent genes.  
- Do not confuse with EGAPx (`notes/egapx_gnomon.md`).
