import sqlite3
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from datetime import datetime, timedelta

import pytest

from story2video.app.store import DATABASE_VERSION, EpisodeStore
from story2video.domain.states import State


@pytest.fixture
def store(tmp_path):
    store = EpisodeStore(tmp_path / "nested" / "episode # store.sqlite3")
    store.initialize()
    return store


def advance(store, states):
    for expected, target in zip(states, states[1:]):
        store.transition(
            "puzzle-0001", 1, expected=expected, target=target, actor="reviewer",
            reason="manifest registered" if target == State.DRAFT else "test transition",
            assets=("artifacts/example.png",),
        )


TO_APPROVED = [
    State.DRAFT, State.VALIDATING, State.VALIDATED, State.ASSET_GENERATING,
    State.ASSET_READY, State.RENDERING, State.RENDERED, State.QA_RUNNING,
    State.QA_PASSED, State.AWAITING_APPROVAL, State.APPROVED,
]


def test_init_is_idempotent_and_versioned(store, valid_file):
    original = store.register(valid_file, actor="tester")
    store.initialize()
    assert store.status() == [original]
    with closing(sqlite3.connect(store.path)) as db:
        assert db.execute("PRAGMA user_version").fetchone()[0] == DATABASE_VERSION


def test_refuses_unknown_sqlite_version(store):
    with closing(sqlite3.connect(store.path)) as db:
        db.execute("PRAGMA user_version = 99")
    with pytest.raises(ValueError, match="Unsupported SQLite schema version 99"):
        store.initialize()
    with pytest.raises(ValueError, match="Unsupported SQLite schema version 99"):
        store.status()


def test_init_leaves_existing_unversioned_database_alone(tmp_path):
    path = tmp_path / "unrelated.sqlite"
    with closing(sqlite3.connect(path)) as db:
        db.execute("CREATE TABLE unrelated (id INTEGER)")
    with pytest.raises(ValueError, match="non-empty, unversioned"):
        EpisodeStore(path).initialize()
    with closing(sqlite3.connect(path)) as db:
        assert db.execute("SELECT name FROM sqlite_schema").fetchall() == [("unrelated",)]


def test_init_refuses_unrelated_database_with_matching_version(tmp_path):
    path = tmp_path / "unrelated.sqlite"
    with closing(sqlite3.connect(path)) as db:
        db.execute(f"PRAGMA user_version = {DATABASE_VERSION}")
    with pytest.raises(ValueError, match="does not belong to story2video"):
        EpisodeStore(path).initialize()


def test_missing_database_status_does_not_create_file(tmp_path):
    path = tmp_path / "missing.sqlite"
    with pytest.raises(FileNotFoundError, match="Run s2v init"):
        EpisodeStore(path).status()
    assert not path.exists()


def test_concurrent_duplicate_registrations_record_one_event(store, valid_file):
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(store.register, valid_file, actor="reviewer-1")
        second = pool.submit(store.register, valid_file, actor="reviewer-2")
        assert first.result() == second.result()
    assert len(store.events("puzzle-0001", 1)) == 1


def test_conflicting_content_requires_new_revision(store, valid_file, episode_data, write_episode):
    original = store.register(valid_file, actor="tester")
    episode_data["title"] = "修訂"
    with pytest.raises(ValueError, match="already has different content"):
        store.register(write_episode(episode_data), actor="tester")
    episode_data["script_revision"] = 2
    revision = store.register(write_episode(episode_data), actor="tester")
    assert store.status("puzzle-0001") == [original, revision]
    assert store.status("puzzle-0001", 2) == [revision]


def test_changed_manifest_cannot_advance_state(store, episode_data, write_episode):
    original = store.register(write_episode(episode_data), actor="tester")
    episode_data["title"] = "修訂"
    write_episode(episode_data)
    with pytest.raises(ValueError, match="Manifest changed"):
        advance(store, [State.DRAFT, State.VALIDATING])
    assert store.status() == [original]
    assert len(store.events("puzzle-0001", 1)) == 1


def test_invalid_input_is_not_stored(store, invalid_file):
    with pytest.raises(ValueError, match="Episode v1 validation failed"):
        store.register(invalid_file, actor="tester")
    assert store.status() == []


def test_transition_history_records_retry_and_draft_return(store, valid_file):
    original = store.register(valid_file, actor="author")
    advance(store, [State.DRAFT, State.VALIDATING, State.REJECTED, State.DRAFT])
    advance(store, TO_APPROVED[:4] + [State.FAILED_RETRYABLE])
    with pytest.raises(ValueError, match="Illegal state transition"):
        advance(store, [State.FAILED_RETRYABLE, State.RENDERING])
    advance(store, [State.FAILED_RETRYABLE, State.ASSET_GENERATING])
    with pytest.raises(ValueError, match="Expected state"):
        advance(store, [State.DRAFT, State.VALIDATING])

    events = store.events("puzzle-0001", 1)
    assert len(events) == 9
    assert events[0]["from_state"] is None
    assert events[0]["actor"] == "author"
    assert events[3]["from_state"] == State.REJECTED
    assert events[-1]["from_state"] == State.FAILED_RETRYABLE
    assert events[-1]["actor"] == "reviewer"
    assert events[-1]["reason"] == "test transition"
    assert events[-1]["assets"] == ["artifacts/example.png"]
    assert events[-1]["result"] == store.status()[0]["state"] == State.ASSET_GENERATING
    assert all(event["input_hash"] == original["input_hash"] for event in events)
    assert all(datetime.fromisoformat(event["timestamp"]).utcoffset() == timedelta(0) for event in events)


def test_state_and_audit_event_roll_back_together(store, valid_file):
    store.register(valid_file, actor="tester")
    with closing(sqlite3.connect(store.path)) as db:
        db.execute("""
            CREATE TRIGGER block_event BEFORE INSERT ON episode_events
            BEGIN SELECT RAISE(ABORT, 'simulated failure'); END
        """)
    with pytest.raises(sqlite3.IntegrityError, match="simulated failure"):
        advance(store, [State.DRAFT, State.VALIDATING])
    assert store.status()[0]["state"] == State.DRAFT
    assert len(store.events("puzzle-0001", 1)) == 1


def test_unknown_audience_blocks_private_upload_state(store, valid_file):
    store.register(valid_file, actor="tester")
    advance(store, TO_APPROVED)
    with pytest.raises(ValueError, match="made_for_kids must be set"):
        advance(store, [State.APPROVED, State.UPLOADING_PRIVATE])
    assert store.status()[0]["state"] == State.APPROVED


def test_private_upload_and_publish_approval_states_are_separate(store, episode_data, write_episode):
    episode_data["youtube"]["made_for_kids"] = False
    store.register(write_episode(episode_data), actor="tester")
    advance(store, TO_APPROVED + [State.UPLOADING_PRIVATE, State.UPLOADED_PRIVATE])
    with pytest.raises(ValueError, match="Illegal state transition"):
        advance(store, [State.UPLOADED_PRIVATE, State.PUBLISHED])
    advance(store, [State.UPLOADED_PRIVATE, State.PUBLISH_APPROVED, State.PUBLISHED, State.ANALYZED])
    assert store.status()[0]["state"] == State.ANALYZED
