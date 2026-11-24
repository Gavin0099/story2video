# Genre pilot production — 2026-11-24

## Private upload attempt — blocked before Studio access

2026-11-24 (Asia/Taipei), Owner authorized the three rendered genre pilots for **PRIVATE only** uploads to CluePause (`@CluePause`, `UCG_nXXBzgg54w2zhkZ33Row`), conditional on Studio quota checks, using the already signed-in Chrome plugin session. **0 uploads and 0 upload attempts.** Browser runtime setup failed twice because `<Codex browser plugin cache>/26.1106.51428/scripts/browser-service.mjs` is missing; a read-only `Test-Path` also returned `False`. No Studio tab could be inspected. This is a local browser runtime failure, not an observed YouTube quota refusal. No login, account/channel setting, visibility, schedule, playlist, comment or external video action occurred. No commit or push was made.

[upload.json](upload.json) records the authorization, exact error, local metadata drafts and hashes. All remote result fields are null. Based on the previous publication's `master_sha256` bindings and `engineering.md` distinction between masters, selectable-track copies and burned review copies, the prepared upload candidates are the **plain masters**, with English and Traditional Chinese SRTs uploaded separately. Both MP4 variants and both final SRTs for each pilot were hashed: **12/12 match** the manifest referenced above; the three `-cc.mp4` hashes also match this document's delivery table. Prepared settings follow the earlier uploads: English (United States) primary metadata, Traditional Chinese title/description translation, both selectable caption tracks, AI/synthetic disclosure **Yes**, audience **not made for kids**, **Private** visibility. Metadata marks each story as fiction and adds no links or hashtags. These are prepared values, not saved Studio values; script rights and human/genre gates retain their earlier pending status.

Engineering verification at Git SHA `da4bb2cb1abba65baf94e454707efb61f03fd8f6`:

| Command | Result |
| --- | --- |
| `python.exe -B -X utf8 artifacts/genre-pilot-20261124/upload-preflight.py` | exit 0; 12 matched hashes, three bilingual metadata drafts, zero upload attempts |
| `uv sync --locked` | exit 0 |
| `uv run --locked pytest --basetemp=D:/s2v-gp/artifacts/genre-pilot-20261124/upload-pytest-tmp` | exit 0; 61 passed in 4.51 s; one pytest-cache permission warning |
| `npm.cmd ci` in `video/` | initial exit -4048: default user npm cache EPERM; following typecheck exit 1 because `tsc` was unavailable |
| `npm.cmd ci --offline` in `video/`, `npm_config_cache=D:/s2v-gp/artifacts/npm-cache` | exit 0; existing Node 24.13.0 versus required Node 22 warning |
| `npm.cmd run typecheck` after the workspace-cache install | exit 0 |
| `python.exe -B -X utf8 artifacts/genre-pilot-20261124/verify-delivery.py` | exit 0; three pilots, 33 bound files consistent |

The Python executable above is `D:/story2video/artifacts/python/cpython-3.13-windows-x86_64-none/python.exe`; uv is `D:/story2video/artifacts/tooling/bin/uv.exe`. Exact environment and initial commands are in [upload-acceptance.ps1](../../../artifacts/genre-pilot-20261124/upload-acceptance.ps1); all initial failures and successful follow-up logs are retained as `artifacts/genre-pilot-20261124/upload-*.log`. No application, renderer, Episode schema or governance source changed.

**Unverified:** signed-in channel, daily quota/verification warnings, remote duplicate/draft state, video IDs, saved Private visibility, metadata translations, caption tracks, AI disclosure, audience, processing and Studio playback. **Market acceptance:** all three remain `HUMAN_TEST_PENDING`; no public or market result is claimed. Resumption requires repairing/reinstalling the Browser plugin through the plugin UI and reconnecting the existing Chrome session, then checking channel, duplicates and quota before any upload.

**Resumed outcome: 3/3 local pilots rendered; runtime blocker resolved. HUMAN_TEST_PENDING for all three. No commit.**

The added base-interpreter access allows the existing read-only render-venv to start. The exact old preflight now imports the packages but exits 1 only because `kokoro_onnx` has no `__version__` attribute. A corrected metadata-based preflight exits 0: Python **3.12.10**, kokoro-onnx **0.6.1**, onnxruntime **1.26.0**, numpy **2.5.5**. A real local Kokoro test produced **56,832 samples at 24 kHz**. This replaces the old access-blocker diagnosis; no environment repair or installation was needed. Exact argv, stdout, stderr, model/tool checks and unchanged reference-file hashes are in [preflight-resume.json](../../../artifacts/genre-pilot-20261124/preflight-resume.json).

This continuation used checkout `D:/s2v-gp`, branch `codex/cluepause-genre-pilot-20261124`, SHA `004fbea349a7ef246786b189140f17f456d2ff0f`, with this document uncommitted. The three source scripts remain byte-for-byte unchanged. `D:/story2video` and `<Owner's Python 3.12 install>` were treated as **READ ONLY**: no install, modification or deletion there. Python ran with `-B`. No credentials, paid API, substitute speech/image service, upload, Studio operation, visibility change, scheduling, publication or commit was used.

### Final delivery

The `-cc.mp4` files below contain **1080×1920, 30 FPS H.264 video, 48 kHz stereo AAC audio and selectable English/Traditional Chinese mov_text subtitle tracks**. English captions and a persistent **FICTION／虛構 • PRIVATE PILOT** label are also burned in. Each folder additionally contains its plain master, `*.en.srt`, `*.zh-Hant.srt`, real narration and mixed WAV, ImageGen sheet, timeline, exact FFmpeg/ffprobe command log, final QA and decoded evidence frames.

| Pilot | Local delivery | Measured duration / frames | EN + zh-Hant SRT cues |
| --- | --- | --- | --- |
| P01 / puzzle | [puzzle-cc.mp4](../../../artifacts/genre-pilot-20261124/puzzle/puzzle-cc.mp4) | 42.000 s / 1,260 | 13 each |
| U01 / uncanny_mystery | [uncanny_mystery-cc.mp4](../../../artifacts/genre-pilot-20261124/uncanny_mystery/uncanny_mystery-cc.mp4) | 43.000 s / 1,290 | 12 each |
| H01 / urban_horror | [urban_horror-cc.mp4](../../../artifacts/genre-pilot-20261124/urban_horror/urban_horror-cc.mp4) | 44.000 s / 1,320 | 18 each |

| Delivery | SHA-256 |
| --- | --- |
| puzzle-cc.mp4 | `626be86b8276ac7b6344752dd4f48cabb7595c54f146900d0db9c48db968a256` |
| uncanny_mystery-cc.mp4 | `632e7c5ce20aa405fee04f12005a1c50e10131211a11ca878442bb68a65af847` |
| urban_horror-cc.mp4 | `de40ad8af58d5663f1f9ecfc18a2ac76d21530ef9ff5c3e02061111d8d6b823e` |

[media-manifest.json](../../../artifacts/genre-pilot-20261124/media-manifest.json) binds final MP4s, SRTs, audio, sheets, timeline, QA and command logs by SHA-256. Plain-master hashes are also recorded there.

### Actual timeline and media acceptance

Onsets below were checked against decoded final-video **PTS**, with adjacent-frame evidence, rather than copied from the target table. They mark the edited visual/narrative onset; they do not measure when a new viewer recognizes the clue.

| Pilot | First visible anomaly: target → actual | Key clue / pressure: target → actual | Reveal consequence: target → actual |
| --- | --- | --- | --- |
| P01 | about 1 s → **1.000 s**, high/low needle cut, same three gold pieces | 14–21 s → **14.000 s**, seller pulling thread | 26–37 s → **26.000 s**, tray attachment cutaway |
| U01 | about 1 s → **0.000 s**, locked dripping cabinet already visible | 14–21 s → **14.000 s**, plant/timer/tube view and 6:00 AM label | 27–38 s → **27.000 s**, cracked-joint spray first appears |
| H01 | about 1 s → **0.000 s**, glowing intercom; rule title at **1.000 s** | 18–24 s → **18.000 s**, mimicry-pressure beat; sound motif at **18.120 s** | 29–36 s → **29.000 s**, consequence shot/narration; saved-word text cut at **29.700 s**, lock sound at **29.750 s** |

All three pass full audio/video decode, exact frame count, 9:16 format, duration, blackdetect, silencedetect, integrated-loudness and true-peak checks. Measured output levels are **−17.79 / −17.17 / −17.47 LUFS** for P/U/H; exact true peaks and signal logs are in each QA record. Both SRTs per film pass ffprobe packet timing checks and exact MP4-to-SRT round-trip comparison. Sentence subtitle boundaries come from actual threshold-trimmed Kokoro PCM, rounded to 30 FPS; independent forced alignment/listening is not claimed. The horror film's three audible invitation echoes have corresponding subtitle cues.

The main agent inspected all generated sheets, final contact sheets, the puzzle needle transition and the horror text-cut boundary. The sheets show no gore or injuries. Independent continuous playback, phone readability, realistic sound recognition, viewer comprehension and perfect physical continuity remain unverified.

- [P01 media QA and deviations](../../../artifacts/genre-pilot-20261124/puzzle/media-qa.md)
- [U01 media QA and deviations](../../../artifacts/genre-pilot-20261124/uncanny_mystery/media-qa.md)
- [H01 media QA and deviations](../../../artifacts/genre-pilot-20261124/urban_horror/media-qa.md)

### Production method and deviations

The continuation follows the referenced `engineering.md` / `make.py` approach: built-in **ImageGen** storyboard sheets, cropped panels with gradual zoom, local **Kokoro** English narration, timed local sound synthesis, FFmpeg composition, dual subtitles and final probing. It imports the existing tested `private-five/build.py` and its pinned media helper read-only. A workspace wrapper confines subprocess working directories and outputs to this checkout, logs exact argv/results, and adds fiction/evidence overlays. It does not invoke the old batch's story-gate loader or claim that these new stories passed it.

Four built-in ImageGen requests were used: three initial sheets plus a puzzle correction to stabilize the three gold pieces and lower-needle state. Prompts are saved in [imagegen-prompts.json](../../../artifacts/genre-pilot-20261124/imagegen-prompts.json) and [imagegen-correction-prompt.json](../../../artifacts/genre-pilot-20261124/imagegen-correction-prompt.json). No standalone paid image/speech API was invoked; built-in account usage has no available per-request monetary amount. TTS/render external API cost is zero.

Original narration and translation wording is retained; Chinese cues are split where needed. Local Kokoro uses `af_heart`, speed **0.95 / 1.0 / 1.0** for P/U/H. Actual narration lengths are **22.903 / 24.262 / 24.642 s**; holds preserve the script's evidence-reading windows. Full evidence panels are fitted over a blurred enlarged crop with **3.5% gradual zoom** so the scale, tube or door is not lost to portrait cropping.

Material visual deviations, also recorded per pilot:

- **P01:** The needle changes by an illustrated before/after cut at 1 s, rather than continuous rotation. Gold count now stays at three, but scale/camera geometry varies slightly. The reveal shows the tray endpoint, while the thread route through the scale interior and the after-cut loose ends remain less explicit than requested. The reveal holds a cutaway and returns to scissors/lower reading at 37 s; it does not show a continuous snip replay.
- **U01:** The anomaly starts at 0 s. The question uses a night-before dry comparison; the 21–27 s investigation reuses the wet-tray evidence with a next-morning label instead of animating the tray pull. A first-render spoiler was corrected by withholding the spray shot until 27 s. The timer time is a large editorial label; the rear route is partly obscured. Small droplets on rubber toe caps weaken the script's strictly dry-upper distinction. Valve closure and next-morning dry shoes share one labeled comparison image.
- **H01:** The anomaly starts at 0 s. Rule/saved-word text is an editorial overlay instead of being tracked onto the illustrated screen. The prefix disappears by a hard cut at 29.7 s instead of fading. Nia's hand lowering and latch retraction are not continuously animated. A soft synthesized two-pulse cough motif needs human recognition testing. Door pressure uses a held illustration, local Kokoro invitation echoes and a final thump.

These are local production candidates with documented limits, not rights-approved or quality-gate-approved releases. The puzzle 90-point gate is unchanged; no independent scores or new genre-gate approvals are claimed.

### Exact commands and repo acceptance

[production-commands.ps1](../../../artifacts/genre-pilot-20261124/production-commands.ps1) records the top-level commands. Each folder's `commands-resume.json` records exact final-render and QA FFmpeg/ffprobe argv, working directory, exit code, stdout and stderr. The production implementation is [produce.py](../../../artifacts/genre-pilot-20261124/produce.py). The final binding/preflight writer is [finalize-resume.py](../../../artifacts/genre-pilot-20261124/finalize-resume.py).

```powershell
$py='D:/story2video/artifacts/render-venv/Scripts/python.exe'
$batch='D:/s2v-gp/artifacts/genre-pilot-20261124'
& $py -B -X utf8 "$batch/preflight-resume.py"
& $py -B -X utf8 "$batch/produce.py" audio
# Run each render and qa command for puzzle, uncanny_mystery and urban_horror:
& $py -B -X utf8 "$batch/produce.py" render puzzle
& $py -B -X utf8 "$batch/produce.py" qa puzzle
& $py -B -X utf8 "$batch/produce.py" render uncanny_mystery
& $py -B -X utf8 "$batch/produce.py" qa uncanny_mystery
& $py -B -X utf8 "$batch/produce.py" render urban_horror
& $py -B -X utf8 "$batch/produce.py" qa urban_horror
& $py -B -X utf8 "$batch/finalize-resume.py"
```

README acceptance reran against SHA `004fbea349a7ef246786b189140f17f456d2ff0f`. All exit 0:

| Command | Outcome / evidence |
| --- | --- |
| `uv sync --locked` | pass, `resume-uv-sync.log` |
| `uv run --locked pytest --basetemp=D:/s2v-gp/artifacts/genre-pilot-20261124/resume-pytest-tmp` | **61 passed in 4.64 s**, `resume-pytest.log` |
| `npm.cmd ci` in `video/` | pass, `resume-npm-ci.log`; existing Node 24.13.0 versus required Node 22 warning remains |
| `npm.cmd run typecheck` in `video/` | pass, `resume-typecheck.log` |
| `git diff --check` | pass |
| `& 'D:/story2video/artifacts/render-venv/Scripts/python.exe' -B -X utf8 'D:/s2v-gp/artifacts/genre-pilot-20261124/verify-delivery.py'` | pass: 3 pilots, 33 bound files; format, subtitle streams, cues, hashes and QA status consistent |

[acceptance-resume.ps1](../../../artifacts/genre-pilot-20261124/acceptance-resume.ps1) preserves UV/Python/temp settings, with caches/temp confined to this checkout. No application source, video source, Episode contract, schema or framework version changed. Governance verification and framework updates were not part of this production task.

**Human/market acceptance:** still **HUMAN_TEST_PENDING** for all three. No independent rights approval, story/genre-gate approval, human viewing/recruitment, upload, public experiment, D1/D7 data or genre winner is claimed. Only local engineering/media checks completed. No commit was made.

## Previous attempt — historical record, superseded by the resumed outcome above

**Previous attempt: 0/3 rendered; 3/3 blocked. HUMAN_TEST_PENDING for all three.**

Owner's current instruction authorizes local production of the three private pilots using the existing CluePause flow. It supersedes the earlier planning-only production boundary in this directory. No upload, Studio operation, visibility change, scheduling, publishing, channel creation or commit was performed. The puzzle 90-point gate is unchanged; no independent scores, rights approval, genre-gate approval or human-test results are claimed.

Production checkout: `D:/s2v-gp`, branch `codex/cluepause-genre-pilot-20261124`, Git SHA `004fbea349a7ef246786b189140f17f456d2ff0f`. The source scripts were preserved byte for byte. All generated records and draft subtitles are under the gitignored `artifacts/genre-pilot-20261124/` directory. This document is the committable summary; it has not been committed.

## Existing production flow found

The published R01–R09 production record is [retention-ten-public README](../retention-ten-public-20261124/README.md), with its film hashes in [media-manifest.json](../retention-ten-public-20261124/media-manifest.json). Read-only implementation references in the Owner's main checkout:

- `D:/story2video/artifacts/cluepause-retention-ten/engineering.md` and `make.py`: ImageGen storyboard sheets, cropped shots with gradual zoom, local Kokoro English narration, timed sound cues, and FFmpeg composition. The sampled R01 configuration uses `af_heart`, speed `0.83`; these are reference settings, not settings used to produce these pilots.
- `D:/story2video/artifacts/private-five/build.py`: hash-bound models and art; sentence-level TTS trimming; a 30 FPS timeline based on actual synthesized samples and holds; English and Traditional Chinese SRT; 1080×1920 H.264/AAC output; local selectable subtitle tracks and subtitle round-trip checks. Render QA checks full decode, black/silent intervals, loudness, true peak, frame count and duration. `make.py` adds Traditional Chinese burned-in review copies and evidence frames.
- `D:/story2video/artifacts/04-v7-pilot/render.py`: pinned FFmpeg/ffprobe executable sizes and SHA-256, encoding settings, and tool validation.
- [Hook v2 record](../hook-v2-private-20261123/README.md) and `D:/story2video/artifacts/26m-hook-v2/render.py`: a revision of an existing 54.8 s, 720×1280 film, preserving 1,499 decoded frames after its opening edit; its narration is reused from that existing film. It is an editing reference, not new narration for these scripts.

`D:/story2video` was used read-only. Its observed branch and HEAD were `codex/threads-science-comic-20261123` and `82d55304cc00b385133341a8b9cb879f6791be52`. No branch change, environment repair or file edit was made there. Reference-file and executable hashes are preserved in [preflight.json](../../../artifacts/genre-pilot-20261124/preflight.json).

## Shared blocker: existing narration runtime unavailable

The existing verified environment is `D:/story2video/artifacts/render-venv`. Its `pyvenv.cfg` points to Python 3.12.10 at `<Owner's Python 3.12 install>/python.exe`. This session cannot access that base directory. The exact preflight command, run from `D:/s2v-gp/artifacts/genre-pilot-20261124`, was:

```powershell
& 'D:/story2video/artifacts/render-venv/Scripts/python.exe' -B -c 'import sys; import numpy; import kokoro_onnx; print(sys.version); print(numpy.__version__); print(kokoro_onnx.__version__)'
```

It exited **101**, reporting `Unable to create process using` the base Python path. Existing package metadata in that environment identifies `kokoro-onnx 0.6.1`, `onnxruntime 1.26.0`, and `numpy 2.5.5`; their imports could not be verified because the interpreter never started.

The existing accessible Python 3.13.18 under `D:/story2video/artifacts/python/` runs, but its preflight reports `kokoro_onnx=False`, `onnxruntime=False`, `numpy=False`. Read-only inspection found those packages only in the unusable render environment. No different speech service, new speech environment, paid API or credentials were used. No ImageGen request was made after discovering that narration could not run.

**Missing to resume:** execution access to the existing Python 3.12.10 base interpreter and its runtime files, allowing the already-tested `render-venv` to launch. This is an environment-access blocker, not a missing model or FFmpeg binary. The two Kokoro model files are readable and their SHA-256 values match the existing bindings; FFmpeg and ffprobe hashes also match their pinned bindings, and ffprobe runs successfully. Changing session access or repairing the Owner's checkout was not attempted.

## Per-pilot result and QA

All timestamp values below are **script targets**, not measured frames or speech. No MP4 exists, so actual duration, first visible anomaly, key clue and reveal timestamps are **NOT_MEASURED**, and each MP4 SHA-256 is **NOT_AVAILABLE**.

| Series / pilot | Status | Duration target | Anomaly target | Key clue target | Reveal target | MP4 SHA-256 | Human status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| puzzle / P01 | blocked | 42 s | about 1 s | 14–21 s | 26–37 s | NOT_AVAILABLE | HUMAN_TEST_PENDING |
| uncanny_mystery / U01 | blocked | 43 s | about 1 s | 14–21 s | 27–38 s | NOT_AVAILABLE | HUMAN_TEST_PENDING |
| urban_horror / H01 | blocked | 44 s | about 1 s | 18–24 s | 29–36 s | NOT_AVAILABLE | HUMAN_TEST_PENDING |

Each series folder contains `source-script.md`, `script-targets.json`, `draft.en.srt`, `draft.zh-Hant.srt`, both `draft.*.ffprobe.json` files, `media-qa.md`, `qa.json`, and `commands.json`:

- [puzzle QA](../../../artifacts/genre-pilot-20261124/puzzle/media-qa.md)
- [uncanny_mystery QA](../../../artifacts/genre-pilot-20261124/uncanny_mystery/media-qa.md)
- [urban_horror QA](../../../artifacts/genre-pilot-20261124/urban_horror/media-qa.md)

The six **draft** SRT files retain the supplied English and Traditional Chinese wording; `／` becomes a line break. ffprobe reads **7 subtitle packets per file**, starting at 0 s and ending at 42 / 43 / 44 s respectively. Every interval has positive duration, is monotonic and nonoverlapping, matches its script beat, and stays within the script duration target. These checks verify draft file structure only. The SRTs are **not aligned to recorded speech, final subtitles, or MP4 subtitle tracks**. In particular, the horror script's longer three-line cues still need production-time segmentation and readability review.

| Source script | Frozen file SHA-256 |
| --- | --- |
| puzzle.md | `ab9c4a5d638d79cc50ffbf218f419f53b990d10fc00706e273f5ff206d8e12be` |
| uncanny_mystery.md | `18ebf21fc44cd334a270b1af15cc88dcbaf171a81b8b9b6fc48d3f86c632e7c7` |
| urban_horror.md | `cafab26d34f4eea385704517cdb95edb8fd3c3241f073bd205da3183ed4597a3` |

Deviations: **no script edits or shot/timing substitutions**. Delivery is incomplete: no images, narration, sound mix, MP4 or final subtitles were produced. Rendered fiction labeling and no-gore presentation remain unverified because there are no rendered visuals; the supplied scripts remain explicitly fictional. Source rights status remains `pending_verification`.

## Commands and engineering acceptance

[commands.json](../../../artifacts/genre-pilot-20261124/commands.json) and each series' `commands.json` preserve exact argv, working directory, exit code, stdout and stderr for runtime preflight and subtitle probes. [prepare_delivery.py](../../../artifacts/genre-pilot-20261124/prepare_delivery.py) records source hashes and writes the blocked records; it does not render or synthesize media. Its successful invocation from `D:/s2v-gp` was:

```powershell
& 'D:/story2video/artifacts/python/cpython-3.13-windows-x86_64-none/python.exe' -B -X utf8 'D:/s2v-gp/artifacts/genre-pilot-20261124/prepare_delivery.py'
```

README acceptance was executed against SHA `004fbea349a7ef246786b189140f17f456d2ff0f`, with no application or video source changes. Exact commands and environment settings are in [acceptance-commands.ps1](../../../artifacts/genre-pilot-20261124/acceptance-commands.ps1); logs are alongside it.

| Command | Result |
| --- | --- |
| `uv sync --locked` | exit 0 |
| `uv run --locked pytest` | exit 1: 40 passed, 21 fixture setup errors caused by the default temporary directory's permissions; retained in `pytest.log` |
| `uv run --locked pytest --basetemp=D:/s2v-gp/artifacts/genre-pilot-20261124/pytest-tmp` | exit 0: **61 passed**, with the temporary directory confined to this checkout |
| `npm.cmd ci` in `video/` | exit 0; Node 24.13.0 gives the existing engine warning for required Node 22 |
| `npm.cmd run typecheck` in `video/` | exit 0 |
| `git diff --check` | exit 0 |

Engineering acceptance of the existing repo checks does **not** establish media acceptance. No rendered format, full media decode, actual cue timestamps, clipping, loudness, silence, visual continuity, spoiler timing, subtitle font, subtitle/audio sync or phone playback could be checked. Governance contracts and framework version were unchanged; governance verification and framework updates were not run.

## Human and market acceptance

**HUMAN_TEST_PENDING** for P01, U01 and H01. No independent reader assessment, human viewing, recruitment, private upload, public experiment or D1/D7 market observation was performed. No genre winner, demand, retention, comprehension, rights approval or quality-gate pass is inferred from script targets or draft subtitle checks. Producing or approving a local pilot does not authorize publication.
