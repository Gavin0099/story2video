# Urban horror — static photographic batch

Three original fictional local videos, H02–H04. H01 was not reused. Rights pending_verification. English narration, separate English and Traditional Chinese SRTs, basic camera moves, local SFX, no character animation.
Story Quality Gate PENDING; Storyboard Quality Gate PENDING; Viewer Gate HUMAN_TEST_PENDING. Technical QA success is separate from story or market acceptance.

Independent review (2026-11-25): H02/H03 are **UPLOAD-CANDIDATE private**, review recommendations without upload authorization. H04 is **HOLD (not uploaded)**: its opening question discloses erasure failure before the false relief, an early outcome spoiler. Future revisions should correct H03's wrong-handed wrist clue and make H02's door closure and fingers crossing the phone plane explicit. No shots.json or master was changed by this records-only update.

| ID | Title | MP4 (repository-relative) | Duration | SHA-256 | ImageGen | Honest quality note |
|---|---|---|---|---|---|---|
| [H02](H02/record.md) | The Smallest Mirror | `artifacts/static-ten-20261124/urban_horror/h02-static-v1/h02-static-v1.mp4` | 36.000 s | `13738ce313dc48e76f0f22dc050d713228e5d9c0d5ab8d54e82fc686f6258ebb` | 3 | Clear mirror-to-phone state progression; crossing depth and off-frame door trigger remain ambiguous. |
| [H03](H03/record.md) | The Woman with the Hammer | `artifacts/static-ten-20261124/urban_horror/h03-static-v1/h03-static-v1.mp4` | 36.000 s | `2cd17a849dffc5184769e11d5d18bffaa4470a24390c48f34fae8df9da9e7d85` | 4 | Hammer re-explains the opening as escape; wrist handedness and window geometry remain inconsistent. |
| [H04](H04/record.md) | The Name Underneath | `artifacts/static-ten-20261124/urban_horror/h04-static-v2/h04-static-v2.mp4` | 36.000 s | `abc02c1c7fc46a136d1a75782691cf23b93ac4c36f254fa5b2e962ed08883a81` | 3 | HOLD: opening question "Why did erasing her name fail?" spoils failure before false relief at 17–23 s. Copy payoff remains readable; blue clue is small and final cheek is cropped. |

## Scope and provenance
Branch: codex/cluepause-static-ten-20261124. Git SHA: `aef24410f8b45c8651fd922343aeb52db11bfc75`. No state-changing git commands; no commit, push, upload, YouTube, or memory edits.
Owner authorization is the current request for three new urban_horror static photographic films. PLAN.md M0 limits were read; this is the explicitly authorized isolated content experiment, not an engine milestone expansion.
Read: shared pipeline README, genre gates, readers-v2/results-v2.md, and the v3 findings via a read-only `git -c safe.directory=... -C ... show` on the specified v3 branch. No configuration change was made. The v3 report still found the H01 trap predictable; these candidates use different rules and avoid replaying the same final explanation. Originality remains externally unverified.

## Local pipeline wrapper and operational limits
job.py imports the shared pipeline unchanged, then overrides OUTPUTS to the authorized urban_horror artifact subtree. This is required because the shared default places story ids directly under the batch root; no shared pipeline file was modified.
The existing read-only TTS environment has Kokoro/Pillow but lacks jsonschema. Inputs were validated with the normal Python, then audio mode used the existing TTS environment to synthesize six per-line WAVs per story. The normal Python rendered from those prerecorded trimmed WAVs. Both operations use shared pipeline functions. No package/environment installation or source-tree cache write was needed.
Image reference sheets sometimes arranged examples differently than requested. Registry canonical cell/crop bindings were corrected to actual visible character/prop/set regions before conditioned shot calls. Reference-call-01.json preserves the exact original prompt; images.jsonl retains its original prompt hash. The reference sheet itself was not altered.
The first H02 image receipt attempt correctly refused while the audio invocation owned the per-story lock. No lock was removed; logging was retried after synthesis finished. Every completed image call is now recorded exactly once per story revision (H04 v2 copies historical receipts, not new calls).
build_inputs.py records the initial pre-image draft and creates local Foley. It is not a safe rebuild command for delivered edits: rerunning it resets final shot/canonical bindings. Delivered story.md/shots.json/references.json are the final inputs. write_records.py only regenerates records from existing media.
All explicit caches/temp, including TTS, pytest and proposed uv cache location, are beneath the authorized urban_horror paths. Existing model/tool files were read only. Executable/model hashes were verified by the pipeline; local installation paths were supplied through environment variables and are not stored in written records.

## Verification
All three final inputs: VALID. All three final masters: all ten technical QA checks true; 1080×1920, 30 fps, 36.000 s, H.264 High/yuv420p, AAC 48 kHz stereo, separate EN/zh-Hant sidecars, faststart, complete decode. Each final master has 162 dense decoded samples inspected by the authoring agent, six source plates and a silent storyboard export.
Pipeline test command: `python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/urban_horror/pytest-cache --basetemp artifacts/static-ten-20261124/urban_horror/pytest-temp` → 33 passed in 0.64 s.
Delivery audit: `python -B experiments/cluepause/static-ten-20261124/urban_horror/audit_delivery.py` checks final input/master/image/prompt hashes, WAV formats, duration, sample counts, untracked-source whitespace and personal absolute paths in text; result retained in `artifacts/static-ten-20261124/urban_horror/delivery-audit.json`.
Per-story validate: `python -B experiments/cluepause/static-ten-20261124/urban_horror/job.py validate H02` (also H03/H04). Render: replace validate with run after supplying the environment bindings from the shared README. Existing masters are protected; use a new revision id for any new encode.
Root README uv/core/video acceptance was not run because this task modifies neither engine nor video source and may not rebuild shared state. uv was not present on PATH. No standalone smoke render was needed: real stories exercised the shared render/QA path. Story-level cost.json, production-cost.json, commands.jsonl, images.jsonl, manifest.json and qa/ retain evidence.
Unique image calls: 10. Unique local TTS line syntheses: 18. Cumulative shot encodes: 24 (includes preserved H04 v1); four final mux invocations. Image billing UNKNOWN, no dollar estimate. Per-story observed wall spans include shared queue time and must not be summed.

## Unverified acceptance
Human listening, physical phone playback, independent comprehension/emotional response, external originality/rights verification and all market evidence remain uncollected. Per-video records list residual continuity and visual-logic ambiguities with timestamps and impact classes. No quality gate is claimed passed.
