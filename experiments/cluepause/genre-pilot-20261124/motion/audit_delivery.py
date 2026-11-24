"""Measure demo cue timing and bind final local delivery files. No service calls."""
import array
import argparse
import importlib.metadata
import math
import platform
from pathlib import Path
import sys
import wave

import hybrid_motion as hm


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--demo-root", type=Path, default=hm.OUTPUTS)
    cli.add_argument("--tools", type=Path, default=hm.HERE / "tools.lock.json")
    args = cli.parse_args()
    tools = hm.Tools(args.tools)
    root = hm.output_path(args.demo_root)
    audio_checks = {}
    for name, expected in (("latch", 2.3), ("hybrid-demo", 9.3)):
        target = root / (name + "-audio-check.wav")
        tools.run("ffmpeg", hm.ffargs()+["-i", root / (name+".mp4"), "-vn", "-ac", "1",
                    "-ar", "48000", "-c:a", "pcm_s16le", target], root)
        with wave.open(str(target), "rb") as stream:
            samples = array.array("h", stream.readframes(stream.getnframes()))
        onset = next(i for i, sample in enumerate(samples) if abs(sample) > 50) / 48000
        if abs(onset-expected) >= 1/30:
            raise ValueError("Sound cue moved by more than a frame")
        audio_checks[name] = dict(expected_cue_s=expected, measured_onset_s=onset,
            peak_dbfs=20*math.log10(max(map(abs, samples))/32768), human_listened=False)
    probe = hm.inspect(tools, root / "hybrid-demo.mp4", root, 330)
    audio = next(s for s in probe["streams"] if s["codec_type"] == "audio")
    assert (audio["codec_name"], audio["sample_rate"], audio["channels"]) == ("aac", "48000", 2)
    assert abs(float(probe["format"]["duration"]) - 11) < 1/30
    hm.save(root / "audio-verification.json", audio_checks)
    hm.save(root / "runtime.json", dict(python=sys.version, python_executable=sys.executable,
        python_sha256=hm.digest(sys.executable), pillow=importlib.metadata.version("Pillow"), platform=platform.platform()))
    code = list(p for p in hm.HERE.iterdir() if p.is_file())
    evidence = [p for p in root.rglob("*") if p.is_file() and p.name != "delivery-manifest.json"
                and not any(part.startswith("pytest-") for part in p.parts)]
    memory = [hm.REPO / "memory" / name for name in (
        "01_active_task.md", "02_workflow.md", "03_knowledge_base.md", "04_review_log.md")]
    checks = [hm.OUTPUTS / name for name in ("mutation-review/results.json", "pytest-final-review.log",
        "portable-review/verification.json", "configured-reference-review/verification.json")]
    checks += list((hm.OUTPUTS / "mutation-review").glob("*.log"))
    files = sorted(set(code + evidence + memory + [p for p in checks if p.is_file()]))
    hm.save(root / "delivery-manifest.json", dict(base_git_sha="5253512d18ad15e7a4e3c7f8e84615b0012b077d",
        branch="codex/cluepause-motion-layer-20261124", committed=False,
        note="Uncommitted review fixes on the committed original delivery; ImageGen originals are not reproducible from prompts alone.",
        files={str(p.relative_to(hm.REPO)): dict(bytes=p.stat().st_size, sha256=hm.digest(p)) for p in files}))
    print(f"PASS: 330-frame master, audio cue timing, final manifest ({len(files)} files)")


if __name__ == "__main__":
    main()
