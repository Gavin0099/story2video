# H04 — The Name Underneath production record

FICTION — original invented urban-horror candidate. Rights: pending_verification.
Revision validation base Git SHA: `79e9afc0e05f1143a4aeaaab56c116eaaff8dd3b`. Working files are uncommitted. No publication authorization is implied.

Status: **UPLOADED_PRIVATE**. Per the integrator's manual report on 2026-11-25 (Asia/Taipei), the unchanged v3 master was uploaded in YouTube Studio on CluePause as video `1dziLaHqEdk`. Independent v3 review returned **UPLOAD-OK (private review copy)** with **BLOCKING: none**; see `artifacts/independent-review-h04-v3-20261125/REVIEW.md`. Story/Storyboard Gates remain **PENDING**; Viewer Gate remains **HUMAN_TEST_PENDING**. Private upload and the review recommendation do not establish quality-gate passage or public-release approval.

Upload facts: visibility private; made_for_kids false; altered/synthetic content (AI) yes. English title/description came from the H04 draft, now consolidated into `experiments/cluepause/static-ten-20261124/upload-metadata.json`. Studio's upload dialog showed **檢查完畢，未發現任何問題** at save time. Both timed caption tracks, **中文（繁體）** from `h04-static-v3.zh-Hant.srt` and **英文** from `h04-static-v3.en.srt`, were published; the auto-generated English (US) track was left in place. The Traditional Chinese title/description translation was published from the draft's zh fields after editor readback. These Studio facts are integrator-reported, not independently reverified in this records update.

Records-only engineering validation (2026-11-25 Asia/Taipei), base Git SHA `7a65c6cb9ac74a022acda159ce569885fcf20e45`: `python -B -` JSON parsing, exact upload-fact assertions, master/two-SRT SHA-256 comparisons, draft-removal assertion, unchanged existing four videos/session assertions, unchanged non-H04 table rows (including working-tree P03), puzzle/memory hash comparisons and personal-path/whitespace scan passed. `git diff --check` and PowerShell `Select-String` personal-path grep passed. Root README `uv sync --locked`, core pytest and video npm acceptance were not rerun for this records-only change; no source/video/governance code changed. Media playback and live Studio state were not independently reverified. Market acceptance remains **NOT_TESTED**. This update performed no commit, push, upload or memory edit.

## Story and rule
At midnight the house visitor comes for every name left in the guestbook. Marks copied onto a bound duplicate page are still names in that same book.
Eva believes the pencil entry is the only entry and the shape outside is the night porter; erasing the visible name appears sufficient.
A blue copying sheet corner is visible below the writing page from the first close-up. Pencil pressure leaves a second entry; erasing the surface does not remove it. No warning text explains this before payoff.

## Delivered files
Master: `artifacts/static-ten-20261124/urban_horror/h04-static-v3/h04-static-v3.mp4`
Duration: 36.000 s; SHA-256: `6c3c636fe7f8ead19575aab1c20698f4bfd16e389513c1ecb844724c97a03469`.
EN sidecar: `artifacts/static-ten-20261124/urban_horror/h04-static-v3/h04-static-v3.en.srt`
Traditional Chinese sidecar: `artifacts/static-ten-20261124/urban_horror/h04-static-v3/h04-static-v3.zh-Hant.srt`
Silent storyboard: `artifacts/static-ten-20261124/urban_horror/h04-static-v3/silent-storyboard.jpg`; timestamped strips: `artifacts/static-ten-20261124/urban_horror/h04-static-v3/qa/shot-01-strip.jpg` through `shot-06-strip.jpg`.

Opening question: **Will erasing her name save her? / 擦掉名字，就能救她嗎？** Only the bilingual question and revision id changed in shots.json; story.md matches. The question is editorial picture text, not spoken narration or a sidecar cue.

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
QA and hash evidence: `artifacts/static-ten-20261124/urban_horror/h04-static-v3/qa/report.json`, `qa/probe.json`, `timeline.json` and `manifest.json` beside the v3 master. The ten checks were rerun for v3; the earlier dense continuity inspection remains supported by identical source plates and pixel-identical shots 02–06.

## v3 spoiler audit and comparison
Reviewed every EN/zh narration line and timed sidecar cue, plus story.md, shots.json, references.json and this production record. The title "The Name Underneath" raises a question without asserting erasure failure. At the v3 revision audit, no H04 entry existed in batch upload-metadata.json. The later manual private-upload facts are now consolidated there. Production notes describe the answer for reviewers, but are not audience captions or early on-screen text.

Lines 01–03 establish the signed book, visitor rule and attempted erasure. Line 04 preserves false relief: "The shape outside disappeared. Eva closed the book and breathed." Reveal lines start at 23.180 s and 28.680 s. No additional pre-23 s outcome disclosure was found in narration or sidecars; no baked-audio issue was identified. All six narration WAVs and three SFX are reused with no synthesis. Both SRTs were regenerated from measured cues and are byte-identical to v2, including all nine speech/SFX cues; neither includes the editorial question.

Full-resolution decoded comparison against v2 covers all 1080 frames. Outside [1.000, 3.500), 1005 frames have SSIM mean **0.999448432**, minimum **0.992466**. Shots 02–06 (5.500–36.000 s), 915 frames, are pixel-identical (SSIM 1.0). The remaining 90 outside-window frames in shot 01 differ after H.264 re-encoding: before the question mean/min 0.995361300/0.994531; after it until 5.500 s mean/min 0.993080583/0.992466. Thus literal pixel equality outside the window is not claimed. Input comparison confirms identical shots, crops, camera moves, timings and narration; extracted plate provenance, full timeline, mix WAV and decoded AAC audio also match v2 exactly.

Decoded frames 29, 30, 45, 60, 75, 90, 104 and 105 were inspected: the correct bilingual text is readable at 1.000–3.467 s and absent at 0.967/3.500 s. Evidence: v3 `qa/question-boundaries.png`, full-size `qa/question-frame-*.png`, `qa/revision-comparison.json`, per-frame SSIM log and both decoded framemd5 files. All 453 snapshotted files across v1/v2, H04 source assets and upload metadata remain hash-identical.

## Continuity and story-logic findings
| Timestamps | Impact class | Observed finding |
|---|---|---|
| 1.000–3.500 | early outcome disclosure (spoiler), corrected candidate | v2's question asserted failure before the false relief. v3 now asks "Will erasing her name save her?" / 「擦掉名字，就能救她嗎？」 without asserting the outcome. Decoded text confirmed; subsequent independent v3 review found no BLOCKING issue for a private review copy. |
| 28.500–35.967 | cosmetic | Right edge trims Eva outer cheek/shoulder. Both eyes and mouth remain visible; the visitor and blue name are retained through the move. |
| 0.000–16.967 | confusing | Blue copying-sheet edge is small on a phone-sized view. It is present but may not be noticed as a fair clue without replay. |

No additional confirmed causal rule violation was identified in this author inspection. This is a limited observation, not proof of a passed story gate. The cosmetic and confusing findings remain unchanged in v3.

The question fix in v3 subsequently received independent UPLOAD-OK for a private review copy and was uploaded privately as reported above. Story/Storyboard Gates remain PENDING; Viewer Gate remains HUMAN_TEST_PENDING.

## Calls, corrections, encodes and wall time
Built-in ImageGen: 3 calls; one canonical sheet first, then two canonical-conditioned shot sheets.
Every completed call has a receipt in `artifacts/static-ten-20261124/urban_horror/h04-static-v2/images.jsonl`. Exported prompts and their hashes are in `artifacts/static-ten-20261124/urban_horror/h04-static-v2/prompts/`. Original generated sheets are retained in assets; no external paid TTS call. Image billed cost UNKNOWN; no invented dollar figure.
Six narration lines synthesized once with the existing local Kokoro model, voice af_heart, speed 1.08; trimmed PCM reused by all renders. Three local mathematical SFX WAVs (pulse/click/chime), no downloaded recordings.
Historical v2 render: 6 libx264 shot encodes + one stream-copy/AAC mux; 37.281 s. Historical v1/v2 cumulative production: 12 shot encodes, 74.562 s of render invocations.
Observed production wall span: 1188.790 s, from 2026-11-24T15:38:56.489176+00:00 to 2026-11-24T15:58:45.278685+00:00. Boundary is initial story-file creation through final QA; includes queue time and other-story work, excludes initial repository reading. Do not sum overlapping story spans. See production-cost.json for the machine-readable cost record.
Fix passes: v2 swapped the first two source cells; v3 changes only the opening question. v1/v2 outputs remain untouched. v3 image-reuse.json binds every reused source asset and distinguishes three historical ImageGen calls from zero new ImageGen/TTS calls; copied receipts/prompts are historical evidence. Final v3 render: 6 shot encodes + one mux, 35.282 s. An earlier attempt was caught by exact question assertions with the old zh text still present after a shell encoding replacement failed. Its master/logs are preserved separately under `artifacts/static-ten-20261124/urban_horror/h04-static-v3-attempt01-failed-text/`; it is not the candidate. No existing master was overwritten. This extra attempt used another six shot encodes + one mux; see its cost.json. Prior v2 inputs are archived in v3 previous-inputs-v2/ and final v3 inputs in input-archive/.

## Acceptance and unverified scope
Story Quality Gate PENDING (no blind readers this round). Storyboard Quality Gate PENDING. Viewer Gate HUMAN_TEST_PENDING. Market acceptance NOT_TESTED; no retention, viewer preference, public data, or revenue evidence.
Not verified: human listening, EN/zh-Hant phone playback, independent silent comprehension, emotional effect, external originality and commercial-rights review. Technical QA cannot establish these.
Reproducible validation: `python -B experiments/cluepause/static-ten-20261124/urban_horror/job.py validate H04`. Production invocation: same entry point with `run H04`; existing master protection refuses overwriting, so a future rerender needs a new revision id.
v3 engineering commands at the base SHA above (all use existing dependencies):

- `python -B experiments/cluepause/static-ten-20261124/urban_horror/job.py validate H04` → VALID.
- `python -B experiments/cluepause/static-ten-20261124/urban_horror/job.py run H04` → technical PASS, all ten checks true; environment tool/font bindings match v2 hashes.
- `python -B artifacts/static-ten-20261124/urban_horror/h04-static-v3/verify_revision.py` → comparison, preservation, audio and caption assertions passed.
- `python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/urban_horror/h04-static-v3/pytest-cache --basetemp artifacts/static-ten-20261124/urban_horror/h04-static-v3/pytest-temp` → **33 passed in 0.75 s**.
- `git diff --check` and personal-path/whitespace scan of all changed tracked files and v3 portable text evidence → PASS; details in v3 delivery-checks.json.
Root README installation/core/video commands were not run: no core/video changes, uv is absent from PATH, and rebuilding shared environments would violate the job-only write boundary. This is isolated pipeline/media engineering verification, not full core-engine acceptance.
The historical v3 revision performed no commit, push, upload, YouTube action, ImageGen, new TTS or memory edit. No core/video/pipeline/governance source changed; that revision did not itself perform independent review, human listening/phone playback or market acceptance. Subsequent independent review and integrator-reported private upload are recorded above. The v3 work writes H04 inputs/record, batch summary records and H04 revision artifacts only; tool files in the other checkout were read only.
