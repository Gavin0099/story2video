# U01 — The Shoes That Stayed Wet

FICTION. Genre: uncanny_mystery. Rights: **pending_verification**.

Retains U01 v3 without changing its story: shoes stored dry become wet inside a locked cabinet. A chalky plant saucer and old exterior streak suggest overflow. Paper beneath the saucer stays dry; the timed watering hose connector leaks inside the cabinet, filling the shallow tray and escaping through its bottom seam.

Story Quality Gate **PENDING** (no blind readers this round). Storyboard Quality Gate **PENDING**. Viewer Gate **HUMAN_TEST_PENDING**. Market acceptance **NOT_TESTED**.

Base Git SHA: `aef24410f8b45c8651fd922343aeb52db11bfc75`. This is the unchanged base, not a commit containing these files. Main-agent image inspection is not human viewer acceptance.

Master: `artifacts/static-ten-20261124/uncanny_mystery/uncanny-u01-v1/uncanny-u01-v1.mp4`. Duration **38 s**; SHA-256 `e075afa52d9e4a6d687076c46f8b0919375785efcca2d57591b37ed61b12fb77`. Sidecars: `uncanny-u01-v1.en.srt` and `uncanny-u01-v1.zh-Hant.srt` beside the master.

## Shot functions and silent-storyboard intent versus observed frames

Authored SILENT STORYBOARD was written in story.md before any ImageGen. The following observations were made by the main agent from the silent export and all dense decoded temporal contact strips, not inferred from the prompts.

| Time | Shot / narrative function | Silent intent | What decoded frames actually show |
| --- | --- | --- | --- |
| 0–3.5 s | shot-01 / establish | Water beads beneath the closed padlocked cabinet while the surrounding tile is dry. | A hanging drip and small puddle beneath a closed brass-padlocked oak cabinet are visible. Wider than intended macro, but the event reads; question appears only during the opening interval. |
| 3.5–7 s | shot-02 / clue | She opens the lock and lifts the shoes; the pale connector is already present in the rear hose loop. | Same bob-haired woman and rust pullover beside open cabinet; key, grey shoes, black tray and pale rear connector visible. Pose is toward camera rather than actively lifting shoes. |
| 7–10 s | shot-03 / clue | Water clings to the rubber sole, while canvas and laces are dry. | Tilted grey shoe has sole droplets; white laces and canvas look dry; pooled tray water visible. Connector has an attached lower hose and no active leak yet. |
| 10–14 s | shot-04 / clue | The plant saucer has a white tide ring; watering equipment sits beside it. | Plant, saucer, reservoir and pump readable. The conspicuous white mineral band is on the pot exterior, not clearly around the saucer inner rim. |
| 14–18 s | shot-05 / clue | A dry exterior streak leads down the cabinet back; the hallway remains dry except near its base. | She points at a dried white streak on the cabinet side/front corner, not clearly the back. Surrounding tile is dry outside the small puddle. |
| 18–22 s | shot-06 / clue | She places a white sheet beneath the entire saucer and rear top edge. | She places white paper under the saucer. The paper covers the footprint but does not visibly seal or cover the complete rear-edge route. |
| 22–25 s | shot-07 / transition | The tray and shoes are dry before the cabinet is closed for the night. | Cloth, dry tray, shoes and key/lock visible. White paper has disappeared from under the pot, contradicting the preceding placement. |
| 25–27 s | shot-08 / reaction | She leaves the key beside her bed; the closed locked cabinet remains visible. | She places the key beside the bed; cabinet remains closed in the doorway. The already-placed paper is absent in the distant cabinet view. |
| 27–29 s | shot-09 / transition | The planted white paper and closed padlock remain undisturbed before morning. | Closed padlock and flat paper reappear with morning/pre-dawn lighting. This restores the intended state without explaining its prior absence. |
| 29–33.5 s | shot-10 / reveal | The same pale ribbed connector now leaks down the inside wall into the shoe tray. | Water visibly exits the pale connector, but its lower black hose is missing; it resembles an open outlet rather than the scripted split in an inline connector. Clock has a single prominent downward hand and no numerals. |
| 33.5–35.5 s | shot-11 / reveal | Lifting the plant saucer exposes completely dry paper across the tested route. | Lifting pot and saucer reveals pristine dry paper. The entire rear-edge route is still not visibly covered. White mineral band remains on pot exterior. |
| 35.5–38 s | shot-12 / reveal | After the cycle, water crosses the low tray lip and cabinet floor to the same bottom seam; the laces stay dry. | Shallow tray overflow and water crossing cabinet floor to base drops are visible. Same shoes and dry-looking uppers persist; lower hose is connected again, contradicting the previous connector close-up. |

The broad silent sequence conveys locked wet storage, an apparent plant source, a paper test, inside watering hardware and overflow. It does not faithfully carry the exact v3 split-connector mechanism or a decisive rear-route exclusion. Those failures cannot be repaired by the unchanged narration. Recurrence and exclusive key ownership remain spoken context.

## Continuity and story logic

| Time | Impact class | Finding / consequence |
| --- | --- | --- |
| 3.5–7 and 22–25 s | cosmetic | The woman looks toward the camera with a nearly neutral smile instead of reacting to the evidence. Hair, face and rust/navy wardrobe remain visually consistent. |
| 10–14 and 33.5–35.5 s | confusing | White mineral band is primarily on the pot exterior, rather than the scripted saucer inner rim; the spoken clue is visually imprecise. |
| 14–18 s | confusing | Old streak appears on a side/front corner instead of clearly on the exterior back, weakening the proposed top-to-rear overflow route. |
| 18–22 and 33.5–35.5 s | breaks story logic | Paper does not visibly cover the entire rear-edge entry route. Its dryness therefore cannot visually exclude all of the proposed overhead overflow path as required by U01 v3. |
| 22–27 s | breaks story logic | Paper disappears after it was placed at 18–22 s, then reappears at 27 s. This breaks the test-state continuity despite the one correction request. |
| 29–33.5 s (compare 7–10 and 35.5–38 s) | breaks story logic | Lower hose vanishes in the leak close-up and reappears in the final shot. Water comes from the open connector end rather than a fine side split; generated imagery misrepresents the retained causal story. |
| 29–33.5 s | confusing | The unnumbered clock has one prominent downward hand; exact six o'clock relies on narration, rather than two clearly readable hands. |

Inspected silent export and every dense strip, shots 01–12. No additional camera-driven clipping, seam exposure, wardrobe/hair change or shoe-shape jump was observed in these samples. Still photographs keep droplets frozen; SFX imply the event, with no animated water. Tray, shoes, reservoir and plant remain broadly recognizable, but the paper and hose-state failures are material.

Visual correction passes: **1**. One resolution-sheet correction was requested before the first encode, targeting paper persistence, a connected inline hose, dry paper coverage and a smaller overflow. It improved the unnumbered clock and reduced the flood appearance but did not repair the important geometry/state defects. The rejected original is preserved. No second correction or second master was made. No further loop was run.

## Engineering QA and commands

Shared validator: VALID. Machine media QA: **PASS**; this is a technical result, not a quality-gate decision. All 10 reported boolean checks: video=True, frames=True, duration=True, audio=True, no_embedded_subtitles=True, faststart=True, full_decode=True, captions_en=True, captions_zh-Hant=True, caption_bounds=True.

Full decode and technical probe: 1080×1920, 30 fps, H.264 High/yuv420p, AAC 48 kHz stereo, faststart, no embedded subtitles. Dense temporal QA: **177 decoded frames**, every 7 frames (4.286 fps) plus each shot final frame; all 12 strips and the silent storyboard inspected by the main agent. Camera zoom is 1.005–1.025; no character animation.

Caption/audio alignment is measured trimmed 24 kHz mono PCM plus exact sidecar-to-cue comparison and bounds validation. Revealing narration starts no earlier than the first reveal shot. This is not ASR, listening, a human comprehension test, or a commercial-rights clearance. Human playback with EN, zh-Hant, captions OFF and sound OFF remains unverified. Original synthetic SFX are illustrative; no borrowed recordings.

Commands, from repository root (environment tool paths supplied externally, never written into inputs):

```text
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/run_local.py validate experiments/cluepause/static-ten-20261124/uncanny_mystery/U01
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/run_local.py prompts experiments/cluepause/static-ten-20261124/uncanny_mystery/U01 --supports-images
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/run_local.py run experiments/cluepause/static-ten-20261124/uncanny_mystery/U01
```

TTS was synthesized once per line with the existing read-only render environment using `prepare_voice.py U01 U02 U03`; render inputs use the saved per-line PCM files. Actual encode, decode, probe and loudness-measurement argument arrays, timings and exit codes are in the portable `commands.jsonl` beside the master. Each image request has a receipt in `images.jsonl`; exact prompts are frozen in this story’s `image-prompts-used.json`.

## Counts, time and cost

- ImageGen requests logged: **5**; bitmap outputs generated: **4** (including rejected bitmaps); tool-validation rejections without an image: **1**. Built-in ImageGen, no API fallback. Cost **UNKNOWN**; do not infer dollars from request count.
- H.264 encode count: **12**, one per shot; one final stream-copy/AAC mux. Master render invocations: **1**. Pipeline measured wall time: **70.469 s**.
- Measured local TTS production: **48.546 s**, af_heart at 1.08. No hosted TTS or model download.
- Elapsed from the initial editorial manifest creation to record assembly: **1829.8 s**; includes tool waits and work on the other two stories, and is not exclusive labor or ImageGen service time.

## Limits and acceptance

Technically complete; unresolved paper-test and connector-state errors break the intended v3 visual logic. Not a qualified storyboard.

No blind readers, phone-scale human test, full human listening, external originality/similarity review or market measurement. Existing v2/v3 text-reader findings informed writing only; none transfers as a gate decision for these films. U01 retains the v3 English/Chinese lines and causal story; generated failures are expressly recorded above. U02 and U03 are new original-fiction candidates with distinct mechanisms. No commit, push, upload, YouTube access, memory edits, production engine changes or shared-pipeline edits.
