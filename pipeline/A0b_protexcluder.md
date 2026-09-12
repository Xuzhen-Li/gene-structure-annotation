# A0b — Keep real genes out of the repeat library

Krabbenhoft / ProtExcluder pattern ([NBISweden/ProtExcluder](https://github.com/NBISweden/ProtExcluder)):

1. After RepeatModeler (or EDTA consensus), BLAST the library against a curated plant proteome / UniProt plant subset.
2. Exclude hits that look like host genes (NLR, kinases, etc.) from the RepeatMasker library.
3. Soft-mask with the cleaned lib only.

This pairs with [vitis-te](https://github.com/Xuzhen-Li/vitis-te) curation notes: never put NLR/R-gene proteins into the TE lib.
