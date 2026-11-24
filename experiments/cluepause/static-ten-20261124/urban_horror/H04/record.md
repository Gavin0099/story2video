# H04 — The Name Underneath production record

FICTION — original invented urban-horror candidate. Rights: pending_verification.
Git SHA: `aef24410f8b45c8651fd922343aeb52db11bfc75`. Working files are uncommitted. No publication authorization is implied.

Status: **HOLD (not uploaded)**. Independent review on 2026-11-25 identified a blocking early outcome disclosure (spoiler) in the retained opening question.

## Story and rule
At midnight the house visitor comes for every name left in the guestbook. Marks copied onto a bound duplicate page are still names in that same book.
Eva believes the pencil entry is the only entry and the shape outside is the night porter; erasing the visible name appears sufficient.
A blue copying sheet corner is visible below the writing page from the first close-up. Pencil pressure leaves a second entry; erasing the surface does not remove it. No warning text explains this before payoff.

## Delivered files
Master: `artifacts/static-ten-20261124/urban_horror/h04-static-v2/h04-static-v2.mp4`
Duration: 36.000 s; SHA-256: `abc02c1c7fc46a136d1a75782691cf23b93ac4c36f254fa5b2e962ed08883a81`.
EN sidecar: `artifacts/static-ten-20261124/urban_horror/h04-static-v2/h04-static-v2.en.srt`
Traditional Chinese sidecar: `artifacts/static-ten-20261124/urban_horror/h04-static-v2/h04-static-v2.zh-Hant.srt`
Silent storyboard: `artifacts/static-ten-20261124/urban_horror/h04-static-v2/silent-storyboard.jpg`; timestamped strips: `artifacts/static-ten-20261124/urban_horror/h04-static-v2/qa/shot-01-strip.jpg` through `shot-06-strip.jpg`.

## Shot table: silent intent versus decoded result
| Shot | Seconds | Narrative function | Silent intent | What the frames show |
|---|---|---|---|---|
| shot-01 | 0.0–5.5 | establish | An indistinct person waits beyond wired glass while the signed book remains on the desk. | Final edit opens on signed book and a hat-wearing silhouette beyond wired glass, showing a possible threat immediately. |
| shot-02 | 5.5–11.0 | clue | She signs EVA; a blue sheet corner protrudes below the cream page. | Pencil EVA is readable; a blue sheet edge is present beneath the cream page. This follows the establishing view as a detail insert. |
| shot-03 | 11.0–17.0 | reaction | The eraser removes the top name but leaves the blue page corner untouched. | Pink eraser removes readable lettering; eraser dust remains. The blue sheet edge stays under the same page stack. |
| shot-04 | 17.0–23.0 | reaction | She closes the book, believing the empty visible page means safety; doorway is empty. | Eva closes the brown book; the outside doorway is empty. Her pixie hair, cardigan, blouse and face match the reference. |
| shot-05 | 23.0–28.5 | reveal | The lifted blank writing leaf reveals an untouched blue copy of EVA below. | Blank rubbed top leaf is lifted, blue copying sheet folded aside, intact dark-blue EVA on cream duplicate below. No explanatory warning text. |
| shot-06 | 28.5–36.0 | reveal | Her intact name is visible in the book; the visitor now stands directly behind her inside the lobby. | Intact blue EVA remains visible and the visitor stands inside directly behind Eva. Her outer cheek/right edge is cropped, but both eyes, mouth, hair, clothing, book and visitor remain readable. |

The initial SILENT STORYBOARD check was generated before ImageGen by build_inputs.py. Delivered story.md also records subsequent staging revisions; H04 initial inputs are preserved in the v1 input-archive. The core object-state event is visible; the precise supernatural rule still requires narration. This author review is not a blind silent-viewer test.

## Engineering QA
Pipeline validator: VALID. Final technical QA: all 10 checks true. 1080×1920, 30 fps, 1080 frames, H.264 High/yuv420p, AAC 48 kHz stereo, faststart, no embedded subtitle stream; complete decode succeeded.
Dense output: 162 decoded samples across six shots at 30/7 fps plus each final frame. All six timestamped strips were visually inspected for face, hair, clothing, prop geometry/state, set, crop and camera continuity.
Opening editorial question is visible only at 1.0–3.5 s. No burned narration captions or fiction labels. In-world text is limited to the declared evidence. Six measured narration WAVs and three synthesized nonverbal SFX are represented in both sidecars.
Caption alignment: measured trimmed source PCM, exact SRT-content comparison and bounds checks; no ASR/listening claim. Mix peak: -3.83 dBFS. Audio loudness/peak diagnostics are in commands.jsonl.
QA and hash evidence: `artifacts/static-ten-20261124/urban_horror/h04-static-v2/qa/report.json`, `artifacts/static-ten-20261124/urban_horror/h04-static-v2/qa/probe.json`, `artifacts/static-ten-20261124/urban_horror/h04-static-v2/timeline.json`, `artifacts/static-ten-20261124/urban_horror/h04-static-v2/manifest.json`.

## Continuity and story-logic findings
| Timestamps | Impact class | Observed finding |
|---|---|---|
| 1.000–3.500 | early outcome disclosure (spoiler) | BLOCKING: the opening question "Why did erasing her name fail?" explicitly discloses that erasing fails before the false relief at 17–23 s. It does not disclose the carbon-copy mechanism, but it crosses the brief's spoiler boundary. Source: shots.json question; the same question is in the rendered master. |
| 28.500–35.967 | cosmetic | Right edge trims Eva outer cheek/shoulder. Both eyes and mouth remain visible; the visitor and blue name are retained through the move. |
| 0.000–16.967 | confusing | Blue copying-sheet edge is small on a phone-sized view. It is present but may not be noticed as a fair clue without replay. |

No additional confirmed causal rule violation was identified in this author inspection. This is a limited observation, not proof of a passed story gate. All listed residual issues remain in the delivered master.

Future revision: ask whether erasing the name will save her without asserting failure, and check the question against the false-relief/reveal boundary before rendering. The current shots.json, story and master remain unchanged so the inputs still match the rendered video; this records-only correction does not clear HOLD.

## Calls, corrections, encodes and wall time
Built-in ImageGen: 3 calls; one canonical sheet first, then two canonical-conditioned shot sheets.
Every completed call has a receipt in `artifacts/static-ten-20261124/urban_horror/h04-static-v2/images.jsonl`. Exported prompts and their hashes are in `artifacts/static-ten-20261124/urban_horror/h04-static-v2/prompts/`. Original generated sheets are retained in assets; no external paid TTS call. Image billed cost UNKNOWN; no invented dollar figure.
Six narration lines synthesized once with the existing local Kokoro model, voice af_heart, speed 1.08; trimmed PCM reused by all renders. Three local mathematical SFX WAVs (pulse/click/chime), no downloaded recordings.
Final render: 6 libx264 shot encodes + one stream-copy/AAC mux; 37.281 s. Cumulative production: 12 shot encodes, 74.562 s of render invocations.
Observed production wall span: 1188.790 s, from 2026-11-24T15:38:56.489176+00:00 to 2026-11-24T15:58:45.278685+00:00. Boundary is initial story-file creation through final QA; includes queue time and other-story work, excludes initial repository reading. Do not sum overlapping story spans. See production-cost.json for the machine-readable cost record.
Fix passes: 1 after v1 QA; first two source cells swapped to show the figure immediately, with no new ImageGen/TTS. Original h04-static-v1 master, QA, cost, and input-archive preserved; final h04-static-v2 reuses the three historical image receipts, documented in image-reuse.json. Cumulative encode count includes both renders.

## Acceptance and unverified scope
Story Quality Gate PENDING (no blind readers this round). Storyboard Quality Gate PENDING. Viewer Gate HUMAN_TEST_PENDING. Market acceptance NOT_TESTED; no retention, viewer preference, public data, or revenue evidence.
Not verified: human listening, EN/zh-Hant phone playback, independent silent comprehension, emotional effect, external originality and commercial-rights review. Technical QA cannot establish these.
Reproducible validation: `python -B experiments/cluepause/static-ten-20261124/urban_horror/job.py validate H04`. Production invocation: same entry point with `run H04`; existing master protection refuses overwriting, so a future rerender needs a new revision id.
Shared pipeline regression: `python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/urban_horror/pytest-cache --basetemp artifacts/static-ten-20261124/urban_horror/pytest-temp` → 33 passed. `git diff --check` → exit 0.
Root README installation/core/video commands were not run: no core/video changes, uv is absent from PATH, and rebuilding shared environments would violate the job-only write boundary. This is isolated pipeline/media engineering verification, not full core-engine acceptance.
No commit, push, upload, YouTube action or memory edit. Only the two authorized urban_horror trees were written.
