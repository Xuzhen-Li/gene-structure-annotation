# A5c — Expression + domain filter (GetaFilter idea)

Peer: [Datapotumas/GetaFilter](https://github.com/Datapotumas/GetaFilter) (post-GETA screen).

After a draft merge, optionally drop models that fail **all** of:

| Filter | Default idea | Keep if |
|--------|--------------|---------|
| RNA support | FPKM / TPM from align_and_estimate_abundance | ≥ cutoff **or** strong protein hit |
| Pfam / HMM | pfam_scan | ≥1 domain |
| Homolog | BLASTP to close proteome | significant hit |
| Ab initio-only | AUGUSTUS score | above cutoff **and** another evidence |

## *Vitis* caution

Defense / secondary-metabolism genes can be **low expression** in your RNA panel.
Never auto-delete NLR / stilbene / CYP candidates on FPKM alone — send them to GSAman instead.

Suggested rule: expression filter only removes genes that also lack Pfam **and** homolog support.
