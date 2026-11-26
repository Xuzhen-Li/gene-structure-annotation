# Knowledge units

[中文](README.zh.md) · [Home page](../../README.md) · [Knowledge map](../KNOWLEDGE_MAP.md)

A knowledge unit is a short page on one concept or one set of criteria. The book chapters are the long text; a unit states the main points and gives, for each statement, the source it was taken from and what was read. Units follow the layout of TE-Lib.

## Units

| Unit | Kind | Chinese |
|---|---|---|
| [Gene models and the evidence behind them](gene-model-concepts.md) | concept | [基因模型及其证据](gene-model-concepts.zh.md) |
| [Soft-masking with a trusted TE library](trusted-softmask.md) | concept | [用可信 TE 库做 soft-mask](trusted-softmask.zh.md) |
| [Is the gene set good enough? (criteria)](model-qc-criteria.md) | criteria | [基因集够不够好？（判据）](model-qc-criteria.zh.md) |

Numbering schemes and how older numbers map to current ones: [`NUMBERING.md`](NUMBERING.md).

The first units cover the topics where mistakes are most common. Other topics are covered in the book and the catalogue; see the [knowledge map](../KNOWLEDGE_MAP.md#topics).

## Layout of a unit

1. **What it is**: the concept in a few sentences.
2. **How the evidence is structured**: the kinds of evidence or products, usually as a table.
3. **How to recognise it**: a short field card to check a file or a report.
4. **Repository default and branches**: a pointer to the workflow pages, not a copy.
5. **What is known in plants and in *Vitis***: with **[待确认]** wherever no opened source supports a statement.
6. **Claims and sources**: a table with the claim, the source, the quoted sentence and what was read.
7. **See also**: book chapters, other units and catalogue sections.

## Rules

- Criteria units explain what a check measures and link to [`docs/EVALUATION.md`](../EVALUATION.md). Thresholds and gates are written only there.
- A quoted sentence is copied from the source named in the same row. If the source was not opened for the unit, the row says so.
- **[待确认]** marks a statement that still needs an opened source. It is not removed until one is cited.
- Each unit has a Chinese page with the same sections; quotations stay in the language of the source.
- Older pages are not moved. They are listed under [older pages](../KNOWLEDGE_MAP.md#older-pages).
