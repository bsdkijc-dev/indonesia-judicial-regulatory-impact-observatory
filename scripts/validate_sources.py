#!/usr/bin/env python3
"""Automated validator for IJRIO source_registry.csv."""
import csv
import sys
from pathlib import Path

SOURCE_PATH = Path(__file__).resolve().parent.parent / "data" / "perma_registry" / "source_registry.csv"

def main():
    with open(SOURCE_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    errors = 0
    for r in rows:
        if not r["base_url"].startswith("https://"):
            print(f"INVALID URL: {r['source_id']}")
            errors += 1
    print(f"Validated {len(rows)} sources. Errors: {errors}")
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
