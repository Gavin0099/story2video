"""Test the visual gate with synthetic images and no episode assets."""

import json
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path

from render_visual import plan_frames, render
from visual_poc import CRITERIA, Project, write_json


def tiny_png(path, intensity):
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

    pixels = (b"\x00" + bytes([intensity]) * 2) * 3
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", 2, 3, 8, 0, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(pixels))
        + chunk(b"IEND", b"")
    )


def build_project(root):
    write_json(root / "story.json", {
        "episode_id": "synthetic-example",
        "segments": [{"id": name} for name in ("hook", "clue", "reveal")],
    })
    relationship = {
        "id": "fixture-location", "subject": "mark", "relation": "below", "object": "shelf",
        "assets": ["master", "first", "hint", "answer", "layout"],
    }
    write_json(root / "scene-bible.json", {
        "story": "story.json", "episode_id": "synthetic-example",
        "reveal_segment": "reveal", "reveal_timing": "at_or_after_spoken_reveal",
        "visual_style": "Neutral fixture style.", "framing": "Portrait.",
        "facts": {"setting": "A library shelf."},
        "landmarks": {"mark": {"level": "lower"}, "shelf": {"level": "upper"}},
        "spatial_relationships": [relationship],
    })
    rows = []
    plan = (
        ("master", "reference", "hook", []),
        ("first", "shot", "hook", ["master"]),
        ("hint", "shot", "clue", ["master"]),
        ("answer", "shot", "reveal", ["hint"]),
        ("layout", "evidence", "reveal", ["master", "answer"]),
    )
    for asset, kind, segment, references in plan:
        rows.append({
            "id": asset, "kind": kind, "segment": segment, "file": f"{asset}.png",
            "references": [{"asset": ref, "role": "Reference fixture"} for ref in references],
            "facts": ["setting"], "brief": f"Render synthetic {asset}.", "attempts": [],
        })
    manifest = root / "shot-manifest.json"
    write_json(manifest, {"scene_bible": "scene-bible.json", "assets": rows})
    project = Project(root)
    hashes = {}
    for index, row in enumerate(project.rows):
        source = root / "fixture.png"
        tiny_png(source, index)
        capture = project.capture(row, source, "test fixture")
        checksum = capture["image"]["sha256"]
        hashes[row["id"]] = checksum
        row["review"] = {
            "status": "PASS", "sha256": checksum,
            "checks": {key: {"status": "PASS", "evidence": "Fixture"} for key in CRITERIA},
        }
    project.manifest["relationship_reviews"] = {
        relationship["id"]: {"status": "PASS", "evidence": "Fixture", "relationship": relationship,
                             "asset_hashes": hashes},
    }
    write_json(manifest, project.manifest)
    return Project(root)


class VisualPilotTest(unittest.TestCase):
    def setUp(self):
        directory = self.enterContext(tempfile.TemporaryDirectory())
        self.project = build_project(Path(directory))

    def assert_blocked(self, reason):
        result = self.project.gate()
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIsNone(result["render_input"])
        self.assertTrue(any(reason in failure for failure in result["failures"]), result)

    def test_gate_emits_ordered_shots_and_excludes_reference_images(self):
        result = self.project.gate()
        self.assertEqual(result["status"], "PASS")
        shots = result["render_input"]["shots"]
        self.assertEqual([item["id"] for item in shots], ["first", "hint", "answer"])
        self.assertEqual([item["stage"] for item in shots], ["before_reveal"] * 2 + ["reveal_or_later"])

    def test_unverified_layout_blocks_render_before_creating_output(self):
        self.project.manifest["relationship_reviews"]["fixture-location"]["status"] = "PENDING"
        self.assert_blocked("fixture-location")
        output = self.project.root / "blocked-output"
        with self.assertRaisesRegex(ValueError, "Visual QA blocked"):
            render(self.project, self.project.root / "no-audio", output)
        self.assertFalse(output.exists())

    def test_spoiler_blocks_gate(self):
        self.project.by_id["hint"]["review"]["checks"]["spoiler"]["status"] = "FAIL"
        self.assert_blocked("hint: spoiler")

    def test_missing_image_blocks_gate(self):
        self.project.by_id["first"]["attempts"][0]["path"] = "images/missing.png"
        self.assert_blocked("missing.png")

    def test_changed_image_invalidates_review_and_dependent_shot(self):
        hint = self.project.selection(self.project.by_id["hint"])
        tiny_png(self.project.local(hint["path"]), 255)
        self.assert_blocked("Image file or checksum changed: hint")
        self.assert_blocked("answer:")

    def test_changed_prompt_invalidates_attempt(self):
        self.project.by_id["first"]["brief"] += " Change framing."
        self.assert_blocked("first: generation context changed (prompt)")

    def test_changed_relationship_invalidates_review(self):
        self.project.relationships[0]["relation"] = "above"
        self.assert_blocked("fixture-location")

    def test_fresh_process_compiles_from_disk_and_follows_its_references(self):
        script = Path(__file__).with_name("visual_poc.py").resolve()
        result = subprocess.check_output([
            sys.executable, "-I", "-X", "utf8", str(script), "--root", str(self.project.root), "prepare", "answer",
        ], text=True, cwd=self.project.root)
        expected = self.project.prepare(self.project.by_id["answer"])
        self.assertEqual(json.loads(result), expected)
        self.assertIn("library shelf", expected["prompt"])
        self.assertEqual(expected["references"][0]["asset"], "hint")

    def test_reveal_waits_for_the_answer_and_rounds_up(self):
        assets = self.project.gate()["render_input"]
        timeline = {
            "reveal_ms": 1481, "duration_ms": 1800,
            "segments": [
                {"id": "hook", "audio_start_ms": 0},
                {"id": "clue", "audio_start_ms": 667},
                {"id": "reveal", "audio_start_ms": 1200, "audio_end_ms": 1481, "caption_start_ms": 1481},
            ],
        }
        frames, total = plan_frames(assets, timeline)
        self.assertEqual([shot["start_frame"] for shot in frames], [0, 21, 45])
        self.assertEqual(total, 54)
        timeline["reveal_ms"] = 1400
        with self.assertRaisesRegex(ValueError, "answer is spoken"):
            plan_frames(assets, timeline)


if __name__ == "__main__":
    unittest.main(verbosity=2)
