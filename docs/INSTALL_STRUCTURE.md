# Install / 安装 — gene-structure-annotation

This guide is for beginners with basic computer skills and walks you through installing three conda environments (a conda environment is an isolated folder of software packages that prevents version conflicts) and a BRAKER container (BRAKER is a gene prediction pipeline, and a container packages it with all its dependencies into a single ready-to-run file). You can run all commands by opening a terminal (on Mac: Terminal app; on Linux: a terminal window; on a cluster: your login shell) inside the `gene-structure-annotation` folder. If you want to try the first run in Step 5 before installing heavy tools, it takes about 1 second and needs only `python3`, `bash`, and `awk` (standard command-line programs for running scripts and processing text).

## Step 1 — get the code

```bash
git clone https://github.com/Xuzhen-Li/gene-structure-annotation.git
cd gene-structure-annotation
```

Run every later command on this page in the same terminal window (on Mac: Terminal app; on Linux: a terminal window; on a cluster: your login shell) from inside this `gene-structure-annotation` folder.

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

The pipeline splits software into three separate conda environments (a conda environment is an isolated folder of software packages that prevents version conflicts) so that incompatible tools do not clash, and you switch to the main one by opening a terminal (on Mac: Terminal app; on Linux: a terminal window; on a cluster: your login shell) inside the `gene-structure-annotation` folder and running `conda activate gsa-structure`. You need `gsa-structure` (built from `envs/structure.yml`) for the main pipeline steps, `gsa-proteome-qc` when running OMArk, OMAmer, and Compleasm (three tools that check protein set completeness and quality, which cannot be installed together with BUSCO 6 and Python 3.12 because their package requirements conflict), and `gsa-repeats` only when you need soft-masking (soft-masking marks repetitive DNA in lowercase letters so gene predictors do not confuse repeats with real genes, and its software is kept apart because it is large).

## Step 3 — BRAKER from its container

```bash
apptainer pull braker3_v3.1.1.sif docker://teambraker/braker3:v3.1.1
# or: singularity pull braker3_v3.1.1.sif docker://teambraker/braker3:v3.1.1
echo "BRAKER_SIF=\"$PWD/braker3_v3.1.1.sif\"" >> config/local.env
apptainer exec braker3_v3.1.1.sif braker.pl --version
```

BRAKER (a pipeline that predicts gene structures in a genome) is not installed inside any conda environment; instead, you pull the container image `docker://teambraker/braker3:v3.1.1` (a container image is a single file that bundles a program with all its required system libraries) using `apptainer` or `singularity` (two container runners commonly used on research computers) from a terminal (on Mac: Terminal app; on Linux: a terminal window; on a cluster: your login shell) inside the `gene-structure-annotation` folder and set the `BRAKER_SIF` variable in `config/local.env` to the downloaded file path. If you work on a cluster and prefer not to use a container, you can instead run the printed `braker.pl` command line directly using your cluster modules (environment modules are pre-installed software packages provided by cluster administrators).

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

When you run `bash scripts/check_tools.sh` or `bash scripts/check_tools.sh --strict` in a terminal (on Mac: Terminal app; on Linux: a terminal window; on a cluster: your login shell) inside the `gene-structure-annotation` folder, the script prints a version number or the word `missing` for each tool, grouped by environment file. The tools `python3`, `bash`, and `awk` (standard command-line programs for running scripts and processing text) are marked `(required)` and are the only programs needed for the first run; without `--strict` the script always finishes with exit code `0` (an exit code is a status number returned to the terminal where `0` means success and `1` means an error), whereas with `--strict` it exits with `1` only if one of those `(required)` tools is missing. If any tool in an environment group says `missing`, create that conda environment or activate it with `conda activate` (for example, `conda activate gsa-structure`), and note that the BRAKER line will say `not checked` until you set `BRAKER_SIF` in `config/local.env`.

## Step 5 — first run on the toy data

```bash
bash scripts/first_run.sh            # writes ./first_run_out/
```

Last line on success:

```text
[OK] first run finished; outputs match the expected listing. Summary: …/first_run_out/work/qc/structure_qa/qc_summary.tsv
```

Running `bash scripts/first_run.sh` in a terminal (on Mac: Terminal app; on Linux: a terminal window; on a cluster: your login shell) inside the `gene-structure-annotation` folder takes about 1 second and writes all results to `./first_run_out/` across 8 steps: Step 1 writes the run plan (`plan.md`), Step 2 saves the tool check (`tools.txt`), Step 3 uses the pre-made toy annotation file in place of running BRAKER and only writes the BRAKER command to `draft_command.txt`, Step 4 calculates gene counts, Step 5 extracts protein sequences keeping the longest isoform per gene (an isoform is one of multiple transcript variants produced from the same gene), Step 6 runs the quality check (`work/qc/structure_qa/qc_summary.tsv`), Step 7 builds the release package (`work/release/toy.v0.1/`), and Step 8 compares your outputs against `testdata/structure/expected/`, exiting with `0` when everything matches or printing `[DIFF]` lines if anything differs. You should open `./first_run_out/plan.md`, `./first_run_out/work/qc/structure_qa/qc_summary.tsv`, and `./first_run_out/work/release/toy.v0.1/` first to inspect the results. Many `WARN` rows in `qc_summary.tsv` are completely expected on this 10-gene toy dataset because BUSCO and OMArk (completeness checking tools) are not run and show `NA`, the total gene count is tiny, and the toy data includes planted errors on purpose to demonstrate the quality checks.

## 中文

本指南面向具备基础电脑操作的初学者，请打开终端（Mac 上为 Terminal 应用，Linux 上为终端窗口，集群上为登录 shell），在克隆仓库后进入 `gene-structure-annotation` 文件夹，后续所有命令都在该文件夹内运行。第一步是准备仓库目录，运行 `git clone https://github.com/Xuzhen-Li/gene-structure-annotation.git` 和 `cd gene-structure-annotation` 进入工作目录。第二步是安装三个独立的 conda 环境（conda 环境是隔离的软件包文件夹，用于避免版本冲突）：主环境 `gsa-structure`（由 `envs/structure.yml` 创建，通过 `conda activate gsa-structure` 激活）用于主要流程步骤；`gsa-proteome-qc` 存放 OMArk、OMAmer 和 Compleasm（这三个评估蛋白质组完整性与质量的工具与 BUSCO 6 及 Python 3.12 存在依赖冲突，无法安装在同一环境中）；`gsa-repeats` 仅用于软屏蔽（软屏蔽将重复 DNA 序列标为小写字母，防止基因预测工具将重复序列误判为基因，因软件包体积较大而单独存放）。第三步是准备 BRAKER（一种预测基因组中基因结构的流程工具），它不在任何 conda 环境中，请使用 `apptainer` 或 `singularity`（科研计算常用的容器运行工具）拉取容器镜像 `docker://teambraker/braker3:v3.1.1`（容器镜像是将程序及其所有系统依赖打包在一起的单个文件），并在 `config/local.env` 中设置 `BRAKER_SIF`；如果在集群上运行，也可以直接使用集群自带的环境模块（由管理员预装的软件包）运行打印出的 `braker.pl` 命令行。第四步是运行 `bash scripts/check_tools.sh` 或 `bash scripts/check_tools.sh --strict` 检查工具，脚本会按环境文件分组打印每个工具的版本号或 `missing`，其中标有 `(required)` 的 `python3`、`bash` 和 `awk`（用于运行脚本和处理文本的标准命令行程序）是首次试运行仅需的工具；不加 `--strict` 时脚本始终返回退出码 `0`（退出码是返回给终端的状态数字，`0` 代表成功，`1` 代表出错），加上 `--strict` 时仅当缺少 `(required)` 工具才会返回 `1`，若某个分组显示 `missing` 请创建或激活对应环境，而在设置 `BRAKER_SIF` 之前 BRAKER 行会显示 `not checked`。第五步是运行 `bash scripts/first_run.sh` 进行首次试运行，耗时约 1 秒并将结果写入 `./first_run_out/`，依次完成 8 个步骤：步骤 1 生成运行计划（`plan.md`），步骤 2 记录工具检查（`tools.txt`），步骤 3 用测试文件代替实际运行 BRAKER 并仅将命令写入 `draft_command.txt`，步骤 4 统计基因数量，步骤 5 提取每个基因最长异构体的蛋白序列（异构体是同一基因产生的不同转录本变体），步骤 6 运行质量检查（`work/qc/structure_qa/qc_summary.tsv`），步骤 7 打包发布目录（`work/release/toy.v0.1/`），步骤 8 与 `testdata/structure/expected/` 比对，完全一致时退出码为 `0`，不一致则打印 `[DIFF]` 行；你可以先打开 `plan.md`、`work/qc/structure_qa/qc_summary.tsv` 和 `work/release/toy.v0.1/` 查看结果，由于未运行 BUSCO 与 OMArk（显示为 `NA`）、总基因数仅有 10 个且测试集内置了预设问题，因此 `qc_summary.tsv` 中出现许多 `WARN` 行属于正常现象。
