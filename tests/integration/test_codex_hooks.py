"""Exercise the report-only prompt launchers without the framework or real prompts.

CODEX_HOOKS_CONFIG can select the complete replacement JSON when the sandbox
protects .codex/. Normal CI runs always load the repository's .codex/hooks.json.
"""

import base64
import copy
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import venv

import pytest


ROOT = Path(__file__).resolve().parents[2]
ADAPTER = Path(
    "additional/ai-governance-framework/runtime_hooks/adapters/codex/user_prompt_submit.py"
)
DIAGNOSTIC = b"Codex UserPromptSubmit adapter missing"
PROMPT = "synthetic-private-prompt-\u6e2c\u8a66".encode()
# Mixed line endings, NUL, invalid UTF-8, and every byte catch text conversions.
PAYLOAD = b'{"prompt":"' + PROMPT + b'"}\r\n\n\x00' + bytes(range(256)) * 512


@pytest.fixture(scope="module")
def config():
    original = json.loads((ROOT / ".codex/hooks.json").read_text(encoding="utf-8"))
    selected = Path(os.environ.get("CODEX_HOOKS_CONFIG", ROOT / ".codex/hooks.json"))
    intended = json.loads(selected.read_text(encoding="utf-8"))

    def without_launchers(value):
        result = copy.deepcopy(value)
        hook = result["hooks"]["UserPromptSubmit"][0]["hooks"][0]
        del hook["command"], hook["commandWindows"]
        return result

    # Snapshot of 9771f762's non-launcher configuration: no other hook entries.
    # This also checks the rest of UserPromptSubmit, including timeout 15.
    unchanged = {
        "hooks": {"UserPromptSubmit": [{"hooks": [{"type": "command", "timeout": 15}]}]}
    }
    assert without_launchers(original) == unchanged
    assert without_launchers(intended) == unchanged
    return intended


@pytest.fixture(scope="module")
def hook(config):
    return config["hooks"]["UserPromptSubmit"][0]["hooks"][0]


def test_windows_command_is_utf16le_encoded(hook):
    executable, no_profile, flag, encoded = hook["commandWindows"].split()
    assert (executable, no_profile, flag) == (
        "powershell", "-NoProfile", "-EncodedCommand"
    )
    raw = base64.b64decode(encoded, validate=True)
    script = raw.decode("utf-16le")
    assert script.encode("utf-16le") == raw
    assert "& $python $adapter --project-root $repo" in script
    assert script.index(".venv-ci\\Scripts\\python.exe") < script.index(
        ".venv\\Scripts\\python.exe"
    ) < script.index("Get-Command python")


@pytest.fixture
def git_repo(tmp_path):
    repo = tmp_path / "temporary repo with spaces"
    repo.mkdir()
    # Do not let a parent Git hook's environment redirect this disposable repo.
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    subprocess.run(
        ["git", "init", "--quiet", str(repo)], env=env,
        capture_output=True, check=True, timeout=15,
    )
    (repo / ".codex").mkdir()
    (repo / ".codex/hooks.json").write_text("{}", encoding="utf-8")
    return repo, env


@pytest.fixture(params=["posix", "windows"])
def launcher(request, git_repo, hook, tmp_path):
    repo, env = git_repo
    if request.param == "windows":
        if sys.platform != "win32":
            pytest.skip("Windows PowerShell launcher requires Windows")
        # Use a real local interpreter at the existing first-choice location.
        venv.EnvBuilder(with_pip=False).create(repo / ".venv-ci")
        command = hook["commandWindows"].split()
    else:
        shell = shutil.which("sh")
        assert shell, "POSIX launcher requires sh (Git for Windows supplies it)"
        # Keep production's python3 lookup; give it a fixture-local interpreter.
        bin_dir = tmp_path / "bin"
        bin_dir.mkdir()
        python3 = bin_dir / "python3"
        python3.write_text(
            "#!/bin/sh\nexec " + shlex.quote(Path(sys.executable).as_posix())
            + ' "$@"\n', encoding="utf-8", newline="\n",
        )
        python3.chmod(0o755)
        env["PATH"] = str(bin_dir) + os.pathsep + env["PATH"]
        command = [shell, "-c", hook["command"]]

    def run():
        result = subprocess.run(
            command, cwd=repo, env=env, input=PAYLOAD,
            capture_output=True, timeout=15, check=False,
        )
        assert result.returncode != 2, result.stderr
        assert result.stdout == b""
        assert PROMPT not in result.stderr
        assert b"synthetic-private-prompt" not in result.stderr
        return result

    return repo, run


def write_adapter(repo, status):
    adapter = repo / ADAPTER
    adapter.parent.mkdir(parents=True, exist_ok=True)
    adapter.write_text(
        "from pathlib import Path\nimport sys\n"
        "assert sys.argv[1] == '--project-root'\n"
        "root = Path(sys.argv[2])\n"
        "(root / 'received.bin').write_bytes(sys.stdin.buffer.read())\n"
        f"sys.exit({status})\n",
        encoding="utf-8",
    )


@pytest.mark.parametrize("framework_present", [False, True], ids=["no-framework", "no-adapter"])
def test_missing_adapter_is_non_blocking(launcher, framework_present):
    repo, run = launcher
    if framework_present:
        (repo / ADAPTER).parent.mkdir(parents=True)
    result = run()
    assert result.returncode == 1
    assert result.stderr.strip() == DIAGNOSTIC
    assert not (repo / "received.bin").exists()


@pytest.mark.parametrize("status", [0, 1, 2, 3, 17, 255])
def test_adapter_status_and_original_stdin(launcher, status):
    repo, run = launcher
    write_adapter(repo, status)
    result = run()
    assert result.returncode == (1 if status == 2 else status)
    assert result.stderr == b""
    assert (repo / "received.bin").read_bytes() == PAYLOAD


def test_missing_hook_config_keeps_existence_guard(launcher):
    repo, run = launcher
    write_adapter(repo, 0)
    (repo / ".codex/hooks.json").unlink()
    assert run().returncode == 1
    assert not (repo / "received.bin").exists()
