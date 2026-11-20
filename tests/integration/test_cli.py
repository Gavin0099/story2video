import json
import os
import subprocess

import pytest


@pytest.fixture
def s2v(tmp_path, monkeypatch):
    monkeypatch.delenv("S2V_DB_PATH", raising=False)

    def run(*args):
        return subprocess.run(
            ["s2v", *map(str, args)],
            cwd=tmp_path,
            env={**os.environ, "PYTHONUTF8": "1"},
            capture_output=True,
            encoding="utf-8",
            check=False,
        )

    return run


def result(call):
    assert call.returncode == 0, call.stderr
    return json.loads(call.stdout)


def test_console_script_init_register_and_status(s2v, valid_file, tmp_path):
    db = tmp_path / "db # store.sqlite3"
    assert not db.exists()
    assert result(s2v("--db", db, "init"))["database_version"] == 1
    assert result(s2v("--db", db, "status")) == []

    validated = result(s2v("validate", "--file", valid_file))
    assert validated["valid"] is True
    args = ("--db", db, "register", "--file", valid_file, "--actor", "reviewer")
    registered = result(s2v(*args))
    assert registered["state"] == "DRAFT"
    assert registered["input_hash"] == validated["input_hash"]
    assert result(s2v(*args)) == registered
    assert result(s2v("--db", db, "status", "--id", "puzzle-0001", "--revision", 1)) == [registered]
    missing = s2v("--db", db, "status", "--id", "missing")
    assert missing.returncode == 1
    assert "No matching episode" in missing.stderr


def test_cli_invalid_fixture_reports_failure(s2v, invalid_file):
    call = s2v("validate", "--file", invalid_file)
    assert call.returncode == 1
    assert not call.stdout
    assert "$.source.source_refs" in call.stderr


def test_config_file_and_overrides(s2v, tmp_path, monkeypatch):
    config = tmp_path / "config" / "settings.toml"
    config.parent.mkdir()
    config.write_text('[storage]\ndatabase = "data/config.sqlite3"\n', encoding="utf-8")
    assert result(s2v("--config", config, "init"))["database"] == str(config.parent / "data/config.sqlite3")
    env_path = tmp_path / "env.sqlite3"
    monkeypatch.setenv("S2V_DB_PATH", str(env_path))
    assert result(s2v("--config", config, "init"))["database"] == str(env_path)
    cli_path = tmp_path / "cli.sqlite3"
    assert result(s2v("--db", cli_path, "init"))["database"] == str(cli_path)


def test_init_default_and_revision_error(s2v, tmp_path):
    assert result(s2v("init"))["database"] == str(tmp_path / "artifacts/story2video.sqlite3")
    call = s2v("status", "--revision", 1)
    assert call.returncode == 1
    assert "requires an episode ID" in call.stderr
