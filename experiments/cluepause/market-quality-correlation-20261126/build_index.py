"""Collect every blind-reader score record this machine can reach.

Two kinds of source:
  git    - final-report.json committed on a remote branch of Gavin0099/story2video.
           Some score evidence lives only on unmerged branches (PR #7,
           codex/story-quality-autoloop), so a local-only scan misses it.
  local  - final-report.json under D:\\story2video\\artifacts, which is not
           version controlled (AGENTS.md: artifacts/ 不進版控).

The content key is story_sha256 = sha256 of the four frozen text fields
(first | second | reveal | english). Version ids such as "62-v1" are reused by
unrelated story lineages and MUST NOT be used as a primary key.

Writes score-index.csv. Read-only over every source.
"""
import csv
import glob
import hashlib
import json
import os
import subprocess

S2V = r"D:\story2video"
GP = r"D:\s2v-gp"
OUT = os.path.dirname(os.path.abspath(__file__))
TEXT_FIELDS = ("first", "second", "reveal", "english")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def story_sha256(obj):
    """Content key for a frozen story, or None when the text fields are absent."""
    if not isinstance(obj, dict):
        return None
    txt = "|".join(str(obj.get(k, "")) for k in TEXT_FIELDS)
    if not txt.strip("|"):
        return None
    return hashlib.sha256(txt.encode("utf-8")).hexdigest()


def sha_of_file(path):
    try:
        return story_sha256(load_json(path))
    except Exception:
        return None


def git(repo, *args):
    r = subprocess.run(["git"] + list(args), cwd=repo, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    return r.stdout if r.returncode == 0 else None


def parse_report(data, rubric, src_kind, src_ref, src_commit, src_path, sha_lookup):
    """Yield one row per scored version inside a final-report.json."""
    for ver, v in (data.get("versions") or {}).items():
        readers = [r.get("score") for r in (v.get("readers") or [])]
        readers = [x for x in readers if isinstance(x, (int, float))]
        cores = sorted({str(val) for r in (v.get("readers") or [])
                        for val in (r.get("cores") or {}).values()})
        yield {
            "story_sha256": sha_lookup(ver) or "",
            "story_id": ver.split("-")[0],
            "version_id": ver,
            "readers": ",".join(str(int(x)) for x in readers),
            "reader_min": min(readers) if readers else "",
            "reader_count": len(readers),
            "cores": "/".join(cores),
            "run_status": v.get("status", ""),
            "rubric_version": rubric,
            "source_kind": src_kind,
            "source_ref": src_ref,
            "source_commit": src_commit,
            "source_path": src_path,
        }


def scan_git(repo):
    rows = []
    branches = [b.strip() for b in (git(repo, "branch", "-r") or "").splitlines()
                if b.strip() and "HEAD" not in b]
    for br in branches:
        listing = git(repo, "ls-tree", "-r", "--name-only", br) or ""
        reports = [p for p in listing.splitlines() if p.endswith("final-report.json")]
        for path in reports:
            blob = git(repo, "show", br + ":" + path)
            if not blob:
                continue
            try:
                data = json.loads(blob)
            except Exception:
                continue
            d = os.path.dirname(path)
            ledger = git(repo, "show", br + ":" + d + "/ledger.json")
            rubric = ""
            if ledger:
                try:
                    rubric = json.loads(ledger).get("protocol", "")
                except Exception:
                    rubric = ""
            commit = (git(repo, "log", "-1", "--format=%H", br, "--", path) or "").strip()

            def lookup(ver, _br=br, _d=d):
                b = git(repo, "show", _br + ":" + _d + "/" + ver + ".json")
                if not b:
                    return None
                try:
                    return story_sha256(json.loads(b))
                except Exception:
                    return None

            rows += list(parse_report(data, rubric, "git", br, commit, path, lookup))
    return rows


def scan_local():
    rows = []
    root = os.path.join(S2V, "artifacts")
    for p in glob.glob(os.path.join(root, "**", "final-report.json"), recursive=True):
        rel = os.path.relpath(p, S2V).replace("\\", "/")
        if "worktrees" in rel:
            continue
        try:
            data = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        d = os.path.dirname(p)
        rubric = ""
        lp = os.path.join(d, "ledger.json")
        if os.path.exists(lp):
            try:
                rubric = load_json(lp).get("protocol", "")
            except Exception:
                rubric = ""
        family = rel.split("/")[1] if rel.startswith("artifacts/") else ""
        rows += list(parse_report(
            data, rubric, "local", "artifacts/" + family, "", rel,
            lambda ver, _d=d: sha_of_file(os.path.join(_d, ver + ".json"))))
    return rows


def main():
    rows = scan_git(GP) + scan_local()
    # de-duplicate identical records seen through more than one branch
    seen = {}
    for r in rows:
        key = (r["story_sha256"], r["version_id"], r["readers"], r["run_status"],
               r["source_path"])
        if key in seen:
            prior = seen[key]
            refs = set(prior["source_ref"].split(" ; ")) | {r["source_ref"]}
            prior["source_ref"] = " ; ".join(sorted(refs))
        else:
            seen[key] = r
    rows = list(seen.values())
    rows.sort(key=lambda r: (r["story_id"], r["version_id"], r["source_kind"]))

    path = os.path.join(OUT, "score-index.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    git_rows = [r for r in rows if r["source_kind"] == "git"]
    keyed = [r for r in rows if r["story_sha256"]]
    print("score records: %d (git %d, local %d)"
          % (len(rows), len(git_rows), len(rows) - len(git_rows)))
    print("with a content key: %d; without: %d"
          % (len(keyed), len(rows) - len(keyed)))
    print("distinct story_sha256: %d" % len({r["story_sha256"] for r in keyed}))
    ids = {}
    for r in keyed:
        ids.setdefault(r["version_id"], set()).add(r["story_sha256"])
    collide = {k: v for k, v in ids.items() if len(v) > 1}
    print("version ids reused by different texts: %d %s"
          % (len(collide), sorted(collide)))
    print("->", path)


if __name__ == "__main__":
    main()
