# Reviews & benchmarks that shape this playbook

Search logged 2026-09-13 via `storm-research` + `plant-lit-review` + `nature-academic-search` fallback (PubMed E-utilities + CrossRef + Web).  
Sources: PubMed, CrossRef, Nature.com listings, EuropePMC/Web.  
Sibling FA patterns: [gene-function-annotation `RECENT_HIGH_QUALITY.md`](https://github.com/Xuzhen-Li/gene-function-annotation/blob/main/docs/RECENT_HIGH_QUALITY.md).

## Inclusion (this note)

- **In:** method reviews, comparative benchmarks, Nature-family method papers that reset defaults for **gene structure** annotation.
- **Out:** single-species genome/data papers (unless they define a reusable METHODS framework).
- **Palm check:** PubMed `(Elaeis OR oil palm OR date palm OR Arecaceae) AND (genome/gene annotation) AND Review` → **0 hits** (2026-09-13). Arecaceae hits are assemblies / evidence-gene-set papers, not Nature reviews.

## Tier A — must-read reviews / benchmarks

| Paper | Venue | Role here |
|-------|--------|-----------|
| Ji, Pertea & Salzberg, **Annotating genomes at increased scale and resolution** | *Nat Rev Genet* **27**:429–441 (2026) doi:[10.1038/s41576-026-00937-3](https://doi.org/10.1038/s41576-026-00937-3) · PMID [41703124](https://pubmed.ncbi.nlm.nih.gov/41703124/) | **The recent Nature-family *review*** on structure + function annotation at EBP/DToL scale; StringTie / Liftoff lineage; ncRNA still hard. Online 2026-02-17. |
| Freedman & Sackton, **Building better genome annotations across the tree of life** | *Genome Research* **35**:1261–1276 (2025) doi:[10.1101/gr.280377.124](https://doi.org/10.1101/gr.280377.124) · PMID [40234028](https://pubmed.ncbi.nlm.nih.gov/40234028/) | **Comparative benchmark** (12 methods × 21 species). Top: **TOGA**, **BRAKER3**, **StringTie**. RNA matters when WGA unavailable; TOGA weaker on some monocots. |
| Yandell & Ence, **A beginner’s guide to eukaryotic genome annotation** | *Nat Rev Genet* 2012 doi:[10.1038/nrg3174](https://doi.org/10.1038/nrg3174) | Classic: prediction ≠ annotation; evidence pipelines (MAKER-era). |
| Mudge & Harrow, **The state of play in higher eukaryote gene annotation** | *Nat Rev Genet* 2016 doi:[10.1038/nrg.2016.119](https://doi.org/10.1038/nrg.2016.119) | AS / ncRNA / functional lag behind structure. |

## Tier B — Nature Methods papers (not reviews; reset defaults)

| Paper | Venue | Maps to |
|-------|--------|---------|
| Holst et al., **Helixer** | *Nat Methods* 2026 doi:[10.1038/s41592-025-02939-1](https://doi.org/10.1038/s41592-025-02939-1) · PMID [41286201](https://pubmed.ncbi.nlm.nih.gov/41286201/) | S13 AI ab initio |
| Zhang, Ye et al., **ANNEVO** | *Nat Methods* 2026 doi:[10.1038/s41592-026-03036-7](https://doi.org/10.1038/s41592-026-03036-7) · PMID [41820667](https://pubmed.ncbi.nlm.nih.gov/41820667/) | S13; “annotation gap” narrative |
| Zimin et al., **EviAnn** | *Nat Methods* 2026 doi:[10.1038/s41592-026-03156-0](https://doi.org/10.1038/s41592-026-03156-0) · PMID [42399474](https://pubmed.ncbi.nlm.nih.gov/42399474/) | S3 evidence-only |

## Decision tree (adopted)

Aligned to Freedman & Sackton 2025 + Harvard FAS tutorial; framed by Ji/Pertea/Salzberg 2026 scale narrative:

```text
Have a close, high-quality reference + WGA feasible?
  YES → TOGA2 (± Liftoff/LiftOn; monocots: check BUSCO, may add BRAKER/StringTie)
  NO  → Have paired-end RNA-seq?
          YES → BRAKER3/4 (S1)  AND  compare StringTie→TransDecoder
                Prefer StringTie path when UTR/noncoding / novel isoforms matter
          NO  → proteins only → GALBA/GALBA2 (S2) or BRAKER-EP
AI ab initio (Helixer / Tiberius / ANNEVO / OrionGeno) = S13 when evidence is thin or as a compare track
Evidence-only (EviAnn) = S3 when RNA+proteins are abundant and you want traceable CDS
Institutional GenBank package = EGAPx (S8)
```

Tutorial: https://informatics.fas.harvard.edu/resources/tutorials/how-to-annotate-a-genome/

## Palm / Arecaceae (not a Nature review)

| Item | What it is |
|------|------------|
| Chan et al., Evidence-based gene models… oil palm | *Biology Direct* 2017 — crop high-confidence gene-set METHODS (Seqping + Fgenesh++), **not** Nature |
| Recent Elaeis / coconut / açaí papers | Genome assemblies + annotation *as Methods sections* (G3, Genome Biology, etc.) |
| PubMed Review filter for palm + gene annotation | **0** reviews (search date above) |

If you remembered “Nature + 棕榈 + 基因注释”, the closest *Nature review* on gene annotation is **Ji et al. 2026 NRG** (no palm). Palm content is crop genome case studies.

## How this changes our package

1. Cite **Ji et al. 2026** as the Nature-family overview; cite **Freedman & Sackton 2025** as the method chooser.  
2. Default **S1 BRAKER4/3**; always keep **StringTie→TransDecoder** compare when RNA exists.  
3. **TOGA2** when WGA+reference exist (check monocots).  
4. Nat Methods trio → S13 / S13 / S3 — not silent S1 replacements.  
5. Qualify with BUSCO + OMArk + PSAURON; single BUSCO% is not enough.
