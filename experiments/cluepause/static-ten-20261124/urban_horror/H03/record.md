# H03 — The Woman with the Hammer production record

FICTION — original invented urban-horror candidate. Rights: pending_verification.
Git SHA: `aef24410f8b45c8651fd922343aeb52db11bfc75`. Working files are uncommitted. No publication authorization is implied.

## Story and rule
The opposite window shows this room shortly before events happen. It is a fixed glimpse of the future, not a portal or an attacker who can travel across the shaft.
A smoky silhouette raising a hammer looks like an intruder about to enter her room. She blocks the entrance to prevent that future.
The figure has a white wrap on the left wrist matching Lea; smoke is visible in the opening image, and the hammer is already on her own sill. The payoff changes the hammer from weapon to escape tool.

## Delivered files
Master: `artifacts/static-ten-20261124/urban_horror/h03-static-v1/h03-static-v1.mp4`
Duration: 36.000 s; SHA-256: `2cd17a849dffc5184769e11d5d18bffaa4470a24390c48f34fae8df9da9e7d85`.
EN sidecar: `artifacts/static-ten-20261124/urban_horror/h03-static-v1/h03-static-v1.en.srt`
Traditional Chinese sidecar: `artifacts/static-ten-20261124/urban_horror/h03-static-v1/h03-static-v1.zh-Hant.srt`
Silent storyboard: `artifacts/static-ten-20261124/urban_horror/h03-static-v1/silent-storyboard.jpg`; timestamped strips: `artifacts/static-ten-20261124/urban_horror/h03-static-v1/qa/shot-01-strip.jpg` through `shot-06-strip.jpg`.

## Shot table: silent intent versus decoded result
| Shot | Seconds | Narrative function | Silent intent | What the frames show |
|---|---|---|---|---|
| shot-01 | 0.0–5.5 | establish | Across a shaft, a smoky figure raises a hammer at a window; a matching hammer rests on the near sill. | Smoke, hammer silhouette and wrapped wrist are visible across the shaft; the same black-handled hammer is on the near sill. |
| shot-02 | 5.5–11.0 | clue | A close-up of the smoky future figure shows a white left wrist wrap that later matches Lea. | Single wrapped hand appears behind the opposite window after the correction. This removes the near-glass mirror reading, though palm anatomy appears to switch handedness. |
| shot-03 | 11.0–17.0 | reaction | She barricades her own exit because she reads the figure as an incoming threat. | Recognizable Lea braces a grey trunk against a cream doorway. Face, bun, sweater and wrist wrap match; the bolt is mostly outside portrait crop. |
| shot-04 | 17.0–23.0 | reaction | Smoke comes from above her blocked doorway; the barricade is now a danger. | Smoke visibly emerges at the vent over the barricaded door. Lea grips the same trunk. The silver sliding bolt differs from the brass barrel bolt in the corrected previous shot. |
| shot-05 | 23.0–28.5 | reveal | The smoky hammer figure is recognizably Lea, using her own hammer to escape her room. | Lea is recognizable behind smoky glass, holding the matching hammer and showing the wrist wrap: the supposed attacker is the protagonist seeking air. |
| shot-06 | 28.5–36.0 | reveal | Broken window gives her air; the hammer was an escape tool. | The glass is broken, Lea leans into fresh air and lowers the hammer. No wounds or flames are shown. Window pane proportions/subject scale drift from the opening. |

The initial SILENT STORYBOARD check was generated before ImageGen by build_inputs.py. Delivered story.md also records subsequent staging revisions; H04 initial inputs are preserved in the v1 input-archive. The core object-state event is visible; the precise supernatural rule still requires narration. This author review is not a blind silent-viewer test.

## Engineering QA
Pipeline validator: VALID. Final technical QA: all 10 checks true. 1080×1920, 30 fps, 1080 frames, H.264 High/yuv420p, AAC 48 kHz stereo, faststart, no embedded subtitle stream; complete decode succeeded.
Dense output: 162 decoded samples across six shots at 30/7 fps plus each final frame. All six timestamped strips were visually inspected for face, hair, clothing, prop geometry/state, set, crop and camera continuity.
Opening editorial question is visible only at 1.0–3.5 s. No burned narration captions or fiction labels. In-world text is limited to the declared evidence. Six measured narration WAVs and three synthesized nonverbal SFX are represented in both sidecars.
Caption alignment: measured trimmed source PCM, exact SRT-content comparison and bounds checks; no ASR/listening claim. Mix peak: -7.66 dBFS. Audio loudness/peak diagnostics are in commands.jsonl.
QA and hash evidence: `artifacts/static-ten-20261124/urban_horror/h03-static-v1/qa/report.json`, `artifacts/static-ten-20261124/urban_horror/h03-static-v1/qa/probe.json`, `artifacts/static-ten-20261124/urban_horror/h03-static-v1/timeline.json`, `artifacts/static-ten-20261124/urban_horror/h03-static-v1/manifest.json`.

## Continuity and story-logic findings
| Timestamps | Impact class | Observed finding |
|---|---|---|
| 5.500–10.967 | confusing | The corrected wrapped palm appears anatomically right-handed although the canonical wrap is left. This weakens the matching-wrist clue; no additional correction allowed after the single fix pass. |
| 11.000 → 17.000 | cosmetic | Door hardware changes from brass barrel bolt to silver sliding bolt between sheets. Both remain closed; the trunk continues to block the door. |
| 0.000 → 23.000–35.967 | confusing | Window pane proportions and protagonist scale differ between the distant opening and exterior payoff, weakening an exact visual match. |
| 11.000–16.967 | cosmetic | The close portrait extraction hides most of the bolt, though the trunk against the door is visible. |

No additional confirmed causal rule violation was identified in this author inspection. This is a limited observation, not proof of a passed story gate. All listed residual issues remain in the delivered master.

Independent review (2026-11-25), SHOULD-FIX for a future revision: correct the right-handed wrapped palm in the 5.500–10.967 s clue insert to match Lea's canonical left-wrist wrap. An exact identifying clue needs matching anatomy. Face/clothes and the later hammer/window sequence still identify Lea, so this does not independently block a private review copy. The retained insert was not changed here.

## Calls, corrections, encodes and wall time
Built-in ImageGen: 4 calls; one canonical sheet first, then two canonical-conditioned shot sheets and one shots-a correction.
Every completed call has a receipt in `artifacts/static-ten-20261124/urban_horror/h03-static-v1/images.jsonl`. Exported prompts and their hashes are in `artifacts/static-ten-20261124/urban_horror/h03-static-v1/prompts/`. Original generated sheets are retained in assets; no external paid TTS call. Image billed cost UNKNOWN; no invented dollar figure.
Six narration lines synthesized once with the existing local Kokoro model, voice af_heart, speed 1.08; trimmed PCM reused by all renders. Three local mathematical SFX WAVs (pulse/click/chime), no downloaded recordings.
Final render: 6 libx264 shot encodes + one stream-copy/AAC mux; 37.797 s. Cumulative production: 6 shot encodes, 37.797 s of render invocations.
Observed production wall span: 792.672 s, from 2026-11-24T15:38:56.456661+00:00 to 2026-11-24T15:52:09.128254+00:00. Boundary is initial story-file creation through final QA; includes queue time and other-story work, excludes initial repository reading. Do not sum overlapping story spans. See production-cost.json for the machine-readable cost record.
Fix passes: 1 before encoding. Initial shots-a.png produced a near-glass mirror reading in the wrist insert; shots-a-fix.png replaces it with a single distant palm. Original and correction both retained and logged (initial accepted receipt was later superseded). Remaining handedness/hardware/geometry issues were not looped.

## Acceptance and unverified scope
Story Quality Gate PENDING (no blind readers this round). Storyboard Quality Gate PENDING. Viewer Gate HUMAN_TEST_PENDING. Market acceptance NOT_TESTED; no retention, viewer preference, public data, or revenue evidence.
Not verified: human listening, EN/zh-Hant phone playback, independent silent comprehension, emotional effect, external originality and commercial-rights review. Technical QA cannot establish these.
Reproducible validation: `python -B experiments/cluepause/static-ten-20261124/urban_horror/job.py validate H03`. Production invocation: same entry point with `run H03`; existing master protection refuses overwriting, so a future rerender needs a new revision id.
Shared pipeline regression: `python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/urban_horror/pytest-cache --basetemp artifacts/static-ten-20261124/urban_horror/pytest-temp` → 33 passed. `git diff --check` → exit 0.
Root README installation/core/video commands were not run: no core/video changes, uv is absent from PATH, and rebuilding shared environments would violate the job-only write boundary. This is isolated pipeline/media engineering verification, not full core-engine acceptance.
No commit, push, upload, YouTube action or memory edit. Only the two authorized urban_horror trees were written.
