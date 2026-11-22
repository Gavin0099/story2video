"""Validate a frozen WhyNest Lab script batch and its published review receipts."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

HERE = Path(__file__).resolve().parent
BATCH_RANGES = {
    "batch-001": range(22, 32),
    "batch-002": range(32, 42),
    "batch-003": range(42, 52),
    "batch-004": range(52, 62),
    "batch-005": range(62, 72),
    "batch-006": range(72, 82),
}
RUBRIC = {
    "hook": 15,
    "clarity": 25,
    "causal_retelling": 25,
    "visual_plan": 20,
    "pacing": 10,
    "natural_language": 5,
}
MINIMUM = 85


def require(condition, message):
    if not condition:
        raise ValueError(message)


def table_rows(content):
    return [
        [cell.strip() for cell in line.strip("|").split("|")]
        for line in content.splitlines()
        if line.startswith("|") and line.endswith("|")
    ]


def verify_script(episode, path, record):
    raw = path.read_bytes()
    content = raw.decode("utf-8")
    require(record["sha256"] == sha256(raw).hexdigest(), f"{episode}: script changed after review")
    require(content.startswith(f"# {episode}｜"), f"{episode}: heading does not match ID")
    version = re.search(r"\*\*版本\*\* v(\d+)", content)
    require(version and type(record["revision"]) is int and int(version[1]) == record["revision"],
            f"{episode}: revision mismatch")
    mechanism = re.search(r"\*\*機制\*\* `([a-z0-9-]+)`", content)
    require(mechanism is not None, f"{episode}: missing mechanism")

    for heading in ("**English title**", "## 影片說明", "## 雙語腳本與分鏡", "## 對照與製作條件", "## 主張與來源"):
        require(heading in content, f"{episode}: missing {heading}")
    description = content.split("## 影片說明", 1)[1].split("## 雙語腳本與分鏡", 1)[0].strip()
    require(len(description.split("\n\n")) == 2, f"{episode}: bilingual description required")

    rows = table_rows(content)
    cues = [row for row in rows if re.fullmatch(r"\d+–\d+", row[0])]
    require(cues, f"{episode}: missing timed scenes")
    end = 0
    for cue in cues:
        require(len(cue) == 4 and all(cue), f"{episode}: incomplete bilingual scene")
        start, next_end = map(int, cue[0].split("–"))
        require(start == end and next_end > start, f"{episode}: invalid scene timing")
        require(re.search(r"[A-Za-z]", cue[1]) and re.search(r"[\u3400-\u9fff]", cue[2]),
                f"{episode}: missing English or Traditional Chinese dialogue")
        end = next_end
    require(30 <= end <= 60, f"{episode}: expected a 30–60 second script")

    sources = {}
    for row in (row for row in rows if re.fullmatch(r"S\d+", row[0])):
        key, cite, scope = row
        link = re.fullmatch(r"\[([^\]]+)\]\((https://[^)]+)\)", cite)
        require(key not in sources and link and scope, f"{episode}: invalid source {key}")
        name, url = link.groups()
        sources[key] = (name.split(" · ", 1)[0], urlsplit(url).hostname)
    claims = [row for row in rows if re.fullmatch(r"C\d+", row[0])]
    require(claims, f"{episode}: missing claims")
    require(len({row[0] for row in claims}) == len(claims), f"{episode}: duplicate claim ID")
    for key, claim, refs in claims:
        ref_ids = refs.split("、")
        require(claim and all(ref_id in sources for ref_id in ref_ids), f"{episode}: unknown source at {key}")
        publishers, hosts = zip(*(sources[ref_id] for ref_id in ref_ids))
        require(len(set(publishers)) >= 2 and len(set(hosts)) >= 2,
                f"{episode}: {key} requires two source publishers")
    cue_digest = sha256(json.dumps(cues, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
    return mechanism[1], cue_digest.hexdigest()


def verify_reviews(episode, record, cue_digest):
    fact = record["fact"]
    visual = record["visual"]
    readers = record["readers"]
    require(len(readers) == 2, f"{episode}: expected two blind readers")
    reviewers = [entry["reviewer"] for entry in (fact, visual, *readers)]
    require(all(reviewers) and len(set(reviewers)) == 4, f"{episode}: review roles must be independent")
    for review in (fact, visual, *readers):
        require(review["sha256"] == record["sha256"], f"{episode}: stale review from {review['reviewer']}")
        require(review["status"] == "PASS" and review["blockers"] == [] and review["note"].strip(),
                f"{episode}: incomplete or blocking review from {review['reviewer']}")
    for reader in readers:
        require(reader["stages"] == ["hook-only", "full-script"], f"{episode}: incomplete blind stages")
        require(reader["cue_sha256"] == cue_digest, f"{episode}: blind reader saw different cues")
        require(reader["core_retelling_correct"] is True and reader["transfer_answer_correct"] is True,
                f"{episode}: comprehension check failed")
        scores = reader["scores"]
        require(set(scores) == set(RUBRIC), f"{episode}: rubric mismatch")
        require(all(type(scores[key]) is int and 0 <= scores[key] <= cap for key, cap in RUBRIC.items()),
                f"{episode}: invalid score range")
        require(sum(scores.values()) == reader["total"] and reader["total"] >= MINIMUM,
                f"{episode}: invalid total or blind reader below threshold")


def verify(root, batch="batch-001"):
    receipt = json.loads((root / "reviews.json").read_text(encoding="utf-8"))
    require(receipt["rubric"] == RUBRIC and receipt["minimum_each_reader"] == MINIMUM, "Changed scoring policy")
    records = receipt["episodes"]
    paths = {path.stem: path for path in (root / "episodes").glob("*.md")}
    expected = {f"WNL-{number:03d}" for number in BATCH_RANGES[batch]}
    require(set(records) == set(paths) == expected, f"{batch}: expected its ten script and review pairs")
    index = (root / "README.md").read_text(encoding="utf-8")
    mechanisms = set()
    for episode in sorted(records):
        record = records[episode]
        mechanism, cue_digest = verify_script(episode, paths[episode], record)
        require(mechanism not in mechanisms, f"{episode}: duplicated mechanism")
        mechanisms.add(mechanism)
        verify_reviews(episode, record, cue_digest)
        first, second = (reader["total"] for reader in record["readers"])
        line = next((line for line in index.splitlines() if f"(episodes/{episode}.md)" in line), "")
        require(f"| {first} | {second} |" in line, f"{episode}: missing or stale index scores")
    return len(records)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch", choices=BATCH_RANGES, default="batch-001")
    args = parser.parse_args()
    try:
        count = verify(HERE.parent / args.batch, args.batch)
    except (KeyError, OSError, TypeError, ValueError) as error:
        sys.exit(f"WhyNest Lab batch rejected: {error}")
    print(f"WhyNest Lab batch verified: {count} scripts, {count * 4} independent review summaries.")
