# Catalog — new structural tools, databases and ideas by stage (2026-11)

Entry cards for software, databases and ideas found in the 2026-11 survey, filed under this repo's own stage IDs (Asm0/Asm1, A0, A1, A2, A4, A5, A3, last mile 01–06, A6). Folder order follows the execution order in [`docs/STAGE_IO.md`](../docs/STAGE_IO.md). Last-mile folders carry an `LM` prefix only so they do not clash with vitis-pangenome script numbers; inside the cards the original number ("last mile 04") and file names are kept. Branch IDs S1–S14 are a view only: [`_branches.md`](_branches.md). Databases across stages: [`_databases.md`](_databases.md). Flat one-page list of the same survey: [`../docs/CATALOG_NEW_TOOLS_2026-11.md`](../docs/CATALOG_NEW_TOOLS_2026-11.md).

**Repo-wide boundary** ([`docs/BOUNDARY.md`](../docs/BOUNDARY.md)): no GO, KEGG, InterPro tables, readable names or eggNOG; no TE library construction (layer 3, vitis-te); no HRP or other NLR classifiers (gene-function-annotation F8). Protein tools whose description says "structure" (e.g. DeepFRI) mean **protein 3D structure** and are not gene-structure annotation; they are not filed here.

| Stage | Entries | Folder |
|---|---|---|
| Asm0 — assembly | 0 | [`Asm0_assembly/`](Asm0_assembly/README.md) |
| Asm1 — assembly QC | 1 | [`Asm1_assembly_qc/`](Asm1_assembly_qc/README.md) |
| A0 / A0b — soft-mask with a trusted library | 2 | [`A0_softmask/`](A0_softmask/README.md) |
| A1 / A1b — engine choice and RNA / Iso-Seq evidence | 11 | [`A1_engine_and_rna/`](A1_engine_and_rna/README.md) |
| A2 — drafts (A2 primary, A2b second predictor, A2c transfer, A2d EGAPx, A2e S11 gap-fill, protein evidence) | 22 | [`A2_drafts/`](A2_drafts/README.md) |
| A4 — aggregation (A4a TSEBRA, A4b Mikado, A4c–A4d EVM, A4e PASA update) | 0 | [`A4_aggregation/`](A4_aggregation/README.md) |
| A5 — structure QC (A5b–A5e, structure_qa qa01–qa10) | 4 | [`A5_structure_qc/`](A5_structure_qc/README.md) |
| A3 — proteins from GFF | 0 | [`A3_proteins/`](A3_proteins/README.md) |
| Last mile 01 — BUSCO / PSAURON QC | 0 | [`LM01_qc_busco_psauron/`](LM01_qc_busco_psauron/README.md) |
| Last mile 02 — priority loci (02, 02b) | 0 | [`LM02_priority_loci/`](LM02_priority_loci/README.md) |
| Last mile 03 — evidence pack | 0 | [`LM03_evidence_pack/`](LM03_evidence_pack/README.md) |
| Last mile 04 — GSAman / manual curation | 5 | [`LM04_gsaman_curation/`](LM04_gsaman_curation/README.md) |
| Last mile 05 — SynGAP polish / multi-haplotype harmonisation | 1 | [`LM05_syngap_polish/`](LM05_syngap_polish/README.md) |
| Last mile 06 — release | 6 | [`LM06_release/`](LM06_release/README.md) |
| A6 / A6b — hand-off to function | 0 | [`A6_handoff_to_function/`](A6_handoff_to_function/README.md) |
| Cross-stage — whole pipelines, reviews, standards | 5 | [`X_cross_stage/`](X_cross_stage/README.md) |

Total entries: 57.

**Card fields:** entry_id (`GSA-<stage>-NNN`), type, stage, branches, what it does, url, doi, venue / year, venue_label (Allowlisted / Below allowlist / Preprint, as in the function repo's `RECENT_HIGH_QUALITY.md`), latest release, license, plant_evidence, existing_doc, io (STAGE_IO variable names), layer_check, verdict (include / needs evidence / exclude), checked_version, checked_at_CST, checked_by.

**How checked:** each DOI was resolved in Crossref (DataCite for Zenodo) and the title matched to the entry; GitHub repos, latest release and licence were read from the GitHub API on 2026-11-12 (CST). `[待确认]` = not verified. No entry was added from memory without a resolved record or official page. Rows marked "update" refer to tools already mentioned in this repo (newer paper, release or angle). Proposals only; nothing changes the default path until tested.
