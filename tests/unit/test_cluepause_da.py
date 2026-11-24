"""Diagnostic derivation, missing values and the real P0 snapshot."""

import csv
from decimal import Decimal
from pathlib import Path
import runpy
from statistics import median

import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "experiments/cluepause/da-20261124/derive_clue_intervals.py"
MODULE = runpy.run_path(str(SCRIPT))


@pytest.mark.parametrize(
    "clue,reveal,paradox,interval,flag",
    [
        ("14.27", "27.23", "0.03", "12.96", "false"),
        ("16", "38.633", "22.9", "22.63", "true"),
        ("1", "2.237", "1", "1.24", "false"),
        ("0", "0", "1", "0.00", "true"),
        ("", "27.23", "1", "", ""),
        ("14.27", "", "20", "", "true"),
        ("", "", "", "", ""),
        ("14.27", "27.23", "", "12.96", ""),
        (" ", "27.23", "1", "", ""),
    ],
)
def test_derive_row(clue, reveal, paradox, interval, flag):
    row = {
        "code": "sample", "cohort": "old", "key_clue_s": clue,
        "reveal_s": reveal, "paradox_stated_s": paradox,
    }
    assert MODULE["derive_row"](row) == {
        "code": "sample", "cohort": "old", "key_clue_s": clue,
        "reveal_s": reveal, "clue_to_reveal_s": interval,
        "clue_before_paradox": flag,
    }


def test_csv_writes_blanks_and_preserves_input(tmp_path):
    source = tmp_path / "input.csv"
    destination = tmp_path / "output.csv"
    content = (
        "code,cohort,key_clue_s,reveal_s,paradox_stated_s\n"
        "sample,new,1,,2\n"
    )
    source.write_text(content, encoding="utf-8")
    assert MODULE["derive_csv"](source, destination) == 1
    with destination.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        assert reader.fieldnames == list(MODULE["FIELDS"])
        row = next(reader)
    assert row["reveal_s"] == row["clue_to_reveal_s"] == ""
    assert row["clue_before_paradox"] == "true"
    assert source.read_text(encoding="utf-8") == content
    with pytest.raises(ValueError, match="Output must differ"):
        MODULE["derive_csv"](source, source)
    assert source.read_text(encoding="utf-8") == content


def test_real_csv_cohort_medians():
    # Reads the actual snapshot, without pytest fixtures or synthetic copies.
    with MODULE["DEFAULT_INPUT"].open(encoding="utf-8-sig", newline="") as stream:
        rows = [MODULE["derive_row"](row) for row in csv.DictReader(stream)]
    assert len(rows) == len({row["code"] for row in rows}) == 29
    for cohort, count, expected in [
        ("old", 20, Decimal("12.16")), ("new", 9, Decimal("8.97")),
    ]:
        values = [Decimal(row["clue_to_reveal_s"]) for row in rows
                  if row["cohort"] == cohort and row["clue_to_reveal_s"] != ""]
        assert len(values) == count
        assert round(median(values), 2) == expected
    assert [row["code"] for row in rows
            if row["clue_before_paradox"] == "true"] == ["26M-B"]
