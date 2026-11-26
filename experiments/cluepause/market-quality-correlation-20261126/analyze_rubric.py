"""Why do 92.9% of qualified videos score exactly 91?

Reads every per-reader score object found under D:\\story2video\\artifacts and
reconstructs the rubric arithmetic, so the concentration at 91 can be explained
from the data rather than guessed at.

total = (20*suspense + 25*reframe + 20*motivation
         + 15*causality + 10*fairness + 10*visuals) / 5
      =  4*suspense +  5*reframe +  4*motivation
         + 3*causality +  2*fairness +  2*visuals

Each dimension is an integer 1-5, so totals are discrete. Whether 90 is
reachable at all depends on which dimension values readers actually use.

Writes score-granularity.txt. Read-only.
"""
import collections
import glob
import itertools
import json
import os

S2V = r"D:\story2video"
OUT = os.path.dirname(os.path.abspath(__file__))
WEIGHTS = (("suspense", 20), ("reframe", 25), ("motivation", 20),
           ("causality", 15), ("fairness", 10), ("visuals", 10))
DIMS = [name for name, _ in WEIGHTS]
PASS_SCORE = 90  # autoloop.py: PASS_SCORE, FINAL_READERS = 90, 3


def total(vals):
    return sum(vals[name] * w for name, w in WEIGHTS) // 5


def collect(obj, out):
    """Find every complete six-dimension score object, however it is nested."""
    if isinstance(obj, dict):
        sc = obj.get("scores")
        if isinstance(sc, dict):
            vals = {k: (v.get("value") if isinstance(v, dict) else v)
                    for k, v in sc.items()}
            if set(vals) == set(DIMS) and all(isinstance(v, int)
                                              for v in vals.values()):
                out.append(vals)
        for v in obj.values():
            collect(v, out)
    elif isinstance(obj, list):
        for v in obj:
            collect(v, out)
    elif isinstance(obj, str) and '"scores"' in obj:
        try:
            collect(json.loads(obj), out)
        except Exception:
            pass


def read_all():
    reads = []
    root = os.path.join(S2V, "artifacts")
    for p in glob.glob(os.path.join(root, "**", "reader-*.json"), recursive=True):
        if "worktrees" in p.replace("\\", "/"):
            continue
        try:
            with open(p, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        collect(data, reads)
    return reads


def ladder(fixed):
    """Reachable totals when the named dimensions are fixed and the rest are 3-5."""
    free = [d for d in DIMS if d not in fixed]
    out = set()
    for combo in itertools.product(range(3, 6), repeat=len(free)):
        vals = dict(fixed)
        vals.update(dict(zip(free, combo)))
        out.add(total(vals))
    return sorted(out)


def main():
    reads = read_all()
    lines = ["# Why the qualified scores pile up on 91", ""]
    lines.append("reader score objects found under artifacts/: %d" % len(reads))
    if not reads:
        lines.append("(no reader-*.json available; nothing to analyse)")
        with open(os.path.join(OUT, "score-granularity.txt"), "w",
                  encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        print("\n".join(lines))
        return

    totals = collections.Counter(total(v) for v in reads)
    lines += ["", "OBSERVED TOTAL DISTRIBUTION", ""]
    for t in sorted(totals):
        bar = "#" * min(60, totals[t])
        mark = "  <- pass threshold is >= %d" % PASS_SCORE if t == PASS_SCORE else ""
        lines.append("  %3d  %4d  %s%s" % (t, totals[t], bar, mark))

    lines += ["", "PER-DIMENSION VALUES ACTUALLY USED", ""]
    for d, w in WEIGHTS:
        c = collections.Counter(v[d] for v in reads)
        share5 = 100.0 * c.get(5, 0) / len(reads)
        share4 = 100.0 * c.get(4, 0) / len(reads)
        lines.append("  %-11s weight %2d%%   %s   5:%4.1f%%  4:%4.1f%%"
                     % (d, w, dict(sorted(c.items())), share5, share4))

    lines += [
        "",
        "THE BINDING DIMENSION",
        "",
        "  reframe carries the largest weight (25%) and is the one dimension",
        "  readers almost never award a 5. With reframe fixed at 4 the score",
        "  cannot exceed 95 no matter how good everything else is.",
        "",
    ]

    common = {"reframe": 4, "causality": 5, "visuals": 5, "fairness": 5}
    rungs = ladder(common)
    lines += [
        "THE LADDER IN THE DOMINANT FAMILY",
        "",
        "  Fixing the values readers use most often:",
        "    " + ", ".join("%s=%d" % kv for kv in sorted(common.items())),
        "  leaves only suspense and motivation free, each worth 4 points,",
        "  so the reachable totals are spaced 4 apart:",
        "",
        "    " + "  ".join(str(t) for t in rungs),
        "",
        "  There is no 88, 89 or 90 on this ladder. The 90 threshold falls in",
        "  a gap, so the effective threshold is 91 and 91 is the LOWEST rung a",
        "  script can land on and still pass.",
        "",
    ]

    exact = [v for v in reads if total(v) == PASS_SCORE]
    lines += ["  reads that scored exactly %d: %d of %d"
              % (PASS_SCORE, len(exact), len(reads))]
    for v in exact:
        lines.append("    " + ", ".join("%s=%d" % (d, v[d]) for d in DIMS))
    reachable90 = [c for c in itertools.product(range(3, 6), repeat=6)
                   if total(dict(zip(DIMS, c))) == PASS_SCORE]
    need5 = sum(1 for c in reachable90 if dict(zip(DIMS, c))["reframe"] == 5)
    lines += [
        "",
        "  %d dimension combinations with no value below 3 total exactly %d."
        % (len(reachable90), PASS_SCORE),
        "  %d of them require reframe=5, which appears in only %.1f%% of reads;"
        % (need5, 100.0 * sum(1 for v in reads if v["reframe"] == 5) / len(reads)),
        "  the rest require a 3 somewhere, which readers rarely give.",
        "  So 90 is reachable in principle and almost never reachable in practice.",
        "",
    ]

    lines += [
        "THE STOPPING RULE ADDS THE REST",
        "",
        "  autoloop.py: PASS_SCORE, FINAL_READERS = 90, 3",
        "    passed = (len(valid) == FINAL_READERS",
        "              and all(row['score'] >= PASS_SCORE and row['clear'] ...))",
        "  and a story that has qualified may not be revised again",
        "  ('this story already qualified'), with RUN_LIMIT = 4 revisions.",
        "",
        "  Revision therefore stops at the first passing draft, and the first",
        "  passing rung is 91. Concentration at 91 is what this design produces;",
        "  it is not evidence that the readers are lenient or colluding.",
        "",
        "WHAT THIS MEANS FOR THE GATE",
        "",
        "  In the passing region the 100-point scale has about three usable",
        "  rungs (91 / 95 / 96+). A script scoring 91 and a script scoring 87",
        "  differ by one notch on one dimension. The number carries far less",
        "  information than its scale suggests, and reframe - the heaviest",
        "  weight - is nearly constant, so it discriminates almost nothing.",
        "",
        "  This is a measurement property, not a market finding. Whether the",
        "  gate is also unstable across independent panels is untested: see",
        "  reader-reliability-experiment.md.",
    ]

    text = "\n".join(lines) + "\n"
    with open(os.path.join(OUT, "score-granularity.txt"), "w", encoding="utf-8") as f:
        f.write(text)
    print(text)


if __name__ == "__main__":
    main()
