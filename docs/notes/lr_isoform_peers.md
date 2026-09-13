# Long-read isoform peers (beyond IsoQuant / SQANTI3)

| Tool | URL | Role |
|------|-----|------|
| **bambu** | https://github.com/GoekeLab/bambu | Bioconductor LR discovery + quant (LRGASP strong) |
| **FLAIR** | https://github.com/BrooksLabUCSC/flair | Correct/define isoforms from noisy LR RNA |
| **FLAMES** | https://github.com/LuyiTian/FLAMES | Full-length isoforms bulk/sc LR |
| **TALON** | https://github.com/mortazavilab/TALON | Known/novel isoform catalog (PacBio/ONT) |
| **PsiCLASS** | https://github.com/splicebox/PsiCLASS | Multi-sample short-read transcriptome assembly |
| **Scallop2** | https://github.com/Shao-Group/scallop2 | Short-read reference-based assembler (StringTie peer) |

**Our mapping:** short-read → PsiCLASS/Scallop2/StringTie → Portcullis → Mikado; long-read → IsoQuant|bambu|FLAIR|FLAMES|TALON → SQANTI3 → EVM/Mikado weights.
