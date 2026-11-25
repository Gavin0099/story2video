# Puzzle static-still delivery — 2026-11-24 batch

Four complete local videos, finished across 2026-11-24/25 Asia/Taipei. English Kokoro narration, clean photographic masters with basic camera moves, synthetic foley, separate EN/zh-Hant sidecars. P01 retains v3 story and all eight narration lines; P02–P04 are original-fiction candidates using printing context, optical shadow and counterweight release mechanisms respectively.

All four pipeline technical reports report engineering PASS. This is file/timing acceptance. P01 and P04 retain material visual story-logic defects after their one allowed correction. Independent review reclassifies P03's wire-shadow disappearance outside the hand shadow as **breaks story logic**, contradicting the optical explanation. P01/P04 and historical P03 v1 are **HOLD (not uploaded)**; P03 v2 is **FIX-CANDIDATE pending independent review, not uploaded**; P02 is **UPLOAD-CANDIDATE private**, a review recommendation without upload authorization. P02/P03 also have documented clue/predictability limitations. All Story Quality Gates PENDING, all Storyboard Quality Gates PENDING, all Viewer Gates HUMAN_TEST_PENDING. Rights pending_verification. Market acceptance NOT_TESTED. No gate is claimed passed.

| Record | Title | MP4 path (repository-relative) | Duration s | SHA-256 | ImageGen invocations | Honest quality note |
| --- | --- | --- | --- | --- | --- | --- |
| [P01](P01/record.md) | The Thread Under the Scale | `artifacts/static-ten-20261124/puzzle/puzzle-p01-static-v1/puzzle-p01-static-v1.mp4` | 36 | `f806ed777997b2fc6e37d4e7a345b605cba2980ff55ad23491d6ebea82469a8e` | 5 (4 images) | Force-path discontinuity remains; heel/two-hand clues weakened by portrait crop. |
| [P02](P02/record.md) | The Blackened Message | `artifacts/static-ten-20261124/puzzle/puzzle-p02-static-v1/puzzle-p02-static-v1.mp4` | 39 | `7cae43e308ba383dcf62aa683151f95cc2186acf7d1674f3a8f844bdc4931865` | 4 (4 images) | Readable printed reveal; backwards-letter clue cropped and printing may be predictable. |
| [P03](P03/record.md) | The Crack That Crossed the Table | `artifacts/static-ten-20261124/puzzle/puzzle-p03-static-v2/puzzle-p03-static-v2.mp4` | 39 | `b30a0b8f62b29fabe83333152211f11e9b164d1902dd99815bbe0155d7a01f80` | 2 new (5 cumulative) | FIX-CANDIDATE pending independent review, not uploaded: whole-vase hand shade and portrait empty-table proof fixed; early answer clues remain. |
| [P04](P04/record.md) | The Rope He Refused to Pull | `artifacts/static-ten-20261124/puzzle/puzzle-p04-static-v1/puzzle-p04-static-v1.mp4` | 39 | `dae5314dea81cbb8c002c1e6fa247e34fd7de0768dc1d26d5d03da6100325bb4` | 4 (4 images) | High flag reveal present; left rope-tail geometry inconsistent and final bag cropped. |

Total: 16 tool invocations, 15 completed image sheets, 36 libx264 cuts, four final stream-copy/AAC muxes. P01 includes one rejected tool input with no generated image. P01/P02/P04 each used one visual correction pass; P03 used none. No quota failure occurred. Charges are UNKNOWN; no cost estimate represented as actual charges.

## Scope, isolation and shared-pipeline workarounds

Only this experiment puzzle folder and `artifacts/static-ten-20261124/puzzle/` were written by this job. No shared pipeline edits, state-changing Git commands, memory edits, commits, pushes, uploads or YouTube actions. The image service itself saves tool-managed generation outputs; selected assets were copied here immediately and all local caches/temp were redirected to puzzle artifacts. No personal absolute path is stored in authored records/configuration.

`run.py` imports the unchanged shared pipeline and changes OUTPUTS to the puzzle artifacts subtree. All Python runs use -B. TEMP/TMP, HF_HOME, XDG_CACHE_HOME, NUMBA_CACHE_DIR and UV_CACHE_DIR are confined there. It also loads the already-installed base Python schema dependencies, since render Python supplies Pillow/Kokoro but lacks jsonschema; the repo environment’s rpds extension targets a different Python ABI. No dependencies were installed and the read-only source checkout was not edited.

This adapter adds central-portrait crop instructions and explicit unused-cell instructions to exported prompts, because the first P02 sheet otherwise ignored cell assignments. It does not change rendering/validation/audio/QA algorithms. The model still did not reliably keep all mechanical evidence inside cover crops; records distinguish the intended framing from the decoded result.

Image tool input cap: five image paths. Six P01/P04 canonical cells are attached as one complete reference sheet, preserving all canonical visual information. P04’s reference came back as six scene studies rather than isolated objects; its canonical cell crops were remapped to the actual visible maker/flag/rig/bag/scissors/set before shot generation. This does not prove every generated rope state is consistent.

P02 audio rejected the 36 s plan before encoding. Its failure cost/manifest are preserved as `cost-timing-attempt1.json` and `manifest-timing-attempt1.json`. All seven PCM files were copied into P02 assets and reused. Final P02/P03/P04 durations are 39 s, P01 is 36 s. No speech was cut to fit.

`prepare.py` preserves the initial authoring plan and refuses to overwrite existing final inputs. Authoritative final inputs are each story.md/shots.json/references.json; do not regenerate them from the initial draft. `finalize.py` derives hashes, timings and records from existing media plus explicit frame observations; it does not generate media.

## Validation evidence and commands

Git base SHA: `aef24410f8b45c8651fd922343aeb52db11bfc75`; branch `codex/cluepause-static-ten-20261124`. Uncommitted content additions are not represented by that base SHA; manifest hashes bind exact story inputs and shared pipeline bytes. Each story was schema/cross-reference validated, rendered and fully decoded with the shared pipeline. Every decoded dense strip (36 shots total) and each silent storyboard was inspected by the primary agent. This is AI inspection, not independent/human approval.

Supply existing trusted installations as environment variables: S2V_RENDER_PYTHON, S2V_FFMPEG, S2V_FFPROBE, S2V_QUESTION_FONT, S2V_KOKORO_MODELS, S2V_GIT_SHA. No paths or credentials are embedded here. Read the shared pipeline README for hash-pinned binaries/model requirements.

```powershell
& $env:S2V_RENDER_PYTHON -B experiments/cluepause/static-ten-20261124/puzzle/run.py validate experiments/cluepause/static-ten-20261124/puzzle/P01
& $env:S2V_RENDER_PYTHON -B experiments/cluepause/static-ten-20261124/puzzle/run.py prompts experiments/cluepause/static-ten-20261124/puzzle/P01 --supports-images
& $env:S2V_RENDER_PYTHON -B experiments/cluepause/static-ten-20261124/puzzle/run.py run experiments/cluepause/static-ten-20261124/puzzle/P01
```

The same validate/run commands were executed for P02, P03 and P04. Run intentionally refuses to overwrite an existing master: choose a fresh revision for reproduction. Do not log another ImageGen receipt unless a call actually occurred.

Shared offline suite executed with bytecode disabled and test temporaries confined here:

```powershell
& $env:S2V_SCHEMA_PYTHON -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/puzzle/pytest-cache --basetemp artifacts/static-ten-20261124/puzzle/pytest-temp
```

Result: 33 passed in 0.51 s. `git diff --check -- experiments/cluepause/static-ten-20261124/puzzle` exited zero (new untracked content was separately scanned). Four concrete full media runs substitute for the synthetic smoke; no extra smoke output written outside scope. Full core engine `uv run --locked pytest`, npm install/typecheck and governance verify were not run because those code paths/contracts were not modified. No code from src/video/memory/governance was edited.

Per-output evidence includes master and sidecars, timeline.json, probe/report, every dense decoded sample, source silent storyboard, images.jsonl, prompts, assets/manifest hashes, commands.jsonl and cost.json. Engineering acceptance and market acceptance are recorded separately. Remaining work is independent story/storyboard review, human viewing/listening/phone checks, external rights clearance and any later owner-authorized revision/publication.

Final integrity evidence: `artifacts/static-ten-20261124/puzzle/delivery-audit.json` checks all four input/master/shared-pipeline hashes, all 16 exact historical prompt hashes, every generated image and reference attachment hash, P01's eight unchanged English lines, and absence of personal absolute paths in authored/output text. `call-prompts/` preserves every matched historical prompt, including rejected calls; `delivery.sha256` binds each master, sidecars, ledger, timeline and manifest. P01’s frozen source is [source-p01-v3.md](P01/source-p01-v3.md); the current work remains uncommitted as requested.

## P03 v2 revision — 2026-11-25

The current P03 row points to the separate v2 candidate. Historical totals and acceptance above describe the original four v1 deliveries. This revision adds 2 calls / 2 images (1 correction), 8 cut encodes and one mux; cumulative batch ImageGen is 18 calls / 17 images. v1 inputs/output remain unchanged. Current v2 inputs are `P03/revisions/v2/`; full checks, per-shot light/wire/hand/shadow/vase table, residuals and commands are in the P03 record. Gates remain PENDING / HUMAN_TEST_PENDING, market NOT_TESTED. No commit, push, upload, YouTube action or memory edit.
