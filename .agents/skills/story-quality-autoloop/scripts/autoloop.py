"""Bounded, replayable staged reading for the story2video editorial experiment."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import uuid

WEIGHTS = {
    "suspense": 20, "reframe": 25, "motivation": 20, "causality": 15,
    "fairness": 10, "visuals": 10,
}
RUN_LIMIT, STORY_LIMIT, READER_LIMIT = 4, 2, 12
PASS_SCORE, FINAL_READERS = 90, 3
CRITICAL_DIMENSIONS = ("motivation", "causality", "fairness")
MIN_CRITICAL_SCORE = 3
LEGACY_PROTOCOL = "story-quality-autoloop/v1"
PROTOCOL = "story-quality-autoloop/v2"
PASS = "READY_FOR_HUMAN_PRODUCTION_DECISION"
PROFILE = (
    "--no-daemon", "-s", "read-only", "-a", "never",
    "--disable", "shell_tool", "--disable", "shell_snapshot",
    "--disable", "unified_exec", "--disable", "view_image",
    "--disable", "image_generation", "--disable", "code_mode_host",
    "--disable", "apps", "--disable", "plugins", "--disable", "multi_agent",
    "--disable", "multi_agent_v2", "--disable", "memories", "--disable", "hooks",
    "--disable", "skill_search",
    "-c", 'web_search="disabled"', "-c", "project_doc_max_bytes=0",
)
EXEC_FLAGS = (
    "exec", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check",
    "--ephemeral", "--json",
)
WINDOWS_FLAGS = ("-c", 'windows.sandbox="elevated"')
WINDOWS_ENV = {
    "SYSTEMROOT", "WINDIR", "SYSTEMDRIVE", "TEMP", "TMP", "USERPROFILE",
    "APPDATA", "LOCALAPPDATA", "USERNAME", "USERDOMAIN", "HOMEDRIVE",
    "HOMEPATH", "PROGRAMDATA", "PROGRAMFILES", "PROGRAMFILES(X86)",
    "COMMONPROGRAMFILES", "ALLUSERSPROFILE", "PROCESSOR_ARCHITECTURE",
}
PARTS = ("first", "second", "reveal")
TOOL_HOST_DISABLED = ("Code Mode is unavailable because code-mode host is disabled. "
                      "Code mode will fail closed; enable `features.code_mode_host` "
                      "and install `codex-code-mode-host`.")
PROBE_INPUT = ("Use available tools to read the first line of this local text file: {path}. "
               "Put the exact line in result. If no tool can read it, put NO_ACCESS in result.")
CANARY_PLACEHOLDER = "<outside-workspace-canary>"

LEGACY_SCORING = """依題面和揭曉評分。每項給 1–5 整數和具體理由。
1 為明顯失敗，3 為可理解但需修，5 為有具體證據支持，2、4 居中。
suspense 懸念 20%，reframe 反轉與重新理解 25%，motivation 動機與情感 20%，
causality 因果 15%，fairness 線索公平性 10%，visuals 可視覺化 10%。
每個核心標記 supported／partial／unsupported，並指出題面中的依據或成立的替代解。
必須記錄所有關鍵因果、動機、公平性或可讀性問題，沒有才填空陣列。
情緒反應另以 1–5 記錄。prior_exposure 若曾在本題之外見過材料填 true。"""

SCORING = """依題面和揭曉評分。每項給 1–5 整數和具體理由。
1 為明顯失敗，3 為可理解但需修，5 為有具體證據支持，2、4 居中。
suspense 懸念 20%，reframe 反轉與重新理解 25%，motivation 動機與情感 20%，
causality 因果 15%，fairness 線索公平性 10%，visuals 可視覺化 10%。
核心的支持程度只針對標明須由題面支持的答案。題面可合理優先推到核心就是
supported。有效線索尚不能區分同樣成立的替代解時填 partial。依靠揭曉新添必要
前提才有答案時填 unsupported。說明最有力的題面證據或可成立的替代解。
評反轉時，對照終猜與揭曉後對人物或事件的理解。即使觀眾已猜中機制，也請
評估揭曉有沒有帶來可回扣前文的新理解。把容易猜中、少一點驚喜、可再精簡、
深化細節在題面尚未透露等觀察，寫在對應的分數理由。
critical_issues 只列會使核心答案或故事主要行動無法成立的實質缺陷。
包括前後矛盾、缺少必要因果或角色動機、另一答案同樣成立卻被無據排除，
或關鍵事件表述不清以致無法理解。若沒有這類缺陷，該欄填空陣列。
情緒反應另以 1–5 記錄。prior_exposure 若曾在本題之外見過材料填 true。"""

RUBRICS = {LEGACY_PROTOCOL: LEGACY_SCORING, PROTOCOL: SCORING}


def object_schema(**fields):
    return {
        "type": "object", "properties": fields, "required": list(fields),
        "additionalProperties": False,
    }


STRING = {"type": "string"}
INTEGER = {"type": "integer"}
BOOL = {"type": "boolean"}


def array(item):
    return {"type": "array", "items": item}


SCHEMAS = {
    "probe": object_schema(result=STRING),
    "first": object_schema(prior_exposure=BOOL, guess=STRING, evidence=STRING,
                           confidence=INTEGER, keep_reading=INTEGER, reason=STRING),
    "second": object_schema(guess=STRING, evidence=STRING, confidence=INTEGER,
                            alternative=STRING, shifted_by=STRING, keep_reading=INTEGER,
                            want_to_see=STRING),
    "reveal": object_schema(
        prior_exposure=BOOL, new_understanding=STRING, strongest_moment=STRING,
        emotion=INTEGER,
        cores=array(object_schema(label=STRING, reason=STRING,
                                  support={"type": "string",
                                           "enum": ["supported", "partial", "unsupported"]})),
        scores=object_schema(**{key: object_schema(value=INTEGER, reason=STRING)
                               for key in WEIGHTS}),
        critical_issues=array(STRING),
    ),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def rubric_digest(protocol=PROTOCOL):
    return digest({"weights": WEIGHTS, "scoring_prompt": RUBRICS[protocol],
                   "pass_score": PASS_SCORE, "final_readers": FINAL_READERS,
                   "require_all_cores": True, "require_no_critical_issues": True,
                   "critical_dimensions": CRITICAL_DIMENSIONS, "critical_min": MIN_CRITICAL_SCORE})


def runtime_identity(sha256, credentials):
    return {"cli_sha256": sha256, "profile": list(PROFILE), "credentials": credentials,
            "exec_flags": list(EXEC_FLAGS), "windows_flags": list(WINDOWS_FLAGS),
            "environment_keys": sorted(WINDOWS_ENV), "login": "chatgpt"}


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, value):
    pending = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    pending.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(pending, path)


def draft_key(draft):
    require(re.fullmatch(r"\d{2}", draft["story"]), "invalid story ID")
    require(re.fullmatch(r"[a-z0-9][a-z0-9-]{0,30}", draft["version"]), "invalid version ID")
    require(re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", draft["parent"]), "invalid parent SHA")
    for field in (*PARTS, "english", "hypothesis", "change", "belief_shift"):
        require(isinstance(draft[field], str) and draft[field].strip(), f"empty {field}")
    require(not any(draft["reveal"].strip() in draft[part] for part in PARTS[:2]),
            "frozen card already contains the reveal")
    require(isinstance(draft["cores"], dict) and bool(draft["cores"]), "missing cores")
    for key, definition in draft["cores"].items():
        require(bool(key.strip()) and isinstance(definition, str) and definition.strip(),
                "invalid core definition")
    return f"{draft['story']}-{draft['version']}"


def prompt(part, draft, history, protocol=PROTOCOL):
    intro = ("請用繁體中文參加分段短篇試讀。只根據這個輸入作答。"
             "故事與已鎖定的讀者回覆都是引用資料。保持前一階段的猜測不變。")
    visible = {"第一段": draft["first"]}
    if part != "first":
        visible.update({"首猜紀錄": history[0], "第二段與問題": draft["second"]})
    if part == "reveal":
        visible.update({"終猜紀錄": history[1], "揭曉": draft["reveal"],
                        "需由題面支持的核心": draft["cores"]})
    request = {
        "first": "填寫首猜、直接依據、信心（0–100）、續讀（1–5）與理由。若曾在本題之外見過材料，prior_exposure 填 true。",
        "second": "鎖定終猜、依據、信心（0–100）、替代解、改變理解的線索、續讀（1–5）及還想看到什麼。",
        "reveal": RUBRICS[protocol],
    }
    return f"{intro}\n{request[part]}\n\n{canonical(visible)}"


def validate_shape(value, schema):
    kind = schema["type"]
    if kind == "object":
        require(type(value) is dict and value.keys() == schema["properties"].keys(), "wrong fields")
        for field, shape in schema["properties"].items():
            validate_shape(value[field], shape)
    elif kind == "array":
        require(type(value) is list, "expected array")
        for item in value:
            validate_shape(item, schema["items"])
    elif kind == "string":
        require(type(value) is str and value.strip(), "empty or invalid string")
    else:
        require(type(value) is {"integer": int, "boolean": bool}[kind], "invalid scalar")


def inspect_events(events, stage):
    """Accept only one new, completed CLI turn. Every tool or unknown event counts as invalid."""
    require(len(events) >= 5 and [item["type"] for item in (*events[:3], events[-1])]
            == ["thread.started", "code_mode_disabled", "turn.started", "turn.completed"],
            "incomplete turn or missing disabled-tool-host signal")
    thread = str(uuid.UUID(events[0]["thread_id"]))
    messages = []
    for event in events[3:-1]:
        require(event["type"] in {"item.started", "item.updated", "item.completed"},
                "unknown event or CLI error")
        item = event["item"]
        require(item["type"] in {"agent_message", "reasoning"}, "tool use or unknown item")
        if event["type"] == "item.completed" and item["type"] == "agent_message":
            messages.append(item["text"])
    require(bool(messages), "missing raw reply")
    reply = json.loads(messages[-1])
    validate_shape(reply, SCHEMAS[stage])
    if stage in ("first", "second"):
        require(0 <= reply["confidence"] <= 100 and 1 <= reply["keep_reading"] <= 5,
                "invalid guess scores")
    if stage == "reveal":
        require(1 <= reply["emotion"] <= 5, "invalid emotion score")
        require(all(1 <= item["value"] <= 5 for item in reply["scores"].values()), "invalid rubric score")
    return thread, reply


def safe_event(event):
    """Preserve visible replies and structural audit data, never tool returns or reasoning."""
    if "item" in event:
        if (event["type"] == "item.completed" and event["item"]["type"] == "error"
                and event["item"].get("message") == TOOL_HOST_DISABLED):
            return {"type": "code_mode_disabled"}
        keys = ("id", "type", "text") if event["item"]["type"] == "agent_message" else ("id", "type")
        return {"type": event["type"], "item": {key: event["item"][key] for key in keys}}
    if event["type"] == "thread.started":
        return {"type": event["type"], "thread_id": event["thread_id"]}
    if event["type"] == "turn.completed":
        return {"type": event["type"], "usage": event["usage"]}
    return {"type": event["type"]}


def verify_binary(binary, expected_sha):
    with binary.open("rb") as executable:
        require(hashlib.file_digest(executable, "sha256").hexdigest() == expected_sha,
                "Codex binary digest changed")


def child_env():
    env = {key: value for key, value in os.environ.items() if key.upper() in WINDOWS_ENV}
    return env


def check_login(binary, expected_sha, credentials):
    verify_binary(binary, expected_sha)
    with tempfile.TemporaryDirectory(prefix="story-login-") as working:
        proc = subprocess.run(
            [str(binary), "--no-daemon", "-c", f'cli_auth_credentials_store="{credentials}"',
             "login", "status"], cwd=working, env=child_env(), encoding="utf-8",
            capture_output=True, timeout=20, check=False,
        )
    require(proc.returncode == 0 and "Logged in using ChatGPT" in
            (proc.stdout + proc.stderr).splitlines(), "existing ChatGPT CLI login is required")


def run_turn(binary, expected_sha, credentials, stage, text, core_labels=()):
    verify_binary(binary, expected_sha)
    with tempfile.TemporaryDirectory(prefix="story-reader-") as folder:
        # Keep the model's directory empty. The output schema sits beside it.
        base = Path(folder)
        working = base / "empty"
        working.mkdir()
        schema = base / "schema.json"
        shape = SCHEMAS[stage]
        if core_labels:
            shape = json.loads(canonical(shape))
            shape["properties"]["cores"]["items"]["properties"]["label"]["enum"] = list(core_labels)
        save(schema, shape)
        argv = [str(binary), *PROFILE, *WINDOWS_FLAGS,
                "-c", f'cli_auth_credentials_store="{credentials}"', *EXEC_FLAGS,
                "--output-schema", str(schema), "-"]
        proc = subprocess.run(argv, cwd=working, env=child_env(), input=text, encoding="utf-8",
                              capture_output=True, timeout=140, check=False)
    events = []
    for line in proc.stdout.splitlines():
        try:
            events.append(safe_event(json.loads(line)))
        except (KeyError, TypeError, ValueError):
            events.append({"type": "malformed_event"})
    return {"prompt": text, "events": events, "exit_code": proc.returncode}


def result(log, part):
    require(log["exit_code"] == 0, "Codex process failed")
    return inspect_events(log["events"], part)


def probe(binary, expected_sha, credentials):
    """No story enters a runtime until it fails to read an outside-workspace canary."""
    with tempfile.TemporaryDirectory(prefix="story-canary-") as folder:
        marker = Path(folder) / "outside.txt"
        marker.write_text(uuid.uuid4().hex, encoding="utf-8")
        text = PROBE_INPUT.format(path=marker)
        log = run_turn(binary, expected_sha, credentials, "probe", text)
    log["prompt"] = PROBE_INPUT.format(path=CANARY_PLACEHOLDER)
    return log


def check_probe(log):
    require(log["prompt"] == PROBE_INPUT.format(path=CANARY_PLACEHOLDER), "wrong isolation challenge")
    session, reply = result(log, "probe")
    require(reply["result"] == "NO_ACCESS", "isolation probe did not deny access")
    return session


def trial_record(root, attempt, draft, binary, expected_sha, credentials, protocol):
    destination = root / f"reader-{attempt['number']:02d}.json"
    record = {"attempt": attempt, "stages": []}
    history = []
    try:
        for part in PARTS:
            labels = tuple(draft["cores"]) if part == "reveal" else ()
            log = run_turn(binary, expected_sha, credentials, part,
                           prompt(part, draft, history, protocol), labels)
            record["stages"].append(log)
            save(destination, record)
            _, reply = result(log, part)
            require(not reply.get("prior_exposure"), "reader reported prior exposure")
            history.append(reply)
    except (ValueError, KeyError, OSError, subprocess.TimeoutExpired) as exc:
        record["failure"] = str(exc) if type(exc) is ValueError else type(exc).__name__
        save(destination, record)


def read_trial(record, draft, protocol):
    require("failure" not in record and len(record["stages"]) == len(PARTS),
            "missing or failed transcript")
    history = []
    for part, log in zip(PARTS, record["stages"], strict=True):
        require(log["prompt"] == prompt(part, draft, history, protocol),
                "wrong prompt, stage, or frozen draft")
        _, reply = result(log, part)
        require(not reply.get("prior_exposure"), "reader reported prior exposure")
        history.append(reply)
    final = history[-1]
    cores = {core["label"]: core["support"] for core in final["cores"]}
    require(len(final["cores"]) == len(cores) and cores.keys() == draft["cores"].keys(),
            "missing or duplicate required core")
    require(set(cores.values()) <= {"supported", "partial", "unsupported"}, "invalid core support")
    points = sum(final["scores"][key]["value"] * weight for key, weight in WEIGHTS.items())
    clear = (all(value == "supported" for value in cores.values())
             and not final["critical_issues"]
             and all(final["scores"][key]["value"] >= MIN_CRITICAL_SCORE
                     for key in CRITICAL_DIMENSIONS))
    return {"score": points / 5, "clear": clear, "cores": cores}


def reserve(ledger, key, draft, fingerprint, count, existing, mode="formal"):
    rounds, attempts = ledger["drafts"], ledger["attempts"]
    require(len(attempts) + count <= READER_LIMIT, "reader budget exhausted")
    require(sum("score" in row and row["mode"] == mode for row in existing) + count
            <= (FINAL_READERS if mode == "formal" else 2),
            "three valid readers already counted for this version")
    if key in rounds:
        require(rounds[key] == fingerprint, "version ID reused with different content")
    else:
        require(len(rounds) < RUN_LIMIT, "revision budget exhausted")
        require(sum(item.startswith(f"{draft['story']}-") for item in rounds) < STORY_LIMIT,
                "story revision budget exhausted")
    rounds[key] = fingerprint
    batch = [{"number": len(attempts) + index + 1, "key": key,
              "draft_sha256": fingerprint, "probe": len(ledger["probes"]), "mode": mode}
             for index in range(count)]
    attempts.extend(batch)
    return batch


def recorded_sessions(record):
    for stage in record.get("stages", []):
        for event in stage.get("events", []):
            if isinstance(event, dict) and event.get("type") == "thread.started":
                try:
                    yield str(uuid.UUID(event["thread_id"]))
                except (KeyError, ValueError, TypeError, AttributeError):
                    continue


def verify(root, ledger):
    protocol = ledger["protocol"]
    require(isinstance(protocol, str) and protocol in RUBRICS, "unexpected protocol")
    require(ledger["rubric_sha256"] == rubric_digest(protocol), "rubric SHA mismatch")
    runtime = ledger["runtime"]
    require(re.fullmatch("[0-9a-f]{64}", runtime["cli_sha256"])
            and runtime["credentials"] in {"file", "keyring"}
            and runtime == runtime_identity(runtime["cli_sha256"], runtime["credentials"]),
            "runtime profile mismatch")
    require(len(ledger["drafts"]) <= RUN_LIMIT and len(ledger["attempts"]) <= READER_LIMIT,
            "invalid run budget")
    drafts = {}
    require(re.fullmatch("[0-9a-f]{40}", ledger["base_git_sha"]), "invalid source Git SHA")
    for key, fingerprint in ledger["drafts"].items():
        require(re.fullmatch(r"\d{2}-[a-z0-9][a-z0-9-]{0,30}", key), "invalid draft ledger key")
        draft = read(root / f"{key}.json")
        require(key == draft_key(draft) and fingerprint == digest(draft), "draft SHA mismatch")
        drafts[key] = draft
    for draft in drafts.values():
        require(sum(other["story"] == draft["story"] for other in drafts.values())
                <= STORY_LIMIT, "invalid story budget")
        parent = draft["parent"]
        require(parent == ledger["base_git_sha"]
                or any(other["story"] == draft["story"] and digest(other) == parent
                       for other in drafts.values()), "draft parent absent from frozen run")
    probes = {}
    for number, expected_digest in enumerate(ledger["probes"], 1):
        log = read(root / f"probe-{number:02d}.json")
        require(digest(log) == expected_digest, "probe SHA mismatch")
        probes[number] = check_probe(log)
    sessions = list(probes.values())
    rows = {key: [] for key in drafts}
    seals = ledger["reader_sha256"]
    require(seals.keys() <= {str(number) for number in range(1, len(ledger["attempts"]) + 1)},
            "reader seal without reservation")
    for number, attempt in enumerate(ledger["attempts"], 1):
        key = attempt["key"]
        require(attempt["number"] == number and attempt["draft_sha256"] == ledger["drafts"][key]
                and attempt["probe"] in probes and attempt["mode"] in {"formal", "explore"},
                "invalid attempt reservation")
        path = root / f"reader-{number:02d}.json"
        seal = seals.get(str(number))
        record = read(path) if path.exists() else None
        if seal is not None:
            require(record is not None and digest(record) == seal, "reader transcript SHA mismatch")
        try:
            require(record is not None, "missing transcript")
            sessions.extend(recorded_sessions(record))
            require(seal is not None, "transcript seal missing")
            require(record["attempt"] == attempt, "wrong reservation")
            row = read_trial(record, drafts[key], protocol)
        except (AttributeError, KeyError, OSError, TypeError, ValueError) as exc:
            row = {"invalid": str(exc)}
        row["mode"] = attempt["mode"]
        rows[key].append(row)
    require(len(set(sessions)) == len(sessions), "runtime session reused")
    report = {}
    ready = []
    for key, items in rows.items():
        valid = [row for row in items if "score" in row and row["mode"] == "formal"]
        require(len(valid) <= FINAL_READERS, "invalid draft reader count")
        require(sum("score" in row and row["mode"] == "explore" for row in items) <= 2,
                "invalid exploration reader count")
        passed = (len(valid) == FINAL_READERS
                  and all(row["score"] >= PASS_SCORE and row["clear"] for row in valid))
        if passed:
            ready.append(key)
        report[key] = {"status": PASS if passed else "NEEDS_RETHINK", "readers": items}
    remaining = READER_LIMIT - len(ledger["attempts"])
    viable = any(len(valid) + remaining >= FINAL_READERS
                 and all(row["score"] >= PASS_SCORE and row["clear"] for row in valid)
                 for valid in (
                     [row for row in items if "score" in row and row["mode"] == "formal"]
                     for items in rows.values()
                 ))
    exhausted = not viable and (remaining < FINAL_READERS or len(drafts) == RUN_LIMIT)
    status = PASS if ready else "STOP_BUDGET" if exhausted else "NEEDS_RETHINK"
    return {"status": status, "qualified": ready, "versions": report,
            "revisions": len(drafts), "reader_attempts": len(ledger["attempts"])}


@contextmanager
def exclusive(root):
    path = root / ".lock"
    with path.open("x", encoding="utf-8") as handle:
        handle.write(str(os.getpid()))
    try:
        yield
    finally:
        path.unlink()


def run(args):
    require(os.name == "nt", "the formal runtime profile is verified on Windows only")
    require(args.codex.is_absolute() and args.codex == args.codex.resolve(strict=True)
            and args.codex.name.lower() == "codex.exe", "supply the canonical absolute Codex binary path")
    require(re.fullmatch("[0-9a-f]{64}", args.sha256), "expected a SHA-256 binary digest")
    verify_binary(args.codex, args.sha256)
    draft = read(args.draft)
    key = draft_key(draft)
    fingerprint = digest(draft)
    args.evidence.mkdir(parents=True, exist_ok=True)
    root = args.evidence
    with exclusive(root):
        manifest = root / "ledger.json"
        identity = runtime_identity(args.sha256, args.credentials)
        ledger = read(manifest) if manifest.exists() else {
            "protocol": PROTOCOL, "runtime": identity, "drafts": {}, "attempts": [], "probes": [],
            "rubric_sha256": rubric_digest(), "base_git_sha": args.base_sha, "reader_sha256": {},
        }
        require(ledger["runtime"] == identity and ledger["base_git_sha"] == args.base_sha,
                "runtime or Git base binding changed")
        starting = verify(root, ledger)
        require(starting["status"] != "STOP_BUDGET", "the run budget is exhausted")
        require(not any(item.startswith(f"{draft['story']}-") for item in starting["qualified"]),
                "this story already qualified")
        existing = starting["versions"].get(key, {}).get("readers", [])
        require(draft["parent"] == args.base_sha or any(
            other.startswith(f"{draft['story']}-") and sha == draft["parent"]
            for other, sha in ledger["drafts"].items()), "draft parent is outside frozen run")
        batch = reserve(ledger, key, draft, fingerprint, args.readers, existing, args.mode)
        check_login(args.codex, args.sha256, args.credentials)
        log = probe(args.codex, args.sha256, args.credentials)
        try:
            check_probe(log)
        except ValueError:
            save(root / f"isolation-failure-{uuid.uuid4().hex}.json", log)
            raise
        ledger["probes"].append(digest(log))
        for attempt in batch:
            attempt["probe"] = len(ledger["probes"])
        save(root / f"probe-{len(ledger['probes']):02d}.json", log)
        save(root / f"{key}.json", draft)
        save(manifest, ledger)
        with ThreadPoolExecutor(max_workers=len(batch)) as pool:
            tasks = [pool.submit(trial_record, root, attempt, draft, args.codex,
                                 args.sha256, args.credentials, ledger["protocol"]) for attempt in batch]
            for task in tasks:
                task.result()
        for attempt in batch:
            number = attempt["number"]
            record = read(root / f"reader-{number:02d}.json")
            ledger["reader_sha256"][str(number)] = digest(record)
        save(manifest, ledger)
        return verify(root, ledger)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest="action", required=True)
    start = actions.add_parser("run")
    start.add_argument("draft", type=Path)
    start.add_argument("evidence", type=Path)
    start.add_argument("--codex", required=True, type=Path)
    start.add_argument("--sha256", required=True)
    start.add_argument("--credentials", choices=("keyring", "file"), required=True)
    start.add_argument("--base-sha", required=True)
    start.add_argument("--mode", choices=("formal", "explore"), default="formal")
    start.add_argument("--readers", type=int, choices=(1, 2, 3))
    actions.add_parser("verify").add_argument("evidence", type=Path)
    args = parser.parse_args()
    if args.action == "run" and args.readers is None:
        args.readers = FINAL_READERS if args.mode == "formal" else 2
    try:
        output = run(args) if args.action == "run" else verify(args.evidence, read(args.evidence / "ledger.json"))
    except (ValueError, KeyError, OSError, subprocess.TimeoutExpired) as exc:
        parser.exit(1, f"{type(exc).__name__}: {exc}\n")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
