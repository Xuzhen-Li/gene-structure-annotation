# Soft-masking with a trusted TE library

[中文](trusted-softmask.zh.md) · [Knowledge units](README.md)

## 1. What it is

Before genes are predicted, repeats in the genome are masked. **Soft-masking** writes repeat bases in lower case and keeps the sequence; gene finders then give those bases less weight. **Hard-masking** replaces repeat bases with `N`, so the sequence is lost. The repeats are found with a library of transposable-element (TE) consensus sequences. Which library is used decides which bases are masked.

## 2. How the evidence is structured

A TE library passes through four products, and only the last one may be used for gene soft-masking:

| Product | What it is | Used for gene soft-mask? |
|---|---|---|
| Raw discovery library (for example the EDTA output) | everything the discovery tools called | no |
| Working library | consensus sequences after clustering and trimming | no |
| Classifier labels | domain and superfamily names added to the working set | no; labels only |
| Trusted library | after a recorded host-gene purge and documented classification rules, with version and sha256 | yes |

Non-TE repeats (tandem repeats, telomere, rDNA) form a separate track and do not enter the trusted library. The library itself is built in [TE-Lib](https://github.com/Xuzhen-Li/TE-Lib); this repository only uses it (step A0).

## 3. How to recognise a correct soft-mask (field card)

- The masked genome has lower-case repeats, not runs of `N`.
- One trusted library file is named, with its version and sha256.
- METHODS says that the working library was not used as the trusted library.
- The masked fraction is not reported as the TE content of the genome; the two are different numbers.

The pass and fail rules are gate G2 and the automatic fails in [`docs/EVALUATION.md`](../EVALUATION.md#g2--soft-mask-honesty); this page does not restate them.

## 4. Repository default and branches

The default step is A0 in [`docs/TE_LIBRARY.md`](../TE_LIBRARY.md) and [`docs/TRUSTED_TE_PATH.md`](../TRUSTED_TE_PATH.md). Changing the library or the masking settings later is branch S10 ([`catalog/_branches.md`](../../catalog/_branches.md)). Tools for this step are in [catalogue section 2](../../catalog/METHODS_CATALOG.md#section-2).

## 5. What is known in plants and in *Vitis*

- EDTA was benchmarked on a curated rice TE library and tested on maize and *Drosophila* (claim 3 below).
- Repeats can hold real genes, for example NLR resistance genes, which is one reason not to hard-mask ([`docs/EVALUATION.md`](../EVALUATION.md#g2--soft-mask-honesty), G2 background).
- The grapevine route from discovery to a trusted library is the worked example in TE-Lib ([soft-mask hand-off](https://github.com/Xuzhen-Li/TE-Lib/blob/main/docs/detection/softmask_handoff.md)). How a host-gene purge tool removes flanking sequence is marked there as **[待确认]** and is not repeated here as fact.

## 6. Claims and sources

| Claim | Source | Quoted sentence or figure | What was read |
|---|---|---|---|
| BRAKER expects a soft-masked genome. | BRAKER README ([Gaius-Augustus/BRAKER](https://github.com/Gaius-Augustus/BRAKER)) | “BRAKER should only be applied to genomes that have been softmasked for repeats!” | README, section on typical BRAKER calls |
| Masking avoids false gene structures in repeats. | BRAKER README, as above | “This will avoid the prediction of false positive gene structures in repetitive and low complexitiy regions.” (spelling as in the source) | README, section on the genome file |
| EDTA builds a filtered, non-redundant TE library; it was benchmarked on rice. | Ou et al. 2019, *Genome Biol* 20:275, [doi:10.1186/s13059-019-1905-y](https://doi.org/10.1186/s13059-019-1905-y) | “Using the most robust programs, we create a comprehensive pipeline called Extensive de-novo TE Annotator (EDTA) that produces a filtered non-redundant TE library for annotation of structurally intact and fragmented elements.” | Abstract (PubMed 31843001) |
| Hard-masking removes sequence that predictors need. | [`docs/EVALUATION.md`](../EVALUATION.md#g2--soft-mask-honesty), G2 background (this repository) | “Hard-masking to `N` deletes sequence that predictors need; soft-mask (`-xsmall`) keeps bases but down-weights repeats” | The file at the current main branch |
| Only the trusted library may be used for gene soft-mask. | TE-Lib, [`docs/detection/softmask_handoff.md`](https://github.com/Xuzhen-Li/TE-Lib/blob/main/docs/detection/softmask_handoff.md) | “This trusted file, with its version and sha256, is the only library that may be used for gene soft-mask or as EDTA `--curatedlib`.” | The file at the current main branch |
| Non-TE repeats stay out of the trusted library. | [`docs/TE_LIBRARY.md`](../TE_LIBRARY.md) (this repository) | “Non-TE repeats (TRF, telomere, rDNA, …) are a **separate non-TE track** — **never** enter `--curatedlib`.” | The file at the current main branch |

## 7. See also

- Book: [chapter 3, Soft-mask with a trusted library](../../book/chapters/03-soft-mask-with-a-trusted-library.md)
- TE-Lib: [home page](https://github.com/Xuzhen-Li/TE-Lib) (TE classes, detection tools, the trusted-library route)
- Knowledge units: [Gene models and the evidence behind them](gene-model-concepts.md); [Is the gene set good enough?](model-qc-criteria.md)
