"""Shared, deterministic dataset operations. No network access is required."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
DIMENSIONS = ("type", "region", "stage", "capital", "attendance", "status")
URL_FIELDS = ("Website", "Application Link", "Primary Source")
CSV_FIELDS = (
    "id", "name", "network", "program_type", "region_tags", "location", "focus",
    "stage_tags", "capital_tags", "funding_support", "equity_terms", "format",
    "attendance_tags", "status_tags", "application_status", "deadline", "website",
    "application_url", "source_urls", "last_verified", "research_confidence",
    "editorial_score", "reported_amount", "reported_currency", "amount_basis",
)


def flat_row(program):
    facts, categories, ranking = program["facts"], program["categories"], program.get("ranking", {})
    fact_columns = {
        "program_type": "Program Type", "location": "Location", "focus": "Focus",
        "funding_support": "Funding / Support", "equity_terms": "Equity / Economic Terms",
        "format": "Format", "application_status": "Application Status", "deadline": "Deadline / Next Intake",
        "website": "Website", "application_url": "Application Link", "source_urls": "Primary Source",
        "last_verified": "Last Verified", "research_confidence": "Research Confidence",
    }
    result = {"id": program["id"], "name": program["name_en"], "network": program["network_en"]}
    result.update({column: facts.get(field) for column, field in fact_columns.items()})
    result.update({dimension + "_tags": " | ".join(categories[dimension]) for dimension in ("region", "stage", "capital", "attendance", "status")})
    result.update({"editorial_score": program.get("score"), "reported_amount": ranking.get("amount"), "reported_currency": ranking.get("currency"), "amount_basis": ranking.get("amountBasis")})
    return result


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"Non-standard JSON number: {value}")


def parse_json(text):
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)


def read_json(path):
    return parse_json(path.read_text(encoding="utf-8"))


def json_text(value):
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_urls(program):
    """Source cells may contain multiple URLs separated by semicolon + space."""
    return re.split(r";\s+", program["facts"]["Primary Source"])


def validator(root=ROOT):
    schema = read_json(root / "schema/program.schema.json")
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema, format_checker=FormatChecker())


def validate_program(program, path, checker, taxonomy):
    errors = []
    for error in sorted(checker.iter_errors(program), key=lambda e: str(list(e.path))):
        field = ".".join(str(v) for v in error.path) or "record"
        errors.append(f"{path.name}: {field}: {error.message}")
    if errors:
        return errors
    if program["id"] != path.stem:
        errors.append(f"{path.name}: filename must match id")
    for field in URL_FIELDS:
        value = program["facts"][field]
        values = source_urls(program) if field == "Primary Source" else [value]
        for url in values:
            try:
                parts = urlsplit(url)
                _ = parts.port  # Also reject invalid ports.
                valid = parts.scheme in {"http", "https"} and parts.hostname and not parts.username and not parts.password
            except ValueError:
                valid = False
            if not valid or any(c.isspace() for c in url):
                errors.append(f"{path.name}: facts.{field}: expected public HTTP(S) URLs without credentials")
    for dimension in DIMENSIONS:
        unknown = set(program["categories"][dimension]) - set(taxonomy[dimension])
        if unknown:
            errors.append(f"{path.name}: unknown {dimension} tags: {sorted(unknown)}")
    score = program.get("score")
    facts_score = program["facts"].get("Foundshore Score")
    if score is not None and facts_score is not None and score != facts_score:
        errors.append(f"{path.name}: score and facts['Foundshore Score'] disagree")
    raw_score = program.get("facts_raw", {}).get("Foundshore Score")
    if score is not None and raw_score is not None and score != raw_score:
        errors.append(f"{path.name}: score and facts_raw['Foundshore Score'] disagree")
    ranking = program.get("ranking", {})
    if (ranking.get("amount") is None) != (ranking.get("currency") is None):
        errors.append(f"{path.name}: ranking amount and currency must be provided together")
    if ranking.get("amount") is not None and not ranking.get("amountBasis", "").strip():
        errors.append(f"{path.name}: a numeric ranking amount needs a documented amountBasis")
    return errors


def load_programs(root=ROOT):
    taxonomy = read_json(root / "data/taxonomy.json")
    schema = read_json(root / "schema/program.schema.json")
    for dimension in DIMENSIONS:
        expected = schema["properties"]["categories"]["properties"][dimension]["items"]["enum"]
        if taxonomy.get(dimension) != expected:
            raise ValueError(f"Taxonomy and schema disagree for {dimension}")
    checker = validator(root)
    programs, errors, ids, orders, identities = [], [], set(), set(), set()
    for path in sorted((root / "data/programs").glob("*.json")):
        try:
            program = read_json(path)
        except (ValueError, OSError) as error:
            errors.append(f"{path.name}: {error}")
            continue
        invalid = validate_program(program, path, checker, taxonomy)
        if invalid:
            errors.extend(invalid)
            continue
        if program["id"] in ids:
            errors.append(f"{path.name}: duplicate id")
        ids.add(program["id"])
        order = program.get("display_order")
        if order is not None:
            if order in orders:
                errors.append(f"{path.name}: duplicate display_order {order}")
            orders.add(order)
        identity = (program["network_en"].casefold().strip(), program["name_en"].casefold().strip())
        if identity in identities:
            errors.append(f"{path.name}: duplicate program name within the same network")
        identities.add(identity)
        programs.append(program)
    if not programs:
        errors.append("No program records found")
    if errors:
        raise ValueError("\n".join(errors))
    return sorted(programs, key=lambda p: (p["name_en"].casefold(), p["id"]))


def check_source(root=ROOT):
    origin = read_json(root / "data/source/provenance.json")
    archive = root / "data/source/accelerators-complete.jsonl"
    if digest(archive) != origin["jsonl_sha256"]:
        raise ValueError("Original source archive checksum does not match provenance.json")
    rows = [parse_json(line) for line in archive.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) != origin["record_count"]:
        raise ValueError("Original archive record count does not match provenance.json")
    count = sum(r.get("record_type") == "program" for r in rows)
    if count != origin["program_count"]:
        raise ValueError("Original archive program count does not match provenance.json")
    return origin
