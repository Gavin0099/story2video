# U03 — The Man in the Pantry Door

FICTION. Genre: uncanny_mystery. Rights: **pending_verification**.

A head-and-shoulders silhouette stands in a closed frosted pantry door each evening. An empty coat hanger inside suggests a hanging coat. But the pantry is empty when opened. A small counter lamp projects the combined shadow of a round perforated colander and a navy tea towel on the dish rack onto the outside of the glass. Moving the colander breaks the head away from the shoulders.

Story Quality Gate **PENDING** (no blind readers this round). Storyboard Quality Gate **PENDING**. Viewer Gate **HUMAN_TEST_PENDING**. Market acceptance **NOT_TESTED**.

Base Git SHA: `aef24410f8b45c8651fd922343aeb52db11bfc75`. This is the unchanged base, not a commit containing these files. Main-agent image inspection is not human viewer acceptance.

Master: `artifacts/static-ten-20261124/uncanny_mystery/uncanny-u03-v1/uncanny-u03-v1.mp4`. Duration **36 s**; SHA-256 `674697a7b378700d69125078e9844f1bab1b1e020d746537d9e92f0ea409c78b`. Sidecars: `uncanny-u03-v1.en.srt` and `uncanny-u03-v1.zh-Hant.srt` beside the master.

## Shot functions and silent-storyboard intent versus observed frames

Authored SILENT STORYBOARD was written in story.md before any ImageGen. The following observations were made by the main agent from the silent export and all dense decoded temporal contact strips, not inferred from the prompts.

| Time | Shot / narrative function | Silent intent | What decoded frames actually show |
| --- | --- | --- | --- |
| 0–4 s | shot-01 / establish | The man faces a person-like shadow on the closed frosted pantry door. Ordinary counter objects are outside this tight frame. | Same curly-haired man and ochre shirt face a dark head-and-shoulders silhouette on closed frosted glass. Complete source objects stay outside the frame; a few faint bright points are present. |
| 4–7 s | shot-02 / clue | A few tiny bright pinholes appear inside the blurred shadow head; no recognizable colander outline. | Soft human-like shadow fills the pane; tiny pinpoints are visible but low-contrast against the frosted grain. No recognizable colander handles remain in the accepted setup. |
| 7–11 s | shot-03 / clue | Opening the door reveals empty shelves and a bare hanger. | Door opens to empty shelves and one bare wooden hanger; no person or coat inside. Man and door/knob remain recognizable. |
| 11–14 s | shot-04 / reaction | He checks the bare hanger, puzzled that there is no coat. | Closer puzzled reaction to bare hanger and empty shelves, maintaining the coat hypothesis as an idea rather than an actual hidden coat. |
| 14–18 s | shot-05 / clue | The closed door again shows the same soft figure, while the man reacts beside it. | Closed door again carries the same soft figure. Counter objects remain below this crop, so no full cause is demonstrated yet. |
| 18–22 s | shot-06 / clue | A curved perforated steel detail catches the lamp light; its dots echo the earlier pinholes without showing the complete arrangement. | Macro of curved perforated steel with navy towel edge and defocused black lamp. Pattern supplies a fair hint, though viewers may already infer projection here. |
| 22–26 s | shot-07 / reaction | His concentrated expression turns down toward the counter; part of the soft figure remains behind him, while source objects stay below this initial portrait crop. | Initial reaction crop shows his concentrated face and door frame; complete object combination stays below frame. Most of the figure is also outside the crop. It is a reaction beat rather than new evidence. |
| 26–30 s | shot-08 / reveal | Lifting the colander away separates the shadow’s head from its towel-shaped shoulders. | He lifts the colander beside the towel on rack; round perforated head shadow is displaced toward the left edge of the pane while shoulder shadow remains. The split is visible, though part of the head is clipped by the pane edge. |
| 30–33 s | shot-09 / reveal | The physical line from lamp through colander and towel to the matching shadows is visible. | Colander now rests low on the counter at the right, but detached round head shadow remains high at the left of the pane. Lamp, rack and towel remain visible; shadow height does not follow the lowered object. |
| 33–36 s | shot-10 / reveal | Removing the towel leaves a bare rack and no human-shaped silhouette. | He holds navy towel away from bare chrome rack. Glass now shows the thin rack grid and no human-shaped figure; colander is outside the frame. Relieved expression, same hair and clothing. |

The silent sequence offers a figure, empty pantry, a bare hanger as a competing explanation, a perforated steel clue, then a visible head/shoulder split and removal of the figure. It can communicate the intended ordinary-object explanation, but the contour change and the high head shadow after the colander is lowered prevent a clean physical demonstration. This is not a verified optical simulation or observed human comprehension result.

## Continuity and story logic

| Time | Impact class | Finding / consequence |
| --- | --- | --- |
| 0–7 and 14–18 s | confusing | Tiny bright holes are subtle against frosted grain. The fair clue may be missed on a phone; human readability is untested. |
| 18–22 s | confusing | The macro metal perforations plus lamp/towel context strongly suggest projection before the reveal. Complete arrangement is withheld, but remaining predictability is not resolved by blind readers this round. |
| 22–26 s | cosmetic | Tight initial reaction crop is softer and cuts part of the face/figure. It preserves expression and avoids showing the entire answer early, but adds no new physical observation. |
| 26–30 s, compared with 0–18 s | confusing | Earlier shadow has a more elongated human contour; reveal shadow is rounder and crisply perforated. Blur could conceal some differences, but the mismatch may feel like a restaged silhouette rather than an exact re-reading. |
| 26–30 s | confusing | Displaced round head reaches the pane's left edge and is partially clipped; separation remains visible but the complete matching shape is not shown. |
| 30–33 s | breaks story logic | Colander has been set low on the counter while its supposed head shadow remains high on the glass at nearly the previous height. The pictured projection does not track the changed source state, undermining the ordinary optical explanation. |

Inspected silent export and all ten dense decoded strips. Man's curls, face, ochre/charcoal wardrobe, mint wall, cream door, brass knob, chrome rack, navy towel and metal colander are broadly recognizable. No further camera-driven state change appears within a shot. The important discontinuity is the object-to-shadow geometry across the reveal cuts, rather than a wardrobe change. The final rack-only shadow resolves the visitor visually, but does not repair the preceding geometric error.

Visual correction passes: **1**. One setup-sheet correction replaced the full early colander/towel display with a tighter figure shot and isolated perforation detail. Original sheet and pre-revision storyboard are preserved. Before the first encode, shot-07 received its initial face/reaction crop, recorded in shots.json and story.md. Only one master was encoded. No second correction was used for the remaining reveal geometry error. No further loop was run.

## Engineering QA and commands

Shared validator: VALID. Machine media QA: **PASS**; this is a technical result, not a quality-gate decision. All 10 reported boolean checks: video=True, frames=True, duration=True, audio=True, no_embedded_subtitles=True, faststart=True, full_decode=True, captions_en=True, captions_zh-Hant=True, caption_bounds=True.

Full decode and technical probe: 1080×1920, 30 fps, H.264 High/yuv420p, AAC 48 kHz stereo, faststart, no embedded subtitles. Dense temporal QA: **164 decoded frames**, every 7 frames (4.286 fps) plus each shot final frame; all 10 strips and the silent storyboard inspected by the main agent. Camera zoom is 1.005–1.025; no character animation.

Caption/audio alignment is measured trimmed 24 kHz mono PCM plus exact sidecar-to-cue comparison and bounds validation. Revealing narration starts no earlier than the first reveal shot. This is not ASR, listening, a human comprehension test, or a commercial-rights clearance. Human playback with EN, zh-Hant, captions OFF and sound OFF remains unverified. Original synthetic SFX are illustrative; no borrowed recordings.

Commands, from repository root (environment tool paths supplied externally, never written into inputs):

```text
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/run_local.py validate experiments/cluepause/static-ten-20261124/uncanny_mystery/U03
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/run_local.py prompts experiments/cluepause/static-ten-20261124/uncanny_mystery/U03 --supports-images
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/run_local.py run experiments/cluepause/static-ten-20261124/uncanny_mystery/U03
```

TTS was synthesized once per line with the existing read-only render environment using `prepare_voice.py U01 U02 U03`; render inputs use the saved per-line PCM files. Actual encode, decode, probe and loudness-measurement argument arrays, timings and exit codes are in the portable `commands.jsonl` beside the master. Each image request has a receipt in `images.jsonl`; exact prompts are frozen in this story’s `image-prompts-used.json`.

## Counts, time and cost

- ImageGen requests logged: **4**; bitmap outputs generated: **4** (including rejected bitmaps); tool-validation rejections without an image: **0**. Built-in ImageGen, no API fallback. Cost **UNKNOWN**; do not infer dollars from request count.
- H.264 encode count: **10**, one per shot; one final stream-copy/AAC mux. Master render invocations: **1**. Pipeline measured wall time: **44.312 s**.
- Measured local TTS production: **41.344 s**, af_heart at 1.08. No hosted TTS or model download.
- Elapsed from the initial editorial manifest creation to record assembly: **1829.8 s**; includes tool waits and work on the other two stories, and is not exclusive labor or ImageGen service time.

## Limits and acceptance

Readable shadow split and stable character/props; a high head shadow persists after the colander is lowered, breaking projection logic.

No blind readers, phone-scale human test, full human listening, external originality/similarity review or market measurement. Existing v2/v3 text-reader findings informed writing only; none transfers as a gate decision for these films. U01 retains the v3 English/Chinese lines and causal story; generated failures are expressly recorded above. U02 and U03 are new original-fiction candidates with distinct mechanisms. No commit, push, upload, YouTube access, memory edits, production engine changes or shared-pipeline edits.
