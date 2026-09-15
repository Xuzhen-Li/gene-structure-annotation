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


## Takeaways from Ji, Pertea & Salzberg 2026 (PDF)

Source: *Nat Rev Genet* doi:10.1038/s41576-026-00937-3 (full text read 2026-09-13). Summaries only — do not redistribute the PDF in this repo.

1. **Chooser depends on available information** — RNA-seq, related-species transcripts/proteins, and/or a close reference annotation (their Fig. 2 workflow).
2. **Close reference exists → prefer liftover** — Liftoff / LiftOn / CAT is often faster and more accurate than de novo; Liftoff also finds extra copies under CNV. Across larger distances, **LiftOn** adds spliced protein alignment (miniprot).
3. **No similar annotated species → automated pipelines** — they explicitly list BRAKER3, MAKER2, Gnomon, Ensembl, FINDER, GALBA, GeMoMa, **EviAnn** (RNA + protein-DNA + ab initio mixes).
4. **Ab initio limits** — AUGUSTUS / GeneMark / Tiberius (and peers) do not recover UTRs and usually one isoform/locus; UTRs and multi-isoform need RNA (or related transcripts).
5. **Transcript evidence** — StringTie (and Scallop / Trinity) for reconstruction; spliced RNA aligners STAR / HISAT2 / minimap2; protein-to-genome miniprot / Spaln3.
6. **Function is a second layer** — homology naming, domains, structure (AlphaFold-era), ncRNA databases; protein-coding FA ≠ GFF structure.
7. **Human still incomplete** — GENCODE / RefSeq / CHESS disagree especially on lncRNA; MANE is a one-isoform clinical consensus, not a full catalogue.
8. **EBP-scale future** — VGP / i5k / 10KP / EBP genomes become liftover sources; annotation quality must keep pace with assembly.

**How we map this (with Freedman & Sackton 2025):**

| Ji 2026 situation | Our branch |
|-------------------|------------|
| Close curated reference | S11 / Liftoff·LiftOn·CAT (provisional→qualify) |
| RNA + proteins, no close ref | **S1** BRAKER4/3 (+ StringTie compare) |
| Proteins only | **S2** GALBA/GALBA2 |
| Deep Iso-seq / evidence-first | **S3** (± EviAnn) |
| GPU ab initio compare | **S13** Tiberius / Helixer / ANNEVO |
| Institutional GenBank | **S8** EGAPx/Gnomon |
| FA after proteins | sibling `gene-function-annotation` |

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

---

## Haul 2026-09-14 (self-audit)

Search: WebSearch + CrossRef (PubMed/EuropePMC fallback). Goal: sources **beyond** Ji *NRG* 2026, Freedman *GR* 2025, Yandell 2012, Mudge 2016, and the Nat Methods Helixer/ANNEVO/EviAnn trio already Tier A/B above.

### Tier A additions (shape chooser or QC honesty)

| Paper | Venue | Role here |
|-------|--------|-----------|
| Vuruputoor et al., **Welcome to the big leaves: Best practices for improving genome annotation in non-model plant genomes** | *Appl Plant Sci* **11**:e11533 (2023) doi:[10.1002/aps3.11533](https://doi.org/10.1002/aps3.11533) | Plant-focused **best-practice** essay (BRAKER/MAKER inputs, soft-mask, short+long RNA, post-filters). Not Nature-family, but the clearest plant METHODS checklist beyond Freedman. |
| Sarrasin, Burger & Lang, **Eukan: a fully automated nuclear genome annotation pipeline for less studied and divergent eukaryotes** | *NAR Genom Bioinform* **8**:lqag003 (2026) doi:[10.1093/nargab/lqag003](https://doi.org/10.1093/nargab/lqag003) | Benchmark narrative on **protists / divergent eukaryotes**; pipelines still leave fragmented/fused/missing models; Eukan as alternate full stack. |
| van Workum et al., **MoGAAAP** | *NAR Genom Bioinform* **8**:lqag008 (2026) doi:[10.1093/nargab/lqag008](https://doi.org/10.1093/nargab/lqag008) | Peer-reviewed Liftoff+Helixer **provisional** + OMArk/BUSCO QC pack — reinforces S6/S11/S13 + A5b, not a new default draft. |

### Tier B additions (methods / commentary; do not silently replace S1)

| Paper | Venue | Maps to |
|-------|--------|---------|
| de Almeida et al., **Annotating the genome at single-nucleotide resolution with DNA foundation models** (SegmentNT) | *Nat Methods* (2025) doi:[10.1038/s41592-025-02881-2](https://doi.org/10.1038/s41592-025-02881-2) | S13 **watchlist** — foundation-model segmentation (genic + regulatory); not a BRAKER replacement when RNA+proteins exist. |
| Hiller, **Learning genes deeply** | *Nat Methods* (2026) doi:[10.1038/s41592-026-03035-8](https://doi.org/10.1038/s41592-026-03035-8) | Commentary on ANNEVO; keeps AI ab initio as **compare track**. |
| Kuster et al., **Ragnarok** (preprint) | bioRxiv (2025) doi:[10.1101/2025.10.03.680343](https://doi.org/10.1101/2025.10.03.680343) | Helixer + StringTie + miniprot → **Mikado** combiner — peer to S13+Mikado notes; wait for peer review before METHODS primacy. |

### Takeaways — what changes ROADMAP vs what does **not**

| Finding | Changes our package? |
|---------|----------------------|
| Plant soft-mask + combined evidence + structural/functional **filters** (Vuruputoor) | **No spine change** — already A0 soft-mask, S1 ETP, AGAT/GSAman; cite in TE/QC honesty. |
| Divergent eukaryotes / protists need dedicated stacks (Eukan) | **Minimal** — document as S14-class peer; default plant/animal chooser unchanged. |
| Provisional Liftoff+Helixer is publishable *with* OMArk/BUSCO caveats (MoGAAAP) | **No** — already S6/S11/S13 + A5b; strengthens “provisional” language. |
| SegmentNT / foundation models | **Watchlist only** — S13 compare; do **not** add a new draft ID. |
| RAGNAROK Mikado combiner | **Peer only** — maps to existing Mikado+Portcullis + S13 notes. |

**Palm / Arecaceae:** still **0** Nature-family gene-annotation *reviews* (rechecked 2026-09-14).

## Haul 2026-09-14b — tutorials & JOBIM meeting

Hands-on + symposium index: [`TUTORIALS_AND_MEETINGS.md`](TUTORIALS_AND_MEETINGS.md).

| Source | Role |
|--------|------|
| Galaxy GTN BRAKER3 / Helixer comparison (2025) | Teach S1 + S13-compare on public tiny genomes |
| JOBIM 2026 structural annotation mini-symposium (PEPI IBIS) | Community pitfalls: Helixer over-call; Tiberius/ANNEVO stronger; EGAPx ≠ RefSeq |
| Tiberius multi-clade preprint doi:10.64898/2026.04.24.720536 | Strengthens S13 plant/fungi/insect applicability |

**Chooser unchanged:** evidence-first; S13 remains compare-not-replace when RNA exists.

## QC packs & completeness cross-checks (2026-09-15)

| Source | Role for us |
|--------|-------------|
| Compleasm (Huang & Li *Bioinformatics* 2023) | Soft cross-check vs BUSCO; keep named BUSCO lineage |
| GAQET2 | Optional one-stop AGAT+BUSCO+PSAURON+OMArk |
| AnnoAudit (ERGA) | Optional RNA support + BRH + BUSCO/OMArk |
| Full shelf | [`QUALITY_SOURCES.md`](QUALITY_SOURCES.md) |
