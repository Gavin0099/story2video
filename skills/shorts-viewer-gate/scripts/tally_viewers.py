"""Tally one exact MP4 version against the Shorts Viewer Gate."""

import argparse
import csv
from hashlib import file_digest
import json
from pathlib import Path


REQUIRED = {
    "clip_code", "mp4_sha256", "viewer_id", "valid", "exclusion_reason",
    "answer_match", "aha_interesting", "answer_verbatim",
    "reframe_and_interest_verbatim",
}


def tally(csv_path, clip_code, mp4):
    with mp4.open("rb") as media:
        digest = file_digest(media, "sha256").hexdigest()
    viewers = {}
    excluded = 0
    with csv_path.open(encoding="utf-8-sig", newline="") as log:
        rows = csv.DictReader(log)
        if not rows.fieldnames or not REQUIRED <= set(rows.fieldnames):
            raise ValueError("The viewer record is missing required fields")
        for row in rows:
            if row["clip_code"] != clip_code:
                continue
            if None in row or any(row[field] is None for field in REQUIRED):
                raise ValueError(f"Incomplete viewer record at row {rows.line_num}")
            if row["mp4_sha256"].lower() != digest:
                continue
            if row["valid"] == "no" and row["exclusion_reason"].strip():
                excluded += 1
                continue
            if row["valid"] != "yes":
                raise ValueError(f"Mark row {rows.line_num} valid, or give an exclusion reason")
            viewer = row["viewer_id"].strip()
            answer, interest = row["answer_match"], row["aha_interesting"]
            if not viewer or viewer in viewers:
                raise ValueError(f"Missing or duplicate viewer at row {rows.line_num}")
            if answer not in {"yes", "no"} or interest not in {"yes", "no"}:
                raise ValueError(f"Use yes or no for both judgments at row {rows.line_num}")
            if (answer == "yes" and not row["answer_verbatim"].strip()
                    or interest == "yes" and not row["reframe_and_interest_verbatim"].strip()):
                raise ValueError(f"Save the viewer's exact response at row {rows.line_num}")
            viewers[viewer] = answer == "yes", interest == "yes"
    if len(viewers) > 5:
        raise ValueError("Use the five valid viewers from the preselected cohort")
    correct = sum(answer for answer, _ in viewers.values())
    interested = sum(interest for _, interest in viewers.values())
    state = "待驗"
    if len(viewers) == 5:
        state = "通過" if correct >= 4 and interested >= 3 else "未通過"
    return {"clip_code": clip_code, "mp4_sha256": digest, "valid": len(viewers),
            "excluded": excluded, "correct": correct, "aha_interesting": interested,
            "state": state}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("csv", type=Path)
    cli.add_argument("code")
    cli.add_argument("mp4", type=Path)
    args = cli.parse_args()
    try:
        print(json.dumps(tally(args.csv, args.code, args.mp4), ensure_ascii=False))
    except (OSError, ValueError) as exc:
        cli.exit(1, f"{exc}\n")


if __name__ == "__main__":
    main()
