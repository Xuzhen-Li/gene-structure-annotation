# A2b — Second prediction set

One engine is not enough for complex plant genomes. Run a complementary set:

| Primary (A2) | Second set | Why |
|--------------|------------|-----|
| BRAKER3 | **GeMoMa** from PN40024 / close *Vitis* | Homology transfer catches models BRAKER fragments |
| BRAKER3 | **EviAnn** | Transcript/evidence backbone (keen-laras) |
| BRAKER3 | **GALBA** | Close-protein path if OrthoDB BRAKER looks thin |
| BRAKER3 | **Liftoff** from PN40024 | Fast haplotype transfer (`A2c`) |
| Helixer | AUGUSTUS / BRAKER | Sylvan-style ab initio diversity |
| (optional) | **EGAPx** | NCBI Gnomon parallel set (`A2d`) |

Outputs: `DRAFT_GFF` (primary) and `DRAFT_GFF_B` (second). Merge in A4.
