# Changelog

[中文](CHANGELOG.zh.md)

A public summary of changes to the pages and the catalogue.

## 2026-11-26: knowledge-base layout and licence

- The home page now opens with how the repository is organised, following TE-Lib, then a knowledge map and the book chapters.
- New knowledge units in [`docs/kb/`](docs/kb/README.md), each with a claim and source for every statement. [`docs/kb/NUMBERING.md`](docs/kb/NUMBERING.md) maps the numbering schemes and marks the older ones as legacy.
- New [`docs/workflow/README.md`](docs/workflow/README.md) names the authoritative page for each workflow question.
- The full methods catalogue moved from the home page to [`catalog/METHODS_CATALOG.md`](catalog/METHODS_CATALOG.md) with its text unchanged apart from relative links. The home page keeps a short list of the sections, and the old section links still work, including the anchors that were generated from the old headings.
- New [`catalog/README.by-type.md`](catalog/README.by-type.md) and [`catalog/COUNTS.md`](catalog/COUNTS.md): 207 entries, recounted from the TSV. Pages that show older totals have a dated note at the end; their text was not changed.
- New [`docs/KNOWLEDGE_MAP.md`](docs/KNOWLEDGE_MAP.md) indexes every page by topic. [`docs/TOOLS_NOTES_OVERLAP.md`](docs/TOOLS_NOTES_OVERLAP.md) lists tools with a page in both `docs/tools/` and `docs/notes/` (suggestions only).
- [`docs/ROADMAP.md`](docs/ROADMAP.md): dated notes were inserted under the headings that still said a pull request was open or the work was not committed, stating that the changes were later merged. Nothing else in the file was changed.
- Code is under the MIT License; text, tables and figures made for this repository are under CC BY 4.0. See [`NOTICE.md`](NOTICE.md).
- Links to the TE repository on the home page use its new name, TE-Lib (formerly vitis-te).
- The two dated notes below moved here from the home page; they are also kept in the catalogue page.

## 2026-11-25: one table per catalogue section

Each type section now shows its entries as one table: tool link, role (default, branch tool or alternative, as stated on this page), what it does and when to use it, paper, lab, tier with OpenAlex citations, and a short evaluation quoted from the paper abstract, a benchmark paper or the GitHub repository. 33 entries were added after three search passes (a drafted candidate list, OpenAlex keyword searches, and curated tool lists plus benchmark papers); each added entry has a DOI that resolves to a matching title, and each link was opened before use. The catalog now has 207 entries, including a new visualization section; the counts in the list below are current. Per-entry data are in `catalog/SOFTWARE_AUTHORITY.tsv` and the same tables, without the section notes, are in [`docs/software/README.md`](docs/software/README.md). A book-style study guide is in [`book/`](book/README.md).

## 2026-11-14: clusters in each catalogue section

Each section now opens with a **Clusters:** list. It groups the entries as alternatives (pick one), complementary (use together) or in order (run in sequence), with a note on when to pick which. Inside a list, “A or B” means pick one of the two and “A → B” is one fixed route. Different versions of one program are now one entry named for the latest version; older versions are only mentioned in that entry's note. A workflow chart with tool choices and decision points is in [`docs/ROADMAP.md`](docs/ROADMAP.md#workflow-2026-11-14).
