# Erratum: GSAman tool paper vs last-mile opinion DOI

- Date: 2026-11-13 00:21 CST (Asia/Shanghai)
- Author: auto-paper-写作
- Purpose: record the DOI split between the GSAman tool paper and the last-mile opinion article. This file is new. It does not change any existing documentation, catalog, or pull request.
- Independent Crossref check (this turn, `https://api.crossref.org/works/{doi}`): both records are `journal-article` in *The Innovation*, issued 2026-10.
  - `10.1016/j.xinn.2026.101537` — *High-quality gene structure annotation: The last mile of reference genomes*. Authors: Chen, Chengjie; Chen, Ling-Ling; Xia, Rui. Keep this DOI as the opinion / last-mile article. Short form: Chen, Chen & Xia 2026.
  - `10.1016/j.xinn.2026.101471` — *GSAman: A gene-structure annotation manual curator for functional genomics research*. Crossref authors: Chen, Chengjie; Wu, Ya; Feng, Kangning; Liu, Hongsen; Liao, Yi; Zeng, Zaohai; Wu, Fengqi; Tan, Mengjin; Xu, Xiaolong; Huang, Songlin; Wang, Zihao; Tang, Shuyuan; Sun, Weijian; Zhang, Jisen; Chen, Ling-Ling; Xia, Rui. This is the GSAman tool paper. Short form used below: Chen, Wu et al. 2026. (A commissioning note listed the first five names only; this erratum uses the full Crossref list.)
- Style follows `/workspace/github-maintain-20261112/status/annot_catalog_v4_erratum_nlr_plantismash.md`.
- Scope: paste-ready English replacements for the three already-online docs named below. Do not edit those files here, do not edit function-catalog v4, do not edit directory frameworks, and do not open or update a pull request.

Replacement sentences below are English, ready to paste into a later new file or a later PR addition. They are not applied here.

---

## Files checked (read-only; blobs match main and the current PR-branch clones)

| Path | git blob | sha256 of the working copy |
|---|---|---|
| `gene-function-annotation/docs/RECENT_HIGH_QUALITY.md` (repo and `pr_clone_20261112`) | `83e56f94fd0755b7c036cdddf92ee732d0a7c4b3` | `2c14d9be5ee34a37f248ebe7e1c48e22b649090c915ad86b96cb1349ecb00c13` |
| `gene-function-annotation/docs/CITATIONS.md` (repo and `pr_clone_20261112`) | `2f713bc0b096ebef7b8a61249344189a4d2c04cc` | `ac617275978a40ddb33d89ab67c7f852c7ce306df39110786bb446111f68b875` |
| `gene-structure-annotation/docs/tools/gsaman.md` (repo and `pr_clone_20261112`) | `cd1457d6a4391c5e6d941df161223c38cc5cf9c8` | `dd8900ee497e8c504c30bc163b8e9c9f187191550913df8e362d1c36aeb4a2ad` |

Working copies used: `/workspace/github-maintain-20261112/gene-function-annotation/repo/docs/` and `/workspace/github-maintain-20261112/gene-structure-annotation/repo/docs/tools/`. The `pr_clone_20261112` copies have the same git blobs. None of these files was edited.

---

## ① — `docs/RECENT_HIGH_QUALITY.md` L24 (table A, tool / method papers)

Current L24:

> | GSAman last-mile | **The Innovation** (Cell Press partner) 2026 | Chen, Chen & Xia doi:10.1016/j.xinn.2026.101537 | upstream curation |

Table A is for tool / method papers to cite in METHODS. `10.1016/j.xinn.2026.101537` is the opinion article, not the GSAman tool paper. “Chen, Chen & Xia” is the correct short form for that opinion article, not for the tool paper.

**Proposed replacement for L24:**

> | GSAman | **The Innovation** (Cell Press partner) 2026 | Chen, Wu et al. doi:10.1016/j.xinn.2026.101471 | upstream curation |

Keep `10.1016/j.xinn.2026.101537` as a citation of the last-mile opinion article, not as the GSAman tool paper. A natural home is section B7 (below), not this METHODS tool row.

---

## ① — `docs/RECENT_HIGH_QUALITY.md` B7 heading and body (L82–L84)

Current L82–L84:

> ### B7. *The Innovation* — GSAman
>
> Upstream last-mile structure before FA.

The heading names the tool; the body uses the last-mile phrasing from the opinion article. After L24 is corrected, B7 should keep both papers, with the DOIs unmixed.

**Proposed replacement for L82–L84:**

> ### B7. *The Innovation* — last-mile structure, and GSAman
>
> The last-mile framing is the opinion article Chen, Chen & Xia, *High-quality gene structure annotation: The last mile of reference genomes*, doi:10.1016/j.xinn.2026.101537. The manual curator itself is GSAman (Chen, Wu et al., doi:10.1016/j.xinn.2026.101471). Cite 101471 for the tool in METHODS; keep 101537 when citing the last-mile argument. Upstream structure curation before FA.

---

## ① — `docs/CITATIONS.md` L31

Current L31:

> | GSAman | Chen, Chen & Xia *The Innovation* 2026 doi:10.1016/j.xinn.2026.101537 |

**Proposed replacement:** split into two rows, so 101537 is kept as the opinion article and 101471 is the tool paper.

> | GSAman | Chen, Wu et al. *The Innovation* 2026 doi:10.1016/j.xinn.2026.101471 |
> | Last-mile gene-structure annotation (opinion) | Chen, Chen & Xia *The Innovation* 2026 doi:10.1016/j.xinn.2026.101537 |

---

## ① — `docs/tools/gsaman.md` L3

Current L3:

> **Role:** Last mile (Chen, Chen & Xia 2026, *The Innovation*). Stages 03–04 in this repo.

“Chen, Chen & Xia 2026” are the authors of the opinion article, not a complete or distinctive author short form for the tool paper.

**Proposed replacement for L3:**

> **Role:** Last-mile manual curation. The tool paper is Chen, Wu et al. 2026, *The Innovation* (doi:10.1016/j.xinn.2026.101471). The last-mile argument is the opinion article Chen, Chen & Xia 2026, *The Innovation* (doi:10.1016/j.xinn.2026.101537). Stages 03–04 in this repo.

---

## Also found, not edited

These overnight catalog files also attach `10.1016/j.xinn.2026.101537` to the GSAman tool entry. They are not in the already-online repo docs named above. This erratum does not change them.

- `/workspace/github-maintain-20261112/gene-structure-annotation/catalog_entries_20261112/LM04_gsaman_curation/README.md` L39: `doi` cell currently `10.1016/j.xinn.2026.101537`. **Proposed:** use `10.1016/j.xinn.2026.101471` for the tool card; if the last-mile opinion is cited, add 101537 as a separate note, not as the tool DOI.
- `/workspace/github-maintain-20261112/gene-structure-annotation/catalog_entries_20261112/entries.tsv` GSA-LM04-001: same DOI swap for the tool row.

The structure-repo literature list already splits the two papers correctly (GSA-088 = 101537 opinion; GSA-095 = 101471 tool) and is not part of this correction.

---

## What this file does not do

- It does not edit `docs/RECENT_HIGH_QUALITY.md`, `docs/CITATIONS.md`, `docs/tools/gsaman.md`, function-catalog v4, either locked `directory_structure_v1.md`, or the catalog_entries files named above.
- It does not open, update, or merge a pull request, and it does not change PR #1 or the annotation PRs.
