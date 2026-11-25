# U03 - The Man in the Pantry Door - current v2

**UPLOADED_PRIVATE** - video_id `MgCZsP25fOM`, CluePause, integrator manual report dated 2026-11-25 Asia/Taipei. The blocking v1 frame kept a high round head shadow after its colander was lowered. v2 replaces only shot-09: the colander now lies flat on the low foreground counter outside the directional beam, and the detached high head shadow disappears. The unchanged towel still casts shoulders; removing it in shot-10 leaves only rack lines. This repairs the visible source/shadow state contradiction in the producing agent's inspection. Exact optical geometry remains unmeasured; the independent private-copy review is recorded below.

Story Quality Gate **PENDING**. Storyboard Quality Gate **PENDING**. Viewer Gate **HUMAN_TEST_PENDING**. Rights **pending_verification**. Market acceptance **NOT_TESTED**.

Revision date: **2026-11-25 Asia/Taipei**. Base Git SHA: `1e3c4f40c92eabfbe5cc66b54b777418e7a169f2`, branch `codex/cluepause-static-ten-20261124`. This SHA is the starting checkout, not a commit of this revision. v2 was the next free source/output revision id. Inputs: `U03/revisions/v2/`; original v1 story, shots, references, assets and all v1 artifact bytes are preserved. The original record is retained verbatim at `revisions/v2/record-v1.md` and below; `revisions/v2/v1-preservation.json` binds their hashes.

Master: `artifacts/static-ten-20261124/uncanny_mystery/uncanny-u03-v2/uncanny-u03-v2.mp4`.
Duration **36.000 s**, 1080 frames. SHA-256 `4a912d85fd66d85dbd050a900dc1298c8f06b823752423e5c9b8f715c6c94b3e`.
Sidecars: `uncanny-u03-v2.en.srt` and `uncanny-u03-v2.zh-Hant.srt` beside the master. Silent storyboard: `silent-storyboard.jpg` and `silent-storyboard.json` beside the master. Full QA, dense strips, portable commands and verification are in that same output directory.

## Private upload record - 2026-11-25 Asia/Taipei

Integrator-reported fact: the unchanged v2 master above was manually uploaded in YouTube Studio on CluePause as `MgCZsP25fOM`, visibility **private**, made_for_kids **false**, AI/altered content **yes** (checked in the upload dialog). At save time the upload dialog showed "檢查完畢，未發現任何問題". This records the integrator's report; no YouTube access was performed for this update.

English title/description were applied from `upload-metadata-draft.json`; their exact values and published Traditional Chinese translation are now retained in `../../upload-metadata.json`, in the U03 entry using the same schema as H04. The integrator read back the draft's zh-Hant title/description in Studio before publishing the translation. Both caption tracks were published **with timing**: Chinese (Traditional), language code `zh-Hant`, from `uncanny-u03-v2.zh-Hant.srt` (SHA-256 `598979909eb3e53b3fc95700466667c6f61c6f253a22a6323a6eef315f8f99de`), and English, language code `en`, from `uncanny-u03-v2.en.srt` (SHA-256 `43e0206122d0fefac64dbec5268c4a6254a87863d98f51823cb67f5c17a3a061`). The auto-generated English (US) track was left in place. The draft was removed after consolidation and validation.

Independent local review: **UPLOAD-OK (private review copy)**, **BLOCKING: none**, per `artifacts/independent-review-u03-v2-20261125/review.md`. Its residual predictability, reveal correspondence/readability and framing findings remain applicable. This private upload does not pass the Story/Storyboard gates (**PENDING**), Viewer Gate (**HUMAN_TEST_PENDING**), rights verification (**pending_verification**) or market acceptance (**NOT_TESTED**), and does not authorize public release.

Engineering verification for this metadata-only update: starting Git SHA `435f4ab3dfec21526358bd3bed3b175ab1a914af`. `python -B` checks parsed both JSON inputs, matched U03's keys/nested schema to H04, preserved all existing video entries/session fields, and recomputed the master and both SRT SHA-256 values against the draft. Post-edit JSON/schema/hash and personal-path regex checks, plus `git diff --check`, passed. Only the shared metadata, this record and the removed U03 draft were written. No commit, push, upload or memory edit was performed. Root README engine/npm/governance acceptance commands were not rerun for this record-only change within the three-file write scope. Platform settings/caption publication are integrator-reported, not independently rechecked here. Market acceptance remains **NOT_TESTED**; human listening, phone playback, silent-story comprehension, rights/originality and exact optical reconstruction remain unverified.

## v2 per-shot changes and mechanism state

**L** means the same fixed warm black task lamp on the kitchen counter, behind the rack and outside the pantry, shining through the object plane toward the outside of the frosted pane. In reveal views it is screen-right, aimed left across the rack. Lamp height, aim and rack/towel placement do not change across the reveal. **Inferred** states are outside a crop and are continuity assumptions, not directly observed coordinates. Image size changes from close-ups are camera framing, not asserted changes of physical magnification. All rows were checked against decoded frames, not just prompts.

| Shot / time / change | Light source position | Colander position | Shadow position / size on glass | Door / pantry state | Character | Transition consistency |
| --- | --- | --- | --- | --- | --- | --- |
| 01 / 0-4 / reused | L, offscreen inferred | Upright above towel on rack, below crop inferred | Soft head over broad shoulders, upper/middle pane; small faint holes | Closed; empty interior hidden | Ochre henley, curls, back/side to camera | Establishes combined shadow; source objects withheld |
| 02 / 4-7 / reused | L, offscreen inferred | Same rack position, offscreen inferred | Same soft joined contour; enlarged by glass close-up, faint holes | Closed; interior hidden | Outside crop | 01 -> 02 changes framing only; no implied object motion |
| 03 / 7-11 / reused | L at frame edge; stays on kitchen counter | Same rack state offscreen inferred | No joined figure visible on swung-away pane; original receiving plane is displaced | Open; empty shelves and one bare hanger, no coat/person | Holds brass knob | 02 -> 03 rotates the receiving surface out of its closed-door beam intersection; no claim of a figure inside |
| 04 / 11-14 / reused | L offscreen inferred | Same rack state offscreen inferred | Receiving glass outside this interior close view; no figure asserted there | Open; same empty shelves/hanger | Looks at hanger, puzzled | 03 -> 04 stays in open-door state |
| 05 / 14-18 / reused | L offscreen inferred | Same rack state below crop inferred | Joined soft head/shoulders return at prior region/scale | Closed; empty interior hidden | Looks toward silhouette | 04 -> 05 returns pane to beam; unchanged sources restore figure |
| 06 / 18-22 / reused | Defocused L behind metal/towel | Macro curved patch of still-upright perforated metal; whole position cropped | Glass outside macro crop; joined projection inferred unchanged | Closed, outside crop inferred | Outside crop | 05 -> 06 only changes framing; no shown source move |
| 07 / 22-26 / reused | L below crop inferred | Still on rack, below crop inferred | Most pane/figure outside face crop; no new shadow state claimed | Closed frame visible; pantry hidden | Looks down, concentrated | 06 -> 07 reaction only, before lifting |
| 08 / 26-30 / reused | L visible at right, behind rack, toward pane | Lifted off rack and held left of towel, still in beam | Round perforated head displaced left of stationary broad shoulders; medium disk partly clipped at left pane edge | Closed; pantry hidden | Holds steel handle in ochre shirt | 07 -> 08 lateral source displacement has matching lateral projection separation; clipping retained as residual |
| 09 / 30-33 / NEW still | L remains at right behind rack, same aim | Flat, low on foreground counter below/outside lamp -> towel -> pane beam | **No detached high head or pinpoints**; broad towel-only shoulder patch stays lower/middle pane, larger in frame due tighter camera | Closed; pantry hidden | Outside crop | 08 -> 09 lowers/rotates source out of beam, so round head disappears; towel shadow remains rather than moving with colander |
| 10 / 33-36 / reused | L remains on counter at right | Still out of beam, now outside crop inferred | Shoulder patch gone; only thin rectangular rack lines low on glass; no head | Closed; pantry hidden | Holds towel away from beam, relieved | 09 -> 10 removes second occluder, leaving rack projection only |

The critical 08 -> 09 -> 10 cuts now read: lifted colander / detached head, lowered out-of-beam colander / no head but shoulders, removed towel / no shoulders. No independently floating head survives the lowered source. These are three static photographed states with gentle camera zoom; the intervening hand motion is not animated. All nine transitions are qualitatively compatible with the stated light direction. Hidden setup geometry, exact magnification and matching individual hole rays remain unmeasured. The earlier human-like contour is softer/longer than the round reveal contour; v2 does not certify pixel-exact optical reconstruction.

## v2 ImageGen evidence and budget

Built-in ImageGen / `precise-object-edit`; **1 call, 1 generated bitmap, 0 correction calls, 0 tool-validation rejections** for this fix. It edits the extracted original shot-09 and is conditioned on the unchanged canonical reference sheet. No new reference/setup/resolution sheet was generated. Original v1 history remains **4 requests / 4 bitmaps**, including its earlier setup correction; lifetime U03 total is now **5 / 5**. ImageGen cost **UNKNOWN**.

Exact prompt, input roles and prompt hash: `revisions/v2/image-prompts-used.json` and output `prompts/repair.json`. Every new call has a receipt in both `revisions/v2/images.jsonl` and output `images.jsonl`; result `assets/shot09-fixed.png` has its SHA bound there. Accepted after inspecting the full still, then all rendered shot-09 samples. No second image call or post-render image correction was necessary. The prompt specifically requests a low flat colander outside the beam, removal of the entire high round shadow, and preservation of the lamp/towel/shoulder state.

## v2 decoded inspection and answer-disclosure audit

The primary agent inspected **all 10 decoded strips / 164 sampled frames**, every seventh 30-fps frame (**4.286 fps**) plus every shot's final frame, and the complete silent storyboard. `qa/shot-01-strip.jpg` through `qa/shot-10-strip.jpg` and their `samples.json` files retain the evidence. In all 14 shot-09 samples (30.000-32.967 s), the low flat colander is visible and the high glass has no round perforated head. Its shoulder-only patch remains; all 14 shot-10 samples show rack lines without the human figure. No camera-driven shadow/source change appears within a shot.

Opening question remains "Who Is Behind the Glass?" / "玻璃後面是誰？" only at 1.0-3.5 s. It does not name a colander, lamp, towel or shadow mechanism. Source narration text, all seven narration WAVs, SFX, measured timing, question plate and both language sidecars are unchanged. Explicit spoken/captioned identification starts with the colander at **26.000 s**, coinciding with the first reveal; the lamp explanation starts **30.200 s**. The pre-reveal lines mention holes, an empty hanger, recurrence and looking in front of the glass, without naming the cause. Exact SRT/cue comparisons and first-reveal bounds pass; no earlier answer was added in v2.

Residual disclosure risk remains **confusing / predictability**: the metal-perforation macro with navy cloth and defocused lamp at 18-22 s can let a viewer infer projection before 26 s. Full object-to-glass alignment is withheld until the reveal. This has not been resolved by blind readers or phone tests, and is not claimed as an objectively spoiler-free story.

## v2 engineering acceptance, commands and limits

Job validation via the existing genre-local entry point: **VALID**. Full machine media QA: **PASS**, all 10 checks true (video, frames, duration, audio, no embedded subtitles, faststart, full decode, both captions, caption bounds). H.264 High/yuv420p, 1080x1920 at 30 fps, AAC 48 kHz stereo. One render invocation; 10 cut encodes and final stream-copy/AAC mux; measured pipeline wall time **44.172 s**. Source/model downloads and TTS calls: **0**. Existing external tool files were read-only and verified against the pipeline's executable size/SHA pins; bindings were supplied only through environment variables.

The U03-only verification additionally confirms v1 source/artifact hash preservation, nine unchanged encoded cuts, the changed shot-09 cut, all seven original WAV hashes, identical mixed WAV, identical decoded master audio, identical question plate, both SRTs byte-identical to v1 and exact against measured cues, prompt/result hashes, dense sample count and pending gates. Source input hashes and starting Git SHA are in the manifest. Portable encode/decode/probe/loudness/audio-hash argv, exits and timing are in `commands.jsonl`.

Commands executed from repository root (tool paths supplied externally, not stored in inputs):

```text
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/run_local.py validate experiments/cluepause/static-ten-20261124/uncanny_mystery/U03/revisions/v2
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/run_local.py run experiments/cluepause/static-ten-20261124/uncanny_mystery/U03/revisions/v2
python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/uncanny_mystery/uncanny-u03-v2/pytest-cache --basetemp artifacts/static-ten-20261124/uncanny_mystery/uncanny-u03-v2/pytest-temp
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/U03/revisions/v2/verify_revision.py
git diff --check
```

Pipeline pytest: **33 passed in 0.54 s** using U03-specific cache/basetemp. U03 verification (including personal-path regex grep and text whitespace checks): **PASS**, evidence in output `verification.json`. `git diff --check`: **PASS**. No source/video/governance code changed; root engine pytest/npm/governance acceptance was not rerun. No framework update. The verification script is delivery evidence, not a production-engine change.

Residuals: subtle opening pinholes; potentially revealing 18-second macro; soft/cropped shot-07 reaction; early elongated contour versus rounder/crisper reveal head; left-edge clipping of the displaced head in shot-08; exact ray geometry and individual hole-constellation correspondence unmeasured. The repaired low-colander/high-head contradiction was not observed in v2. Full listening, phone playback in both caption languages/on/off, human silent-story comprehension, rights/originality checks and market results remain **unverified**. Engineering PASS does not advance story/storyboard/viewer gates or market acceptance.

During v2 production, no commit, push, upload, YouTube access or memory edit was performed. The later private upload is recorded above. No puzzle/P03 file was modified. Only U03, the uncanny README and the batch README's U03 row were changed; unrelated existing work was preserved.

---

## Archived v1 record - historical findings below apply to v1

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
