# Startup Accelerators & Founder Programs

A source-linked directory of startup accelerators, incubators, residencies, fellowships and other programs for founders. Compare funding, equity terms, eligibility, attendance and application requirements without losing the underlying sources.

[![Validate & build](https://github.com/luc3xhj/startup-accelerators/actions/workflows/data.yml/badge.svg?branch=main)](https://github.com/luc3xhj/startup-accelerators/actions/workflows/data.yml)
[![Data: CC BY 4.0](https://img.shields.io/badge/data-CC_BY_4.0-blue)](LICENSE-DATA)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue)](LICENSE)

**[Browse the directory →](DIRECTORY.md)** · [中文](README.zh-CN.md) · [Download data](#use-the-data) · [Contribute](CONTRIBUTING.md)

<!-- STATS:start -->
**150 programs · 96 networks · 6 program types · 7 region tags**

Source-recorded verification dates: **2026-09-06**. Application status and terms are a research snapshot; check official pages before applying.

| Program type | Entries |
| --- | --- |
| Accelerator | 54 |
| Incubator | 5 |
| Residency | 16 |
| Fellowship | 16 |
| Corporate / market access | 16 |
| Community / education | 43 |

<!-- STATS:end -->

## Find a program

Start with the [directory](DIRECTORY.md): programs are grouped by type and alphabetized. Each program has its own profile with the recorded funding terms, eligibility, deadlines and primary sources. Use your browser's find function to search the page, or use the CLI for combined filters.

- [Accelerators](DIRECTORY.md#accelerator)
- [Incubators](DIRECTORY.md#incubator)
- [Residencies](DIRECTORY.md#residency)
- [Fellowships](DIRECTORY.md#fellowship)
- [Corporate / market access](DIRECTORY.md#corporate--market-access)
- [Community / education](DIRECTORY.md#community--education)

For example: [Y Combinator](docs/programs/y-combinator-fd002d99.md), [Entrepreneurs First](docs/programs/entrepreneurs-first-us-funding-fellowships-9ba1def0.md), [HF0](docs/programs/hf0-residency-a7169369.md) and [Antler Singapore](docs/programs/antler-singapore-2f3bd4a5.md).

## Use the data

| Format | File | Contents |
| --- | --- | --- |
| JSON | [accelerators.json](data/accelerators.json) | All program records, including English and original-language facts |
| JSONL | [accelerators.jsonl](data/accelerators.jsonl) | One program per line; no metadata rows |
| CSV | [accelerators.csv](data/accelerators.csv) | A flat selection of 25 fields for spreadsheets and analysis |
| Per-program JSON | [data/programs/](data/programs/) | Canonical records; edit these when contributing |
| Original archive | [accelerators-complete.jsonl](data/source/accelerators-complete.jsonl) | Unmodified import: 150 programs and seven metadata records |

[Releases](https://github.com/luc3xhj/startup-accelerators/releases) provide versioned downloads. [datapackage.json](datapackage.json) describes the exports; [SHA256SUMS](SHA256SUMS) records their checksums. See the [data dictionary](docs/data-dictionary.md) for field definitions and CSV mappings.

Read the JSON directly, with no package installation:

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

## Filter locally

Requires Python 3.10 or newer. The only direct dependency is `jsonschema`, used to validate the data before querying or building.

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

Run `python scripts/query.py --help` for every filter. Repeating one filter matches any supplied value; different filters must all match. Recorded application status is historical, including when filtering `--status Open`.

## Sources & editorial notes

The initial dataset was compiled by **Lucas Jin ([luc3xhj](https://github.com/luc3xhj)) / Foundshore**. Every record includes official website and application links, primary sources, research confidence and a recorded verification date. Original-language facts and the original mixed-record JSONL are preserved.

Foundshore scores, tiers and verdicts are imported editorial assessments. The source does not provide a complete scoring formula, and this repository does not recalculate them. Listings default to alphabetical order. Funding ceilings, credits, prizes and conditional investments are not interchangeable with guaranteed cash.

Read the [methodology & provenance](docs/methodology.md) and [data quality report](docs/quality-report.md) for coverage and known gaps. The original logo paths are metadata; image assets were not included in the source file.

## Contribute

Found a changed deadline, missing program or incorrect funding term? [Open an issue](https://github.com/luc3xhj/startup-accelerators/issues/new/choose) or submit a pull request with an official source and verification date. English and Chinese contributions are welcome.

Edit `data/programs/<id>.json`, then regenerate the derived files:

```bash
python scripts/validate.py
python scripts/build.py
python scripts/build.py --check
python -m unittest discover -s tests -v
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the record template, scope and review process. CI checks schema validity, identifiers, taxonomy, source integrity and reproducible exports. It does not re-verify program websites. [Design notes](docs/design-notes.md) explain the directory repositories that informed this structure.

## License & attribution

The dataset, directory and documentation are licensed under **[CC BY 4.0](LICENSE-DATA)**. Code, validation schemas and automation are licensed under **[MIT](LICENSE)**. See [NOTICE](NOTICE) for the boundaries of each license.

Suggested attribution: “Startup Accelerators & Founder Programs, compiled by Lucas Jin (luc3xhj) / Foundshore, CC BY 4.0,” with a link to this repository and an indication of changes. [CITATION.cff](CITATION.cff) provides citation metadata.
