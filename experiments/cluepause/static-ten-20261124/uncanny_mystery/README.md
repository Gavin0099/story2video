# Uncanny mystery — static photographic pilots

Three local fictional candidates. Story Quality Gate **PENDING**; Storyboard Quality Gate **PENDING**; Viewer Gate **HUMAN_TEST_PENDING**. Rights **pending_verification**. Market acceptance **NOT_TESTED**. No blind readers or humans tested these MP4s. No release approval is implied.

Base Git SHA: `aef24410f8b45c8651fd922343aeb52db11bfc75`; branch `codex/cluepause-static-ten-20261124`. Files are uncommitted; this SHA is provenance for the base, not a claim that these new files are committed.

| ID | Title / MP4 (repository relative) | Duration | SHA-256 | ImageGen requests / generated bitmaps | Honest quality note |
| --- | --- | --- | --- | --- | --- |
| U01 | The Shoes That Stayed Wet — `artifacts/static-ten-20261124/uncanny_mystery/uncanny-u01-v1/uncanny-u01-v1.mp4` | 38 s | `e075afa52d9e4a6d687076c46f8b0919375785efcca2d57591b37ed61b12fb77` | 5 / 4 | Technically complete; unresolved paper-test and connector-state errors break the intended v3 visual logic. Not a qualified storyboard. |
| U02 | The Chair That Came to Breakfast — `artifacts/static-ten-20261124/uncanny_mystery/uncanny-u02-v1/uncanny-u02-v1.mp4` | 36 s | `621fef7371db356fb6c16ecfb85772158d2200e9bd8ac72896c51a5501e446e2` | 3 / 3 | Visible towing mechanism and broadly consistent references; tie origin is edge-cropped and final tie attachment is occluded. Human comprehension untested. |
| U03 | The Man in the Pantry Door — `artifacts/static-ten-20261124/uncanny_mystery/uncanny-u03-v1/uncanny-u03-v1.mp4` | 36 s | `674697a7b378700d69125078e9844f1bab1b1e020d746537d9e92f0ea409c78b` | 4 / 4 | Readable shadow split and stable character/props; a high head shadow persists after the colander is lowered, breaking projection logic. |

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
