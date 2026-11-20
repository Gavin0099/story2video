import argparse
import json
import subprocess
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
FRAMEWORK_PATH = Path("additional/ai-governance-framework")
RULE_ID = "story2video-episode-v1"


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the story2video external governance contract.")
    parser.add_argument("--framework-root", type=Path, default=PROJECT / FRAMEWORK_PATH)
    args = parser.parse_args()
    lock = json.loads((PROJECT / "governance" / "framework.lock.json").read_text(encoding="utf-8"))
    expected_sha = lock["adopted_commit"]
    gitlink = subprocess.check_output(
        ["git", "-C", str(PROJECT), "ls-files", "--stage", "--", FRAMEWORK_PATH.as_posix()],
        text=True,
    ).split()
    if gitlink[:3] != ["160000", expected_sha, "0"]:
        parser.error("Git submodule pin differs from governance/framework.lock.json")

    root = args.framework_root.resolve()
    if not (root / "governance_tools" / "domain_validator_loader.py").is_file():
        parser.error("framework unavailable; run git submodule update --init")
    git = ["git", "-C", str(root)]
    head = subprocess.check_output([*git, "rev-parse", "HEAD"], text=True).strip()
    if head != expected_sha:
        parser.error(f"expected framework {expected_sha}, found {head}")
    changes = subprocess.check_output([*git, "status", "--short"], text=True)
    if changes.strip():
        parser.error("use a clean framework checkout")

    sys.path.insert(0, str(root))
    from governance_tools.domain_contract_loader import load_domain_contract
    from governance_tools.domain_validator_loader import preflight_domain_validators, run_domain_validators

    contract_file = PROJECT / "contract.yaml"
    contract = load_domain_contract(contract_file)
    preflight = preflight_domain_validators(contract_file)
    if not contract or not all(item["exists"] for item in contract["documents"]):
        parser.error("contract or referenced documents are missing")
    if not preflight or not preflight["ok"] or preflight["count"] != 1:
        print(json.dumps(preflight, indent=2), file=sys.stderr)
        return 1

    fixtures = PROJECT / "tests" / "fixtures"
    outcomes = {}
    for name, checks, expected in [
        ("valid", {"episode_manifest": str(fixtures / "episode.valid.json")}, True),
        ("invalid", {"episode_manifest": str(fixtures / "episode.invalid.json")}, False),
        ("missing", {}, False),
    ]:
        results = run_domain_validators(
            contract_file=contract_file, payload={"checks": checks}, active_rule_ids=[RULE_ID]
        )
        passed = (
            len(results) == 1
            and not results[0].get("errors")
            and results[0]["ok"] is expected
            and (expected or bool(results[0]["violations"]))
        )
        outcomes[name] = {"passed": passed, "results": results}

    ok = all(item["passed"] for item in outcomes.values())
    print(json.dumps({"ok": ok, "framework_sha": head, "cases": outcomes}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
