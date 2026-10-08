"""One-time, lossless import of the original mixed-record JSONL snapshot."""
import argparse
import shutil
from pathlib import Path

from common import ROOT, digest, json_text, parse_json, validator, validate_program


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    destination = ROOT / "data/programs"
    if destination.exists() and any(destination.iterdir()):
        parser.error("Canonical records already exist. Edit those files instead of re-importing over community changes.")
    rows = [parse_json(line) for line in args.source.read_text(encoding="utf-8").splitlines() if line.strip()]
    programs = [r for r in rows if r.get("record_type") == "program"]
    metadata = [r for r in rows if r.get("record_type") != "program"]
    manifest = next(r for r in metadata if r["record_type"] == "manifest")
    taxonomy = next(r["taxonomy"] for r in metadata if r["record_type"] == "taxonomy")
    if manifest["program_count"] != len(programs) or len({p["id"] for p in programs}) != len(programs):
        parser.error("Source counts or unique identifiers do not match")
    checker = validator(ROOT)
    for program in programs:
        errors = validate_program(program, Path(program["id"] + ".json"), checker, taxonomy)
        if errors:
            parser.error("\n".join(errors))
    destination.mkdir(parents=True, exist_ok=True)
    source_dir = ROOT / "data/source"
    source_dir.mkdir(parents=True, exist_ok=True)
    archive = source_dir / "accelerators-complete.jsonl"
    shutil.copyfile(args.source, archive)
    for program in programs:
        (destination / (program["id"] + ".json")).write_text(json_text(program), encoding="utf-8")
    (ROOT / "data/taxonomy.json").write_text(json_text(taxonomy), encoding="utf-8")
    (source_dir / "metadata.json").write_text(json_text(metadata), encoding="utf-8")
    provenance = {
        "archive": "accelerators-complete.jsonl",
        "jsonl_sha256": digest(archive),
        "record_count": len(rows),
        "program_count": len(programs),
        "original_manifest": manifest,
        "attribution": "Lucas Jin (luc3xhj) / Foundshore",
        "license": "CC-BY-4.0",
    }
    (source_dir / "provenance.json").write_text(json_text(provenance), encoding="utf-8")
    print(f"Imported {len(programs)} programs and {len(metadata)} metadata records; source bytes preserved.")


if __name__ == "__main__":
    main()
