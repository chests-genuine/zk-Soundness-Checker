#!/usr/bin/env python3
import argparse
import json
import sys

def parse_args():
    parser = argparse.ArgumentParser(
        description="Quick summary checker for zk-Soundness-Checker"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to input JSON file with check results."
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output"
    )
    return parser.parse_args()

def load_checks(path):
    try:
             with open(path, "r", encoding="utf-8") as f:
            raw = f.read().lstrip("\ufeff")
            data = json.loads(raw)
        return data
    except Exception as e:
        print(f"ERROR: Failed to load JSON from {path}: {e}", file=sys.stderr)
        sys.exit(1)

def summarize(checks, verbose=False):
    total = len(checks)
    passed = sum(1 for c in checks if c.get("status") == "pass")
    failed = total - passed
    print(f"Total checks: {total}")
    print(f"Passed:       {passed}")
    print(f"Failed:       {failed}")
    if verbose and failed > 0:
        print("\nFailures details:")
        for c in checks:
            if c.get("status") != "pass":
                name = c.get("name", "<unknown>")
                msg  = c.get("message", "<no-message>")
                print(f" - {name}: {msg}")

def main():
    args = parse_args()
    checks = load_checks(args.input)
    if not isinstance(checks, list):
        print("ERROR: Expected a list of check results (JSON array).", file=sys.stderr)
        sys.exit(1)
    summarize(checks, verbose=args.verbose)
    if any(c.get("status") != "pass" for c in checks):
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
