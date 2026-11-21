import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from uuid import uuid4

import autoloop as loop


ROOT = Path(__file__).resolve().parents[4]
V4 = ROOT / "experiments/shorts-story-review/blind-tests/10-v4.md"


def fixture():
    source = V4.read_text(encoding="utf-8")
    parts = [chunk.split("\n\n", 1)[1].split("\n### 讀者 D", 1)[0].strip()
             for chunk in source.split(" · 投遞的故事全文")[1:]]
    return {
        "story": "10", "version": "v4", "parent": "0fa371a1e3f087cc6fda72cdbb083f3d57e6ffb1",
        "first": parts[0], "second": parts[1], "reveal": parts[2],
        "english": "Regression metadata only. The staged prompts use the original Chinese v4 text.",
        "cores": {"父親的反應": "父親讓失手的孩子回到工桌旁。"},
        "hypothesis": "Regression fixture", "change": "Regression fixture",
        "belief_shift": "Regression fixture",
    }


def turn(prompt, reply):
    return {"prompt": prompt, "exit_code": 0, "events": [
        {"type": "thread.started", "thread_id": str(uuid4())},
        {"type": "code_mode_disabled"},
        {"type": "turn.started"},
        {"type": "item.completed", "item": {"type": "agent_message", "text": json.dumps(reply)}},
        {"type": "turn.completed"},
    ]}


def stages(draft, values, support, critical=(), protocol=loop.PROTOCOL):
    replies = (
        {"prior_exposure": False, "guess": "首猜", "evidence": "膠帶",
         "confidence": 70, "keep_reading": 4, "reason": "留下痕跡"},
        {"guess": "終猜", "evidence": "缺漆", "confidence": 89, "alternative": "玩車時碰到",
         "shifted_by": "木車", "keep_reading": 5, "want_to_see": "父親反應"},
        {"prior_exposure": False, "new_understanding": "留下孩子", "strongest_moment": "扶住車",
         "emotion": 4, "cores": [{"label": "父親的反應", "support": support, "reason": "矮凳"}],
         "scores": {key: {"value": value, "reason": "fixture"}
                    for key, value in zip(loop.WEIGHTS, values, strict=True)},
         "critical_issues": list(critical)},
    )
    return [turn(loop.prompt(part, draft, replies[:index], protocol), replies[index])
            for index, part in enumerate(loop.PARTS)]


class GateTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.draft = fixture()
        self.key = loop.draft_key(self.draft)
        self.sha = loop.digest(self.draft)
        self.ledger = {"protocol": loop.PROTOCOL, "drafts": {}, "attempts": [], "probes": [],
                       "runtime": loop.runtime_identity("0" * 64, "keyring"),
                       "base_git_sha": self.draft["parent"], "rubric_sha256": loop.rubric_digest(),
                       "reader_sha256": {}}
        probe = turn(loop.PROBE_INPUT.format(path=loop.CANARY_PLACEHOLDER), {"result": "NO_ACCESS"})
        self.ledger["probes"] = [loop.digest(probe)]
        loop.save(self.root / "probe-01.json", probe)
        loop.save(self.root / f"{self.key}.json", self.draft)
        self.attempts = loop.reserve(self.ledger, self.key, self.draft, self.sha, 3, [])
        for attempt in self.attempts:
            attempt["probe"] = 1

    def put(self, number, events):
        record = {"attempt": self.attempts[number - 1], "stages": events}
        loop.save(self.root / f"reader-{number:02d}.json", record)
        self.ledger["reader_sha256"][str(number)] = loop.digest(record)

    def report(self):
        return loop.verify(self.root, self.ledger)

    def fill(self, values=(5, 5, 5, 5, 5, 5), support="supported", critical=()):
        for number in range(1, 4):
            self.put(number, stages(self.draft, values, support, critical))

    def test_scratch_v4_regression(self):
        self.assertIn("小名", self.draft["second"])
        for number, scores in enumerate(((4, 4, 5, 4, 4, 5), (4, 4, 5, 5, 4, 5)), 1):
            self.put(number, stages(self.draft, scores, "partial"))
        rows = self.report()["versions"][self.key]["readers"]
        self.assertEqual([row.get("score") for row in rows], [86, 89, None])
        self.assertFalse(self.report()["qualified"])

    def test_exact_gate(self):
        self.fill((5, 4, 5, 5, 4, 5))  # 93
        self.put(2, stages(self.draft, (4, 4, 5, 5, 4, 5), "supported"))  # 89
        self.assertFalse(self.report()["qualified"])
        self.put(2, stages(self.draft, (4, 5, 4, 5, 4, 5), "supported"))  # 90
        self.assertEqual(self.report()["qualified"], [self.key])
        self.assertEqual(self.report()["versions"][self.key]["readers"][1]["score"], 90)

    def test_unsupported_core_and_critical_issue(self):
        for support, critical in [("partial", ()), ("unsupported", ()), ("supported", ("因果矛盾",))]:
            with self.subTest(support=support, critical=critical):
                self.fill(support=support, critical=critical)
                self.assertFalse(self.report()["qualified"])
        self.fill((5, 5, 5, 5, 1, 4))
        self.assertFalse(self.report()["qualified"])

    def test_leak_tool_and_malformed_reply(self):
        self.fill()
        for stage, detail in [
            (0, {"type": "item.started", "item": {"type": "mcp_tool_call"}}),
            (2, {"type": "item.completed", "item": {"type": "agent_message", "text": '{"score":100}'}}),
        ]:
            with self.subTest(stage=stage, detail=detail):
                evidence = stages(self.draft, (5,) * 6, "supported")
                evidence[stage]["events"].insert(-1, detail)
                self.put(2, evidence)
                self.assertFalse(self.report()["qualified"])
        evidence = stages(self.draft, (5,) * 6, "supported")
        evidence[0]["prompt"] += self.draft["reveal"]
        self.put(2, evidence)
        self.assertFalse(self.report()["qualified"])
        self.draft["first"] += self.draft["reveal"]
        with self.assertRaisesRegex(ValueError, "contains the reveal"):
            loop.draft_key(self.draft)

    def test_reused_runtime_and_changed_draft(self):
        self.fill()
        evidence = stages(self.draft, (5,) * 6, "supported")
        self.put(1, evidence)
        self.put(2, copy.deepcopy(evidence))
        with self.assertRaisesRegex(ValueError, "session reused"):
            self.report()
        self.draft["english"] += "x"
        loop.save(self.root / f"{self.key}.json", self.draft)
        with self.assertRaisesRegex(ValueError, "SHA mismatch"):
            self.report()

    def test_partial_reader_cannot_be_reused_and_sealed_files_cannot_be_modified(self):
        self.fill()
        evidence = stages(self.draft, (5,) * 6, "supported")
        self.put(1, evidence[:2])
        self.put(2, evidence)
        with self.assertRaisesRegex(ValueError, "session reused"):
            self.report()
        trial = self.root / "reader-02.json"
        changed = loop.read(trial)
        changed["stages"][0]["events"][0]["thread_id"] = str(uuid4())
        loop.save(trial, changed)
        with self.assertRaisesRegex(ValueError, "transcript SHA mismatch"):
            self.report()

    def test_exploration_never_counts_as_formal(self):
        self.attempts[0]["mode"] = "explore"
        self.fill()
        self.assertFalse(self.report()["qualified"])

    def test_original_protocol_replays_with_its_own_rubric(self):
        original = loop.LEGACY_PROTOCOL
        self.ledger["protocol"] = original
        self.ledger["rubric_sha256"] = loop.rubric_digest(original)
        for number in range(1, 4):
            self.put(number, stages(self.draft, (5,) * 6, "supported", protocol=original))
        self.assertEqual(self.report()["qualified"], [self.key])
        self.ledger["protocol"] = loop.PROTOCOL
        with self.assertRaisesRegex(ValueError, "rubric SHA mismatch"):
            self.report()
        self.ledger["rubric_sha256"] = loop.rubric_digest()
        self.assertFalse(self.report()["qualified"])

    def test_budget_caps_and_same_version_mutation(self):
        with self.assertRaisesRegex(ValueError, "version ID reused"):
            loop.reserve(self.ledger, self.key, self.draft, "changed", 1, [])
        with self.assertRaisesRegex(ValueError, "three valid"):
            loop.reserve(self.ledger, self.key, self.draft, self.sha, 1,
                         [{"score": 89, "mode": "formal"}] * 3)
        for story, version in [("10", "v5"), ("03", "v3"), ("07", "v3")]:
            draft = dict(self.draft, story=story, version=version)
            loop.reserve(self.ledger, loop.draft_key(draft), draft, loop.digest(draft), 1, [])
        with self.assertRaisesRegex(ValueError, "revision budget"):
            loop.reserve(self.ledger, "12-v1", dict(self.draft, story="12"), "hash", 1, [])
        with self.assertRaisesRegex(ValueError, "reader budget"):
            loop.reserve(dict(self.ledger, attempts=self.attempts * 4), self.key,
                         self.draft, self.sha, 1, [])

    def test_executable_byte_binding_and_child_environment(self):
        binary = self.root / "codex.exe"
        binary.write_bytes(b"test executable placeholder")
        sha = hashlib.sha256(binary.read_bytes()).hexdigest()

        def fake_runner(argv, **kwargs):
            self.assertEqual(argv[0], str(binary))
            self.assertIn("--ignore-user-config", argv)
            self.assertIn("--ephemeral", argv)
            self.assertEqual(list(Path(kwargs["cwd"]).iterdir()), [])
            self.assertEqual(kwargs["input"], "only visible text")
            self.assertFalse({"OPENAI_API_KEY", "CODEX_HOME", "CODEX_APP_TOOLS_PIPE_PATH"}
                             & kwargs["env"].keys())
            events = turn("canary", {"result": "NO_ACCESS"})["events"]
            events[1] = {"type": "item.completed",
                         "item": {"type": "error", "message": loop.TOOL_HOST_DISABLED}}
            events[-1]["usage"] = {}
            events[-2]["item"]["id"] = "item_1"
            return loop.subprocess.CompletedProcess(argv, 0, "\n".join(map(json.dumps, events)), "")

        with patch.dict(os.environ, {"OPENAI_API_KEY": "fixture", "CODEX_HOME": "fixture",
                                     "CODEX_APP_TOOLS_PIPE_PATH": "fixture"}):
            with patch.object(loop.subprocess, "run", side_effect=fake_runner) as called:
                with self.assertRaisesRegex(ValueError, "binary digest"):
                    loop.run_turn(binary, "0" * 64, "keyring", "probe", "only visible text")
                called.assert_not_called()
                result = loop.run_turn(binary, sha, "keyring", "probe", "only visible text")
                self.assertEqual(loop.result(result, "probe")[1]["result"], "NO_ACCESS")


if __name__ == "__main__":
    unittest.main()
