# Methodology & provenance

## Initial research snapshot

The initial import is the contributor-supplied `accelerators-complete.jsonl`, exported at `2026-09-19T08:13:23.463Z`. Its manifest names the source workbook as `Foundshore_Founder_Programs_Intelligence_v10_Official_Logo_Pass_2026-09-06.xlsx`. The workbook itself was not supplied or independently checked during repository preparation.

The JSONL contains 150 program records and seven metadata records: manifest, source, translations, order, taxonomy, ranking metadata and logo layouts. All initial program values were preserved when splitting the data into individual JSON files. The original file is retained byte for byte in [data/source/](../data/source/), alongside the extracted metadata and [provenance record](../data/source/provenance.json).

Two hashes have different meanings: the imported manifest's `source_sha256` identifies the named workbook according to the supplied manifest; `provenance.json`'s `jsonl_sha256` is computed from the supplied JSONL bytes. Only the latter is checked against a file in this repository.

The initial records all carry `Last Verified: 2026-09-06`. This date comes from the research data. Repository import, release publication and a successful CI run do not constitute fresh verification of program facts.

## Scope & interpretation

This is a directory of programs rather than a list of investment firms. One network can run several distinct programs; network names and program names are retained separately. Normalized categories support filtering across type, region, stage, capital, attendance and recorded application status. A program may have multiple tags, so category totals can overlap. `Global` is an explicit tag from the research, not a replacement for specific geography.

`facts` contains the supplied English presentation, while `facts_raw` retains the original-language values when available. Normalized tags complement the detailed facts; they do not replace restrictions, exceptions or nuanced application terms. The flat CSV selects common fields, whereas JSON and JSONL keep the full program records.

Funding values can describe guaranteed investments, conditional funding, upper limits, prizes, stipends or non-cash credits. Always read `Funding / Support`, `Funding Trigger`, equity terms and `ranking.amountBasis` together. Missing numeric amounts remain `null`; this does not mean a program offers no support. The archived FX metadata is retained as supplied and is not refreshed or used to convert the exported amounts.

## Editorial assessments

Foundshore scores, tiers, verdicts and fit notes are the source author's editorial assessments. Ranking metadata is also preserved from the source. A complete scoring formula, calibration procedure and reproducible reputation rubric were not included, so this repository does not claim to reproduce or independently validate those judgments.

Directory sections and exports use case-insensitive alphabetical ordering by English program name, then ID. The archived display order and featured flags do not change this default. Contributors may add factual records without scores, ranking metadata or featured status.

## Updates & reproducibility

The authoritative, maintainable dataset lives in `data/programs/*.json`. Community corrections change those records, leaving the original archive intact. Contributors must include evidence and a genuine verification date; do not advance a date merely because a script has run.

`scripts/validate.py` checks schema, IDs, taxonomy, URL syntax and the original archive's checksum. `scripts/build.py` regenerates the JSON/JSONL/CSV exports, readable directory, profiles, statistics, data-package descriptor and checksums. `--check` verifies those outputs without writing. Builds do not rely on live external services or insert a current timestamp.

Read the generated [quality report](quality-report.md) for current structural coverage and known gaps. CI validates structure and consistency, not external factual accuracy or the continuing availability of an application form.

## Assets & permissions

Logo paths and source/layout metadata remain in the records and original archive. The referenced image files were not provided and are not rendered or bundled. Program names and marks identify their respective owners; inclusion does not imply endorsement. The directory's attribution and license boundaries are documented in [NOTICE](../NOTICE).
