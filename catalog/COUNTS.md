# Catalogue counts

Checked on 2026-11-26 (CST). [中文](#中文)

## Current count

The catalogue has **207 entries**: one row each in [`SOFTWARE_AUTHORITY.tsv`](SOFTWARE_AUTHORITY.tsv). This is the number to cite. It was counted from the repository root with:

```bash
python3 -B -c "import csv;print(sum(1 for _ in csv.DictReader(open('catalog/SOFTWARE_AUTHORITY.tsv',encoding='utf-8'),delimiter='\t')))"
```

Output: `207`. The breakdown below was counted with:

```bash
python3 -B -c "import csv,collections;r=list(csv.DictReader(open('catalog/SOFTWARE_AUTHORITY.tsv',encoding='utf-8'),delimiter='\t'));[print(k,v) for c in ('section','tier','added_2026_11_25') for k,v in collections.Counter(x[c] for x in r).items()]"
```

| Section | Title in the TSV | Entries |
|---|---|---|
| 1 | Assembly and assembly QC | 22 |
| 2 | Soft-mask with a trusted library | 11 |
| 3 | RNA and Iso-Seq evidence | 31 |
| 4 | Protein evidence | 8 |
| 5 | Ab initio gene finders | 12 |
| 6 | DNA language-model predictors | 11 |
| 7 | Lift-over and annotation transfer | 10 |
| 8 | Combiners and annotation pipelines | 15 |
| 9 | Non-coding RNA and pseudogene loci | 17 |
| 10 | Gene-model QC | 7 |
| 11 | Curation and browsers | 8 |
| 12 | GFF3 cleanup and release | 11 |
| 13 | Reference databases | 11 |
| 14 | Standards and reviews | 13 |
| 15 | Ideas not yet tied to one tool | 8 |
| viz | Visualization tools | 12 |
| | **Total** | **207** |

| Tier | Entries |
|---|---|
| standard | 81 |
| established | 57 |
| newer | 30 |
| niche | 16 |
| no paper | 23 |

## Why older pages show other numbers

Three totals appear in the repository. They are not in conflict: each is the total at a different date.

| Total | Date | What it counted | Can it be recounted from the TSV? |
|---|---|---|---|
| 135 | 2026-11 survey | 57 stage-folder cards in `catalog/` plus 78 entries in `docs/CATALOG_BY_TYPE_2026-11.md` | no; the survey files are kept as written |
| 174 | after 2026-11-14 | 135 − 2 older-version entries merged + 41 added | yes: rows with `added_2026_11_25 = no` (174) |
| 207 | after 2026-11-25 | 174 + 33 added | yes: all rows (207); rows with `added_2026_11_25 = yes`: 33 |

Pages that still show the older totals have a dated **Counts updated** note added at the end; their text was not changed:

- [`catalog/README.md`](../catalog/README.md) line 26
- [`docs/CATALOG_BY_TYPE_2026-11.md`](../docs/CATALOG_BY_TYPE_2026-11.md) line 33
- [`docs/CATALOG_BY_TYPE_2026-11.md`](../docs/CATALOG_BY_TYPE_2026-11.md) line 350
- [`docs/ROADMAP.md`](../docs/ROADMAP.md) line 170
- [`docs/ROADMAP.md`](../docs/ROADMAP.md) line 182
- [`docs/ROADMAP.md`](../docs/ROADMAP.md) line 258

## 中文

目录共 **207 条**，即 [`SOFTWARE_AUTHORITY.tsv`](SOFTWARE_AUTHORITY.tsv) 的行数，引用时以此为准。统计命令和分项见上文。
仓库里出现的 135、174、207 三个总数并不矛盾，分别是 2026-11 调研、2026-11-14 更新后和 2026-11-25 更新后的总数。仍写旧总数的页面已在文末追加一条带日期的“Counts updated”说明，正文未改。
