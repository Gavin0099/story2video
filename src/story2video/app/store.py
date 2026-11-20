import json
import sqlite3
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path

from story2video.domain.episode import EpisodeManifest
from story2video.domain.states import State, require_transition

DATABASE_VERSION = 1
APPLICATION_ID = 0x53325631  # "S2V1"

CREATE_EPISODES = """
CREATE TABLE episodes (
    episode_id TEXT NOT NULL,
    script_revision INTEGER NOT NULL,
    schema_version TEXT NOT NULL,
    manifest_path TEXT NOT NULL,
    input_hash TEXT NOT NULL,
    state TEXT NOT NULL,
    PRIMARY KEY (episode_id, script_revision)
)
"""

CREATE_EVENTS = """
CREATE TABLE episode_events (
    event_id INTEGER PRIMARY KEY,
    episode_id TEXT NOT NULL,
    script_revision INTEGER NOT NULL,
    actor TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    input_hash TEXT NOT NULL,
    from_state TEXT,
    result TEXT NOT NULL,
    reason TEXT NOT NULL,
    assets_json TEXT NOT NULL,
    FOREIGN KEY (episode_id, script_revision)
        REFERENCES episodes (episode_id, script_revision)
)
"""


class EpisodeStore:
    def __init__(self, path: Path):
        self.path = path.resolve()

    def _connect(self, mode: str) -> sqlite3.Connection:
        if mode != "rwc" and not self.path.is_file():
            raise FileNotFoundError(f"Database not found: {self.path}. Run s2v init first.")
        db = sqlite3.connect(f"{self.path.as_uri()}?mode={mode}", uri=True)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys = ON")
        return db

    @staticmethod
    def _version(db: sqlite3.Connection) -> int:
        return db.execute("PRAGMA user_version").fetchone()[0]

    @classmethod
    def _require_version(cls, db: sqlite3.Connection) -> None:
        version = cls._version(db)
        if version != DATABASE_VERSION:
            raise ValueError(f"Unsupported SQLite schema version {version}; expected {DATABASE_VERSION}")
        if db.execute("PRAGMA application_id").fetchone()[0] != APPLICATION_ID:
            raise ValueError("SQLite database does not belong to story2video")

    def initialize(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect("rwc")) as db, db:
            db.execute("BEGIN IMMEDIATE")
            version = self._version(db)
            if version != 0:
                self._require_version(db)
                return
            if (
                db.execute("PRAGMA application_id").fetchone()[0] != 0
                or db.execute("SELECT 1 FROM sqlite_schema LIMIT 1").fetchone()
            ):
                raise ValueError("Refusing to initialize a non-empty, unversioned SQLite database")
            db.execute(CREATE_EPISODES)
            db.execute(CREATE_EVENTS)
            db.execute("CREATE INDEX episode_event_history ON episode_events (episode_id, script_revision)")
            db.execute(f"PRAGMA application_id = {APPLICATION_ID}")
            db.execute(f"PRAGMA user_version = {DATABASE_VERSION}")

    @staticmethod
    def _record_event(
        db: sqlite3.Connection,
        episode: sqlite3.Row,
        result: State,
        *,
        previous: State | None = None,
        actor: str,
        reason: str,
        assets: tuple[str, ...] = (),
    ) -> None:
        db.execute(
            """
            INSERT INTO episode_events (
                episode_id, script_revision, actor, timestamp, input_hash,
                from_state, result, reason, assets_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                episode["episode_id"], episode["script_revision"], actor,
                datetime.now(UTC).isoformat(), episode["input_hash"], previous,
                result, reason, json.dumps(assets),
            ),
        )

    @staticmethod
    def _find(db: sqlite3.Connection, episode_id: str, revision: int) -> sqlite3.Row | None:
        return db.execute(
            "SELECT * FROM episodes WHERE episode_id = ? AND script_revision = ?",
            (episode_id, revision),
        ).fetchone()

    def register(self, path: Path, *, actor: str) -> dict:
        if not actor.strip():
            raise ValueError("Actor is required")
        manifest = EpisodeManifest.read(path)
        episode_id, revision = manifest.episode_id, manifest.script_revision
        with closing(self._connect("rw")) as db, db:
            self._require_version(db)
            db.execute("BEGIN IMMEDIATE")
            existing = self._find(db, episode_id, revision)
            if existing is not None:
                if existing["input_hash"] != manifest.input_hash:
                    raise ValueError(f"{episode_id} revision {revision} already has different content")
                return dict(existing)

            episode = db.execute(
                """
                INSERT INTO episodes (
                    episode_id, script_revision, schema_version, manifest_path, input_hash, state
                ) VALUES (?, ?, ?, ?, ?, ?) RETURNING *
                """,
                (episode_id, revision, manifest.schema_version, str(manifest.path),
                 manifest.input_hash, State.DRAFT),
            ).fetchone()
            self._record_event(db, episode, State.DRAFT, actor=actor, reason="manifest registered")
            return dict(episode)

    def status(self, episode_id: str | None = None, revision: int | None = None) -> list[dict]:
        if revision is not None and episode_id is None:
            raise ValueError("A script revision requires an episode ID")
        with closing(self._connect("ro")) as db:
            self._require_version(db)
            if revision is not None:
                row = self._find(db, episode_id, revision)
                return [dict(row)] if row else []
            if episode_id is not None:
                rows = db.execute(
                    "SELECT * FROM episodes WHERE episode_id = ? ORDER BY script_revision",
                    (episode_id,),
                )
            else:
                rows = db.execute("SELECT * FROM episodes ORDER BY episode_id, script_revision")
            return [dict(row) for row in rows]

    def events(self, episode_id: str, revision: int) -> list[dict]:
        with closing(self._connect("ro")) as db:
            self._require_version(db)
            rows = db.execute(
                """
                SELECT * FROM episode_events
                WHERE episode_id = ? AND script_revision = ? ORDER BY event_id
                """,
                (episode_id, revision),
            )
            events = []
            for row in rows:
                event = dict(row)
                event["assets"] = json.loads(event.pop("assets_json"))
                events.append(event)
            return events

    def transition(
        self,
        episode_id: str,
        revision: int,
        *,
        expected: State,
        target: State,
        actor: str,
        reason: str,
        assets: tuple[str, ...] = (),
    ) -> dict:
        if not actor.strip() or not reason.strip():
            raise ValueError("Actor and reason are required")
        with closing(self._connect("rw")) as db, db:
            self._require_version(db)
            db.execute("BEGIN IMMEDIATE")
            episode = self._find(db, episode_id, revision)
            if episode is None:
                raise ValueError(f"Unknown episode: {episode_id} revision {revision}")

            current = State(episode["state"])
            if current != expected:
                raise ValueError(f"Expected state {expected}; found {current}")
            failed_stage = None
            if current == State.FAILED_RETRYABLE:
                last_event = db.execute(
                    """
                    SELECT from_state FROM episode_events
                    WHERE episode_id = ? AND script_revision = ?
                    ORDER BY event_id DESC LIMIT 1
                    """,
                    (episode_id, revision),
                ).fetchone()
                failed_stage = State(last_event["from_state"])
            require_transition(current, target, failed_stage=failed_stage)

            manifest = EpisodeManifest.read(Path(episode["manifest_path"]))
            if manifest.input_hash != episode["input_hash"]:
                raise ValueError(f"Manifest changed for {episode_id} revision {revision}; use a new revision")
            if target == State.UPLOADING_PRIVATE and manifest.made_for_kids is None:
                raise ValueError("made_for_kids must be set before entering UPLOADING_PRIVATE")

            updated = db.execute(
                "UPDATE episodes SET state = ? WHERE episode_id = ? AND script_revision = ? RETURNING *",
                (target, episode_id, revision),
            ).fetchone()
            self._record_event(
                db, episode, target, previous=current, actor=actor, reason=reason, assets=assets
            )
            return dict(updated)
