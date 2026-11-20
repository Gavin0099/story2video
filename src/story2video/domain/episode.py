import hashlib
import json
from dataclasses import dataclass
from functools import cache
from importlib.resources import files
from pathlib import Path

from jsonschema import Draft202012Validator


@cache
def episode_validator() -> Draft202012Validator:
    schema_file = files("story2video").joinpath("schemas", "episode.v1.schema.json")
    schema = json.loads(schema_file.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"Duplicate JSON key: {key}")
        obj[key] = value
    return obj


def _reject_constant(value: str) -> None:
    raise ValueError(f"Invalid JSON constant: {value}")


@dataclass(frozen=True)
class EpisodeManifest:
    episode_id: str
    schema_version: str
    script_revision: int
    path: Path
    input_hash: str
    made_for_kids: bool | None

    @classmethod
    def read(cls, path: Path) -> "EpisodeManifest":
        path = path.resolve()
        raw = path.read_bytes()
        data = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
        errors = sorted(episode_validator().iter_errors(data), key=lambda e: e.json_path)
        if errors:
            details = "; ".join(f"{error.json_path}: {error.message}" for error in errors)
            raise ValueError(f"Episode v1 validation failed: {details}")

        line_ids = [line["id"] for line in data["narration"]]
        if len(set(line_ids)) != len(line_ids):
            raise ValueError("$.narration: line IDs must be unique")

        return cls(
            episode_id=data["episode_id"],
            schema_version=data["schema_version"],
            script_revision=int(data["script_revision"]),
            path=path,
            input_hash=hashlib.sha256(raw).hexdigest(),
            made_for_kids=data["youtube"]["made_for_kids"],
        )
