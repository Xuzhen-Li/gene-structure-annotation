# Classic ab initio engines (high citation building blocks)

| Tool | Role | Notes |
|------|------|-------|
| **AUGUSTUS** | HMM ab initio / hints | Core of BRAKER; Stanke lab |
| **GeneMark** (ES/ET/EP/ETP) | Self-training / evidence | Core of BRAKER; Borodovsky lab |
| **SNAP** | Semi-HMM ab initio | Often inside MAKER |
| **GlimmerHMM** | Ab initio | Fungal/plant stacks historically |
| **EVidenceModeler (EVM)** | Weighted consensus | Haas et al.; our **S14** |
| **PASA** | Transcript / polish | Haas et al.; our **S14** |
| **StringTie / HISAT2 / STAR** | RNA assembly / align | Evidence inputs to S1 |

These are the citation-heavy primitives almost every modern pipeline re-packages. Prefer calling them through BRAKER/MAKER/funannotate rather than hand-wiring unless debugging.
