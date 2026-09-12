# Optional: SynGAP polish

Paper: Wu F., Mai Y., Chen C., Xia R. (2024) SynGAP: a synteny-based toolkit for
gene structure annotation polishing. *Genome Biology* 25:218.
doi:10.1186/s13059-024-03359-8

Use when you have **two or more** related haplotype / cultivar annotations and
want synteny to flag missing or split models before another GSAman pass.

Typical place in the grape stack: after first GSAman pass on PN40024-like ref,
before transferring models onto other haplotypes that feed
[vitis-pangenome](https://github.com/Xuzhen-Li/vitis-pangenome).

Install and run from upstream SynGAP; keep only notes and parameter choices here.
