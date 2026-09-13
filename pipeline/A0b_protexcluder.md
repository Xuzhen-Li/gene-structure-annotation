# A0b — Keep real genes out of the repeat library

Part of the lab TE scheme: [`../docs/TE_LIBRARY.md`](../docs/TE_LIBRARY.md) step 5–6a.  
Pattern: Krabbenhoft / [ProtExcluder](https://github.com/NBISweden/ProtExcluder) · tool notes [`../docs/tools/protexcluder.md`](../docs/tools/protexcluder.md).

## Why

EDTA/RepeatModeler consensi often include **host gene fragments**. If those stay in the RepeatMasker library, soft-mask will lowercase real exons (NLR, LRR, kinase, stilbene synthase, …) and structure annotation will miss or shatter them — fatal for grape T2T / S5 delivery.

## Order

1. Start from **trimmed** consensi (post-TEtrimmer), not only raw EDTA if you already trimmed.  
2. BLAST/DIAMOND the library against a curated plant proteome / UniProt plant subset / grape proteins.  
3. Exclude significant gene hits from the lib (or quarantine into a “held_out_genelike.fasta” for METHODS).  
4. Soft-mask **only** with the purged lib (`A0_softmask.md`).  
5. Keep a list of removed consensi IDs in `WORK_DIR/mask/te_hostgene_excluded.txt`.

## Red lines

- Never put NLR / R-gene / clear CDS peptides into the TE lib.  
- Pair with [vitis-te](https://github.com/Xuzhen-Li/vitis-te) curation — do not publish another group’s raw TE calls as yours.  
- Skipping A0b to “save time” is not allowed on S5 / publication soft-mask.
