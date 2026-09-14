# A0b — Optional host-gene purge (ProtExcluder-style)

**Optional** extra filter if your TE library may still contain host CDS fragments.  
**Not** the laboratory grape gate itself (that gate is CDS BLAST + class rules → `emit_trusted`; see [`../docs/TE_LIBRARY.md`](../docs/TE_LIBRARY.md)).

Pattern: [ProtExcluder](https://github.com/NBISweden/ProtExcluder) · [`../docs/tools/protexcluder.md`](../docs/tools/protexcluder.md).

## Why (optional)

Even after a trusted emit, some projects re-check the lib against a proteome before soft-mask.  
Skipping A0b is OK when METHODS already documents a **CDS-gated trusted** file with version/sha256.  
Do **not** treat A0b as a substitute for building trusted (working → curatedlib is wrong).

## Order (if you run it)

1. Start from the **trusted** FASTA you will soft-mask with (not raw EDTA / not whole working).  
2. BLAST/DIAMOND against a curated proteome for your species/clade.  
3. Quarantine gene-like hits; keep an exclusion ID list for METHODS.  
4. Soft-mask with the purged lib (`A0_softmask.md`).

## Red lines

- Never put NLR / clear CDS peptides into the TE lib.  
- Do not claim “S5 requires A0b” — S5 requires **trusted** soft-mask + structure QC; A0b is optional hygiene.  
- Public stub: [vitis-te](https://github.com/Xuzhen-Li/vitis-te).
