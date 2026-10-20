# Preflight check before RUN=1 / 运行前检查

Open a terminal (Mac: Terminal app; Linux: a terminal window; cluster: your login shell) inside the `gene-structure-annotation` folder and use `python3 pipeline/preflight.py` as your check before every `RUN=1`. A pipeline is a series of automated data processing steps. Setting `RUN=1` is what makes a pipeline script actually run, while scripts without it and `print_qc_commands.py` only print commands. The preflight tool reads `config/local.env` directly so values cannot hide, checks one pipeline step, and runs nothing. You can run `python3 pipeline/preflight.py --list` to list steps, or run `python3 pipeline/preflight.py --env config/local.env --step proteins` to check that input files and folders exist, that no value is still a placeholder such as `/path/to` or `YOUR_*` (a placeholder is temporary sample text that you must replace with your real path or setting), that output paths can be created, that needed tools are installed or the container image is present (a container image is a ready-to-run package that bundles a program and everything it needs), and that lineage names look valid (a lineage name is the biological group used as a reference for your organism).

```bash
python3 pipeline/preflight.py --list
python3 pipeline/preflight.py --env config/local.env --step proteins
echo $?    # 0 = PASS, 1 = STOP, 2 = usage error
```

| Step | Script it checks |
|---|---|
| `softmask` | `pipeline/A0_softmask.md` |
| `draft` | `pipeline/A2_run_draft.sh` |
| `merge` | `pipeline/A4_merge_sets.sh` |
| `proteins` | `pipeline/A3_proteins_from_gff.sh` |
| `agat` | `pipeline/A5_agat_stats.sh` |
| `busco` | `pipeline/01_qc_busco_psauron.sh` |
| `omark` | `pipeline/A5b_omark_compleasm.sh` |
| `structure_qa` | `pipeline/structure_qa/run_structure_qa.py` |
| `release` | `pipeline/check_release_pack.py` |

Each output line starts with `[PASS]`, `[STOP]`, or `[WARN]` and names the problem and the fix, and because this check only looks at the current step, files made by later steps are not required to exist yet. Only `[STOP]` lines block your run, while `[WARN]` lines do not change the result. When a check fails, it prints `RESULT proteins: STOP (5 to fix). Do not use RUN=1 yet.` and the command to re-run the check, and when a check succeeds, it prints `RESULT <step>: PASS. Next:` followed by `set -a && source config/local.env && set +a` and the `RUN=1` command to use. You can also run `echo $?` right after the check to see the exit code (an exit code is a number a program returns when it finishes to show whether it succeeded or failed): `0` = PASS, `1` = STOP, `2` = usage error.

## 中文

请在 `gene-structure-annotation` 文件夹中打开终端 (Mac: 终端应用; Linux: 终端窗口; 集群: 登录 shell)，在每次使用 `RUN=1` 之前运行 `python3 pipeline/preflight.py` 进行预检。流程 (pipeline) 是一系列自动执行的数据处理步骤，`RUN=1` 用于让流程脚本真正开始执行，不加该参数以及运行 `print_qc_commands.py` 都只会打印命令而不执行。预检工具直接读取 `config/local.env` 以确保配置值不会隐藏，它只检查单个步骤且不运行任何实际任务：你可以运行 `python3 pipeline/preflight.py --list` 查看所有步骤，或运行 `python3 pipeline/preflight.py --env config/local.env --step proteins` 检查单个步骤的输入文件和文件夹是否存在 (后续步骤才会生成的文件此时不需要存在)、是否有配置值仍为 `/path/to` 或 `YOUR_*` 等占位符 (占位符是必须替换为你自己真实路径或设置的临时示例文本)、输出路径是否可以创建、所需软件或容器镜像是否存在 (容器镜像是将程序及其运行环境打包在一起的即用型文件)，以及谱系名称是否有效 (谱系名称是用于所研究物种参考对比的生物类群名称)。输出的每一行以 `[PASS]`、`[STOP]` 或 `[WARN]` 开头并指出具体问题和修复方法，其中只有 `[STOP]` 会阻止运行，`[WARN]` 不会改变结果；检查未通过时会打印 `RESULT proteins: STOP (5 to fix). Do not use RUN=1 yet.` 和重新检查的命令，通过时则会打印 `RESULT <step>: PASS. Next:` 以及 `set -a && source config/local.env && set +a` 和接下来要使用的 `RUN=1` 命令，你也可以运行 `echo $?` 查看退出码 (退出码是程序结束时用数字表示成功或失败的状态码)：`0` 为 PASS，`1` 为 STOP，`2` 为用法错误。
