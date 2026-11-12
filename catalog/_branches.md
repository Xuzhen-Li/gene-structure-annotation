# Branch view (S1–S14)

Branch IDs follow [`docs/ROADMAP.md`](../docs/ROADMAP.md). They are views over the stage folders; no entry is stored here.

- **Draft routes** (pick one per genome): S1, S2, S3, S6, S11 (incl. S11-lite), S13, S14.
- **Overlays**: S4, S5, S7, S8, S9, S10, S12. README L2 = L1 + S5 overlay.

| Branch | Path through stages (links to entries) |
|---|---|
| S1 | [A1](A1_engine_and_rna/README.md) → [A2](A2_drafts/README.md) → [A4](A4_aggregation/README.md) → [A5](A5_structure_qc/README.md) → [A3](A3_proteins/README.md) → last mile |
| S3 | [A1 long-read evidence](A1_engine_and_rna/README.md) → [A2](A2_drafts/README.md) → A4 → A5 |
| S4 | after S1/S3 → [A2c transfer](A2_drafts/README.md) → [LM05 harmonise](LM05_syngap_polish/README.md) |
| S5 | [A5 QC](A5_structure_qc/README.md) → [LM04 curation](LM04_gsaman_curation/README.md) |
| S7 | any draft → **use the NLR result of gene-function-annotation F8 to mark windows** → [LM04](LM04_gsaman_curation/README.md) re-curates gene models in those windows. HRP itself appears only in the function catalog. Genome-level NLR locus finders (e.g. NLR-Annotator): placement F8 vs S7 [待确认] |
| S10 | back to [A0](A0_softmask/README.md): change the trusted library or masking settings only; rebuilding the TE library goes to vitis-te → rerun the same draft route |
| S11 | [A2c](A2_drafts/README.md) (Liftoff/LiftOn/CAT) → A2e gap-fill → A4 → A5 → last mile |
| S13 | [A2b compare tracks](A2_drafts/README.md) — do not silently replace an evidence draft when RNA exists |
| S12 | [LM06 release](LM06_release/README.md) freeze rules |

[Back to catalog index](README.md)
