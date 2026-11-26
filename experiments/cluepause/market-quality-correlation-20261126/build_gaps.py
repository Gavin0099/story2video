"""Generate data-gaps.csv from the sources, so it cannot drift from the findings.

An earlier hand-maintained version of this file still claimed 04-v7 had no score
record after that had been disproved. Everything here is derived: window states
come from the recorded publication stamps, and score gaps come from the join, so
re-running after new evidence lands updates the gap list automatically.

Read-only over every source.
"""
import csv
import datetime as dt
import os

import build_table as bt

OUT = os.path.dirname(os.path.abspath(__file__))
FIELDS = ["slice", "scope", "code", "video_id", "window", "closes_taipei",
          "state", "what_to_read", "note"]
STUDIO_D1 = ("views / engaged views / avg view duration / avg % viewed / likes / "
             "shorts feed shown / stayed to watch % / thumbnail impressions / CTR")


def closes(published, days):
    if published is None:
        return ""
    return (published + dt.timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S+08:00")


def cluepause_rows(rows, now):
    out = []
    for r in rows:
        published = bt.parse_taipei(r["published_at_taipei"])
        slic = "S1" if r["cohort"] == "new" else "S4"
        scope = ("CluePause retention ten (new cohort)" if r["cohort"] == "new"
                 else "CluePause old cohort")
        for days, name in ((1, "D1"), (3, "D3"), (7, "D7")):
            has = (name == "D1" and bt.num(r["d1_views"]) is not None)
            state = bt.window_state(published, days, has, now)
            if state == "COLLECTED":
                continue
            out.append({
                "slice": slic, "scope": scope, "code": r["code"],
                "video_id": r["video_id"], "window": name,
                "closes_taipei": closes(published, days), "state": state,
                "what_to_read": STUDIO_D1,
                "note": "published " + (r["published_at_taipei"] or "unknown"),
            })
    return out


def static_ten_rows(now):
    """The five videos made public on 2026-11-25, absent from media-map.json."""
    meta = bt.read_gp_csv  # not a CSV; read the json through git instead
    import json
    import subprocess
    r = subprocess.run(
        ["git", "show", "origin/codex/cluepause-static-ten-20261124:"
         "experiments/cluepause/static-ten-20261124/upload-metadata.json"],
        cwd=bt.GP, capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        return []
    del meta
    data = json.loads(r.stdout)
    out = []
    for v in data.get("videos", []):
        if v.get("observed_visibility") != "public":
            continue
        for name in ("D1", "D3", "D7"):
            out.append({
                "slice": "S2", "scope": "static-ten public five",
                "code": v["id"], "video_id": v.get("video_id", ""), "window": name,
                "closes_taipei": "", "state": "UNKNOWN_PUBLISH_TIME",
                "what_to_read": STUDIO_D1,
                "note": ("visibility observed public on %s; only the date is "
                         "recorded, so the window boundary is ambiguous within "
                         "that day" % v.get("observed_visibility_date", "?")),
            })
    out.append({
        "slice": "S2", "scope": "static-ten public five",
        "code": "all five", "video_id": "", "window": "-", "closes_taipei": "",
        "state": "MISSING_FIELD", "what_to_read": "Studio publish time (hh:mm)",
        "note": "record the exact time so D1/D3/D7 become computable",
    })
    return out


def whynest_rows(now):
    out = []
    try:
        rows = bt.read_gp_csv("experiments/science-shorts/public-20-20261122/d1.csv")
    except SystemExit:
        return out
    for r in rows:
        if (r.get("data_status") or "").strip() not in ("", "waiting"):
            continue
        due = bt.parse_taipei(r.get("d1_due_taipei", ""))
        state = ("CLOSED_NOT_COLLECTED" if due and due <= now
                 else "PENDING_WINDOW" if due else "UNKNOWN_PUBLISH_TIME")
        out.append({
            "slice": "S3", "scope": "WhyNest Lab public ten",
            "code": r.get("episode_id", ""), "video_id": r.get("video_id", ""),
            "window": "D1",
            "closes_taipei": (r.get("d1_due_taipei") or "").strip(),
            "state": state,
            "what_to_read": ("views / engaged views / stayed to watch % / "
                             "avg % viewed / subscribers delta"),
            "note": "d1.csv data_status=" + (r.get("data_status") or "empty"),
        })
    return out


def score_rows(rows):
    out = []
    for r in rows:
        if r["version_check"] == "VERSION_UNVERIFIED":
            out.append({
                "slice": "S4", "scope": "quality-market join", "code": r["code"],
                "video_id": r["video_id"], "window": "-", "closes_taipei": "",
                "state": "VERSION_UNVERIFIED",
                "what_to_read": "not a Studio item: locate the frozen story text",
                "note": ("no readable story text for this master, so no score can "
                         "be attached; it is neither a pass nor a failure"),
            })
        elif r["ai_gate_state"] == "NOT_TESTED":
            out.append({
                "slice": "S4", "scope": "quality-market join", "code": r["code"],
                "video_id": r["video_id"], "window": "-", "closes_taipei": "",
                "state": "SCORE_RECORD_MISSING",
                "what_to_read": "not a Studio item: locate or re-run the blind read",
                "note": "published text has no matching blind-reader record",
            })
    return out


def standing_rows():
    return [
        {"slice": "S5", "scope": "per-second retention", "code": "all but 04-v7, V09",
         "video_id": "", "window": "-", "closes_taipei": "", "state": "NOT_AVAILABLE",
         "what_to_read": "Studio retention card (per-second curve)",
         "note": "only two curves exist; the rest have too few views to render one"},
        {"slice": "S5", "scope": "shorts feed metrics", "code": "all",
         "video_id": "", "window": "D1", "closes_taipei": "",
         "state": "NEVER_CAPTURED",
         "what_to_read": "shorts_feed_shown and stayed_to_watch_pct",
         "note": ("both columns exist in first-24h-and-timing.csv but are empty "
                  "for every row; only lifetime stayed % was captured")},
        {"slice": "S4", "scope": "rubric comparability", "code": "26M-B",
         "video_id": "2mLUR21IRg0", "window": "-", "closes_taipei": "",
         "state": "DIFFERENT_RUBRIC",
         "what_to_read": "not a Studio item",
         "note": ("scored on the six-dimension editorial rubric (weighted 82/100), "
                  "not the three-reader 90 protocol; the scales are not comparable")},
    ]


def main():
    now = dt.datetime.now(bt.TAIPEI)
    rows = bt.build_rows(now)
    gaps = (cluepause_rows(rows, now) + static_ten_rows(now) + whynest_rows(now)
            + score_rows(rows) + standing_rows())
    path = os.path.join(OUT, "data-gaps.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(gaps)
    counts = {}
    for g in gaps:
        counts[g["state"]] = counts.get(g["state"], 0) + 1
    print("as of %s" % now.strftime("%Y-%m-%d %H:%M %z"))
    print("gap rows: %d" % len(gaps))
    for k in sorted(counts):
        print("  %-22s %d" % (k, counts[k]))
    print("->", path)


if __name__ == "__main__":
    main()
