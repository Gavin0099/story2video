"""Prepare reference-backed prompts and gate locally reviewed visual assets."""

import argparse
import hashlib
import json
import shutil
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path

CRITERIA = ("story_beat", "continuity", "spoiler", "portrait_framing")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    temp = path.with_suffix(".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def digest(path):
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def image_details(path):
    with path.open("rb") as source:
        header = source.read(24)
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"Expected a PNG image: {path.name}")
    width, height = struct.unpack(">II", header[16:24])
    if width <= 0 or width >= height:
        raise ValueError(f"Expected a portrait image: {path.name}")
    return {"width": width, "height": height, "sha256": digest(path)}


class Project:
    def __init__(self, root):
        self.root = root.resolve()
        self.manifest_path = self.local("shot-manifest.json")
        self.manifest = read_json(self.manifest_path)
        self.bible = read_json(self.local(self.manifest["scene_bible"]))
        self.story_path = self.local(self.bible["story"])
        self.story = read_json(self.story_path)
        self.rows = self.manifest["assets"]
        self.by_id = {asset["id"]: asset for asset in self.rows}
        self.order = [segment["id"] for segment in self.story["segments"]]
        if self.story["episode_id"] != self.bible["episode_id"]:
            raise ValueError("The scene bible and story refer to different episodes")
        if len(self.by_id) != len(self.rows) or len(set(self.order)) != len(self.order):
            raise ValueError("Duplicate asset or segment ID")
        if len({row["file"] for row in self.rows}) != len(self.rows):
            raise ValueError("Duplicate image filename")
        self.relationships = self.bible["spatial_relationships"]
        landmarks = self.bible["landmarks"]
        if len({item["id"] for item in self.relationships}) != len(self.relationships):
            raise ValueError("Duplicate spatial relationship ID")
        if not self.relationships or any(
            item["subject"] not in landmarks or item["object"] not in landmarks
            or not item["assets"] or any(asset not in self.by_id for asset in item["assets"])
            for item in self.relationships
        ):
            raise ValueError("Spatial relationships must name valid landmarks and evidence assets")
        masters = [row for row in self.rows if row["kind"] == "reference"]
        if len(masters) != 1 or masters[0] is not self.rows[0] or masters[0]["references"]:
            raise ValueError("Exactly one unreferenced master must begin the manifest")
        shots = [row for row in self.rows if row["kind"] == "shot"]
        reveal_at = self.order.index(self.bible["reveal_segment"])
        shot_order = [self.order.index(row["segment"]) for row in shots]
        if shot_order != sorted(set(shot_order)) or not shot_order or reveal_at not in shot_order:
            raise ValueError("Shot segments must be unique, in story order, and include the reveal")
        seen = set()
        for row in self.rows:
            if row["kind"] not in {"reference", "shot", "evidence"}:
                raise ValueError(f"Unknown asset kind: {row['kind']}")
            refs = [ref["asset"] for ref in row["references"]]
            if any(ref not in seen for ref in refs) or (row["kind"] != "reference" and not refs):
                raise ValueError(f"References must point to earlier assets: {row['id']}")
            if self.stage(row) == "before_reveal" and any(
                self.stage(self.by_id[ref]) != "before_reveal" for ref in refs
            ):
                raise ValueError(f"A pre-reveal asset cannot use a reveal reference: {row['id']}")
            seen.add(row["id"])

    def local(self, relative):
        path = (self.root / relative).resolve()
        if not path.is_relative_to(self.root):
            raise ValueError(f"Path leaves the proof of concept: {relative}")
        return path

    def stage(self, row):
        if self.order.index(row["segment"]) < self.order.index(self.bible["reveal_segment"]):
            return "before_reveal"
        return "reveal_or_later"

    def selection(self, row):
        number = row.get("selected_attempt")
        attempt = next((entry for entry in row["attempts"] if entry["number"] == number), None)
        if attempt is None:
            raise ValueError(f"No image selected: {row['id']}")
        if image_details(self.local(attempt["path"])) != attempt["image"]:
            raise ValueError(f"Image file or checksum changed: {row['id']}")
        return attempt

    def prepare(self, row):
        refs = []
        for position, ref in enumerate(row["references"], start=1):
            selected = self.selection(self.by_id[ref["asset"]])
            refs.append({
                **ref,
                "position": position,
                "path": selected["path"],
                "sha256": selected["image"]["sha256"],
            })
        lines = ["Use case: photorealistic-natural. Asset: production still for a vertical mystery short."]
        if refs:
            lines.extend(f"Image {ref['position']}: {ref['role']}." for ref in refs)
        lines.extend([self.bible["visual_style"], self.bible["framing"]])
        lines.extend(self.bible["facts"][fact] for fact in row["facts"])
        lines.append(row["brief"])
        prompt = "\n".join(lines)
        return {
            "asset": row["id"],
            "segment": row["segment"],
            "stage": self.stage(row),
            "story_sha256": digest(self.story_path),
            "prompt": prompt,
            "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            "references": refs,
        }

    def capture(self, row, source, provider):
        source_image = image_details(source)
        prepared = self.prepare(row)
        number = len(row["attempts"]) + 1
        name = Path(row["file"]).stem
        path = self.local(f"images/{name}-v{number}.png")
        path.parent.mkdir(exist_ok=True)
        if path.exists():
            raise ValueError(f"The next version already exists: {path.name}")
        shutil.copyfile(source, path)
        row["attempts"].append({
            "number": number,
            **prepared,
            "path": path.relative_to(self.root).as_posix(),
            "image": source_image,
            "provider": provider,
            "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
            "generation_parameters": {
                "requested_frame": "9:16-safe portrait",
                "transparent_background": False,
                "model": None,
                "seed": None,
                "quality": None,
            },
        })
        row["selected_attempt"] = number
        row["review"] = {"status": "PENDING"}
        write_json(self.manifest_path, self.manifest)
        return row["attempts"][-1]

    def gate(self):
        failures = []
        render_shots = []
        checksums = {}
        for row in self.rows:
            asset_id = row["id"]
            try:
                active = self.selection(row)
                for key, value in self.prepare(row).items():
                    if active.get(key) != value:
                        failures.append(f"{asset_id}: generation context changed ({key})")
            except (OSError, ValueError) as error:
                failures.append(f"{asset_id}: {error}")
                continue
            review = row["review"]
            checksums[asset_id] = active["image"]["sha256"]
            if review.get("status") != "PASS" or review.get("sha256") != active["image"]["sha256"]:
                failures.append(f"{asset_id}: current image lacks a passing review")
            checks = review.get("checks", {})
            for key in CRITERIA:
                check = checks.get(key, {})
                if check.get("status") != "PASS" or not check.get("evidence", "").strip():
                    failures.append(f"{asset_id}: {key} did not pass with evidence")
            if row["kind"] == "shot":
                render_shots.append({
                    "id": asset_id,
                    "file": active["path"],
                    "segment": row["segment"],
                    "stage": self.stage(row),
                    "sha256": active["image"]["sha256"],
                })
        relationship_reviews = self.manifest.get("relationship_reviews", {})
        for relationship in self.relationships:
            name = relationship["id"]
            review = relationship_reviews.get(name, {})
            expected = {asset: checksums.get(asset) for asset in relationship["assets"]}
            if (None in expected.values() or review.get("status") != "PASS"
                    or not review.get("evidence", "").strip()
                    or review.get("asset_hashes") != expected
                    or review.get("relationship") != relationship):
                failures.append(f"{name}: spatial relationship lacks passing evidence for current assets")
        return {
            "status": "BLOCKED" if failures else "PASS",
            "failures": failures,
            "render_input": None if failures else {
                "story_sha256": digest(self.story_path),
                "reveal_segment": self.bible["reveal_segment"],
                "reveal_timing": self.bible["reveal_timing"],
                "shots": render_shots,
            },
        }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Local directory containing the story and visual manifests")
    sub = parser.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("asset")
    capture = sub.add_parser("capture")
    capture.add_argument("asset")
    capture.add_argument("source", type=Path)
    capture.add_argument("--provider", default="codex-image_gen")
    sub.add_parser("check")
    args = parser.parse_args()
    try:
        project = Project(args.root)
        if args.command == "prepare":
            result = project.prepare(project.by_id[args.asset])
        elif args.command == "capture":
            result = project.capture(project.by_id[args.asset], args.source, args.provider)
        else:
            result = project.gate()
    except (KeyError, OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return int(result.get("status") == "BLOCKED")


if __name__ == "__main__":
    raise SystemExit(main())
