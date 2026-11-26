"""Join blind-reader scores to recorded Studio market data, keyed by story content.

Primary key is story_sha256 (see build_index.py), not the version id: ids such as
"62-v1" are reused by unrelated lineages. Run build_index.py first.

Each published video is matched by hashing the frozen story text its master was
built from, then looking that hash up in score-index.csv. A video whose text
cannot be read is reported as VERSION_UNVERIFIED, never as a pass.

Scope note: the rows are the entries of media-map.json, i.e. the 29 videos that
were public when that map was written. Five further CluePause videos went public
on 2026-11-25 and have no data yet; they appear in data-gaps.csv, not here.

D1, D3, D7 and lifetime are separate columns and are never mixed inside one
correlation. Read-only over every source.
"""
import csv
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys

S2V = r"D:\story2video"
GP = r"D:\s2v-gp"
OUT = os.path.dirname(os.path.abspath(__file__))
# Market CSVs are read from this branch (PR #19 head, the base of this work).
# The same two files are byte-identical on codex/cluepause-static-ten-20261124.
GPB = "origin/codex/cluepause-performance-p0-20261124"
TEXT_FIELDS = ("first", "second", "reveal", "english")
TAIPEI = dt.timezone(dt.timedelta(hours=8))

# Where each published master's frozen story text lives, when it is not the
# default <artifact family>/<episode>/story.json.
TEXT_OVERRIDE = {
    "04-v7": os.path.join(S2V, "artifacts", "04-v7-pilot", "approved-story.json"),
}


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def story_sha256(obj):
    if not isinstance(obj, dict):
        return None
    txt = "|".join(str(obj.get(k, "")) for k in TEXT_FIELDS)
    if not txt.strip("|"):
        return None
    return hashlib.sha256(txt.encode("utf-8")).hexdigest()


def published_sha(code, family, episode):
    path = TEXT_OVERRIDE.get(code)
    if path is None and family and episode:
        path = os.path.join(S2V, "artifacts", family, episode, "story.json")
    if not path or not os.path.exists(path):
        return None
    try:
        return story_sha256(load_json(path))
    except Exception:
        return None


def read_gp_csv(path):
    r = subprocess.run(["git", "show", GPB + ":" + path], cwd=GP,
                       capture_output=True, text=True, encoding="utf-8")
    if r.returncode:
        sys.exit("git show failed for " + path + ": " + r.stderr[:200])
    return list(csv.DictReader(r.stdout.lstrip("\ufeff").splitlines()))


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def parse_taipei(text):
    """Parse the publication stamps used in the market CSVs, or None."""
    if not text:
        return None
    s = text.strip().replace("T", " ")
    s = re.sub(r"\s*\+08:?00$", "", s)
    # .NET writes seven fractional digits; %f accepts at most six.
    s = re.sub(r"(\.\d{6})\d+$", r"\1", s)
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return dt.datetime.strptime(s, fmt).replace(tzinfo=TAIPEI)
        except ValueError:
            continue
    return None


def window_state(published, days, has_data, now):
    """Status of one observation window, instead of a hardcoded placeholder."""
    if has_data:
        return "COLLECTED"
    if published is None:
        return "UNKNOWN_PUBLISH_TIME"
    closes = published + dt.timedelta(days=days)
    return "CLOSED_NOT_COLLECTED" if closes <= now else "PENDING_WINDOW"


# The gate contract, from autoloop.py on codex/story-quality-autoloop:
#     PASS_SCORE, FINAL_READERS = 90, 3
#     passed = (len(valid) == FINAL_READERS
#               and all(row["score"] >= PASS_SCORE and row["clear"] for row in valid))
# All three conditions are reproduced below. Checking only the minimum score
# would pass a record that had a single reader, or readers who did not mark the
# story clear.
PASS_SCORE = 90
FINAL_READERS = 3


def record_passes(rec):
    """True / False, or None when the record cannot be judged."""
    if not rec.get("cores"):
        return None
    count = num(rec.get("reader_count"))
    if count is None:
        return None
    low = num(rec.get("reader_min"))
    if low is None:
        return False
    if int(count) != FINAL_READERS:
        return False
    clear = rec.get("all_readers_clear")
    if clear not in ("yes", "no"):
        return None
    return low >= PASS_SCORE and clear == "yes" and rec["cores"] == "supported"


def gate_state(recs):
    if not recs:
        return "NOT_TESTED"
    verdicts = [record_passes(r) for r in recs]
    if any(v is None for v in verdicts):
        return "CORES_NOT_RECORDED"
    if all(verdicts):
        return "GATE_PASS"
    if any(verdicts):
        return "CONFLICTING_RUNS"
    return "BELOW_GATE"


def load_index():
    path = os.path.join(OUT, "score-index.csv")
    if not os.path.exists(path):
        sys.exit("score-index.csv missing: run build_index.py first")
    with open(path, encoding="utf-8") as f:
        index_rows = list(csv.DictReader(f))
    by_sha = {}
    for r in index_rows:
        by_sha.setdefault(r["story_sha256"], []).append(r)
    return by_sha


def load_schema():
    """Market columns are declared in market-schema.json, not hardcoded here,
    so adding a metric is a schema edit rather than a code edit."""
    return load_json(os.path.join(OUT, "market-schema.json"))


def build_rows(now=None):
    now = now or dt.datetime.now(TAIPEI)
    schema = load_schema()
    by_sha = load_index()
    media = load_json(os.path.join(S2V, "artifacts", "cluepause-performance-lab",
                                   "media-map.json"))
    tables = {}
    for name, src in schema["sources"].items():
        tables[name] = {r[src["key"]]: r for r in read_gp_csv(src["path"])}
    d1 = tables["d1_csv"]
    lf = tables["windows_csv"]

    rows = []
    for m in media:
        code = m["code"]
        episode = m.get("episode") or ""
        asset = (m.get("asset") or "").replace("\\", "/").split("/")
        family = asset[1] if len(asset) > 1 and asset[0] == "artifacts" else ""
        sha = published_sha(code, family, episode)
        recs = by_sha.get(sha, []) if sha else []

        if sha is None:
            version_check = "VERSION_UNVERIFIED"
        elif recs:
            # The scored text equals the text in the artifact the master was
            # built from. It does not re-verify the uploaded video's narration.
            version_check = "TEXT_MATCHES_MASTER_SOURCE"
        else:
            version_check = "NO_SCORE_FOR_PUBLISHED_TEXT"
        state = gate_state(recs) if sha is not None else "VERSION_UNVERIFIED"

        a = d1.get(code, {})
        b = lf.get(code, {})
        engaged = num(a.get("engaged_views_d1"))
        avg_raw = num(a.get("avg_viewed_d1_pct"))
        # An avg % viewed reported against zero engaged views is not a 0%
        # retention observation, it is an absent one.
        avg_valid = avg_raw if (engaged and engaged > 0) else None
        # Values above 100% mean the Short was replayed; they are not on the
        # same scale as sub-100 values and are flagged so they can be excluded.
        repeat = "yes" if (avg_valid is not None and avg_valid > 100) else (
            "" if avg_valid is None else "no")
        published = parse_taipei(a.get("published_at_taipei", ""))
        rows.append({
            "cohort": m["cohort"], "code": code, "episode": episode,
            "story_sha256": sha or "",
            "video_id": m.get("video_id", ""), "title_zh": m.get("title_zh", ""),
            "artifact_family": family,
            "duration_s": round(m.get("length") or 0, 2),
            "published_at_taipei": a.get("published_at_taipei", ""),
            "ai_scores": " ; ".join(r["readers"] for r in recs),
            "ai_min": min([num(r["reader_min"]) for r in recs
                           if num(r["reader_min"]) is not None], default=""),
            "ai_cores": " ; ".join(r["cores"] for r in recs),
            "ai_gate_state": state,
            "version_check": version_check,
            "rubric_version": " ; ".join(sorted({r["rubric_version"] for r in recs})),
            "score_source_kind": " ; ".join(sorted({r["source_kind"] for r in recs})),
            "score_source_ref": " ; ".join(sorted({r["source_ref"] for r in recs})),
            "score_source_commit": " ; ".join(sorted({r["source_commit"] for r in recs
                                                      if r["source_commit"]})),
            "score_source_path": " ; ".join(sorted({r["source_path"] for r in recs})),
        })
        # Market columns come from the schema, in its declared order.
        for spec in schema["fields"]:
            src = a if spec["source"] == "d1_csv" else b
            rows[-1][spec["field"]] = src.get(spec["column"], "")
        rows[-1]["d1_avg_viewed_pct_valid"] = "" if avg_valid is None else avg_valid
        rows[-1]["d1_repeat_play"] = repeat
        rows[-1]["d1_window"] = window_state(
            published, 1, num(a.get("views_d1")) is not None, now)
        rows[-1]["d3_window"] = window_state(published, 3, False, now)
        rows[-1]["d7_window"] = window_state(published, 7, False, now)
        if not a:
            rows[-1]["d1_source_note"] = "NO_ROW"
    return rows


# ---------------------------------------------------------------- statistics
def pearson(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < 3:
        return None
    xs2 = [p[0] for p in pairs]
    ys2 = [p[1] for p in pairs]
    mx = sum(xs2) / len(xs2)
    my = sum(ys2) / len(ys2)
    den = (sum((x - mx) ** 2 for x in xs2) * sum((y - my) ** 2 for y in ys2)) ** 0.5
    if den == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in pairs) / den


def ranked(vs):
    order = sorted(range(len(vs)), key=lambda i: vs[i])
    out = [0.0] * len(vs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vs[order[j + 1]] == vs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            out[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return out


def spearman(xs, ys):
    pairs = [(x, y) for x, y in zip(xs, ys) if x is not None and y is not None]
    if len(pairs) < 3:
        return None
    return pearson(ranked([p[0] for p in pairs]), ranked([p[1] for p in pairs]))


def quartiles(xs):
    """Linear-interpolated quartiles, so Q3+3*IQR means what a reader expects."""
    s = sorted(xs)

    def q(p):
        if len(s) == 1:
            return s[0]
        pos = p * (len(s) - 1)
        lo = int(pos)
        hi = min(lo + 1, len(s) - 1)
        return s[lo] + (s[hi] - s[lo]) * (pos - lo)
    return q(0.25), q(0.75)


def outlier_codes(rows, key):
    """Codes above Q3 + 3*IQR (linear-interpolated quartiles)."""
    vals = [(num(r[key]), r["code"]) for r in rows if num(r[key]) is not None]
    if len(vals) < 4:
        return []
    q1, q3 = quartiles([v for v, _ in vals])
    hi = q3 + 3 * (q3 - q1)
    return [c for v, c in vals if v > hi]


def fmt(v):
    return "n/a" if v is None else format(v, "+.3f")


def pair_line(label, xs, ys, indent="  "):
    n = sum(1 for x, y in zip(xs, ys) if x is not None and y is not None)
    miss_x = sum(1 for x, y in zip(xs, ys) if x is None and y is not None)
    miss_y = sum(1 for x, y in zip(xs, ys) if y is None)
    distinct = len({x for x, y in zip(xs, ys) if x is not None and y is not None})
    rp = pearson(xs, ys)
    rs = spearman(xs, ys)
    note = ""
    if rp is not None and rs is not None and abs(rp) > 0.3 and abs(rs) < 0.15:
        note = "  <- Pearson driven by outliers, rank order flat"
    if distinct <= 3 and n:
        note += "  <- predictor takes only %d distinct values" % distinct
    return ("%s~ %-22s n=%2d missing_x=%d missing_y=%2d distinct_x=%d "
            "pearson=%s spearman=%s%s" % (indent, label, n, miss_x, miss_y,
                                          distinct, fmt(rp), fmt(rs), note))


PREDICTORS = [("ai_min", "AI min reader score"), ("duration_s", "duration s"),
              ("anomaly_s", "first anomaly s"), ("key_clue_s", "key clue s"),
              ("reveal_s", "reveal s")]


def block(lines, title, rows, target, extra=""):
    ys = [num(r[target]) for r in rows]
    have = [r for r in rows if num(r[target]) is not None]
    dens = [num(r["d1_engaged_views"]) for r in have
            if num(r["d1_engaged_views"]) is not None]
    lines.append("")
    lines.append("%s  [%s]%s" % (title, target, extra))
    lines.append("  rows with this target: %d   outliers(>Q3+3IQR): %s"
                 % (len(have), ", ".join(outlier_codes(rows, target)) or "none"))
    if dens and target.startswith("d1_avg"):
        lines.append("  smallest engaged-view denominator behind a retention "
                     "value: %d" % int(min(dens)))
    for key, label in PREDICTORS:
        lines.append(pair_line(label, [num(r[key]) for r in rows], ys))


def correlations(rows):
    lines = [
        "# Correlations over the published CluePause videos in media-map.json.",
        "# Every line reports n, how many values were missing on each side, and",
        "# how many distinct predictor values the used pairs actually contain.",
        "# D1, D3, D7 and lifetime never appear in the same line.",
        "",
        "# Retention is reported three ways so the effect of each exclusion is",
        "# auditable rather than asserted:",
        "#   _raw   - as Studio printed it, including rows with 0 engaged views",
        "#   _valid - rows with 0 engaged views treated as MISSING, not as 0%",
        "#   _valid minus repeat-play - also drops values above 100%, which come",
        "#            from replays and are not on the same scale as sub-100 values",
        "",
    ]
    scored = [r for r in rows if r["ai_min"] != ""]
    mins = sorted({num(r["ai_min"]) for r in scored})
    lines += [
        "PREDICTOR RANGE RESTRICTION",
        "  published videos with a score: %d of %d" % (len(scored), len(rows)),
        "  ai_min observed values: %s" % mins,
        "  the 90 gate filters before publication, so no published video scores",
        "  below it. Any coefficient against ai_min is computed inside a %.0f point"
        " band" % ((max(mins) - min(mins)) if mins else 0),
        "  and cannot establish or refute the gate's predictive value.",
    ]
    usable = [r for r in rows if r["ai_min"] != "" and num(r["d1_views"]) is not None]
    lines.append("")
    lines.append("ANALYSIS SET: rows with both a traceable score and a D1 row: %d"
                 % len(usable))

    block(lines, "D1 views", usable, "d1_views")
    # sensitivity: the same target with the three heavy outliers removed
    outl = set(outlier_codes(usable, "d1_views"))
    if outl:
        block(lines, "D1 views, outliers removed (%s)" % ", ".join(sorted(outl)),
              [r for r in usable if r["code"] not in outl], "d1_views")
    block(lines, "D1 engaged views", usable, "d1_engaged_views")
    block(lines, "D1 avg % viewed, raw", usable, "d1_avg_viewed_pct_raw",
          "  <- includes rows whose engaged views are 0; kept only for comparison")
    block(lines, "D1 avg % viewed, valid", usable, "d1_avg_viewed_pct_valid")
    block(lines, "D1 avg % viewed, valid minus repeat-play",
          [r for r in usable if r["d1_repeat_play"] != "yes"],
          "d1_avg_viewed_pct_valid")
    block(lines, "lifetime stayed %", usable, "lifetime_stayed_pct")
    return "\n".join(lines) + "\n"


def main():
    rows = build_rows()
    with open(os.path.join(OUT, "quality-vs-market.csv"), "w", encoding="utf-8",
              newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    text = correlations(rows)
    with open(os.path.join(OUT, "correlations.txt"), "w", encoding="utf-8") as f:
        f.write(text)
    print(text)
    for r in rows:
        print("%-4s %-6s %-7s %-12s %-26s %-22s d1v=%5s avgOK=%6s %s" % (
            r["cohort"], r["code"], r["episode"], r["ai_gate_state"],
            r["version_check"], r["ai_scores"], r["d1_views"] or "-",
            r["d1_avg_viewed_pct_valid"] or "-", r["d1_window"]))


if __name__ == "__main__":
    main()
