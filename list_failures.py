#!/usr/bin/env python3
import argparse
import json
import sys


def parse_args() -> argmparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print failing checks from a JSON results file."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input JSON file (array of check objects).",
    )
    parser.add_argument(
        "--names-only",
        action="store_true",
        help="Only print the names of failing checks, one per line.",
    )
    return parser.parse_args()


def load_results(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: failed to read JSON from {path}: {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(data, list):
        print("ERROR: expected a JSON array of check results.", file=sys.stderr)
        sys.exit(1)

    return data


def main() -> None:
    args = parse_args()
    checks = load_results(args.input)

    failures = [c for c in checks if c.get("status") != "pass"]

     if not failures:
        print("No failing checks 🎉 (all checks passed)")
        sys.exit(0)

    if args.names_only:
        for c in failures:
            name = c.get("name", "<unknown>")
            print(name)
    else:
        for c in failures:
            name = c.get("name", "<unknown>")
            status = c.get("status", "<unknown>")
            msg = c.get("message", "")
            print(f"[{status}] {name}")
            if msg:
                print(f"  -> {msg}")
        print(f"\nTotal failures: {len(failures)}")

    # non-zero exit if there are failures
    sys.exit(2)


if __name__ == "__main__":
    main()
