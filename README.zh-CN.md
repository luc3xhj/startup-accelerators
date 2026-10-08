# 创业加速器与创业者项目目录

一个保留来源的开放数据目录，覆盖加速器、孵化器、驻留项目、Fellowship 和其他创业支持项目。可以比较资金与股权条款、申请资格、参与方式和申请材料，并查看背后的官方来源。

[![Validate & build](https://github.com/luc3xhj/startup-accelerators/actions/workflows/data.yml/badge.svg?branch=main)](https://github.com/luc3xhj/startup-accelerators/actions/workflows/data.yml)
[![Data: CC BY 4.0](https://img.shields.io/badge/data-CC_BY_4.0-blue)](LICENSE-DATA)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue)](LICENSE)

**[浏览中文目录 →](DIRECTORY.zh-CN.md)** · [English](README.md) · [下载数据](#使用数据) · [参与贡献](CONTRIBUTING.md)

<!-- STATS:start -->
**150 个项目 · 96 个项目网络 · 6 类项目 · 7 个地区标签**

数据中记录的核验日期：**2026-09-06**。申请状态与条款是研究快照，申请前请查看官方页面。

| 项目类型 | 数量 |
| --- | --- |
| 加速器 | 54 |
| 孵化器 | 5 |
| 驻留项目 | 16 |
| Fellowship | 16 |
| 企业合作与市场拓展 | 16 |
| 社群与创业教育 | 43 |

<!-- STATS:end -->

## 查找项目

[目录](DIRECTORY.zh-CN.md)按项目类型分组，每组按英文名称排序。每个项目都有独立详情页，展示研究中记录的资金条款、申请要求、截止时间和来源。可以用浏览器的页面查找搜索名称，也可以用命令行组合筛选条件。

例如：[Y Combinator](docs/programs/y-combinator-fd002d99.md)、[Entrepreneurs First](docs/programs/entrepreneurs-first-us-funding-fellowships-9ba1def0.md)、[HF0](docs/programs/hf0-residency-a7169369.md)、[Antler Singapore](docs/programs/antler-singapore-2f3bd4a5.md)。详情页保留英文整理内容，并可展开原始语言字段。

## 使用数据

| 格式 | 文件 | 内容 |
| --- | --- | --- |
| JSON | [accelerators.json](data/accelerators.json) | 所有项目完整记录，包括英文与原始语言字段 |
| JSONL | [accelerators.jsonl](data/accelerators.jsonl) | 每行一个项目，不含元数据行 |
| CSV | [accelerators.csv](data/accelerators.csv) | 25 个常用字段，适合表格和数据分析 |
| 独立 JSON | [data/programs/](data/programs/) | 用于维护和提交修改的权威条目文件 |
| 原始归档 | [accelerators-complete.jsonl](data/source/accelerators-complete.jsonl) | 完整保留的原始文件：150 个项目与 7 条元数据 |

[Releases](https://github.com/luc3xhj/startup-accelerators/releases) 提供带版本的下载。[datapackage.json](datapackage.json) 描述导出格式，[SHA256SUMS](SHA256SUMS) 提供文件校验值。[字段说明](docs/data-dictionary.md)解释数据结构与 CSV 映射。

可以直接读取 JSON，不需要安装依赖：

```python
import json
from pathlib import Path

programs = json.loads(Path("data/accelerators.json").read_text(encoding="utf-8"))
european_seed_programs = [
    p for p in programs
    if "Europe" in p["categories"]["region"]
    and "Seed" in p["categories"]["stage"]
]
```

## 本地筛选

需要 Python 3.10 或更高版本。唯一的直接依赖是 `jsonschema`，用于读取、筛选和生成前的数据校验。

```bash
git clone https://github.com/luc3xhj/startup-accelerators.git
cd startup-accelerators
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt

python scripts/query.py --region Europe --stage Seed
python scripts/query.py --type Fellowship --capital "Grant / stipend"
python scripts/query.py --search "Y Combinator" --format json
python scripts/query.py --attendance Remote --format csv > remote.csv
```

运行 `python scripts/query.py --help` 查看全部选项。同一筛选条件可重复，匹配其中任一值；不同条件之间需要同时满足。`--status Open` 筛选的是研究中记录的状态，不代表现在仍可申请。

## 来源与评分

初始数据由 **Lucas Jin（[luc3xhj](https://github.com/luc3xhj)）/ Foundshore** 整理。每个条目都有官网、申请链接、主要来源、研究置信度与核验日期；原始语言字段和完整 JSONL 归档均保留。

Foundshore 评分、等级和评价属于原始研究的编辑判断。源文件没有提供完整评分公式，仓库也不会重新计算。目录默认按名称排序。资金上限、云服务额度、奖金和有条件投资需要分别理解，不能直接当作保证到账的现金。

更多说明见[方法与来源](docs/methodology.md)、[数据质量报告](docs/quality-report.md)。源文件中的 logo 路径作为元数据保留，实际图片文件未包含在数据中。

## 参与贡献

发现截止日期变化、资金条款错误或遗漏项目？欢迎[提交 Issue](https://github.com/luc3xhj/startup-accelerators/issues/new/choose)，也可以附上官方来源与核验日期提交 PR。中文和英文均可。

修改 `data/programs/<id>.json` 后，重新生成目录和导出文件：

```bash
python scripts/validate.py
python scripts/build.py
python scripts/build.py --check
python -m unittest discover -s tests -v
```

[贡献指南](CONTRIBUTING.md)提供条目模板、收录范围和审核流程。CI 自动检查数据结构、标识、分类、原始归档完整性和生成结果；它不会重新访问项目官网核实事实。[仓库设计参考](docs/design-notes.md)记录了这套结构参考的成熟目录仓库。

## 许可证与署名

数据、目录和文档采用 **[CC BY 4.0](LICENSE-DATA)**；代码、校验 Schema 和自动化采用 **[MIT](LICENSE)**。具体范围见 [NOTICE](NOTICE)。

建议署名：“Startup Accelerators & Founder Programs，由 Lucas Jin（luc3xhj）/ Foundshore 整理，CC BY 4.0”，附上本仓库链接并说明是否修改。[CITATION.cff](CITATION.cff) 提供引用信息。
