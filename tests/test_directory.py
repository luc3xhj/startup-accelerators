"""Protect contributor inputs, lossless import, and public export consistency."""
import contextlib
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build import generate
from common import check_source, json_text, load_programs, parse_json, read_json, validate_program, validator
import import_snapshot


class ContributorValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.taxonomy = read_json(ROOT / "data/taxonomy.json")
        cls.checker = validator()
        cls.example = read_json(ROOT / "templates/program.json")

    def errors(self, program):
        return validate_program(program, Path(program["id"] + ".json"), self.checker, self.taxonomy)

    def test_minimal_new_record_needs_no_editorial_score_or_assets(self):
        self.assertEqual(self.errors(self.example), [])

    def test_unknown_taxonomy_and_duplicate_tags_are_rejected(self):
        for tags in [["Imaginary region"], ["Europe", "Europe"]]:
            with self.subTest(tags=tags):
                program = copy.deepcopy(self.example)
                program["categories"]["region"] = tags
                self.assertTrue(self.errors(program))

    def test_invalid_date_is_rejected(self):
        program = copy.deepcopy(self.example)
        program["facts"]["Last Verified"] = "2026-02-30"
        self.assertTrue(self.errors(program))

    def test_source_urls_must_be_public_http_syntax(self):
        for url in ["javascript:alert(1)", "https://user:password@example.org/", "https://example.org/a b", "https://example.org:wrong/"]:
            with self.subTest(url=url):
                program = copy.deepcopy(self.example)
                program["facts"]["Primary Source"] = url
                self.assertTrue(self.errors(program))

    def test_multiple_primary_sources_are_accepted(self):
        program = copy.deepcopy(self.example)
        program["facts"]["Primary Source"] = "https://example.org/terms; https://example.org/apply"
        self.assertEqual(self.errors(program), [])

    def test_filename_must_match_stable_id(self):
        errors = validate_program(self.example, Path("wrong-id.json"), self.checker, self.taxonomy)
        self.assertTrue(any("filename" in error for error in errors))

    def test_missing_evidence_is_rejected(self):
        for field in ["Primary Source", "Last Verified", "Website", "Application Link"]:
            with self.subTest(field=field):
                program = copy.deepcopy(self.example)
                del program["facts"][field]
                self.assertTrue(self.errors(program))

    def test_editorial_score_cannot_disagree_with_fact_score(self):
        program = copy.deepcopy(self.example)
        program["score"] = 80
        program["facts"]["Foundshore Score"] = 90
        self.assertTrue(any("disagree" in error for error in self.errors(program)))

    def test_numeric_amount_needs_currency_and_basis(self):
        for ranking in [{"amount": 100000, "currency": None, "amountBasis": "Conditional"}, {"amount": 100000, "currency": "USD", "amountBasis": ""}]:
            with self.subTest(ranking=ranking):
                program = copy.deepcopy(self.example)
                program["ranking"] = ranking
                self.assertTrue(self.errors(program))

    def test_json_duplicate_keys_and_nonstandard_numbers_are_rejected(self):
        for text in ['{"id":"one","id":"two"}', '{"amount":NaN}', '{"amount":Infinity}']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_json(text)


class ImportTests(unittest.TestCase):
    def test_import_preserves_source_bytes_and_program_values(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "schema").mkdir()
            shutil.copyfile(ROOT / "schema/program.schema.json", root / "schema/program.schema.json")
            program = read_json(ROOT / "templates/program.json")
            program["facts_raw"] = {"Program": "示例创业项目", "Notes": "Keep Unicode and punctuation: <>&;"}
            taxonomy = read_json(ROOT / "data/taxonomy.json")
            rows = [{"record_type": "manifest", "program_count": 1, "source": "test.xlsx"}, {"record_type": "taxonomy", "taxonomy": taxonomy}, program]
            original = root / "source.jsonl"
            source_bytes = ("\r\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\r\n").encode("utf-8")
            original.write_bytes(source_bytes)
            with patch.object(import_snapshot, "ROOT", root), patch.object(sys, "argv", ["import_snapshot.py", str(original)]), contextlib.redirect_stdout(io.StringIO()):
                import_snapshot.main()
            self.assertEqual((root / "data/source/accelerators-complete.jsonl").read_bytes(), source_bytes)
            self.assertEqual(read_json(root / "data/programs/example-accelerator.json"), program)
            self.assertEqual(check_source(root)["program_count"], 1)

    def test_archive_tampering_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "data/source", root / "data/source")
            archive = root / "data/source/accelerators-complete.jsonl"
            archive.write_bytes(archive.read_bytes() + b"\n")
            with self.assertRaisesRegex(ValueError, "checksum"):
                check_source(root)


class PublicOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.programs = load_programs()
        cls.output = generate()

    def test_full_json_and_program_only_jsonl_round_trip(self):
        self.assertEqual(parse_json(self.output["data/accelerators.json"]), self.programs)
        rows = [parse_json(line) for line in self.output["data/accelerators.jsonl"].splitlines()]
        self.assertEqual(rows, self.programs)
        self.assertTrue(all(row["record_type"] == "program" for row in rows))

    def test_csv_has_one_row_per_program_and_unknown_amounts_are_blank(self):
        rows = list(csv.DictReader(io.StringIO(self.output["data/accelerators.csv"])))
        self.assertEqual([row["id"] for row in rows], [p["id"] for p in self.programs])
        for row, program in zip(rows, self.programs):
            self.assertEqual(row["funding_support"], program["facts"].get("Funding / Support", ""))
            if program.get("ranking", {}).get("amount") is None:
                self.assertEqual(row["reported_amount"], "")

    def test_generation_is_deterministic(self):
        self.assertEqual(generate(), self.output)

    def test_checksums_match_export_and_archive_bytes(self):
        for line in self.output["SHA256SUMS"].splitlines():
            expected, name = line.split("  ", 1)
            content = self.output[name].encode("utf-8") if name in self.output else (ROOT / name).read_bytes()
            self.assertEqual(hashlib.sha256(content).hexdigest(), expected)

    def test_local_document_links_resolve(self):
        documents = {p.relative_to(ROOT).as_posix(): p.read_text(encoding="utf-8") for p in ROOT.rglob("*.md")}
        documents.update({name: text for name, text in self.output.items() if name.endswith(".md")})
        for name, text in documents.items():
            for raw in re.findall(r"\]\(([^)]+)\)", text):
                target = raw.strip("<>").split("#", 1)[0]
                if not target or re.match(r"[a-zA-Z][\w+.-]*:", target):
                    continue
                path = ROOT / Path(name).parent / target
                relative = path.resolve().relative_to(ROOT).as_posix()
                self.assertTrue(path.exists() or relative in self.output, f"Broken local link in {name}: {raw}")

    def test_combined_cli_filters_and_json_output(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/query.py"), "--region", "Europe", "--stage", "Seed", "--format", "json"], capture_output=True, text=True, check=True)
        rows = parse_json(result.stdout)
        expected = [p for p in self.programs if "Europe" in p["categories"]["region"] and "Seed" in p["categories"]["stage"]]
        self.assertEqual(rows, expected)

    def test_jsonl_cli_with_no_matches_outputs_no_records(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/query.py"), "--search", "not-a-real-program-7c639d", "--format", "jsonl"], capture_output=True, text=True, check=True)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
