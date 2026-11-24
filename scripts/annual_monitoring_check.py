#!/usr/bin/env python3
"""Stage 13 annual monitoring check: flags stale records (>365 days), NOT ASSESSED cells, and coherence review items."""
import csv
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "data"
TODAY = datetime.strptime("2026-11-24", "%Y-%m-%d")

def main():
    stale = 0
    with open(BASE / "perma_registry" / "perma_registry.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            dt = datetime.strptime(r["verification_date"], "%Y-%m-%d")
            if (TODAY - dt).days > 365:
                stale += 1

    na_cells = []
    with open(BASE / "impact_indicators" / "ria_assessments.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["score_1_to_5_or_NA"] == "NOT ASSESSED":
                na_cells.append(f"{r['perma_id']}:{r['dimension_code']}")

    coh_flags = []
    with open(BASE / "perma_registry" / "legal_coherence.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if "REQUIRES" in r["contradictions_or_gaps"] or "SUPERSEDED" in r["contradictions_or_gaps"]:
                coh_flags.append(f"{r['perma_id']} ({r['contradictions_or_gaps']})")

    print(f"Monitoring Summary: stale_records={stale}, NOT_ASSESSED_cells={len(na_cells)}, coherence_watch_items={len(coh_flags)}")
    if na_cells:
        print("NOT ASSESSED targets for Stage 13 data collection:", ", ".join(na_cells))
    if coh_flags:
        print("Coherence watch items:", "; ".join(coh_flags[:5]), "...")

if __name__ == "__main__":
    main()
