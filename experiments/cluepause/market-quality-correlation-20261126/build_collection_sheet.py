"""Produce a ready-to-fill Studio collection sheet.

The market line should not wait on the scoring work. This turns data-gaps.csv
into one row per cell that is collectable now, with empty value columns to type
or paste into, so the Owner's Studio session is transcription rather than
navigation. Rows whose window has not closed are left out: collecting them
early would mix windows.

Writes studio-collection-sheet.csv. Read-only over its sources.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
# What to read in Studio, in the order the analysis wants it back.
VALUE_COLUMNS = [
    "views", "engaged_views", "avg_view_duration_s", "avg_viewed_pct",
    "likes", "shares", "shorts_feed_shown", "stayed_to_watch_pct",
    "thumbnail_impressions", "thumbnail_ctr_pct", "subscribers_delta",
]
COLLECTABLE = {"CLOSED_NOT_COLLECTED"}


def main():
    with open(os.path.join(HERE, "data-gaps.csv"), encoding="utf-8") as f:
        gaps = list(csv.DictReader(f))

    rows = []
    for g in gaps:
        if g["state"] not in COLLECTABLE:
            continue
        if not g["video_id"]:
            continue
        row = {
            "slice": g["slice"], "scope": g["scope"], "code": g["code"],
            "video_id": g["video_id"], "window": g["window"],
            "window_closed_taipei": g["closes_taipei"],
            "studio_url": "https://studio.youtube.com/video/%s/analytics"
                          % g["video_id"],
            "observed_at_taipei": "",
        }
        for c in VALUE_COLUMNS:
            row[c] = ""
        row["note"] = ""
        rows.append(row)

    rows.sort(key=lambda r: (r["slice"], r["window"], r["code"]))
    path = os.path.join(HERE, "studio-collection-sheet.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    by_slice = {}
    for r in rows:
        by_slice[r["slice"]] = by_slice.get(r["slice"], 0) + 1
    print("rows ready to fill: %d" % len(rows))
    for k in sorted(by_slice):
        print("  %s: %d" % (k, by_slice[k]))
    print("value columns: %s" % ", ".join(VALUE_COLUMNS))
    print("leave a cell blank when Studio does not show it; do not type 0")
    print("->", path)


if __name__ == "__main__":
    main()
