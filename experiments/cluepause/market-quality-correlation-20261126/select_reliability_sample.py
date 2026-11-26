"""Pick the frozen scripts for the reader-reliability experiment.

Selects from score-index.csv by band of reader_min, under the constraints the
Owner set: one rubric version only, and never two versions of the same story.
Selection is deterministic (ordered by story id then version id), so the sample
can be re-derived and audited rather than taken on trust.

Writes reliability-sample.csv. Read-only over its sources.
"""
import csv
import os

OUT = os.path.dirname(os.path.abspath(__file__))
RUBRIC = "story-quality-autoloop/v2"
BANDS = [("low", 82, 87), ("borderline", 88, 91), ("high", 92, 100)]
FULL_PER_BAND = 4
REDUCED_PER_BAND = 2


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def main():
    path = os.path.join(OUT, "score-index.csv")
    with open(path, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    eligible = [r for r in rows
                if r["rubric_version"] == RUBRIC
                and num(r["reader_min"]) is not None
                and r["reader_count"] == "3"
                and r["story_sha256"]]

    picked = []
    used_stories = set()
    pool = {name: sum(1 for r in eligible if lo <= num(r["reader_min"]) <= hi)
            for name, lo, hi in BANDS}
    # Fill the scarcest band first. The high band holds only a handful of
    # records, so letting a commoner band claim one of their stories under the
    # one-version-per-story rule would strand it.
    for name, lo, hi in sorted(BANDS, key=lambda b: pool[b[0]]):
        band = [r for r in eligible if lo <= num(r["reader_min"]) <= hi]
        band.sort(key=lambda r: (r["story_id"].zfill(4), r["version_id"]))
        for r in band:
            if r["story_id"] in used_stories:
                continue
            if sum(1 for p in picked if p["band"] == name) >= FULL_PER_BAND:
                break
            used_stories.add(r["story_id"])
            picked.append({
                "band": name,
                "band_range": "%d-%d" % (lo, hi),
                "reduced_set": "",
                "story_id": r["story_id"],
                "version_id": r["version_id"],
                "story_sha256": r["story_sha256"],
                "original_readers": r["readers"],
                "original_reader_min": r["reader_min"],
                "original_cores": r["cores"],
                "all_readers_clear": r["all_readers_clear"],
                "rubric_version": r["rubric_version"],
                "source_kind": r["source_kind"],
                "source_ref": r["source_ref"],
                "source_commit": r["source_commit"],
                "source_path": r["source_path"],
                "evidence_sha256": r["evidence_sha256"],
            })
    # the first N of each band also form the reduced 6-script pilot
    for name, _, _ in BANDS:
        inband = [p for p in picked if p["band"] == name]
        for p in inband[:REDUCED_PER_BAND]:
            p["reduced_set"] = "yes"

    picked.sort(key=lambda p: ([b[0] for b in BANDS].index(p["band"]),
                               p["story_id"].zfill(4)))
    out = os.path.join(OUT, "reliability-sample.csv")
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(picked[0].keys()))
        w.writeheader()
        w.writerows(picked)

    print("eligible records (rubric %s, 3 readers, content key): %d"
          % (RUBRIC, len(eligible)))
    for name, lo, hi in BANDS:
        got = sum(1 for p in picked if p["band"] == name)
        print("  %-11s %3d-%3d  pool=%3d  selected=%d%s"
              % (name, lo, hi, pool[name], got,
                 "   SHORT OF TARGET" if got < FULL_PER_BAND else ""))
    print()
    print("%-11s %-9s %-7s %-12s %s" % ("band", "version", "min", "readers", "reduced"))
    for p in picked:
        print("%-11s %-9s %-7s %-12s %s"
              % (p["band"], p["version_id"], p["original_reader_min"],
                 p["original_readers"], p["reduced_set"] or "-"))
    print()
    print("full run:    %d scripts x 2 fresh panels x 3 readers = %d blind reads"
          % (len(picked), len(picked) * 2 * 3))
    red = sum(1 for p in picked if p["reduced_set"])
    print("reduced run: %d scripts x 2 fresh panels x 3 readers = %d blind reads"
          % (red, red * 2 * 3))
    print("->", out)


if __name__ == "__main__":
    main()
