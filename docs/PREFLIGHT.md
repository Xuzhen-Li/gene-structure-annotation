# Preflight check before RUN=1 / 运行前检查

<!-- Prose on this page is a placeholder. Replace each [[TODO-TEXT]] with reviewed text. -->

[[TODO-TEXT: what preflight is, and that it is the check before every RUN=1 (print_qc_commands.py only prints commands).]]

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

[[TODO-TEXT: how to read [PASS] / [STOP] / [WARN] lines and the next-step hint; that outputs of later steps are not required to exist yet.]]

## 中文

[[TODO-TEXT: 中文说明，内容与英文部分对应。]]
