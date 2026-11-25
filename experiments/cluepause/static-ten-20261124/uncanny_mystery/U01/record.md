# U01 v2 — The Shoes That Stayed Wet

**REVIEWED: UPLOAD-OK private review copy, not uploaded yet.** This is a new visual revision of U01, not an acceptance of v1. The original v1 story, shots, references, assets, narration and master are unchanged, verified by hashes. The original record is retained byte-for-byte at `revisions/v2/v1-record-snapshot.md`; its findings below remain historical v1 findings.

The new rear camera views show a continuous dry paper apron above the entire rear vent entry width. The sheet visibly persists on top through the intervening exterior/front shots. The leak close-up retains both black hose attachments and shows a jet from the ivory connector's side wall; the final view retains that assembly. These observations support the intended mechanism, subject to the residuals and independent review below.

Master: `artifacts/static-ten-20261124/uncanny_mystery/uncanny-u01-v2/uncanny-u01-v2.mp4`. Duration **38.000 s**, 1140 frames, 1080x1920, 30 fps, H.264 High/yuv420p, AAC 48 kHz stereo, faststart, no embedded subtitles.

SHA-256: `146f6f92fa651d07818f9b4bddda5a2819db5919a7a1a9116e4194f2bdff06d4`.

Sidecars beside master: `uncanny-u01-v2.en.srt`, `uncanny-u01-v2.zh-Hant.srt`. Silent storyboard: `silent-storyboard.jpg` and companion JSON; no question/captions in the silent image. Final dense decoded evidence: `qa/shot-01-strip.jpg` through `qa/shot-12-strip.jpg` and per-shot `samples.json`.

Base Git SHA: `b7801291cf7af830272070e416130125ed0df7b5` on `codex/cluepause-static-ten-20261124`. This is provenance of the existing checkout, not a commit containing this revision. At v2 production time, no commit, push, upload, YouTube operation, memory edit, other-story edit, shared-pipeline edit or README edit was performed. The review integration below subsequently updates only U01 records and the two authorized U01 README rows, and prepares a separate upload derivative. The separate source checkout was only read for pinned render executables. Tool paths are supplied externally through environment variables and scrubbed from saved command evidence.

Story Quality Gate **PENDING**. Storyboard Quality Gate **PENDING**. Viewer Gate **HUMAN_TEST_PENDING**. Independent media review **UPLOAD-OK private review copy; BLOCKING: none**. Market acceptance **NOT_TESTED**. Rights **pending_verification**. No status here grants upload/publication authority.

## Independent review integration - 2026-11-25 (Asia/Taipei)

The [independent U01 v2 review](../../../../../artifacts/independent-review-u01-v2-20261125/review.md) returned **UPLOAD-OK (private review copy only), BLOCKING: none**, with **REQUEST_CHANGES for the supplied records**. The clock residual is now recorded below, in mechanism.md and in inspection.json; the inherited mineral-ring/streak mismatch remains disclosed. The CR-CR-LF pytest transcript and extra EOF blank line are normalized, and the copied mechanism link is corrected. These edits address the record findings without new media generation; they do not claim fresh independent approval of the edited records or upload derivative.

Status: **REVIEWED: UPLOAD-OK private review copy, not uploaded yet**. This media recommendation grants no upload/public-release authority, story/viewer-gate pass or rights clearance. Engineering checks and the separate upload-copy evidence are recorded in the integration acceptance below; market acceptance remains **NOT_TESTED**.

## Review integration engineering acceptance - 2026-11-25 (Asia/Taipei)

Base Git SHA: `c99491c411fe42988eb9876be26392d5f2701368`; branch `codex/cluepause-static-ten-20261124`. Engineering acceptance **PASS** for this records/derivative scope: the [integration verifier](revisions/v2/verify_review_integration.py) checks 938 pre-edit file hashes, unchanged files outside the seven authorized existing record/README edits, README changes limited to U01 rows, JSON/style/spoiler checks, master/copy/SRT hashes, format/duration equality, all U01 UTF-8 text including untracked files, Python syntax and portable paths. Results are saved in [review-integration-checks.json](revisions/v2/review-integration-checks.json). Ordinary tracked Git diff and separate no-index checks for every untracked U01 text file both pass; the earlier tracked-only check did not supply that coverage. Normalizing the saved pytest transcript did not rerun pytest.

Commands from repository root:

```text
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/U01/revisions/v2/make_upload_copy.py
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/U01/revisions/v2/verify_review_integration.py
git -c core.excludesFile=NUL diff --check
# The verifier executes the following for every proposed untracked U01 text file:
git -c core.excludesFile=NUL -c core.autocrlf=false -c core.safecrlf=false diff --no-index --check -- NUL <file>
```

The [upload-copy evidence](../../../../../artifacts/static-ten-20261124/uncanny_mystery/uncanny-u01-v2/upload-copy.md) records the unchanged master and the separate `artifacts/static-ten-20261124/uncanny_mystery/uncanny-u01-v2/uncanny-u01-v2-upload.mp4`: **9,177,244 bytes**, SHA-256 `79b04a066320d7401ed07a968de812f34718347ba7c543c57ef723576fcdc666`. P01's two-pass method preserves 1080x1920, 30 fps, H.264 High/yuv420p, AAC 48 kHz stereo and **38.000000 s**; duration delta **0.000000 s**. Full audio/video decode and faststart pass. SSIM over all 1,140 frames: mean **0.994366**, minimum **0.989576**. No independent derivative review or human playback is claimed.

[upload-metadata-draft.json](upload-metadata-draft.json) contains the four audience-facing EN/zh-Hant fields, master/copy provenance and both unchanged timed SRT paths/hashes. The unnamed woman uses she/her; the hook states only the wet-shoes situation and withholds the cause and test. Its five `uploaded_file_*` fields follow P01's names and describe a prepared copy, **not a completed upload**.

Market acceptance **NOT_TESTED**; Story/Storyboard Gates **PENDING**, Viewer Gate **HUMAN_TEST_PENDING**, rights **pending_verification**. Human playback/listening, phone/caption-toggle acceptance, rights clearance, browser/YouTube processing and market measurement remain unverified. Root README `uv run --locked pytest`, `npm ci` / `npm run typecheck`, and governance verification were not rerun: no application, video project or governance code changed. No commit, push, upload, memory edit, master rerender or ImageGen was performed.

## Mechanism states, per-shot changes and transitions

The mechanism table and all eleven adjacent-cut observations (with residual continuity limits) are maintained in [mechanism.md](revisions/v2/mechanism.md). OOF states are explicitly distinguished from direct visual evidence. The table is also included here for review.

OOF = outside the frame or hidden by the closed cabinet; carried state is an editorial continuity inference, not a direct observation. W = the same invented woman, black bob, rust pullover and navy trousers. All uppers and white laces remain dry where visible.

| Shot / seconds | Change from v1 | Paper placement / rear coverage / wet-dry | Hose and connector | Leak source | Shoes | Character |
| --- | --- | --- | --- | --- | --- | --- |
| 01 / 0-3.5 | Reused | Not introduced | Interior OOF | Bottom seam drips; internal cause withheld | OOF; wet condition introduced in narration | None |
| 02 / 3.5-7 | Reused | Absent before evening test | Both black hose attachments present; lower hose curves behind shoes | Inactive connector; no split exposed | In tray; soles' wetness becomes explicit in 03; uppers/laces dry-looking | W, key, open door |
| 03 / 7-10 | Reused | Absent; top mostly OOF | Both hose ends attached; lower section partly occluded by lifted shoe | Shoe sole droplets, no connector jet | Lifted sole visibly wet; laces/canvas dry | W's profile and hands |
| 04 / 10-14 | Reused | Absent | Reservoir/pump and upper hose visible; inline assembly OOF | No active exterior leak | OOF; previous wet state | None |
| 05 / 14-18 | Reused | Absent | Top equipment visible; inline assembly OOF | Old dried exterior mark, no current exterior stream | OOF; previous wet state | W points at old streak |
| 06 / 18-22 | Regenerated; canonical rear view | Newly placed full top sheet; continuous downward rear apron above complete vent; dry | Exterior hose enters below apron; inside assembly OOF | None visible | OOF; wiping/reset follows in 07 | W across cabinet, side hand |
| 07 / 22-25 | Regenerated | Full top white sheet persists under saucer and reservoir; rear apron hidden by front view; exposed paper dry | Both black hoses attached; inactive ivory connector and lower curve visible | None | Tray and shoes visibly dry-looking after reset | W with dry cloth and key |
| 08 / 25-27 | Regenerated | Full top sheet visibly persists on distant closed cabinet; rear apron OOF; no wet marks visible | Exterior top hose visible; assembly hidden by doors | None visible | Hidden; carry dry reset state | W places single key beside bed |
| 09 / 27-29 | Regenerated | Same full top sheet persists; rear apron OOF; exposed paper dry | Top hose visible; assembly hidden by doors | None visible | Hidden; carry dry reset state | None |
| 10 / 29-33.5 | Regenerated | Cabinet top OOF; paper not removed | Both black hoses visibly attached, lower hose descends from sealed connector end | Thin side jet from connector right middle wall, away from both end seals; arcs into tray | Soles in shallow water; uppers/laces dry-looking | None |
| 11 / 33.5-35.5 | Regenerated; rear view, fixed zoom | Same rear apron spans complete vent; dry top and apron; pot/saucer slightly lifted, paper stays put | Exterior rear hose visible below apron; inside connector OOF | No exterior stream; current internal leak established by 10 | OOF; carry wet soles | W, rust sleeves, hands at saucer |
| 12 / 35.5-38 | Regenerated | Top OOF; no removal established | Both hoses remain attached; residual small side beads, no open outlet | Pump cycle ended; tray overtops low lip and crosses floor to bottom seam | Soles wet; uppers/laces dry-looking | None |


## Engineering acceptance and disclosure

Shared job validation: **VALID**. Final machine media QA: **PASS**, all 10 checks true, including full decode, expected video/frame/duration/audio, faststart, no embedded subtitles, both exact SRT comparisons and caption bounds. Source PCM is reused, not resynthesized: all nine original WAVs and all nine EN/zh-Hant narration lines match v1 byte-for-byte. All source/input, image result, conditioning-image and exact-prompt hashes match. See `revisions/v2/verification.json`, `revisions/v2/inspection.json`, and artifact `qa/report.json`, `manifest.json`, `assets.json`, `commands.jsonl`.

The main agent inspected **all 12 final decoded strips / 177 frames at 4.286 fps plus shot-end samples**, and the final silent storyboard. First-attempt strips and silent storyboard were also inspected before the permitted corrections. No white sheet-divider exposure or additional camera clipping of the rear vent/apron, hose attachments or side jet was observed in final samples. Shot-11 holds at 1.0 zoom; the other shots retain gentle 1.005-1.025 zoom. Generated column widths are unequal, so explicit measured whole-sheet crops in `crop-evidence.json` replace an equal-grid assumption. No painted water, digital paper patches or explanatory diagrams were added.

Opening question remains only at 1.0-3.5 s. The same question and non-reveal narration do not disclose the answer. Connector is inactive before 29 s. Reveal line-08 and its EN/zh-Hant captions run **29.000-32.610625 s**; line-09 runs **33.500-36.266458 s**. Pump sound/caption starts 29.1 s. Exact SRT-to-PCM schedule comparison and text inspection found no early answer disclosure; this is not ASR or human listening evidence.

Pipeline pytest: **33 passed in 0.53 s**, using the U01-specific cache/basetemp directories above; `revisions/v2/pipeline-pytest.txt` contains the result. The initial test invocation had 31 fixture-setup errors and 2 passes because the basetemp parent did not exist; creating that parent fixed the setup and the same suite passed. The final audit's first path scan matched its own literal search pattern; splitting that literal fixed the scanner and it passed without changing media or story inputs.

Commands from repo root, with existing pinned tools/font and Git SHA supplied by environment:

```text
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/U01/revisions/v2/run_revision.py validate
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/U01/revisions/v2/run_revision.py run
python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/uncanny_mystery/uncanny-u01-v2/cache/pytest --basetemp artifacts/static-ten-20261124/uncanny_mystery/uncanny-u01-v2/tmp/pytest
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/U01/revisions/v2/audit_revision.py
git diff --check
```

Historical production results: validate VALID; final render PASS; pytest 33 passed; revision audit PASS. The original `git diff --check` passed for tracked changes only; it did not cover the then-untracked v2 files. Independent review found their transcript/EOF whitespace defects. The current integration acceptance below covers the full U01 text set, including untracked files, after cleanup. Personal-path grep is implemented by `audit_revision.py` across U01 and its v2 output tree; final result PASS. No production source, video application, governance contract or framework version changed; their unrelated npm/core/governance suites were not rerun for this local story revision. The shared pipeline remains unchanged.

## ImageGen ledger, attempts and counts

**4 new built-in ImageGen calls / 4 bitmaps** for v2; cost **UNKNOWN**. Exactly one correction per sheet: mechanism attempts 1/2, resolution attempts 1/2. No API fallback or additional correction. Every call is recorded in `revisions/v2/images.jsonl` and the artifact ledger; exact prompts and conditioning hashes are frozen in `revisions/v2/image-prompts-used.json`. v1's historical five requests/four bitmaps remain unchanged; cumulative U01 history is nine requests/eight bitmaps, not four total.

| Call | Sheet / attempt | Disposition | Result SHA-256 |
| --- | --- | --- | --- |
| 1 | mechanism / 1 | rejected | `01aa0a4fd06691e0d01f949e5d51c953a0cfec57a1510ac6eee551ea9fcd1867` |
| 2 | resolution / 1 | rejected | `7e94f6850e23bf788c36de088ae90f3c19ec481a7d7034abb81d021ac3669d75` |
| 3 | mechanism / 2 | accepted | `bcd1aef2a9f7aff80e686a52a8d8fa90406bc3e394900afa81ded82a29d7158a` |
| 4 | resolution / 2 | accepted | `0ee56b6ac4d7b9465df2db993249b50d60f0c37a8b980d7695ed3f46e9b6f84c` |

First master was technically valid but rejected after producer review for insufficiently explicit rear-fold geometry and a white seam at shot-08. Preserved with its inputs and full QA under artifact `attempt1/`, and as `uncanny-u01-v2-attempt1.mp4`; SHA-256 `d640bb33ffc3420ff18cfbf59507474b67a641183641838b574b5baffb3fe7de`. Original generated images are preserved as `mechanism-attempt1.png` and `resolution-attempt1.png`.

Two render invocations, 12 H.264 cut encodes and one stream-copy/AAC mux each: **24 cut encodes total**, two final muxes. First pipeline wall time **57.86 s**; final pipeline wall time **55.421 s**. No new TTS. Image generation wait time and producer review are outside those render durations.

## Residuals and unverified acceptance

The entire paper footprint under the saucer is not exposed: shot-11 only slightly lifts it. The visible dry evidence is the surrounding top paper and uninterrupted rear apron across the whole entry opening. Rear-apron persistence in front-facing 07-09 is inferred from the continuously visible full top sheet and matching rear views 06/11; it is not directly visible behind the cabinet in those front views. Exact five-centimetre fold depth is unmeasured. Narrow side rails remain outside the paper, but no unpapered path from the saucer to the rear vent is visible. Independent review supports the depicted exclusion argument, without laboratory proof of every hidden route.

Clock continuity residual (SHOULD-FIX, noncausal): shot-10 (29-33.5 s) shows a prominent clock on the cabinet floor in front of the tray; the wider final interior shot-12 (35.5-38 s) exposes that floor/front edge without the clock, and no removal is established. Independent samples at 29.5 and 36 s document the disappearance. This does not undo the water mechanism; it remains unfixed in the unchanged master.

Inherited residuals: strongest mineral band remains on pot exterior (04), old streak remains on a side/front corner (05), neutral camera-facing expression remains in 02. Side jet arcs into the tray rather than visibly tracking down the rear wood. Static water and hand actions remain frozen. Recurrence, sole key ownership and elapsed time partly rely on narration. No new line was invented to excuse a visual problem.

Independent media review is recorded above. No independent story/viewer-gate acceptance, human phone-scale viewing, complete human listening, EN/zh-Hant/OFF playback acceptance, originality/commercial-rights clearance, or market measurement. The genre and batch README U01 rows now select reviewed v2; the old proposed rows remain historical production evidence.

---

## Archived v1 findings (historical; not observations of v2)


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
