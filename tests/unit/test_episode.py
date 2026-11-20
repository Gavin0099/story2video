import hashlib

import pytest

from story2video.domain.episode import EpisodeManifest, episode_validator


def test_valid_fixture(valid_file):
    episode = EpisodeManifest.read(valid_file)
    assert episode.episode_id == "puzzle-0001"
    assert episode.schema_version == "1.0"
    assert episode.script_revision == 1
    assert episode.made_for_kids is None
    assert episode.input_hash == hashlib.sha256(valid_file.read_bytes()).hexdigest()


def test_invalid_fixture(invalid_file):
    with pytest.raises(ValueError, match=r"\$\.source\.source_refs"):
        EpisodeManifest.read(invalid_file)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("episode_id", "../puzzle"),
        ("episode_id", "puzzle-0001\n"),
        ("schema_version", "2.0"),
        ("script_revision", 0),
        ("script_revision", True),
        ("content_type", "news"),
        ("language", "en"),
        ("format", "landscape"),
        ("duration_target_sec", 29),
        ("duration_target_sec", 61),
        ("question", "  "),
        ("youtube", {"made_for_kids": False, "privacy_status": "public"}),
        ("extra", "unknown"),
    ],
)
def test_schema_rejects_invalid_fields(episode_data, field, value):
    episode_data[field] = value
    assert not episode_validator().is_valid(episode_data)


def test_schema_requires_a_revision_and_a_reveal(episode_data):
    del episode_data["script_revision"]
    episode_data["narration"].pop()
    errors = list(episode_validator().iter_errors(episode_data))
    assert {error.validator for error in errors} == {"required", "contains"}


def test_duplicate_narration_id_is_invalid(episode_data, write_episode):
    episode_data["narration"][1]["id"] = episode_data["narration"][0]["id"]
    with pytest.raises(ValueError, match="line IDs must be unique"):
        EpisodeManifest.read(write_episode(episode_data))


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        ('{"title":"A","title":"B"}', "Duplicate JSON key"),
        ('{"duration_target_sec":NaN}', "Invalid JSON constant"),
        ("{", "Expecting"),
    ],
)
def test_json_parser_rejects_ambiguous_or_malformed_input(tmp_path, raw, message):
    path = tmp_path / "episode.json"
    path.write_text(raw, encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        EpisodeManifest.read(path)
