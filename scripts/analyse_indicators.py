#!/usr/bin/env python3
"""Summary statistics script for IJRIO perma_registry.csv using pandas."""
import pandas as pd
from pathlib import Path

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "data" / "perma_registry" / "perma_registry.csv"

def main():
    df = pd.read_csv(REGISTRY_PATH)
    print(f"Total PERMA records: {len(df)}")
    print("\nBy Legal Status:")
    print(df["current_legal_status"].value_counts().to_string())
    print("\nBy Verification Status:")
    print(df["verification_status"].value_counts().to_string())
    print("\nBy Year:")
    print(df["year"].value_counts().sort_index().to_string())

if __name__ == "__main__":
    main()
