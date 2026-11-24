"""Write private allocation under ignored artifacts; print only its commitment.

Slots are empty study places, never participant data. Supply a fresh secret seed.
Publish the dated hash before viewing; reveal the file and seed after answers lock.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import random


REPO = Path(__file__).resolve().parents[4]
ARTIFACTS = (REPO / "artifacts").resolve()
PRIVATE = ARTIFACTS / "genre-pilot-20261124" / "h01-viewer-gate-private"


def allocation(n, seed):
    rng = random.Random(seed)
    cuts = ["STILL"] * (n // 2) + ["MOTION"] * (n // 2)
    if n % 2:
        cuts.append(rng.choice(["STILL", "MOTION"]))
    rng.shuffle(cuts)
    # Never reuse a public code key. Both labels have the same neutral format.
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    labels = set()
    codes = {}
    for cut in ("STILL", "MOTION"):
        while True:
            label = "".join(rng.choice(alphabet) for _ in range(6))
            if label not in labels:
                break
        labels.add(label)
        codes[cut] = label
    return {
        "schema_version": 1,
        "algorithm": "python-random-v2-balanced-shuffle-then-codes-v1",
        "python_version": platform.python_version(),
        "seed": seed,
        "planned_n": n,
        "code_key": {code: cut for cut, code in codes.items()},
        "slots": [{"slot": f"S{i:02d}", "playback_code": codes[cut],
                   "host_cut": cut} for i, cut in enumerate(cuts, 1)],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, choices=range(8, 13), default=10)
    seeds = parser.add_mutually_exclusive_group(required=True)
    seeds.add_argument("--seed", help="host-supplied secret; prefer --seed-file")
    seeds.add_argument("--seed-file", type=Path, help="private UTF-8 seed file")
    parser.add_argument("--output", type=Path, default=PRIVATE / "assignment-plan.json",
                        help="new file under artifacts/.../h01-viewer-gate-private/")
    args = parser.parse_args()
    output = args.output.resolve()
    # Resolve junctions/symlinks before checking to prevent escape.
    if not PRIVATE.resolve().is_relative_to(ARTIFACTS) or not output.is_relative_to(PRIVATE.resolve()):
        parser.error("output must stay inside the private artifacts directory")
    # Fail if this repository's storage ignore boundary is removed.
    if "/artifacts/" not in (REPO / ".gitignore").read_text(encoding="utf-8").splitlines():
        parser.error("the repository /artifacts/ ignore rule is missing")
    try:
        seed = args.seed
        if args.seed_file is not None:
            seed_file = args.seed_file.resolve()
            if seed_file.is_relative_to(REPO) and not seed_file.is_relative_to(ARTIFACTS):
                parser.error("seed files inside the repository must be under artifacts/")
            seed = seed_file.read_text(encoding="utf-8").strip()
        if not seed or not seed.strip():
            parser.error("a nonempty private seed is required")
        payload = (json.dumps(allocation(args.n, seed), ensure_ascii=True, indent=2)
                   + "\n").encode("utf-8")
        output.parent.mkdir(parents=True, exist_ok=True)
        # Preserve any previously committed allocation; never overwrite it.
        with output.open("xb") as stream:
            stream.write(payload)
    except (OSError, UnicodeError):
        parser.error("could not read the private seed or create a NEW private allocation file")
    print(f"SHA-256 commitment: {hashlib.sha256(payload).hexdigest()}")


if __name__ == "__main__":
    main()
