"""Run the reduced reader-reliability benchmark with the project's own instrument.

This does not reimplement the blind read. It materialises each frozen draft,
verifies its story_sha256, and invokes autoloop.py -- the same script that
produced the original 160 records -- once per (draft, panel) with --readers 3.
Each invocation gets its own evidence directory, so the two panels never share
a ledger and no reader sees another panel's work.

    python run_reliability.py --out DIR [--only VERSION] [--panels A B] [--dry-run]

Nothing is retried on a low score: a completed read is kept whatever it says.
An invalid read (non-zero exit, isolation failure) is recorded as invalid and
is never silently replaced.
"""
import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
S2V = r"D:\story2video"
GP = r"D:\s2v-gp"
AUTOLOOP_REF = "origin/codex/story-quality-autoloop"
AUTOLOOP_PATH = ".agents/skills/story-quality-autoloop/scripts/autoloop.py"
CODEX_EXE = (r"C:\Users\daish\AppData\Roaming\npm\node_modules\@openai\codex"
             r"\node_modules\@openai\codex-win32-x64\vendor"
             r"\x86_64-pc-windows-msvc\bin\codex.exe")
TEXT_FIELDS = ("first", "second", "reveal", "english")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(path):
    with open(path, "rb") as f:
        return sha256_bytes(f.read())


def story_sha256(obj):
    txt = "|".join(str(obj.get(k, "")) for k in TEXT_FIELDS)
    return sha256_bytes(txt.encode("utf-8"))


def git(repo, *args):
    r = subprocess.run(["git"] + list(args), cwd=repo, capture_output=True,
                       encoding="utf-8", errors="replace")
    if r.returncode:
        raise RuntimeError("git %s failed: %s" % (args[0], r.stderr[:200]))
    return r.stdout


def load_sample():
    path = os.path.join(HERE, "reliability-sample.csv")
    with open(path, encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["reduced_set"] == "yes"]


def materialise_draft(row, dest_dir):
    """Write the frozen draft and confirm its content key before any read."""
    name = row["version_id"] + ".json"
    src_rel = row["source_path"].replace("\\", "/")
    if row["source_kind"] == "git":
        ref = row["source_commit"] or AUTOLOOP_REF
        blob = git(GP, "show", ref + ":" + os.path.dirname(src_rel) + "/" + name)
        data = json.loads(blob)
        origin = ref + ":" + os.path.dirname(src_rel) + "/" + name
    else:
        path = os.path.join(S2V, os.path.dirname(src_rel), name)
        with open(path, encoding="utf-8-sig") as f:
            data = json.load(f)
        origin = path
    got = story_sha256(data)
    if got != row["story_sha256"]:
        raise RuntimeError("%s: story hash mismatch, expected %s got %s"
                           % (row["version_id"], row["story_sha256"], got))
    out = os.path.join(dest_dir, name)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return out, data, origin


def runtime_identity():
    ver = subprocess.run([CODEX_EXE, "--version"], capture_output=True,
                         encoding="utf-8", errors="replace")
    return {
        "codex_version": (ver.stdout or ver.stderr).strip(),
        "codex_exe": CODEX_EXE,
        "codex_sha256": sha256_file(CODEX_EXE),
        "original_run_codex_sha256":
            "83f5c2dd2ac2902e0d96ba5d8ccdd27d513f57df4a9ab73e06a5a518028e9a2f",
        "model": "CLI default; autoloop.py pins no model and the original runs "
                 "recorded none, so it cannot be matched to the original",
        "reasoning_effort": "CLI default; not pinned by autoloop.py",
        "credentials": "keyring",
        "protocol": "story-quality-autoloop/v2",
        "host_os": sys.platform,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", action="append", default=[],
                    help="limit to these version ids")
    ap.add_argument("--panels", nargs="+", default=["A", "B"])
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    out_root = os.path.abspath(args.out)
    os.makedirs(out_root, exist_ok=True)

    autoloop = os.path.join(out_root, "autoloop.py")
    if not os.path.exists(autoloop):
        src = git(GP, "show", AUTOLOOP_REF + ":" + AUTOLOOP_PATH)
        with open(autoloop, "w", encoding="utf-8", newline="") as f:
            f.write(src)
    ident = runtime_identity()
    ident["autoloop_sha256"] = sha256_file(autoloop)
    ident["autoloop_source"] = AUTOLOOP_REF + ":" + AUTOLOOP_PATH
    ident["codex_matches_original_run"] = (
        ident["codex_sha256"] == ident["original_run_codex_sha256"])

    manifest_path = os.path.join(out_root, "run-manifest.json")
    manifest = {"runtime": ident, "started_at": dt.datetime.now().astimezone().isoformat(),
                "invocations": []}
    if os.path.exists(manifest_path):
        with open(manifest_path, encoding="utf-8") as f:
            manifest = json.load(f)
            manifest["runtime"] = ident

    rows = load_sample()
    if args.only:
        rows = [r for r in rows if r["version_id"] in args.only]
    print("codex %s  sha256=%s  matches original run: %s"
          % (ident["codex_version"], ident["codex_sha256"][:12],
             ident["codex_matches_original_run"]))
    print("drafts: %s" % ", ".join(r["version_id"] for r in rows))
    print("panels: %s   invocations: %d"
          % (", ".join(args.panels), len(rows) * len(args.panels)))
    if args.dry_run:
        return

    done = {(i["version_id"], i["panel"]) for i in manifest["invocations"]
            if i.get("exit_code") == 0}
    for row in rows:
        for panel in args.panels:
            key = (row["version_id"], panel)
            if key in done:
                print("skip %s panel %s: already completed" % key)
                continue
            evid = os.path.join(out_root, "panel-" + panel, row["version_id"])
            if os.path.exists(evid):
                shutil.rmtree(evid)
            os.makedirs(evid, exist_ok=True)
            draft_path, draft, origin = materialise_draft(row, evid)
            argv = [sys.executable, autoloop, "run", draft_path, evid,
                    "--codex", CODEX_EXE, "--sha256", ident["codex_sha256"],
                    "--credentials", "keyring", "--base-sha", draft["parent"],
                    "--mode", "formal", "--readers", "3"]
            print("\n=== %s panel %s ===" % (row["version_id"], panel))
            start = time.time()
            proc = subprocess.run(argv, capture_output=True, encoding="utf-8",
                                  errors="replace")
            took = time.time() - start
            rec = {
                "version_id": row["version_id"], "band": row["band"],
                "panel": panel, "evidence_dir": os.path.relpath(evid, out_root),
                "draft_origin": origin, "story_sha256": row["story_sha256"],
                "base_sha": draft["parent"], "exit_code": proc.returncode,
                "seconds": round(took, 1),
                "stdout_tail": (proc.stdout or "")[-2000:],
                "stderr_tail": (proc.stderr or "")[-2000:],
                "ran_at": dt.datetime.now().astimezone().isoformat(),
            }
            manifest["invocations"] = [i for i in manifest["invocations"]
                                       if (i["version_id"], i["panel"]) != key]
            manifest["invocations"].append(rec)
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
            print("exit=%s  %.1fs" % (proc.returncode, took))
            if proc.returncode:
                print((proc.stderr or proc.stdout or "")[-600:])
    print("\nmanifest ->", manifest_path)


if __name__ == "__main__":
    main()
