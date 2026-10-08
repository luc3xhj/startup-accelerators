"""Validate source integrity, schema, identifiers, URLs, and taxonomy."""
import sys

from common import check_source, load_programs


def main():
    try:
        programs = load_programs()
        check_source()
    except (ValueError, OSError) as error:
        print(error, file=sys.stderr)
        return 1
    print(f"OK: {len(programs)} program records; schema, URLs, taxonomy and source checksum valid.")
    print("URL validation checks syntax, not live program availability or external page content.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
