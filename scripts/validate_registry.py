#!/usr/bin/env python3
"""Automated quality control validator for IJRIO perma_registry.csv."""
import csv
import sys
from pathlib import Path

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "data" / "perma_registry" / "perma_registry.csv"
REPORT_PATH = Path(__file__).resolve().parent.parent / "quality_assurance" / "validation_report.csv"

MANDATORY_FIELDS = [
    "perma_id", "perma_number", "year", "official_title",
    "issuing_institution", "official_source_url", "current_legal_status",
    "verification_status", "verification_date"
]
VALID_STATUSES = {"BERLAKU", "BERLAKU_DIUBAH", "TIDAK_BERLAKU", "DICABUT", "DIGANTI"}
VALID_VERIF = {"VERIFIED", "PARTIALLY_VERIFIED", "UNVERIFIED", "NOT_AVAILABLE"}

def main():
    issues = []
    seen_ids = set()
    seen_num_year = set()
    row_count = 0

    with open(REGISTRY_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=2):
            row_count += 1
            pid = row.get("perma_id", "").strip()
            for field in MANDATORY_FIELDS:
                if not row.get(field, "").strip():
                    issues.append((pid or f"ROW_{idx}", "MISSING_MANDATORY_FIELD", f"Missing {field}"))
            if pid in seen_ids:
                issues.append((pid, "DUPLICATE_PERMA_ID", f"Duplicate perma_id {pid}"))
            seen_ids.add(pid)

            key = (row.get("perma_number", "").strip(), row.get("year", "").strip())
            if key in seen_num_year:
                issues.append((pid, "DUPLICATE_NUMBER_YEAR", f"Duplicate number/year {key}"))
            seen_num_year.add(key)

            url = row.get("official_source_url", "").strip()
            if not url.startswith("https://"):
                issues.append((pid, "INVALID_SOURCE_URL", f"Invalid URL: {url}"))

            if row.get("current_legal_status", "").strip() not in VALID_STATUSES:
                issues.append((pid, "INVALID_LEGAL_STATUS", row.get("current_legal_status", "")))

            if row.get("verification_status", "").strip() not in VALID_VERIF:
                issues.append((pid, "INVALID_VERIFICATION_STATUS", row.get("verification_status", "")))

            prom = row.get("promulgation_date", "").strip()
            eff = row.get("effective_date", "").strip()
            if prom not in ("", "NOT_AVAILABLE") and eff not in ("", "NOT_AVAILABLE") and eff < prom:
                issues.append((pid, "INCONSISTENT_DATES", f"effective_date {eff} < promulgation_date {prom}"))

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["record_id", "check_type", "details"])
        if not issues:
            w.writerow(["ALL", "PASS", f"Validated {row_count} records with 0 errors"])
        else:
            w.writerows(issues)

    print(f"Validated {row_count} PERMA records. Issues found: {len(issues)}")
    return 1 if issues else 0

if __name__ == "__main__":
    sys.exit(main())
