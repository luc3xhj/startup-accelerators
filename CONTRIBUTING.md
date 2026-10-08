# Contributing / 贡献指南

Corrections, new programs, translations and tooling improvements are welcome. You can contribute in English or Chinese. / 欢迎修正资料、补充项目、改进翻译和工具，中文或英文均可。

## What belongs here

Include identifiable, publicly documented programs that help startup founders through acceleration, incubation, residencies, fellowships, corporate access or structured founder education. A general investor database, paid promotional listing or unsupported program recommendation is outside this directory's scope.

Use official program pages, official application forms, published terms or announcements from the program operator. Distinguish cash investment, grants, prizes, service credits and conditional offers. A correction should explain the old value, the new value and the supporting source.

## Suggest a change without writing code

[Open an issue](https://github.com/luc3xhj/startup-accelerators/issues/new/choose) with the program name, official links, the change you suggest and the date you checked it. An official representative can identify their affiliation, but affiliation does not replace source evidence. Do not submit private contact details.

## Edit a record

1. Fork the repository and create a branch.
2. Edit the relevant `data/programs/<id>.json` file. Keep the existing ID when renaming or correcting a program.
3. For a new program, copy [templates/program.json](templates/program.json), choose a unique lowercase hyphenated ID and use the same ID as the filename. Replace every example value with researched facts.
4. Keep `facts` in English. `name`, `network` and optional `facts_raw` can preserve the original language. If you update a field that exists in both `facts` and `facts_raw`, update both consistently.
5. Choose normalized tags from [data/taxonomy.json](data/taxonomy.json). `stage: []` means genuinely unclassified, not every stage. Propose taxonomy changes in both the taxonomy file and [program schema](schema/program.schema.json).
6. Record sources in `facts["Primary Source"]` and the date you actually checked them in `facts["Last Verified"]` (`YYYY-MM-DD`). Separate multiple primary-source URLs with `; `.

`score`, `ranking`, `featured`, `display_order` and logo metadata are optional. New contributors do not need to invent an editorial score or source layout. Preserve existing editorial fields unless the change specifically addresses them and explains why. Numeric funding metadata needs its currency and `amountBasis`; unknown is `null`, not zero.

The initial original JSONL and `data/source/metadata.json` are archival evidence. Do not rewrite them when a current record changes. The workbook checksum in the original manifest identifies the source workbook; the separate provenance checksum identifies the actual JSONL archive.

## Build and check

Python 3.10+ is required. On Windows, activate the environment with `.venv\Scripts\activate` instead of the Unix command below.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python scripts/build.py
python scripts/build.py --check
python -m unittest discover -s tests -v
```

Include the canonical JSON changes **and** regenerated files in the pull request. Do not hand-edit exports, directory tables, generated program profiles, manifest, data-package descriptor or checksums. The README statistics between the `STATS` markers are generated; the rest of each README is editable.

Each pull request runs structural validation, archive integrity checks, reproducibility checks and tests. These checks do not confirm the truth or current availability of a program. A maintainer reviews the source evidence and may request clearer terms or a narrower claim before merging.

For tooling changes, include a test when it protects a data or contribution invariant. Changes to formatting alone do not need new tests. Keep builds deterministic and usable without external network calls.

## Attribution & conduct

Contributions to data and documentation use [CC BY 4.0](LICENSE-DATA); contributions to tooling, schemas and automation use [MIT](LICENSE). Credit sources and other contributors. Discuss corrections respectfully, disclose relevant affiliations, and keep issues focused on the program or repository.

中文提示：更新单个 JSON 条目即可；不要直接修改生成的目录和 CSV。请附官方来源及实际核验日期，运行上面的命令后，将生成结果一起提交。
