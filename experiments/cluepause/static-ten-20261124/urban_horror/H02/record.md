# H02 — The Smallest Mirror production record

FICTION — original invented urban-horror candidate. Rights: pending_verification.
Git SHA: `aef24410f8b45c8651fd922343aeb52db11bfc75`. Working files are uncommitted. No publication authorization is implied.

## Story and rule
When the lift doors close, the passenger behind the glass can cross through an uncovered reflection. The rule applies to reflections, not just the large wall mirror.
A loose white coat seems to be moving over the wall mirror; the plausible threat appears to remain behind that large mirror.
The same grey fingers press against glass; the phone is present from the first frame but initially lit. Its screen goes black only after the coat covers the large mirror.

## Delivered files
Master: `artifacts/static-ten-20261124/urban_horror/h02-static-v1/h02-static-v1.mp4`
Duration: 36.000 s; SHA-256: `13738ce313dc48e76f0f22dc050d713228e5d9c0d5ab8d54e82fc686f6258ebb`.
EN sidecar: `artifacts/static-ten-20261124/urban_horror/h02-static-v1/h02-static-v1.en.srt`
Traditional Chinese sidecar: `artifacts/static-ten-20261124/urban_horror/h02-static-v1/h02-static-v1.zh-Hant.srt`
Silent storyboard: `artifacts/static-ten-20261124/urban_horror/h02-static-v1/silent-storyboard.jpg`; timestamped strips: `artifacts/static-ten-20261124/urban_horror/h02-static-v1/qa/shot-01-strip.jpg` through `shot-06-strip.jpg`.

## Shot table: silent intent versus decoded result
| Shot | Seconds | Narrative function | Silent intent | What the frames show |
|---|---|---|---|---|
| shot-01 | 0.0–5.5 | establish | A lone woman faces a mirror containing an extra grey passenger; her lit phone is already in hand. | Extra grey figure is visible only in the oval mirror; Mira, white coat, green sweater and lit phone are clear. |
| shot-02 | 5.5–11.0 | clue | Grey fingers press from behind the wall mirror, identifying glass as the boundary. | Grey fingertips appear on the far side of the large mirror. They remain there throughout the camera move. |
| shot-03 | 11.0–17.0 | reaction | She holds the door button while starting to remove her white coat. | Mira looks alarmed, coat half removed, lit phone in hand. The door-open button is mostly lost in portrait extraction; pressing it is not demonstrated clearly. |
| shot-04 | 17.0–23.0 | clue | The white coat hides the large mirror; one raised fold suggests the threat is still there. | White coat covers the oval mirror; Mira now wears only the green sweater. Cloth creases are visible, but pressure underneath is not an independently clear event. |
| shot-05 | 23.0–28.5 | reaction | The phone screen goes black while the large mirror remains covered and the doors close. | Black phone screen and the still-covered large mirror are both visible. The doors closing are outside this tight framing. |
| shot-06 | 28.5–36.0 | reveal | Grey fingers physically emerge from the black phone; the covered mirror is no longer the apparent source. | Grey fingers occupy the phone screen while the large mirror remains covered. The depth cue is ambiguous: a viewer could still read this as an image/reflection rather than fingers entering real space. |

The initial SILENT STORYBOARD check was generated before ImageGen by build_inputs.py. Delivered story.md also records subsequent staging revisions; H04 initial inputs are preserved in the v1 input-archive. The core object-state event is visible; the precise supernatural rule still requires narration. This author review is not a blind silent-viewer test.

## Engineering QA
Pipeline validator: VALID. Final technical QA: all 10 checks true. 1080×1920, 30 fps, 1080 frames, H.264 High/yuv420p, AAC 48 kHz stereo, faststart, no embedded subtitle stream; complete decode succeeded.
Dense output: 162 decoded samples across six shots at 30/7 fps plus each final frame. All six timestamped strips were visually inspected for face, hair, clothing, prop geometry/state, set, crop and camera continuity.
Opening editorial question is visible only at 1.0–3.5 s. No burned narration captions or fiction labels. In-world text is limited to the declared evidence. Six measured narration WAVs and three synthesized nonverbal SFX are represented in both sidecars.
Caption alignment: measured trimmed source PCM, exact SRT-content comparison and bounds checks; no ASR/listening claim. Mix peak: -5.87 dBFS. Audio loudness/peak diagnostics are in commands.jsonl.
QA and hash evidence: `artifacts/static-ten-20261124/urban_horror/h02-static-v1/qa/report.json`, `artifacts/static-ten-20261124/urban_horror/h02-static-v1/qa/probe.json`, `artifacts/static-ten-20261124/urban_horror/h02-static-v1/timeline.json`, `artifacts/static-ten-20261124/urban_horror/h02-static-v1/manifest.json`.

## Continuity and story-logic findings
| Timestamps | Impact class | Observed finding |
|---|---|---|
| 11.000–16.967 | confusing | Door-open button/press is largely outside the portrait crop. The coat-removal reaction is visible, but the safe open-door state depends on narration. |
| 17.000–22.967 | confusing | Cloth creases do not clearly demonstrate something pushing underneath; threat location is suggested rather than shown. |
| 23.000–28.467 | confusing | Door closure is off-frame, so the rule trigger is carried by narration and edit timing. |
| 28.500–35.967 | confusing | Grey fingers on black glass have weak physical depth; the payoff could be interpreted as another reflection. Covered wall mirror and phone states remain coherent. |

No additional confirmed causal rule violation was identified in this author inspection. This is a limited observation, not proof of a passed story gate. All listed residual issues remain in the delivered master.

Independent review (2026-11-25), SHOULD-FIX for a future revision: show the door closing as the rule trigger, then show the fingers physically crossing the phone's reflection plane. The current images leave both events insufficiently explicit and narration carries the rule/payoff. This does not independently block a private review copy; no storyboard, input or master was changed here.

## Calls, corrections, encodes and wall time
Built-in ImageGen: 3 calls; one canonical sheet first, then two canonical-conditioned shot sheets.
Every completed call has a receipt in `artifacts/static-ten-20261124/urban_horror/h02-static-v1/images.jsonl`. Exported prompts and their hashes are in `artifacts/static-ten-20261124/urban_horror/h02-static-v1/prompts/`. Original generated sheets are retained in assets; no external paid TTS call. Image billed cost UNKNOWN; no invented dollar figure.
Six narration lines synthesized once with the existing local Kokoro model, voice af_heart, speed 1.08; trimmed PCM reused by all renders. Three local mathematical SFX WAVs (pulse/click/chime), no downloaded recordings.
Final render: 6 libx264 shot encodes + one stream-copy/AAC mux; 44.781 s. Cumulative production: 6 shot encodes, 44.781 s of render invocations.
Observed production wall span: 399.151 s, from 2026-11-24T15:38:56.429150+00:00 to 2026-11-24T15:45:35.579926+00:00. Boundary is initial story-file creation through final QA; includes queue time and other-story work, excludes initial repository reading. Do not sum overlapping story spans. See production-cost.json for the machine-readable cost record.
Fix passes: 0. Pre-generation staging removed hinted fingers from shot-05 so the phone mechanism is not shown before the payoff. Door/crossing ambiguities recorded above were left as review findings.

## Acceptance and unverified scope
Story Quality Gate PENDING (no blind readers this round). Storyboard Quality Gate PENDING. Viewer Gate HUMAN_TEST_PENDING. Market acceptance NOT_TESTED; no retention, viewer preference, public data, or revenue evidence.
Not verified: human listening, EN/zh-Hant phone playback, independent silent comprehension, emotional effect, external originality and commercial-rights review. Technical QA cannot establish these.
Reproducible validation: `python -B experiments/cluepause/static-ten-20261124/urban_horror/job.py validate H02`. Production invocation: same entry point with `run H02`; existing master protection refuses overwriting, so a future rerender needs a new revision id.
Shared pipeline regression: `python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/urban_horror/pytest-cache --basetemp artifacts/static-ten-20261124/urban_horror/pytest-temp` → 33 passed. `git diff --check` → exit 0.
Root README installation/core/video commands were not run: no core/video changes, uv is absent from PATH, and rebuilding shared environments would violate the job-only write boundary. This is isolated pipeline/media engineering verification, not full core-engine acceptance.
No commit, push, upload, YouTube action or memory edit. Only the two authorized urban_horror trees were written.
