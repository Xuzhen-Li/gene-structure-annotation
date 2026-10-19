# Install / 安装 — gene-structure-annotation

<!-- Prose on this page is a placeholder. Replace each [[TODO-TEXT]] with reviewed text.
     Commands and versions are the code side and may be edited mechanically. -->

[[TODO-TEXT: who this page is for, what gets installed, how long it takes, and that the first run (Step 4) needs only Python 3 and bash.]]

## Step 1 — get the code

```bash
git clone https://github.com/Xuzhen-Li/gene-structure-annotation.git
cd gene-structure-annotation
```

[[TODO-TEXT: one line: every later command runs inside this folder.]]

## Step 2 — create the environments

```bash
# mamba (or conda) from Miniforge: https://github.com/conda-forge/miniforge
mamba env create -f envs/structure.yml               # gsa-structure: BUSCO, AGAT, gffread, …
mamba env create -f envs/structure-proteome-qc.yml   # gsa-proteome-qc: OMArk, OMAmer, Compleasm
mamba env create -f envs/structure-repeats.yml       # gsa-repeats: RepeatMasker, RepeatModeler
conda activate gsa-structure
```

| File | Tools (pinned 2026-10-19) |
|---|---|
| `envs/structure.yml` | python 3.12, samtools 1.24, gffread 0.12.9, gffcompare 0.12.10, agat 1.7.0, hisat2 2.2.3, stringtie 3.0.3, miniprot 0.18, liftoff 1.6.3, busco 6.1.0, psauron 1.1.3 |
| `envs/structure-proteome-qc.yml` | omamer 2.1.2, omark 0.5.0, compleasm 0.2.10 |
| `envs/structure-repeats.yml` | repeatmasker 4.2.4, repeatmodeler 2.0.9 |

[[TODO-TEXT: why there are three environments (they do not solve together), and when each is needed.]]

## Step 3 — BRAKER from its container

```bash
apptainer pull braker3_v3.1.1.sif docker://teambraker/braker3:v3.1.1
# or: singularity pull braker3_v3.1.1.sif docker://teambraker/braker3:v3.1.1
echo "BRAKER_SIF=\"$PWD/braker3_v3.1.1.sif\"" >> config/local.env
apptainer exec braker3_v3.1.1.sif braker.pl --version
```

[[TODO-TEXT: why BRAKER comes as a container (GeneMark licence, many dependencies); cluster module alternative.]]

## Step 4 — check every tool

```bash
bash scripts/check_tools.sh            # prints a version or "missing" for each tool
bash scripts/check_tools.sh --strict   # exit 1 if a tool needed for the first run is missing
```

Each tool on its own:

```bash
python3 --version
samtools --version | head -1
gffread --version
gffcompare --version
agat --version
hisat2 --version | head -1
stringtie --version
miniprot --version
liftoff --version
busco --version
omamer --version
omark --version
compleasm --version
RepeatMasker -v
busco --list-datasets | grep -E 'embryophyta|eudicotyledons'
```

[[TODO-TEXT: what a good result looks like; what to do when a tool is "missing".]]

## Step 5 — first run on the toy data

```bash
bash scripts/first_run.sh            # writes ./first_run_out/
```

Last line on success:

```text
[OK] first run finished; outputs match the expected listing. Summary: …/first_run_out/work/qc/structure_qa/qc_summary.tsv
```

[[TODO-TEXT: what each of the 8 printed steps did, which files to open first, and that the many WARN rows are expected on a 10-gene toy (BUSCO/OMArk are not run here).]]

## 中文

[[TODO-TEXT: 中文说明，内容与英文部分对应。]]
