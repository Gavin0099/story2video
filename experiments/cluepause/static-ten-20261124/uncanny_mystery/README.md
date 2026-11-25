# Uncanny mystery — static photographic pilots

Three local fictional candidates. Story Quality Gate **PENDING**; Storyboard Quality Gate **PENDING**; Viewer Gate **HUMAN_TEST_PENDING**. Rights **pending_verification**. Market acceptance **NOT_TESTED**. No blind readers or humans tested these MP4s. No release approval is implied.

Base Git SHA: `aef24410f8b45c8651fd922343aeb52db11bfc75`; branch `codex/cluepause-static-ten-20261124`. Files are uncommitted; this SHA is provenance for the base, not a claim that these new files are committed.

| ID | Title / MP4 (repository relative) | Duration | SHA-256 | ImageGen requests / generated bitmaps | Honest quality note |
| --- | --- | --- | --- | --- | --- |
| U01 | The Shoes That Stayed Wet - `artifacts/static-ten-20261124/uncanny_mystery/uncanny-u01-v2/uncanny-u01-v2.mp4` | 38 s | `146f6f92fa651d07818f9b4bddda5a2819db5919a7a1a9116e4194f2bdff06d4` | v2: 4 / 4; lifetime: 9 / 8 | REVIEWED: UPLOAD-OK private review copy, not uploaded yet; BLOCKING: none. Rear-route paper and attached side-wall leak repaired; clock disappearance and inherited mineral-ring/streak mismatch remain. Gates PENDING / PENDING / HUMAN_TEST_PENDING. |
| U02 | The Chair That Came to Breakfast — `artifacts/static-ten-20261124/uncanny_mystery/uncanny-u02-v1/uncanny-u02-v1.mp4` | 36 s | `621fef7371db356fb6c16ecfb85772158d2200e9bd8ac72896c51a5501e446e2` | 3 / 3 | Visible towing mechanism and broadly consistent references; tie origin is edge-cropped and final tie attachment is occluded. Human comprehension untested. |
| U03 | The Man in the Pantry Door - `artifacts/static-ten-20261124/uncanny_mystery/uncanny-u03-v2/uncanny-u03-v2.mp4` | 36.000 s | `4a912d85fd66d85dbd050a900dc1298c8f06b823752423e5c9b8f715c6c94b3e` | v2: 1 / 1; lifetime: 5 / 5 | FIX-CANDIDATE pending independent review, not uploaded. Flat low colander leaves beam; high head disappears, towel shoulders remain. Shot-08 clipping and early macro predictability remain. |

## U03 v2 local mechanism repair - 2026-11-25

Current U03 is **FIX-CANDIDATE pending independent review, not uploaded** at starting Git SHA `1e3c4f40c92eabfbe5cc66b54b777418e7a169f2`. Only shot-09 (30-33 s) has a new still, conditioned on its original plate and canonical references: colander flat below/outside beam, no high round head shadow, unchanged towel shoulders. Shot-10 then removes the towel. The full per-shot mechanism state/transition table and residuals are in [U03/record.md](U03/record.md); revision inputs and exact prompt/receipt are in `U03/revisions/v2/`. All v1 source/media bytes are preserved. New ImageGen calls **1**, corrections **0**, new TTS **0**; cost UNKNOWN. Lifetime U03 requests/bitmaps **5 / 5**. Counts and render statistics later in this README describe the original v1 deliveries.

Job validation VALID; full media QA 10/10 PASS; 33 pipeline tests passed in 0.54 s with U03-specific cache/basetemp; primary agent inspected all 10 dense strips / 164 samples at 4.286 fps and the silent storyboard. Nine encoded cuts, all seven WAVs, decoded audio, question plate and both SRTs equal v1. Render 44.172 s, 10 cut encodes, 36.000 s master. Verification/personal-path grep and git diff --check PASS; evidence `artifacts/static-ten-20261124/uncanny_mystery/uncanny-u03-v2/verification.json`. Question/narration/captions add no early answer; the inherited 18-second macro can still suggest projection before the 26-second reveal. Shot-08 head clipping, contour differences and human readability remain unverified. Story/Storyboard Gates PENDING; Viewer Gate HUMAN_TEST_PENDING; market NOT_TESTED. No independent review, upload, YouTube action, commit/push or memory edit.

## Isolation and local workarounds

`run_local.py` imports the shared pipeline read-only and reroutes OUTPUTS to `artifacts/static-ten-20261124/uncanny_mystery/`. It confines Python/TTS/temp/provider caches to this genre folder, uses Python `-B`, and supplies the whole canonical sheet as one attached reference image because ImageGen accepts at most five reference paths while the pipeline can export six cells. No shared file was changed. ImageGen itself uses its tool-managed default image output; every project asset was copied into the allowed genre tree.

The wrapper appends a tall-cell layout instruction before prompt hashing. U01’s initial reference used the stock prompt; its exact prompt is recovered and frozen by hash. Its six-reference tool rejection is counted conservatively as a request, even though it generated no image. U01’s correction has an archived initial payload and a separate written correction instruction. No automatic image client or unlogged API fallback was used.

Kokoro models and FFmpeg/ffprobe were read from an existing installation using external environment bindings. Model and executable hashes are verified by the shared pipeline. Per-line WAVs were generated once, copied into each story’s assets, and measured for render timing. `author.py` is the initial authoring helper: rerunning it would reset the measured input file bindings; do not run it over a finished delivery.

## Verification and acceptance boundaries

`python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/uncanny_mystery/cache/pytest --basetemp artifacts/static-ten-20261124/uncanny_mystery/tmp/pytest` → **33 passed in 0.70 s**. All three inputs were VALID before ImageGen. Each completed master has its own probe, dense frames, measured timeline, sidecars, silent export, input hashes, commands and cost record.

`python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/verify_delivery.py` checks all three masters, input/receipt/prompt hashes, exact sidecars, image budgets, pending gate states, Python syntax, authored whitespace and personal-path confinement. Final evidence: `artifacts/static-ten-20261124/uncanny_mystery/verification.json`. U01’s nine EN/zh-Hant source lines were retained verbatim. Main agent inspected all **32 dense strips / 506 sampled decoded frames**, plus the three silent exports. This is visual inspection by the producing agent, not a blind or human viewer test.

Final local renders: U01 **38 s**, 12 cut encodes, 70.469 s pipeline wall time; U02 **36 s**, 10 cut encodes, 46.141 s; U03 **36 s**, 10 cut encodes, 44.312 s. Total **12 ImageGen requests / 11 generated bitmaps**; U01 includes one request rejected by tool validation before generation. ImageGen cost remains UNKNOWN. One visual correction pass each for U01 and U03, none for U02; one master render per story. Defects remain documented rather than looped.

Root engine/Node/governance commands were not rerun: their code was unchanged, and installing dependencies or writing their shared environments would exceed the explicit genre-only write boundary. No framework update or state-changing Git command was run. Engineering checks and market acceptance are recorded separately; all story/storyboard/viewer gates retain the pending states above.

All authored and generated project files are confined to the two authorized genre directories. The existing source installation was used read-only for preinstalled models/tools. No personal absolute paths are stored in this delivery. See each `<id>/record.md` for defects and unverified scope.
