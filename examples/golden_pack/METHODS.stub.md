<!-- EXAMPLE STUB — not a real release. Replace every FILL. Do not invent scores. -->
# METHODS — gene structure (EXAMPLE stub)

**Grade / status / primary (fill first):**  
`grade=L0|L1|L2` ; `status=provisional|qualified` ; `primary=S1|S11|S11-lite|S2|…` ; `TAG=FILL`

```text
Assembly: FILL (or ASSEMBLY_OK=yes — finished genome, Asm0/Asm1 checklist only).
Soft-mask: RepeatMasker -xsmall with trusted TE curatedlib FILL_filename
  (version FILL; sha256:FILL). working/raw EDTA not used for A0.
  softmasked_fraction=FILL (homology to this lib ≠ genome TE%).
Primary draft: FILL (S11 = Liftoff vFILL + gap-fill FILL; S11-lite = lift-only provisional).
  Protein evidence: FILL (OrthoDB/clade/path). RNA: FILL samples / BAM policy.
Merge / polish: FILL (none | EVM | TSEBRA | …).
Proteins: one representative CDS translation per gene from release GFF.
QC: BUSCO vFILL lineage FILL_odb12 (mode proteins) C/D/F/M=FILL;
    PSAURON FILL; priority loci FILL (curated or deferred).
Optional S5: OMArk/Compleasm FILL.
Release: GFF + proteins.faa + this METHODS under release/<TAG>/.
```

**Do not** claim L1/qualified for S11-lite. **Do not** leave `YOUR_*` or bare `eukaryota` lineages.
