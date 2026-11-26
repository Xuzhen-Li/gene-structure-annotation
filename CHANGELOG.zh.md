# 变更记录

[English](CHANGELOG.md)

本页公开记录各页面和目录的改动。

## 2026-11-26：知识库结构与许可

- 首页开头改为说明本仓库怎么组织（与 TE-Lib 一致），然后是知识地图和书的各章。
- 新增知识单元 [`docs/kb/`](docs/kb/README.zh.md)，每句话都有论断和来源。[`docs/kb/NUMBERING.zh.md`](docs/kb/NUMBERING.zh.md) 给出各套编号的对照，并把旧编号标为旧版。
- 新增 [`docs/workflow/README.zh.md`](docs/workflow/README.zh.md)，说明每个流程问题以哪一页为准。
- 完整方法目录从首页移到 [`catalog/METHODS_CATALOG.zh.md`](catalog/METHODS_CATALOG.zh.md)，正文只调整了相对链接，并改写了几处表述。首页保留各节的简表，原来的小节链接（包括由旧标题自动生成的锚点）仍然有效。
- 新增 [`catalog/README.by-type.zh.md`](catalog/README.by-type.zh.md) 和 [`catalog/COUNTS.md`](catalog/COUNTS.md)：按 TSV 重新统计为 207 条。仍写旧总数的页面在文末追加了带日期的说明，正文未改。
- 新增 [`docs/KNOWLEDGE_MAP.zh.md`](docs/KNOWLEDGE_MAP.zh.md)，按主题索引全部页面。[`docs/TOOLS_NOTES_OVERLAP.md`](docs/TOOLS_NOTES_OVERLAP.md) 列出在 `docs/tools/` 和 `docs/notes/` 都有页面的工具（只是建议）。
- [`docs/ROADMAP.md`](docs/ROADMAP.md) 里仍写着“拉取请求未合并”或“未提交”的四处标题下，插入了带日期的补注，说明这些改动后来已合并；文件其余部分未改。
- 代码采用 MIT 许可；为本仓库撰写的文字、表格和绘制的图采用 CC BY 4.0。见 [`NOTICE.md`](NOTICE.md)。
- 首页上指向转座子仓库的链接改用新名 TE-Lib（原名 vitis-te）。
- 下面两条带日期的说明从首页移到这里，目录页中也保留。

## 2026-11-25：每个目录小节改为一张表

每个类型小节的条目改为一张表：工具链接、角色（按本页写明的默认、分支工具或备选）、用途与何时用、原始论文、实验室、权威度与 OpenAlex 被引次数，以及一句引自论文摘要、评测论文或 GitHub 仓库的评价。经过三次检索（一份起草的候选清单、OpenAlex 关键词检索、公开工具清单与评测论文）新增 33 条；每条新增条目的 DOI 都能解析到题名一致的论文，链接都实际打开核对过。目录现有 207 条，含新加的可视化一节；下面目录中的数字为当前数字。逐条数据见 `catalog/SOFTWARE_AUTHORITY.tsv`，同样的表格（不含各节说明）见 [`docs/software/README.zh.md`](docs/software/README.zh.md)。书籍形式的学习笔记见 [`book/`](book/README.zh.md)。

## 2026-11-14：每个目录小节加分组

每节开头新增 **分组：** 列表，把本节条目分为可替代（选一个）、互补（一起用）或按顺序（依次运行），并说明什么情况下选哪个。列表中的「A 或 B」表示二选一，「A → B」表示一条固定路线。同一软件的不同版本现在合并为一条，以最新版本命名；旧版本只在该条的说明里提及。带工具选择和判断节点的流程图见 [`docs/ROADMAP.md`](docs/ROADMAP.md#workflow-2026-11-14)。
