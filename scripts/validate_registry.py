#!/usr/bin/env python3
"""Full-suite automated quality control validator for all IJRIO v1.0 datasets."""
import csv
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data"
REG_DIR = BASE / "perma_registry"
IMP_DIR = BASE / "implementation"
IND_DIR = BASE / "impact_indicators"
REPORT_PATH = Path(__file__).resolve().parent.parent / "quality_assurance" / "validation_report.csv"

VALID_STATUSES = {"BERLAKU", "BERLAKU_DIUBAH", "TIDAK_BERLAKU", "DICABUT", "DIGANTI"}
VALID_VERIF = {"VERIFIED", "PARTIALLY_VERIFIED", "UNVERIFIED", "NOT_AVAILABLE"}
VALID_SCORES = {"1", "2", "3", "4", "5", "NOT ASSESSED"}
VALID_OPTIONS = {"OPTION A", "OPTION B", "OPTION C", "OPTION D", "OPTION E", "OPTION F", "OPTION G"}

def main():
    issues = []
    seen_ids = set()
    seen_num_year = set()
    reg_count = 0

    with open(REG_DIR / "perma_registry.csv", newline="", encoding="utf-8") as f:
        for idx, row in enumerate(csv.DictReader(f), start=2):
            reg_count += 1
            pid = row.get("perma_id", "").strip()
            if not pid or not row.get("official_title", "").strip():
                issues.append((pid or f"ROW_{idx}", "MISSING_MANDATORY_FIELD", "Missing perma_id or title"))
            if pid in seen_ids:
                issues.append((pid, "DUPLICATE_PERMA_ID", pid))
            seen_ids.add(pid)
            key = (row.get("perma_number", "").strip(), row.get("year", "").strip())
            if key in seen_num_year:
                issues.append((pid, "DUPLICATE_NUMBER_YEAR", str(key)))
            seen_num_year.add(key)
            if not row.get("official_source_url", "").strip().startswith("https://"):
                issues.append((pid, "INVALID_SOURCE_URL", row.get("official_source_url", "")))
            if row.get("current_legal_status", "").strip() not in VALID_STATUSES:
                issues.append((pid, "INVALID_LEGAL_STATUS", row.get("current_legal_status", "")))
            if row.get("verification_status", "").strip() not in VALID_VERIF:
                issues.append((pid, "INVALID_VERIFICATION_STATUS", row.get("verification_status", "")))

    # Cross-table checks
    tables_with_url = [
        (REG_DIR / "perma_legal_status.csv", "status_id"),
        (REG_DIR / "legal_coherence.csv", "coherence_id"),
        (REG_DIR / "regulatory_problems.csv", "problem_id"),
        (REG_DIR / "regulatory_objectives.csv", "objective_id"),
        (IMP_DIR / "implementation_evidence.csv", "impl_id"),
        (IND_DIR / "impact_indicators.csv", "indicator_id"),
        (IND_DIR / "stakeholder_impacts.csv", "stakeholder_impact_id"),
        (IND_DIR / "unintended_consequences.csv", "consequence_id"),
    ]
    total_rows = reg_count
    for path, id_col in tables_with_url:
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                total_rows += 1
                pid = row.get("perma_id", "").strip()
                if pid not in seen_ids:
                    issues.append((row.get(id_col, "?"), "ORPHAN_PERMA_ID", pid))
                if not row.get("source_url", "").strip().startswith("https://"):
                    issues.append((row.get(id_col, "?"), "INVALID_SOURCE_URL", row.get("source_url", "")))

    with open(IND_DIR / "ria_assessments.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total_rows += 1
            if row.get("perma_id", "").strip() not in seen_ids:
                issues.append((row.get("assessment_id", "?"), "ORPHAN_PERMA_ID", row.get("perma_id", "")))
            if row.get("score_1_to_5_or_NA", "").strip() not in VALID_SCORES:
                issues.append((row.get("assessment_id", "?"), "INVALID_SCORE", row.get("score_1_to_5_or_NA", "")))

    with open(IND_DIR / "recommendations.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            total_rows += 1
            if row.get("perma_id", "").strip() not in seen_ids:
                issues.append((row.get("recommendation_id", "?"), "ORPHAN_PERMA_ID", row.get("perma_id", "")))
            if row.get("option_code", "").strip() not in VALID_OPTIONS:
                issues.append((row.get("recommendation_id", "?"), "INVALID_OPTION", row.get("option_code", "")))

    with open(REPORT_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["record_id", "check_type", "details"])
        if not issues:
            w.writerow(["ALL", "PASS", f"Validated {total_rows} total rows across all master datasets with 0 errors"])
        else:
            w.writerows(issues)

    print(f"Validated {total_rows} rows across all master datasets. Issues found: {len(issues)}")
    return 1 if issues else 0

if __name__ == "__main__":
    sys.exit(main())
