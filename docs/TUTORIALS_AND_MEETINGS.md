# External tutorials & meetings — gene structure

Curated **hands-on software tutorials** and **meeting / symposium** notes that teach structural annotation.  
These are **complements**, not replacements, for this repo’s ROADMAP / flow_tool / EVALUATION.

Chinese teaching twin: [`zh/17_外部教程与会议.md`](zh/17_外部教程与会议.md).

---

## Why look outside

Galaxy GTN and conference mini-symposia show the same tools on small public datasets, with BUSCO/OMArk and browser views. Use them to **learn the buttons**; use this playbook to **choose the branch** and **grade a release**.

---

## A. Software flow tutorials (hands-on)

| Tutorial | What you practice | Maps to us | URL |
|----------|-------------------|------------|-----|
| **Galaxy — Genome annotation with BRAKER3** | Masked genome + RNA BAM + proteins → BRAKER3 → BUSCO / OMArk → JBrowse | **S1** spine + QC | https://training.galaxyproject.org/training-material/topics/genome-annotation/tutorials/braker3/tutorial.html |
| **Galaxy — Helixer vs BRAKER3 comparison** | Run both; compare BUSCO/OMArk | **S1** + **S13 compare** (not silent replace) | https://training.galaxyproject.org/training-material/topics/genome-annotation/tutorials/comparison-braker-helixer-annotation/tutorial.html |
| **Galaxy — Genome annotation with Helixer** | Ab initio DL path (see GTN genome-annotation topic) | **S13** | https://training.galaxyproject.org/training-material/topics/genome-annotation/ |
| **Galaxy — Masking repeats with RepeatMasker** | Soft/hard mask literacy (BRAKER tutorial prerequisite) | **A0** | Linked from BRAKER3 GTN “Requirements” |
| **Harvard FAS — How to annotate a genome** | Evidence chooser teaching | Chooser / ROADMAP | https://informatics.fas.harvard.edu/resources/tutorials/how-to-annotate-a-genome/ |
| **Harvard Informatics GenomeAnnotation wrappers** | BRAKER / Liftoff / TOGA / MAKER tutorials | S1 / S11 peers | https://github.com/harvardinformatics/GenomeAnnotation |
| **NCBI EGAPx README** | Public EGAPx / Gnomon-style package | **S8** compare | https://github.com/ncbi/egapx |
| **WorkflowHub — annotation-braker3** | Portable Galaxy workflow + OMArk | S1 lab demo | https://workflowhub.org/workflows/2029 |

**Honesty:** GTN BRAKER3 uses a **tiny fungal** demo (`Mucor`). Completeness will look different on a plant T2T. Still excellent for learning the **flow**.

---

## B. Meetings & community feedback (2026)

### JOBIM 2026 — mini-symposium on eukaryotic **structural** gene annotation

- **Title (FR):** *L’annotation structurale des gènes dans les génomes Eucaryotes reste-t-elle toujours un défi ?*  
- **Hub:** https://pepi-ibis.inrae.fr/node/136  
- **Theme:** long-read RNA for coding/ncRNA/isoforms; **AI ab initio** (Helixer / Tiberius / ANNEVO); expression-break ideas; still need manual expertise / combiners on hard gene families.

**Slides / talks to read (public PDFs on PEPI IBIS):**

| Talk | Take-home for this playbook | URL |
|------|-----------------------------|-----|
| Legeai / Chathuant — *Successes and pitfalls…* | Helixer **over-calls** + short aberrant exons; ANNEVO ≈ Tiberius ≳ Helixer; EGAPx ≠ RefSeq and is RNA-library sensitive; combiners still needed | https://pepi-ibis.inrae.fr/sites/pepi-ibis/files/PoleAnnotationGenome/JOBIM2026/05_JOBIM2026_Legeai-Chathuant.pdf |
| Brunaud — Arabidopsis official vs Helixer | Helixer easy/fast; coding-only limits; Tiberius plant models often preferred in their notes; no isoforms/ncRNA from Helixer-class alone | https://pepi-ibis.inrae.fr/sites/pepi-ibis/files/PoleAnnotationGenome/JOBIM2026/03_JOBIM2026_Brunaud.pdf |

**How we encode this:** S13 = **compare** lane; EVALUATION automatic-fail if Helixer silently replaces S1 when RNA exists; soft metrics warn that rising gene counts ≠ better.

Related preprint (multi-clade Tiberius): doi:[10.64898/2026.04.24.720536](https://doi.org/10.64898/2026.04.24.720536).

---

## C. Institutional / consume-not-DIY

| Source | Use | URL |
|--------|-----|-----|
| Ensembl / DToL genebuild materials | Understand projection vs full build; prefer **S11 consume** over claiming DIY Ensembl | Ensembl DToL docs (see PEER_PIPELINES) |
| CantuLab AnnotationPipeline2-EVM | S14 teaching parallel | https://github.com/CantuLab/AnnotationPipeline2-EVM_based-DClab |

---

## D. What this page is not

- Not a live conference calendar.  
- Not permission to skip EVALUATION.  
- Functional eggNOG/IPS Galaxy tutorial → sibling [gene-function-annotation `TUTORIALS_AND_MEETINGS.md`](https://github.com/Xuzhen-Li/gene-function-annotation/blob/main/docs/TUTORIALS_AND_MEETINGS.md).

See also: [`REVIEWS.md`](REVIEWS.md) · [`PEER_PIPELINES.md`](PEER_PIPELINES.md).
