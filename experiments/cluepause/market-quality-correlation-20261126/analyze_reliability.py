"""Analyse the reader-reliability benchmark.

Reads the evidence directories produced by run_reliability.py and reports, per
script: the six-dimension scores each panel gave, the spread, whether the gate
verdict flipped, whether the cores verdicts moved, and which dimensions the
87 <-> 91 crossings came from.

The primary comparison is panel A against panel B: both ran on today's runtime,
so a disagreement between them measures run-to-run reproducibility. Comparison
against the original score is reported too but is confounded whenever the Codex
binary differs from the one the original run used, which run-manifest.json
records.

Invalid reads (non-zero exit, isolation failure) are counted separately and are
never replaced by a re-draw.

Writes reliability-results.csv and reliability-report.txt.
"""
import csv
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WEIGHTS = (("suspense", 20), ("reframe", 25), ("motivation", 20),
           ("causality", 15), ("fairness", 10), ("visuals", 10))
DIMS = [d for d, _ in WEIGHTS]
PASS_SCORE, FINAL_READERS = 90, 3
# autoloop.py lines 21-22 and 350-353: `clear` is a conjunction, not a synonym
# for "no critical issues". Exporting it as an OR made the published CSV
# recompute a failing panel as a pass.
CRITICAL_DIMENSIONS = ("motivation", "causality", "fairness")
MIN_CRITICAL_SCORE = 3


def is_clear(scores, cores, critical_issues):
    """Reproduce autoloop.read_trial's `clear` exactly."""
    return (all(v == "supported" for v in cores.values())
            and not critical_issues
            and all(scores[k] >= MIN_CRITICAL_SCORE for k in CRITICAL_DIMENSIONS))


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def total(vals):
    return sum(vals[d] * w for d, w in WEIGHTS) // 5


def find_scored(obj, out):
    if isinstance(obj, dict):
        sc = obj.get("scores")
        if isinstance(sc, dict):
            vals = {k: (v.get("value") if isinstance(v, dict) else v)
                    for k, v in sc.items()}
            if set(vals) == set(DIMS) and all(isinstance(v, int) for v in vals.values()):
                out.append((vals, obj))
        for v in obj.values():
            find_scored(v, out)
    elif isinstance(obj, list):
        for v in obj:
            find_scored(v, out)
    elif isinstance(obj, str) and '"scores"' in obj:
        try:
            find_scored(json.loads(obj), out)
        except Exception:
            pass


def read_panel(evidence_dir):
    """One reader row per reader-NN.json, plus the token usage it reported."""
    rows = []
    for name in sorted(os.listdir(evidence_dir)):
        if not (name.startswith("reader-") and name.endswith(".json")):
            continue
        rec = load_json(os.path.join(evidence_dir, name))
        found = []
        find_scored(rec, found)
        usage = {"input_tokens": 0, "output_tokens": 0, "cached_input_tokens": 0}
        stack = [rec]
        while stack:
            cur = stack.pop()
            if isinstance(cur, dict):
                u = cur.get("usage")
                if isinstance(u, dict):
                    for k in usage:
                        usage[k] += u.get(k) or 0
                stack.extend(cur.values())
            elif isinstance(cur, list):
                stack.extend(cur)
        if not found:
            rows.append({"reader": name, "valid": False, "reason": "no scored stage",
                         "usage": usage})
            continue
        vals, holder = found[-1]
        issues = holder.get("critical_issues") or []
        cores = {c.get("label"): c.get("support")
                 for c in (holder.get("cores") or []) if isinstance(c, dict)}
        rows.append({
            "reader": name, "valid": True, "scores": vals, "total": total(vals),
            "clear": is_clear(vals, cores, issues),
            "critical_issues": issues,
            "cores": cores,
            "emotion": holder.get("emotion"),
            "usage": usage,
        })
    return rows


def verdict(rows):
    valid = [r for r in rows if r["valid"]]
    if len(valid) != FINAL_READERS:
        return "INVALID(%d valid reads)" % len(valid)
    # autoloop.py line 451, verbatim: score and clear, nothing else. `clear`
    # already carries the cores condition, so it must not be re-added here.
    if all(r["total"] >= PASS_SCORE and r["clear"] for r in valid):
        return "PASS"
    return "FAIL"


def main():
    out_root = sys.argv[1] if len(sys.argv) > 1 else None
    if not out_root:
        sys.exit("usage: python analyze_reliability.py <run output dir>")
    manifest = load_json(os.path.join(out_root, "run-manifest.json"))
    sample = {r["version_id"]: r for r in
              csv.DictReader(open(os.path.join(HERE, "reliability-sample.csv"),
                                  encoding="utf-8"))}

    panels = {}
    for inv in manifest["invocations"]:
        evid = os.path.join(out_root, inv["evidence_dir"])
        if inv["exit_code"] != 0 or not os.path.isdir(evid):
            panels[(inv["version_id"], inv["panel"])] = {
                "rows": [], "verdict": "INVOCATION_FAILED",
                "exit_code": inv["exit_code"], "seconds": inv["seconds"]}
            continue
        rows = read_panel(evid)
        panels[(inv["version_id"], inv["panel"])] = {
            "rows": rows, "verdict": verdict(rows),
            "exit_code": inv["exit_code"], "seconds": inv["seconds"]}

    versions = sorted({k[0] for k in panels},
                      key=lambda v: (sample.get(v, {}).get("band", ""), v))

    # ---- per-reader CSV
    csv_rows = []
    for (ver, panel), info in sorted(panels.items()):
        for r in info["rows"]:
            row = {"version_id": ver, "band": sample.get(ver, {}).get("band", ""),
                   "panel": panel, "reader": r["reader"], "valid": r["valid"],
                   "total": r.get("total", ""), "clear": r.get("clear", ""),
                   "cores": " ; ".join("%s=%s" % kv for kv in
                                       sorted((r.get("cores") or {}).items())),
                   "critical_issues": len(r.get("critical_issues") or []),
                   "input_tokens": r["usage"]["input_tokens"],
                   "output_tokens": r["usage"]["output_tokens"]}
            for d in DIMS:
                row[d] = (r.get("scores") or {}).get(d, "")
            csv_rows.append(row)
    if csv_rows:
        with open(os.path.join(HERE, "reliability-results.csv"), "w",
                  encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(csv_rows[0].keys()))
            w.writeheader()
            w.writerows(csv_rows)

    # ---- report
    L = []
    rt = manifest["runtime"]
    L += ["# Reader reliability benchmark, reduced run", "",
          "RUNTIME", "  codex: %s  sha256=%s" % (rt["codex_version"],
                                                 rt["codex_sha256"][:16]),
          "  same binary as the original 160 records: %s"
          % rt.get("codex_matches_original_run"),
          "  model / reasoning effort: %s" % rt["model"],
          "  autoloop.py: %s  sha256=%s" % (rt["autoloop_source"],
                                            rt["autoloop_sha256"][:16]),
          "  protocol: %s" % rt["protocol"], ""]
    if not rt.get("codex_matches_original_run"):
        L += ["  NOTE: the CLI binary differs from the original run, and no",
              "  record of the original model survives, so ONLY the A-vs-B",
              "  comparison isolates run-to-run variance. Any difference from",
              "  the original score also contains the runtime change.", ""]

    flips = same = invalid = 0
    L += ["PER SCRIPT", ""]
    for ver in versions:
        row = sample.get(ver, {})
        a = panels.get((ver, "A"))
        b = panels.get((ver, "B"))
        L.append("%s  band=%s  original=%s (min %s)"
                 % (ver, row.get("band", "?"), row.get("original_readers", "?"),
                    row.get("original_reader_min", "?")))
        for label, info in (("A", a), ("B", b)):
            if info is None:
                L.append("  panel %s: not run" % label)
                continue
            if info["verdict"].startswith("INVOCATION_FAILED"):
                L.append("  panel %s: INVOCATION FAILED (exit %s)"
                         % (label, info["exit_code"]))
                invalid += 1
                continue
            totals = [r["total"] for r in info["rows"] if r["valid"]]
            L.append("  panel %s: %-20s %s  (%.0fs)"
                     % (label, ",".join(str(t) for t in totals),
                        info["verdict"], info["seconds"]))
            for r in info["rows"]:
                if not r["valid"]:
                    L.append("      %s INVALID: %s" % (r["reader"], r["reason"]))
                    continue
                L.append("      %s total=%3d  %s  cores: %s"
                         % (r["reader"], r["total"],
                            " ".join("%s=%d" % (d[:4], r["scores"][d]) for d in DIMS),
                            " ".join("%s" % v for v in r["cores"].values()) or "-"))
        if a and b and a["verdict"] in ("PASS", "FAIL") and b["verdict"] in ("PASS", "FAIL"):
            if a["verdict"] != b["verdict"]:
                flips += 1
                L.append("  >>> GATE FLIP between panels: A=%s B=%s"
                         % (a["verdict"], b["verdict"]))
            else:
                same += 1
            ta = [r["total"] for r in a["rows"] if r["valid"]]
            tb = [r["total"] for r in b["rows"] if r["valid"]]
            if ta and tb:
                L.append("  spread: A min=%d max=%d | B min=%d max=%d | "
                         "min-to-min gap=%d"
                         % (min(ta), max(ta), min(tb), max(tb),
                            abs(min(ta) - min(tb))))
                moved = []
                for d in DIMS:
                    va = [r["scores"][d] for r in a["rows"] if r["valid"]]
                    vb = [r["scores"][d] for r in b["rows"] if r["valid"]]
                    if va and vb and (sum(va) / len(va)) != (sum(vb) / len(vb)):
                        moved.append("%s %.2f->%.2f"
                                     % (d, sum(va) / len(va), sum(vb) / len(vb)))
                L.append("  dimensions that moved: %s" % ("; ".join(moved) or "none"))
        L.append("")

    comparable = flips + same
    L += ["SUMMARY", "",
          "  scripts with two comparable panels: %d" % comparable,
          "  gate verdict identical across panels: %d" % same,
          "  GATE FLIPS: %d" % flips,
          "  failed or invalid invocations: %d" % invalid, ""]

    # ---- how the verdict moved, and on which dimension
    L += ["WHAT CHANGED THE VERDICT", ""]
    for ver in versions:
        a, b = panels.get((ver, "A")), panels.get((ver, "B"))
        if not (a and b) or a["verdict"] not in ("PASS", "FAIL")                 or b["verdict"] not in ("PASS", "FAIL"):
            continue
        if a["verdict"] == b["verdict"]:
            continue
        fail = b if b["verdict"] == "FAIL" else a
        reasons = []
        for r in fail["rows"]:
            if not r["valid"]:
                continue
            if r["total"] < PASS_SCORE:
                reasons.append("%s scored %d, below %d" % (r["reader"], r["total"],
                                                           PASS_SCORE))
            bad = [k for k, v in r["cores"].items() if v != "supported"]
            if bad:
                reasons.append("%s marked a core %s"
                               % (r["reader"],
                                  "/".join(sorted({r["cores"][k] for k in bad}))))
            if not r["clear"]:
                reasons.append("%s did not mark it clear" % r["reader"])
        L.append("  %s: %s" % (ver, "; ".join(reasons) or "unclear"))
    L.append("")

    # ---- per-dimension stability across the two panels
    L += ["PER-DIMENSION STABILITY (panel mean, A vs B)", ""]
    for d in DIMS:
        diffs = []
        for ver in versions:
            a, b = panels.get((ver, "A")), panels.get((ver, "B"))
            if not (a and b):
                continue
            va = [r["scores"][d] for r in a["rows"] if r["valid"]]
            vb = [r["scores"][d] for r in b["rows"] if r["valid"]]
            if va and vb:
                diffs.append(abs(sum(va) / len(va) - sum(vb) / len(vb)))
        if diffs:
            unchanged = sum(1 for x in diffs if x == 0)
            L.append("  %-11s identical on %d/%d scripts   mean |diff| = %.2f"
                     % (d, unchanged, len(diffs), sum(diffs) / len(diffs)))
    L.append("")

    # ---- cores verdicts
    core_rows = [r for (_, _), info in panels.items() for r in info["rows"]
                 if r["valid"]]
    not_supported = [r for r in core_rows
                     if any(v != "supported" for v in r["cores"].values())]
    L += ["CORES", "",
          "  valid reads: %d" % len(core_rows),
          "  reads marking at least one core not supported: %d"
          % len(not_supported), ""]

    # ---- totals across all reads
    alltot = sorted(r["total"] for r in core_rows)
    L += ["ALL %d TOTALS" % len(alltot), "",
          "  " + " ".join(str(t) for t in alltot),
          "  at or above %d: %d of %d"
          % (PASS_SCORE, sum(1 for t in alltot if t >= PASS_SCORE), len(alltot)),
          ""]

    # ---- against the original, reported but confounded
    L += ["AGAINST THE ORIGINAL VERDICT (confounded by the runtime change)", ""]
    for ver in versions:
        row = sample.get(ver, {})
        orig_min = float(row.get("original_reader_min") or 0)
        orig = "PASS" if orig_min >= PASS_SCORE else "FAIL"
        got = []
        for label in ("A", "B"):
            info = panels.get((ver, label))
            got.append("%s=%s" % (label, info["verdict"] if info else "not run"))
        L.append("  %-7s original=%-4s  %s" % (ver, orig, "  ".join(got)))
    L.append("")

    tin = sum(r["input_tokens"] for r in csv_rows)
    tout = sum(r["output_tokens"] for r in csv_rows)
    secs = sum(i["seconds"] for i in manifest["invocations"])
    L += ["COST",
          "  blind reads recorded: %d" % len(csv_rows),
          "  input tokens: %d   output tokens: %d" % (tin, tout),
          "  wall clock across invocations: %.0f s" % secs,
          "  (token counts are what the CLI reported; no price is applied)", ""]
    L += ["This is an exploratory benchmark. Six scripts and two panels cannot",
          "establish the reliability of the scoring system, and nothing here",
          "says whether the gate predicts market performance."]

    text = "\n".join(L) + "\n"
    with open(os.path.join(HERE, "reliability-report.txt"), "w",
              encoding="utf-8") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
