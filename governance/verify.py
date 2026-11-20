import argparse
import json
import subprocess
import sys
from pathlib import Path

FRAMEWORK_SHA = "b8a16828481e6b537c474d4e2e4be4d3e047e3e8"
PROJECT = Path(__file__).resolve().parents[1]
RULE_ID = "story2video-episode-v1"


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the story2video external governance contract.")
    parser.add_argument("--framework-root", type=Path, required=True)
    args = parser.parse_args()
    root = args.framework_root.resolve()
    git = ["git", "-C", str(root)]
    head = subprocess.check_output([*git, "rev-parse", "HEAD"], text=True).strip()
    if head != FRAMEWORK_SHA:
        parser.error(f"expected framework {FRAMEWORK_SHA}, found {head}")
    changes = subprocess.check_output(
        [*git, "status", "--short", "--", "governance_tools"], text=True
    )
    if changes.strip():
        parser.error("use a framework checkout with clean governance_tools")

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
