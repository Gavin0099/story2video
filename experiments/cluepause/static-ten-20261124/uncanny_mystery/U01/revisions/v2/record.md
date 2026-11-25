# U01 v2 — The Shoes That Stayed Wet

**REVIEWED: UPLOAD-OK private review copy, not uploaded yet.** This is a new visual revision of U01, not an acceptance of v1. The original v1 story, shots, references, assets, narration and master are unchanged, verified by hashes. The original record is retained byte-for-byte at `v1-record-snapshot.md`; its findings below remain historical v1 findings.

The new rear camera views show a continuous dry paper apron above the entire rear vent entry width. The sheet visibly persists on top through the intervening exterior/front shots. The leak close-up retains both black hose attachments and shows a jet from the ivory connector's side wall; the final view retains that assembly. These observations support the intended mechanism, subject to the residuals and independent review below.

Master: `artifacts/static-ten-20261124/uncanny_mystery/uncanny-u01-v2/uncanny-u01-v2.mp4`. Duration **38.000 s**, 1140 frames, 1080x1920, 30 fps, H.264 High/yuv420p, AAC 48 kHz stereo, faststart, no embedded subtitles.

SHA-256: `146f6f92fa651d07818f9b4bddda5a2819db5919a7a1a9116e4194f2bdff06d4`.

Sidecars beside master: `uncanny-u01-v2.en.srt`, `uncanny-u01-v2.zh-Hant.srt`. Silent storyboard: `silent-storyboard.jpg` and companion JSON; no question/captions in the silent image. Final dense decoded evidence: `qa/shot-01-strip.jpg` through `qa/shot-12-strip.jpg` and per-shot `samples.json`.

Base Git SHA: `b7801291cf7af830272070e416130125ed0df7b5` on `codex/cluepause-static-ten-20261124`. This is provenance of the existing checkout, not a commit containing this revision. At v2 production time, no commit, push, upload, YouTube operation, memory edit, other-story edit, shared-pipeline edit or README edit was performed. The review integration below subsequently updates only U01 records and the two authorized U01 README rows, and prepares a separate upload derivative. The separate source checkout was only read for pinned render executables. Tool paths are supplied externally through environment variables and scrubbed from saved command evidence.

Story Quality Gate **PENDING**. Storyboard Quality Gate **PENDING**. Viewer Gate **HUMAN_TEST_PENDING**. Independent media review **UPLOAD-OK private review copy; BLOCKING: none**. Market acceptance **NOT_TESTED**. Rights **pending_verification**. No status here grants upload/publication authority.

## Independent review integration - 2026-11-25 (Asia/Taipei)

The [independent U01 v2 review](../../../../../../../artifacts/independent-review-u01-v2-20261125/review.md) returned **UPLOAD-OK (private review copy only), BLOCKING: none**, with **REQUEST_CHANGES for the supplied records**. The clock residual is now recorded below, in mechanism.md and in inspection.json; the inherited mineral-ring/streak mismatch remains disclosed. The CR-CR-LF pytest transcript and extra EOF blank line are normalized, and the copied mechanism link is corrected. These edits address the record findings without new media generation; they do not claim fresh independent approval of the edited records or upload derivative.

Status: **REVIEWED: UPLOAD-OK private review copy, not uploaded yet**. This media recommendation grants no upload/public-release authority, story/viewer-gate pass or rights clearance. Engineering checks and the separate upload-copy evidence are recorded in the integration acceptance below; market acceptance remains **NOT_TESTED**.

## Review integration engineering acceptance - 2026-11-25 (Asia/Taipei)

Base Git SHA: `c99491c411fe42988eb9876be26392d5f2701368`; branch `codex/cluepause-static-ten-20261124`. Engineering acceptance **PASS** for this records/derivative scope: the [integration verifier](verify_review_integration.py) checks 938 pre-edit file hashes, unchanged files outside the seven authorized existing record/README edits, README changes limited to U01 rows, JSON/style/spoiler checks, master/copy/SRT hashes, format/duration equality, all U01 UTF-8 text including untracked files, Python syntax and portable paths. Results are saved in [review-integration-checks.json](review-integration-checks.json). Ordinary tracked Git diff and separate no-index checks for every untracked U01 text file both pass; the earlier tracked-only check did not supply that coverage. Normalizing the saved pytest transcript did not rerun pytest.

Commands from repository root:

```text
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/U01/revisions/v2/make_upload_copy.py
python -B experiments/cluepause/static-ten-20261124/uncanny_mystery/U01/revisions/v2/verify_review_integration.py
git -c core.excludesFile=NUL diff --check
# The verifier executes the following for every proposed untracked U01 text file:
git -c core.excludesFile=NUL -c core.autocrlf=false -c core.safecrlf=false diff --no-index --check -- NUL <file>
```

The [upload-copy evidence](../../../../../../../artifacts/static-ten-20261124/uncanny_mystery/uncanny-u01-v2/upload-copy.md) records the unchanged master and the separate `artifacts/static-ten-20261124/uncanny_mystery/uncanny-u01-v2/uncanny-u01-v2-upload.mp4`: **9,177,244 bytes**, SHA-256 `79b04a066320d7401ed07a968de812f34718347ba7c543c57ef723576fcdc666`. P01's two-pass method preserves 1080x1920, 30 fps, H.264 High/yuv420p, AAC 48 kHz stereo and **38.000000 s**; duration delta **0.000000 s**. Full audio/video decode and faststart pass. SSIM over all 1,140 frames: mean **0.994366**, minimum **0.989576**. No independent derivative review or human playback is claimed.

[upload-metadata-draft.json](../../upload-metadata-draft.json) contains the four audience-facing EN/zh-Hant fields, master/copy provenance and both unchanged timed SRT paths/hashes. The unnamed woman uses she/her; the hook states only the wet-shoes situation and withholds the cause and test. Its five `uploaded_file_*` fields follow P01's names and describe a prepared copy, **not a completed upload**.

Market acceptance **NOT_TESTED**; Story/Storyboard Gates **PENDING**, Viewer Gate **HUMAN_TEST_PENDING**, rights **pending_verification**. Human playback/listening, phone/caption-toggle acceptance, rights clearance, browser/YouTube processing and market measurement remain unverified. Root README `uv run --locked pytest`, `npm ci` / `npm run typecheck`, and governance verification were not rerun: no application, video project or governance code changed. No commit, push, upload, memory edit, master rerender or ImageGen was performed.

## Mechanism states, per-shot changes and transitions

The mechanism table and all eleven adjacent-cut observations (with residual continuity limits) are maintained in [mechanism.md](mechanism.md). OOF states are explicitly distinguished from direct visual evidence. The table is also included here for review.

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

Shared job validation: **VALID**. Final machine media QA: **PASS**, all 10 checks true, including full decode, expected video/frame/duration/audio, faststart, no embedded subtitles, both exact SRT comparisons and caption bounds. Source PCM is reused, not resynthesized: all nine original WAVs and all nine EN/zh-Hant narration lines match v1 byte-for-byte. All source/input, image result, conditioning-image and exact-prompt hashes match. See `verification.json`, `inspection.json`, and artifact `qa/report.json`, `manifest.json`, `assets.json`, `commands.jsonl`.

The main agent inspected **all 12 final decoded strips / 177 frames at 4.286 fps plus shot-end samples**, and the final silent storyboard. First-attempt strips and silent storyboard were also inspected before the permitted corrections. No white sheet-divider exposure or additional camera clipping of the rear vent/apron, hose attachments or side jet was observed in final samples. Shot-11 holds at 1.0 zoom; the other shots retain gentle 1.005-1.025 zoom. Generated column widths are unequal, so explicit measured whole-sheet crops in `crop-evidence.json` replace an equal-grid assumption. No painted water, digital paper patches or explanatory diagrams were added.

Opening question remains only at 1.0-3.5 s. The same question and non-reveal narration do not disclose the answer. Connector is inactive before 29 s. Reveal line-08 and its EN/zh-Hant captions run **29.000-32.610625 s**; line-09 runs **33.500-36.266458 s**. Pump sound/caption starts 29.1 s. Exact SRT-to-PCM schedule comparison and text inspection found no early answer disclosure; this is not ASR or human listening evidence.

Pipeline pytest: **33 passed in 0.53 s**, using the U01-specific cache/basetemp directories above; `pipeline-pytest.txt` contains the result. The initial test invocation had 31 fixture-setup errors and 2 passes because the basetemp parent did not exist; creating that parent fixed the setup and the same suite passed. The final audit's first path scan matched its own literal search pattern; splitting that literal fixed the scanner and it passed without changing media or story inputs.

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

**4 new built-in ImageGen calls / 4 bitmaps** for v2; cost **UNKNOWN**. Exactly one correction per sheet: mechanism attempts 1/2, resolution attempts 1/2. No API fallback or additional correction. Every call is recorded in `images.jsonl` and the artifact ledger; exact prompts and conditioning hashes are frozen in `image-prompts-used.json`. v1's historical five requests/four bitmaps remain unchanged; cumulative U01 history is nine requests/eight bitmaps, not four total.

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
