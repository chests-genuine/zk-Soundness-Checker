#!/usr/bin/env python3

import argparse
import json
import sys

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate simple summary report of results."
    )
    parser.add_argument(
        "--file", "-f",
        required=True,
        help="Path to JSON file with results (list of objects)."
    )
    return parser.parse_args()

def load_data(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: Could not load JSON file {path}: {e}", file=sys.stderr)
        sys.exit(1)

def summarize(results):
    total = len(results)
    passes = sum(1 for r in results if r.get("status") == "pass")
    fails = total - passes
    print(f"Total checks: {total}")
    print(f"Passed     : {passes}")
    print(f"Failed     : {fails}")
     if fails:
        print("\nFailures details:")
        failures = [r for r in results if r.get("status") != "pass"]
        for r in sorted(failures, key=lambda x: str(x.get("name", ""))):
                name = r.get("name", "<unnamed>")
                msg  = r.get("message", "")
                print(f" * {name}: {msg}")

def main():
    args = parse_args()
    data = load_data(args.file)
    if not isinstance(data, list):
        print("ERROR: expected JSON array of result objects", file=sys.stderr)
        sys.exit(1)
    summarize(data)
    if any(r.get("status") != "pass" for r in data):
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
