# U02 — The Chair That Came to Breakfast

FICTION. Genre: uncanny_mystery. Rights: **pending_verification**.

Each morning, a mustard-apron-draped rolling kitchen stool has left its place and arrived at the doorway. A tilted floor and rolling marble suggest gravity. Yet a strip of rug is crossed uphill. A robot vacuum winds the apron tie into its brush and tows the stool; the curved floor marks were the route of its wheels.

Story Quality Gate **PENDING** (no blind readers this round). Storyboard Quality Gate **PENDING**. Viewer Gate **HUMAN_TEST_PENDING**. Market acceptance **NOT_TESTED**.

Base Git SHA: `aef24410f8b45c8651fd922343aeb52db11bfc75`. This is the unchanged base, not a commit containing these files. Main-agent image inspection is not human viewer acceptance.

Master: `artifacts/static-ten-20261124/uncanny_mystery/uncanny-u02-v1/uncanny-u02-v1.mp4`. Duration **36 s**; SHA-256 `621fef7371db356fb6c16ecfb85772158d2200e9bd8ac72896c51a5501e446e2`. Sidecars: `uncanny-u02-v1.en.srt` and `uncanny-u02-v1.zh-Hant.srt` beside the master.

## Shot functions and silent-storyboard intent versus observed frames

Authored SILENT STORYBOARD was written in story.md before any ImageGen. The following observations were made by the main agent from the silent export and all dense decoded temporal contact strips, not inferred from the prompts.

| Time | Shot / narrative function | Silent intent | What decoded frames actually show |
| --- | --- | --- | --- |
| 0–4 s | shot-01 / establish | A rolling stool with an apron blocks the doorway; its place at the breakfast counter is empty. | Same grey rolling stool and mustard apron wait at the dark doorway, woman looking toward them; curved floor marks visible. Movement and recurrence are supplied by subsequent frames and speech, not this still alone. |
| 4–7 s | shot-02 / clue | The stool has free caster wheels and paired curved scuffs end beside them. | Free black casters, chrome stem, long mustard tie and paired curved scuffs visible in a clear low close-up. |
| 7–10 s | shot-03 / clue | A blue marble is set on the floor toward the doorway, suggesting a slope. | Woman crouches with a blue marble near her fingers; dock is visible below the cabinet. No rolling animation, as intended for stills. |
| 10–13 s | shot-04 / clue | The same marble now rests against the doorway side of the rug. | Blue marble now rests beside the raised charcoal rug edge; before/after placement supports the slope hypothesis but does not measure a slope. |
| 13–17 s | shot-05 / clue | The stool’s curved wheel trail continues over the raised rug ridge. | Stool caster is on the far side of the rug ridge; paired scuffs and yellow tie lead across the foreground. Crossing reads, but a still is not a proof that gravity could never carry it there. |
| 17–21 s | shot-06 / reaction | She resets the stool at the counter; the hanging tie and docked vacuum share the floor. | Woman resets the apron-draped stool at the counter; the charcoal/grey vacuum sits at its dock beside the hanging tie. Expression is visibly puzzled. |
| 21–25 s | shot-07 / clue | The loose yellow tie lies across the path from the vacuum dock. | Long tie lies loose on the floor in front of vacuum dock. Stool and vacuum remain separate, with no taut connection yet. |
| 25–30 s | shot-08 / reveal | The apron tie is taut between the stool and the vacuum’s brush intake. | Mustard tie is taut between apron/stool at the left edge and vacuum intake at the right. Both materials match; stool seat/apron origin is near the left crop edge and is less clear than intended. |
| 30–33 s | shot-09 / reveal | Lifting the vacuum reveals the same yellow tie wound around its black brush roller. | Sage-sleeved hands lift the same vacuum; multiple yellow loops around the black underside roller supply a clear physical explanation. |
| 33–36 s | shot-10 / reveal | The freed stool stays at the counter while the vacuum sits alone at the rug crossing. | Stool is back at counter; woman holds yellow ties off the floor, vacuum sits at doorway, scuffs remain. Tie attachment passes behind her body and is not directly traceable in this closing view. |

The silent sequence carries the visible core: displaced wheeled stool, a tentative slope/rug test, a loose apron tie near a vacuum, a taut connection, and the same tie wrapped around the brush. The reveal reassigns the curved marks from passive rolling to a towing route. Exact recurrence, exclusive key ownership and the inference of a slight floor slope still rely partly on speech. Silent human comprehension has not been tested.

## Continuity and story logic

| Time | Impact class | Finding / consequence |
| --- | --- | --- |
| 17–25 s | cosmetic | Evening/night separation is modest; under-counter lighting changes but not a strong time-of-day transition. Narration supplies the overnight chronology. |
| 25–30 s | confusing | Stool seat and apron origin are close to the left crop edge, so the taut tie is clear while its upper attachment is less explicit. The following underside insert resolves the brush mechanism. |
| 33–36 s | confusing | Held tie lengths pass behind the woman rather than remaining fully traceable to the apron. Could briefly look detached, though no visible cutting or changed prop is shown. |

Inspected silent export and all ten dense decoded strips. No observed hair, face, sage/cream wardrobe, grey stool, mustard apron, blue marble, vacuum-shell or set-state change that breaks the causal story. The loading roller is new reveal detail of the already-established vacuum, not a new device. No active coupling is shown before 25 s. Modest camera zoom preserves the marble, rug ridge, taut tie and roller loops in the sampled frames. Robot towing force and rug crossing were not physically bench-tested.

Visual correction passes: **0**. No visual correction or re-encode pass was used; the two source shot sheets are the first generated versions. Remaining crop/occlusion issues are documented instead of adding an optional loop. No further loop was run.

## Engineering QA and commands

Shared validator: VALID. Machine media QA: **PASS**; this is a technical result, not a quality-gate decision. All 10 reported boolean checks: video=True, frames=True, duration=True, audio=True, no_embedded_subtitles=True, faststart=True, full_decode=True, captions_en=True, captions_zh-Hant=True, caption_bounds=True.

Full decode and technical probe: 1080×1920, 30 fps, H.264 High/yuv420p, AAC 48 kHz stereo, faststart, no embedded subtitles. Dense temporal QA: **165 decoded frames**, every 7 frames (4.286 fps) plus each shot final frame; all 10 strips and the silent storyboard inspected by the main agent. Camera zoom is 1.005–1.025; no character animation.

Caption/audio alignment is measured trimmed 24 kHz mono PCM plus exact sidecar-to-cue comparison and bounds validation. Revealing narration starts no earlier than the first reveal shot. This is not ASR, listening, a human comprehension test, or a commercial-rights clearance. Human playback with EN, zh-Hant, captions OFF and sound OFF remains unverified. Original synthetic SFX are illustrative; no borrowed recordings.

Commands, from repository root (environment tool paths supplied externally, never written into inputs):

```text
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/run_local.py validate experiments/cluepause/static-ten-20261124/uncanny_mystery/U02
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/run_local.py prompts experiments/cluepause/static-ten-20261124/uncanny_mystery/U02 --supports-images
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/run_local.py run experiments/cluepause/static-ten-20261124/uncanny_mystery/U02
```

TTS was synthesized once per line with the existing read-only render environment using `prepare_voice.py U01 U02 U03`; render inputs use the saved per-line PCM files. Actual encode, decode, probe and loudness-measurement argument arrays, timings and exit codes are in the portable `commands.jsonl` beside the master. Each image request has a receipt in `images.jsonl`; exact prompts are frozen in this story’s `image-prompts-used.json`.

## Counts, time and cost

- ImageGen requests logged: **3**; bitmap outputs generated: **3** (including rejected bitmaps); tool-validation rejections without an image: **0**. Built-in ImageGen, no API fallback. Cost **UNKNOWN**; do not infer dollars from request count.
- H.264 encode count: **10**, one per shot; one final stream-copy/AAC mux. Master render invocations: **1**. Pipeline measured wall time: **46.141 s**.
- Measured local TTS production: **43.672 s**, af_heart at 1.08. No hosted TTS or model download.
- Elapsed from the initial editorial manifest creation to record assembly: **1829.8 s**; includes tool waits and work on the other two stories, and is not exclusive labor or ImageGen service time.

## Limits and acceptance

Visible towing mechanism and broadly consistent references; tie origin is edge-cropped and final tie attachment is occluded. Human comprehension untested.

No blind readers, phone-scale human test, full human listening, external originality/similarity review or market measurement. Existing v2/v3 text-reader findings informed writing only; none transfers as a gate decision for these films. U01 retains the v3 English/Chinese lines and causal story; generated failures are expressly recorded above. U02 and U03 are new original-fiction candidates with distinct mechanisms. No commit, push, upload, YouTube access, memory edits, production engine changes or shared-pipeline edits.
