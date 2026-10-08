# Data dictionary / 字段说明

JSON and JSONL preserve full records. The CSV is a selected flat view, not a lossless replacement. All data files use UTF-8. / JSON 与 JSONL 保留完整记录；CSV 为常用字段视图，所有文件均使用 UTF-8。

## Canonical program record

| Field | Meaning |
| --- | --- |
| `record_type` | Always `program`. |
| `id` | Stable, unique lowercase hyphenated identifier; matches the JSON filename. |
| `name`, `network` | Program and operator names in the original presentation. |
| `name_en`, `network_en` | English names used for listing and sorting. |
| `facts` | English research fields described below. Five fields are required: Program Type, Website, Application Link, Primary Source and Last Verified. |
| `facts_raw` | Optional original-language research values, retaining the source field names. |
| `categories` | Normalized arrays for type, region, stage, capital, attendance and status. |
| `score` | Optional imported Foundshore editorial score, integer 0–100 or null; must agree with any fact-level score. |
| `ranking` | Optional original numeric and qualitative ranking metadata; described below. |
| `display_order`, `featured` | Optional source presentation order and featured flag; not the directory sorting rule. |
| `logo`, `logoSource`, `logoLayout` | Optional source asset path, source notes and layout metadata. Images are not bundled. |


## Normalized categories

Allowed values are defined in [taxonomy.json](../data/taxonomy.json) and synchronized with the [JSON Schema](../schema/program.schema.json). All six arrays are required. Tags are unique within an array and may overlap across records; `stage` can be empty when unclassified.

| Dimension | Allowed values |
| --- | --- |
| type | Accelerator, Incubator, Residency, Fellowship, Corporate / market access, Community / education |
| region | North America, Latin America, Europe, Asia, Middle East, Oceania, Global |
| stage | Pre-company, Pre-seed, Seed, Series A, Growth |
| capital | Investment, Grant / stipend, Conditional funding, Prizes, Credits / services, Not disclosed |
| attendance | In person, Hybrid, Remote, Varies by program, Not disclosed |
| status | Open, Rolling, Upcoming, Waitlist, Closed, To confirm, Inactive |


## Research fields

The initial records contain the following 49 research fields. Most values are descriptive strings; editorial scores are integers and unavailable public-contact fields may be null. Preserve explanatory unknown values instead of inventing missing facts.

### Overview

| Field | Meaning |
| --- | --- |
| Program | Program name recorded in the research. |
| Network | Parent network or operator, which may run more than one program. |
| Program Type | Original descriptive program type; normalized type tags are in categories.type. |
| Primary Value | The main kind of support or benefit described by the researcher. |
| Region | Original geographic description; see categories.region for normalized multi-value tags. |
| Location | Recorded operating location or locations and any relevant detail. |
| Focus | Industry, technology or founder focus described in the source. |
| Stage | Original description of the startup stages served; normalized tags may be empty if unclassified. |
| Duration | Recorded program duration or participation period. |


### Funding & economic terms

| Field | Meaning |
| --- | --- |
| Capital Type | Original description of the kind of funding or support. |
| Guaranteed Capital | Whether support is guaranteed according to the recorded terms; read conditions in context. |
| Funding / Support | Recorded funding, stipend, prize, credits or other support, including caveats. |
| Funding Trigger | Conditions or milestones that trigger an offer or disbursement. |
| Non-dilutive | Recorded assessment of whether support avoids equity dilution. |
| Equity / Economic Terms | Equity, SAFE or other economic terms, including program fees where recorded. |
| Capital Disclosure Status | How much of the capital terms the researcher found publicly disclosed. |
| Capital Terms Confidence | Researcher confidence in the interpretation of capital terms. |


### Eligibility

| Field | Meaning |
| --- | --- |
| Company Required at Application | Whether an incorporated company is required when applying. |
| Geography / Affiliation Restriction | Residency, university, company or other affiliation restrictions. |
| Can Apply Pre-Idea | Recorded eligibility for applicants who have not settled on an idea. |
| Can Apply Solo | Recorded eligibility for solo founders. |
| Official / Must-Have Requirements | Eligibility and application requirements supported by official sources. |
| Strong-to-Have | Desirable characteristics recorded separately from mandatory requirements. |
| Eligibility Disclosure Status | How much of the eligibility criteria is publicly documented. |
| Eligibility Confidence | Researcher confidence in the eligibility interpretation. |


### Attendance & international founders

| Field | Meaning |
| --- | --- |
| Format | Original delivery format, such as a cohort, residency, hybrid or virtual program. |
| On-site Required | Recorded requirement to participate in person. |
| On-site / Attendance | Attendance, relocation or presence expectations and exceptions. |
| International Founder | Recorded access or restrictions for international founders. |
| Visa Support Level | Researcher classification of publicly documented visa support. |
| Visa / Relocation | Detailed source-based visa or relocation notes; not a guarantee of visa issuance. |


### Applications & public contacts

| Field | Meaning |
| --- | --- |
| Application Status | Application status when researched; not a live status feed. |
| Deadline / Next Intake | Deadline or intake information recorded at the verification date. |
| Application Materials | Requested application materials or application process. |
| Application Link | Public HTTP(S) application page; may be a general route if no active form was recorded. |
| Website | Public HTTP(S) program or operator website. |
| Public Contact Name | Publicly listed contact name, or null when unavailable. |
| Public Contact Role | Publicly listed contact role, or null when unavailable. |
| Public Email | Publicly advertised business contact email, or null when unavailable. |
| Public Contact Route | Official publicly available route for contacting the program. |


### Sources & verification

| Field | Meaning |
| --- | --- |
| Research Confidence | Supplied research-confidence assessment, not a CI-generated score. |
| Last Verified | Date the facts were checked according to the researcher, in YYYY-MM-DD format. |
| Primary Source | One official source URL or multiple URLs separated by semicolon and space. |
| Verification | Recorded source or verification notes. |


### Foundshore editorial assessment

| Field | Meaning |
| --- | --- |
| Foundshore Score | Imported editorial score from 0 to 100; optional, not independently recomputed. |
| Foundshore Tier | Imported editorial tier or recommendation band. |
| Foundshore Verdict | Imported editorial summary of the program. |
| Foundshore Best Fit | Editorial view of founders or startups best suited to the program. |
| Foundshore Not Fit | Editorial view of cases less suited to the program. |
| Notes | Additional research caveats, interpretation or editorial notes. |


## Ranking metadata

| Field | Meaning |
| --- | --- |
| `fundingTier` | Imported funding classification, integer 0–3; no complete rubric supplied. |
| `amount`, `currency` | Reported nonnegative amount and three-letter source currency; both must be present together or both null. |
| `amountBasis` | Required explanation when a numeric amount is supplied, e.g. a ceiling, conditional offer or stipend. |
| `cohortsCompleted`, `cohortSource` | Optional reported completed-cohort count and its source URL. |
| `reputation`, `reputationSource` | Optional imported reputation indicator (0–3) and its source; not independently recalculated. |


## CSV columns

Lists of tags are joined with ` | `. Unknown values become empty CSV cells, never zero. `source_urls` retains the semicolon-separated source links. Amounts retain the source currency. `program_type` is the descriptive research field; JSON supplies normalized type tags.

| CSV column | JSON source |
| --- | --- |
| `id` | `id` |
| `name` | `name_en` |
| `network` | `network_en` |
| `program_type` | `facts.Program Type` |
| `region_tags` | `categories.region` |
| `location` | `facts.Location` |
| `focus` | `facts.Focus` |
| `stage_tags` | `categories.stage` |
| `capital_tags` | `categories.capital` |
| `funding_support` | `facts.Funding / Support` |
| `equity_terms` | `facts.Equity / Economic Terms` |
| `format` | `facts.Format` |
| `attendance_tags` | `categories.attendance` |
| `status_tags` | `categories.status` |
| `application_status` | `facts.Application Status` |
| `deadline` | `facts.Deadline / Next Intake` |
| `website` | `facts.Website` |
| `application_url` | `facts.Application Link` |
| `source_urls` | `facts.Primary Source` |
| `last_verified` | `facts.Last Verified` |
| `research_confidence` | `facts.Research Confidence` |
| `editorial_score` | `score` |
| `reported_amount` | `ranking.amount` |
| `reported_currency` | `ranking.currency` |
| `amount_basis` | `ranking.amountBasis` |


## Missing values & archives

In canonical JSON, missing optional values may be null, absent, empty arrays or explicit explanatory strings as supplied. JSON Schema permits scalar research values but rejects duplicate keys, invalid dates, unknown taxonomy tags and malformed core URLs through the validator.

The original mixed-record archive has seven metadata rows in addition to program rows. The generated program-only JSONL contains no metadata rows. [provenance.json](../data/source/provenance.json), [metadata.json](../data/source/metadata.json) and the [methodology](methodology.md) explain the original export, archive hash and editorial boundaries.
