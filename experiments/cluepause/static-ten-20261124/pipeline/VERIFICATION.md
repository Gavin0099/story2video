# Task 0 acceptance — 2026-11-24

The shared static pipeline renders independently of the motion module. It is
ready for separate genre jobs to supply stories, canonical references and shot
sheets. This delivery creates no production story or publication approval.

Base/worktree Git HEAD: `f21677f7a78d8e68fbb0c23fd12952640efda1fb`.
Branch: `codex/cluepause-static-ten-20261124`. All delivered files are uncommitted;
the SHA identifies the unchanged base, not a committed pipeline revision.
The smoke manifest also binds the Python implementation and input file hashes.

## Engineering acceptance

| Check / command from repository root | Observed result |
| --- | --- |
| `uv run --locked pytest -q` with the root README's default test selection and isolated cache/temp | 61 core tests passed |
| `python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/pipeline-pytest-cache --basetemp artifacts/static-ten-20261124/pipeline-test-temp` | 33 pipeline tests passed with local Python 3.12.10 |
| `uv run --locked pytest -q tests experiments/cluepause/static-ten-20261124/pipeline/tests -o cache_dir=artifacts/static-ten-20261124/final-pytest-cache --basetemp artifacts/static-ten-20261124/final-test-temp` | Final combined run: 94 passed in 6.17 s, Python 3.13.18 |
| `python -B experiments/cluepause/static-ten-20261124/pipeline/smoke.py --id synthetic-proof` | PASS with local Python 3.12.10, Pillow, pinned FFmpeg/ffprobe and local bilingual font; no ImageGen or TTS |
| `git diff --check` | PASS |
| `git diff --no-index --check -- NUL <file>` for every new pipeline file | PASS after normalizing delivered text to LF; includes files absent from ordinary unstaged diff |
| Personal-path grep over delivered text and generated static-ten text evidence | PASS; no user directories or actual absolute checkout/reference roots. JSON Schema URLs and synthetic invalid-path test strings are not personal paths |
| `git status --short` | Only the new `experiments/cluepause/static-ten-20261124/` tree is untracked |

The uv executable came from the existing read-only tool installation. Runs used
`UV_OFFLINE=1` and a checkout-local `UV_CACHE_DIR`; no dependency installation or
network access was needed. All writes stayed in this worktree. No `memory/*.md`,
engine source, `video/`, governance contract or framework version changed.

Latest synthetic outputs:
`artifacts/static-ten-20261124/synthetic-proof/`.

- Master: 8.0 s, 240 frames, 1080×1920, 30 fps, H.264 High/yuv420p,
  AAC 48 kHz stereo, faststart. Full decode passed and no subtitle stream exists.
- Master SHA-256: `d8bba90c5117f9925cc631f10c2373c05ae575d6af01938dca8925927a80920b`.
- EN and zh-Hant sidecars exactly match measured tone/SFX cue boundaries.
- Dense decoded strips sample every 7 frames (4.286 fps), including final frames.
- Independent question-boundary samples at frames 29/30/104/105 have
  0/12371/12416/0 bright text pixels. The interval is `[1.0,3.5)` across a cut.
- Silent storyboard contains the four isolated color cells with no question;
  a separate JSON list carries their intended narrative meanings.
- Cost: zero ImageGen calls, four H.264 encodes plus final stream-copy/AAC mux;
  measured pipeline wall time 6.187 s. Extra smoke pixel assertions run afterward.
- Validator tests cover missing functions/reveal/clue close-up/reference ids,
  cue bindings, crop/cell confinement, output locking/cache isolation, image
  budget receipts and measured audio/SFX truncation failures.

## Unverified and market acceptance

Real Kokoro synthesis was implemented using the prior model hashes, PCM trimming,
voice and natural speed approach, but was not invoked in this task. Real
ImageGen calls, image-conditioned generation quality, photographic reference
consistency, speech intelligibility, human listening, translated meaning, phone
readability, fairness, silent-story comprehension and attraction remain untested.
The synthetic smoke establishes renderer plumbing and machine format/timing;
solid-color cells do not establish narrative quality. Manual image call receipts
cannot detect calls made outside the documented workflow.

Market acceptance: **NOT_TESTED**. No upload, visibility change, YouTube access,
commit or push occurred. The existing motion module remains available but is not
a dependency. Node/Remotion and governance checks were not rerun because their
code/contracts were unchanged.
