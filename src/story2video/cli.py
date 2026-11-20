import argparse
import json
import sqlite3
import sys
from pathlib import Path

from story2video.app.store import DATABASE_VERSION, EpisodeStore
from story2video.config import database_path
from story2video.domain.episode import EpisodeManifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="s2v", description="Manage local episode manifests.")
    parser.add_argument("--config", type=Path, help="Use this TOML file")
    parser.add_argument("--db", type=Path, help="Override the SQLite path")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="Initialize the local database")

    validate = commands.add_parser("validate", help="Check an Episode v1 manifest")
    validate.add_argument("--file", type=Path, required=True)

    register = commands.add_parser("register", help="Index a local manifest in DRAFT")
    register.add_argument("--file", type=Path, required=True)
    register.add_argument("--actor", required=True)

    status = commands.add_parser("status", help="List episodes and their stored states")
    status.add_argument("--id")
    status.add_argument("--revision", type=int)

    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            manifest = EpisodeManifest.read(args.file)
            result = {
                "valid": True,
                "episode_id": manifest.episode_id,
                "script_revision": manifest.script_revision,
                "input_hash": manifest.input_hash,
            }
        else:
            store = EpisodeStore(database_path(args.config, args.db))
            if args.command == "init":
                store.initialize()
                result = {"database": str(store.path), "database_version": DATABASE_VERSION}
            elif args.command == "register":
                result = store.register(args.file, actor=args.actor)
            else:
                result = store.status(args.id, args.revision)
                if args.id is not None and not result:
                    raise ValueError(f"No matching episode: {args.id}")
    except (OSError, ValueError, sqlite3.Error) as error:
        print(f"s2v: {error}", file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
