"""Derive diagnostic timing columns; no scoring or publication decisions."""

import argparse
import csv
from decimal import Decimal
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_INPUT = HERE.parent / "performance-p0-20261124/first-24h-and-timing.csv"
DEFAULT_OUTPUT = HERE / "clue-to-reveal.csv"
FIELDS = (
    "code", "cohort", "key_clue_s", "reveal_s", "clue_to_reveal_s",
    "clue_before_paradox",
)


def derive_row(row):
    """Keep missing values blank; compare clue/paradox independently of reveal."""
    clue = row["key_clue_s"].strip()
    reveal = row["reveal_s"].strip()
    paradox = row["paradox_stated_s"].strip()
    return {
        "code": row["code"],
        "cohort": row["cohort"],
        "key_clue_s": row["key_clue_s"],
        "reveal_s": row["reveal_s"],
        "clue_to_reveal_s": (
            format(round(Decimal(reveal) - Decimal(clue), 2), ".2f")
            if clue and reveal else ""
        ),
        "clue_before_paradox": (
            str(Decimal(clue) < Decimal(paradox)).lower()
            if clue and paradox else ""
        ),
    }


def derive_csv(source, destination):
    source, destination = Path(source), Path(destination)
    if source.resolve() == destination.resolve():
        raise ValueError("Output must differ from input")
    with source.open(encoding="utf-8-sig", newline="") as stream:
        rows = [derive_row(row) for row in csv.DictReader(stream)]
    with destination.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(f"Wrote {derive_csv(args.input, args.output)} rows to {args.output}")


if __name__ == "__main__":
    main()
