# AI-assisted annotation — prompts, data, order, checks

Use an AI assistant (Cursor / chat agent / lab bot) as a **runbook co-pilot**, not as a replacement for BUSCO, IGV/GSAman, or METHODS. This page is the contract: what to prepare, what to say, in what order, and how **you** verify the answer.

Related: [`DETAILED_GUIDE.md`](DETAILED_GUIDE.md) · [`SCENARIOS.md`](SCENARIOS.md) · [`TOOLS.md`](TOOLS.md) · [`PLAYBOOK.md`](PLAYBOOK.md)

---

## 1. What AI is good / bad at

| Good | Bad (do not trust alone) |
|------|---------------------------|
| Choosing branch S1–S14 from your evidence list | Inventing BUSCO % or gene counts |
| Drafting `braker.pl` / EVM / PASA command lines from this repo | Claiming a GFF is “publication ready” without your QC files |
| Explaining a log error / TSEBRA collapse | Silent overwrites of curated GFF |
| Building priority lists, METHODS text, checklists | Running GeneMark without your license / cluster paths |
| Comparing two AGAT/BUSCO tables you paste | Hallucinating tool flags that do not exist |

**Rule:** AI proposes; **you** run tools and keep the files. Every numeric claim must come from a file on disk.

---

## 2. Prepare data before you ask

Put a **manifest** in the chat (or a `WORK_DIR/MANIFEST.md`). Minimum:

```text
Species / accession:
Ploidy / haplotypes: 1 or 2+
Assembly: path + N50 + #scaffolds (or attach seqkit_stats.txt)
Asm1 BUSCO genome: C/D/F/M + lineage
Evidence:
  - RNA-seq BAM? tissues? mapping %
  - Iso-seq? depth?
  - Protein DB? (OrthoDB / grape)
  - Reference FA+GFF? (PN40024…)
TE lib: curated / EDTA / none
Goal: provisional | qualified | paper T2T | family/QTL only
Cluster: singularity|conda|modules; THREADS=
Branch guess (optional): S1 / S14 / …
```

**Do attach or paste:**

- `seqkit_stats.txt`, genome BUSCO short summary  
- After drafts: AGAT stats, protein BUSCO short_summary, PSAURON head, `A5d` stage_qc.tsv  
- Exact error log tails (last 80 lines), not “it failed”

**Do not paste:** private FASTQ, unpublished sample sheets, license keys, passwords.

Directory layout AI should assume (from this repo):

```text
$WORK_DIR/{asm,mask,rna,draft,qc,curate,release}
# S14 also: 00-External … 07-Filtering (see config/example.env)
```

---

## 3. Prompt patterns (copy-paste)

### 3.1 Pick a branch

```text
You are helping with Vitis gene annotation using the playbook at
https://github.com/Xuzhen-Li/gene-function-annotation (docs/SCENARIOS.md).

Here is my MANIFEST:
<paste>

Recommend one primary branch (S1–S14) and one fallback.
Say which steps to skip. Do not invent metrics I did not provide.
```

### 3.2 Next command only (slow is fast)

```text
We are on branch S___, finished steps: Asm0, Asm1, A0.
Next step only: give the exact commands for ___ using variables from
config/example.env. Prefer containers. Stop after that step’s QC check.
Point to the matching file under docs/ or pipeline/.
```

### 3.3 Debug a failure

```text
Tool: BRAKER3 / EVM / PASA / …
Command I ran:
<code>

Last 80 lines of log:
<log>

Working dir listing (ls of relevant folder):
<ls>

Using docs/tools/<tool>.md and notes/copetti.md if relevant:
what failed, what to try once, what NOT to retry blindly.
```

### 3.4 Interpret QC (you supply numbers)

```text
Protein BUSCO short_summary:
<paste>

AGAT gene/mRNA counts:
<paste>

A5d stage_qc.tsv:
<paste>

Goal: qualified release for Vitis.
Are we in S10 (TE inflation), Copetti TSEBRA collapse, S9 (high D),
or OK to build priority.tsv? Cite thresholds from PLAYBOOK.md.
```

### 3.5 GSAman / last mile

```text
priority.tsv top 20:
<paste>

ERROR_CLASSES.md classes only.
For each top locus suggest: which evidence tracks to load,
likely error class, stop rule from S12.
Do not invent exon coordinates.
```

### 3.6 METHODS paragraph

```text
Draft a METHODS paragraph from this real tool version list and branch ID.
Only use versions I list. Mention S14 (EVM) / BRAKER S1 accurately.
Versions:
<list>
```

### 3.7 Anti-prompts (say this when needed)

```text
Do not run cloud agents. Do not push to GitHub unless I say so.
One finished step at a time. Public files English. Talk to me in Chinese.
If unsure, say what file you need from me instead of guessing.
```

---

## 4. Order of work with AI (recommended)

Same spine as the homepage flowchart — AI joins **at decision points**, you run compute.

```text
0. You: fill MANIFEST + Asm0/Asm1 files
1. AI: pick branch (S1–S14) from MANIFEST
2. You: soft-mask (A0); AI: review TE/ProtExcluder plan if gene count later explodes
3. You: RNA / evidence; AI: aligner flags only if stuck
4. You: draft engine (BRAKER or S14 Augustus/GeneMark/PASA)
5. AI+You: A5d stage counts / AGAT — interpret before merge
6. You: merge (EVM/TSEBRA/Mikado); AI: weights file choice
7. You: proteins + BUSCO + PSAURON; AI: interpret tables you paste
8. You: priority → GSAman; AI: triage list, not freehand gene models
9. You: re-QC; AI: qualification checklist walkthrough
10. You: freeze release GFF + METHODS; AI: draft METHODS from your versions
```

**Never** ask AI to “annotate the genome” in one shot. Chunk by step IDs in [`DETAILED_GUIDE.md`](DETAILED_GUIDE.md) / [`steps/MAIN.md`](steps/MAIN.md).

---

## 5. How to check AI output (before you run it)

Checklist for every AI-suggested command block:

- [ ] Paths are **your** `$WORK_DIR` / env vars, not invented `/data/...`  
- [ ] Soft-mask (`-xsmall`) if BRAKER/GALBA/Augustus  
- [ ] Tool name matches [`TOOLS.md`](TOOLS.md) page  
- [ ] Flags exist in `--help` / container docs (spot-check one)  
- [ ] Next QC file is named (AGAT / BUSCO / A5d / …)  
- [ ] No delete/overwrite of `CURATED_GFF` without backup  

If AI gives a metric you did not paste → **reject** that sentence.

---

## 6. How **you** understand results (literacy)

Learn to read these yourself; AI only coaches:

| File / metric | Healthy intuition (*Vitis*-like) |
|---------------|----------------------------------|
| Genome BUSCO-C | High; extreme BUSCO-D → S9 / haplotypes |
| AGAT gene count | Same order as related grape annotations × ploidy; huge jump → S10 |
| Mono:multi (`A5d`) | Compare GeneMark / Augustus / BRAKER; BRAKER ≪ others → TSEBRA rescue |
| Protein BUSCO-C after merge | Should not crash vs draft; isoforms inflate D — use one protein/gene |
| PSAURON low tail | Curation queue, not auto-delete (protect NLR) |
| GSAman changelog | Every fix has an [`ERROR_CLASSES.md`](ERROR_CLASSES.md) tag |
| Release checklist | [`PLAYBOOK.md`](PLAYBOOK.md) all boxes — or label `provisional` |

Browser: load soft-masked genome + GFF + RNA BAM + homolog lift + TE track (Copetti habit). If a contig is empty of genes but has TE only, check evidence tracks before blaming EVM.

---

## 7. Minimal “AI session” template

```text
Playbook: Xuzhen-Li/gene-function-annotation
Branch: S___
Step: ___
MANIFEST: <attached or pasted>
Artifacts: <paths or pasted summaries>
Ask: <one decision OR one command block OR one QC interpretation>
Constraints: one step; no fabricated numbers; Chinese replies; English files if editing repo
```

---

## 8. After AI helps — your sign-off

Before calling annotation qualified:

1. Re-run AGAT + protein BUSCO yourself  
2. Skim 10 random priority loci in GSAman/IGV  
3. Write METHODS with **your** versions  
4. Tag `RELEASE_TAG`; never commit BAM/FASTQ  

AI chat is not the archive — `release/` + METHODS are.


---

## Functional annotation prompts (main product)

### Pick F-branch

```text
Playbook: Xuzhen-Li/gene-function-annotation functional spine
(docs/SCENARIOS_FUNCTIONAL.md). Proteins: <path or BUSCO summary>.
Goal: paper|fast|names|NLR. Recommend F1–F8. No invented GO counts.
```

### Next functional command

```text
Branch F1. Done: F0. Next step only: eggNOG-mapper or InterProScan
using config/example.env. Point to pipeline/F*.sh.
```

### Interpret emapper/IPS

```text
I paste head -50 of emapper.annotations and IPS tsv.
Explain columns; how to merge with F_merge_tables.py;
what fraction unannotated is normal — only from my numbers.
```
