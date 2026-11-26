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
# What to read in Studio, highest-priority first. The first five are the ones
# the Owner named: feed exposure and stayed-to-watch are the opening-appeal
# metrics that have never once been captured, and the retention card is the
# only measure that does not scale with how much traffic the video was given.
VALUE_COLUMNS = [
    "shorts_feed_shown", "stayed_to_watch_pct", "engaged_views",
    "avg_viewed_pct", "retention_card_available",
    "views", "avg_view_duration_s", "likes", "shares",
    "thumbnail_impressions", "thumbnail_ctr_pct", "subscribers_delta",
]
COLLECTABLE = {"CLOSED_NOT_COLLECTED"}
# Videos whose window boundary is unknown still need collecting; the publish
# time is simply the first thing to read. Excluding them would hide them.
NEEDS_PUBLISH_TIME = {"UNKNOWN_PUBLISH_TIME"}


def main():
    with open(os.path.join(HERE, "data-gaps.csv"), encoding="utf-8") as f:
        gaps = list(csv.DictReader(f))

    rows = []
    for g in gaps:
        if g["state"] not in COLLECTABLE | NEEDS_PUBLISH_TIME:
            continue
        if not g["video_id"]:
            continue
        needs_time = g["state"] in NEEDS_PUBLISH_TIME
        row = {
            "slice": g["slice"], "scope": g["scope"], "code": g["code"],
            "video_id": g["video_id"], "window": g["window"],
            "state": g["state"],
            "read_publish_time_first": "YES" if needs_time else "",
            "publish_time_taipei": "",
            "window_closed_taipei": g["closes_taipei"],
            "studio_url": "https://studio.youtube.com/video/%s/analytics"
                          % g["video_id"],
            "observed_at_taipei": "",
        }
        for c in VALUE_COLUMNS:
            row[c] = ""
        row["note"] = ("window boundary unknown: read the publish time, then "
                       "collect whatever windows have in fact closed"
                       if needs_time else "")
        rows.append(row)

    rows.sort(key=lambda r: (r["read_publish_time_first"] == "", r["slice"],
                             r["window"], r["code"]))
    path = os.path.join(HERE, "studio-collection-sheet.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    counts = {}
    for r in rows:
        key = (r["slice"], r["state"])
        counts[key] = counts.get(key, 0) + 1
    print("rows to fill: %d" % len(rows))
    for k in sorted(counts):
        print("  %-3s %-22s %d" % (k[0], k[1], counts[k]))
    print()
    print("priority order: %s" % ", ".join(VALUE_COLUMNS[:5]))
    print("rows needing the publish time first: %d"
          % sum(1 for r in rows if r["read_publish_time_first"]))
    print("leave a cell blank when Studio does not show it; do not type 0")
    print("retention_card_available: yes / no  (Studio only renders the")
    print("  per-second curve once a video has enough views)")
    print("->", path)


if __name__ == "__main__":
    main()
