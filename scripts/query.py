"""Search the canonical directory with exact taxonomy filters and free text."""
import argparse
import json
import sys

from build import csv_text, table, md
from common import DIMENSIONS, ROOT, load_programs, read_json


def main():
    taxonomy = read_json(ROOT / "data/taxonomy.json")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--search", default="", help="Case-insensitive search across names, networks and English facts")
    for dimension in DIMENSIONS:
        parser.add_argument("--" + dimension, action="append", choices=taxonomy[dimension], default=[])
    parser.add_argument("--format", choices=["table", "json", "jsonl", "csv"], default="table")
    args = parser.parse_args()
    try:
        programs = load_programs()
    except (ValueError, OSError) as error:
        print(error, file=sys.stderr)
        return 1
    matches = []
    for program in programs:
        if any(getattr(args, dimension) and not set(getattr(args, dimension)).intersection(program["categories"][dimension]) for dimension in DIMENSIONS):
            continue
        text = " ".join(str(v) for v in [program["name"], program["name_en"], program["network_en"], *program["facts"].values()])
        if args.search.casefold() not in text.casefold():
            continue
        matches.append(program)
    if args.format == "json":
        print(json.dumps(matches, ensure_ascii=False, indent=2, allow_nan=False))
    elif args.format == "jsonl":
        for program in matches:
            print(json.dumps(program, ensure_ascii=False, allow_nan=False))
    elif args.format == "csv":
        print(csv_text(matches), end="")
    else:
        print(f"{len(matches)} programs\n")
        print(table(["Program", "Location", "Type", "Last verified"], [[md(p["name_en"]), md(p["facts"].get("Location")), md(", ".join(p["categories"]["type"])), md(p["facts"]["Last Verified"])] for p in matches]), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
