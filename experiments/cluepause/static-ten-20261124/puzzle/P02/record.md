# P02 — The Blackened Message — production record

Original fictional puzzle. Rights: pending_verification. No claim of a real event, person, business or external originality clearance.

A printmaker inks a hand-carved invitation block until its pale lettering disappears. The apparent vandalism is how she prints the invitation.

Story Quality Gate PENDING (no blind readers in this round).
Storyboard Quality Gate PENDING (primary-agent observations below are not independent approval).
Viewer Gate HUMAN_TEST_PENDING. Market acceptance NOT_TESTED.

## Delivered files and engineering acceptance

- MP4: `artifacts/static-ten-20261124/puzzle/puzzle-p02-static-v1/puzzle-p02-static-v1.mp4`
- Duration: 39 s; 1080×1920; 30 fps; H.264 High/yuv420p; AAC stereo 48 kHz; faststart.
- SHA-256: `7cae43e308ba383dcf62aa683151f95cc2186acf7d1674f3a8f844bdc4931865`
- EN sidecar: `artifacts/static-ten-20261124/puzzle/puzzle-p02-static-v1/puzzle-p02-static-v1.en.srt`
- zh-Hant sidecar: `artifacts/static-ten-20261124/puzzle/puzzle-p02-static-v1/puzzle-p02-static-v1.zh-Hant.srt`
- Source Git SHA: `aef24410f8b45c8651fd922343aeb52db11bfc75` (uncommitted genre additions; SHA identifies unchanged worktree base).
- Shared schema validator: VALID. Pipeline engineering result: PASS. Checks: video=True; frames=True; duration=True; audio=True; no_embedded_subtitles=True; faststart=True; full_decode=True; captions_en=True; captions_zh-Hant=True; caption_bounds=True.
- 178 dense decoded frames sampled every 7 video frames plus each shot’s last frame; all 8 timestamped strips personally inspected by the primary agent. Also inspected the ordered source `silent-storyboard.jpg` export. This is AI visual inspection, not human testing.
- Opening question only at 1.0–3.5 s; captions remain separate; photographed evidence text only P02 HOME.
- Alignment is measured trimmed PCM timing plus exact SRT-content/bounds comparison, not ASR, independent listening or human comprehension.

## Shot table: silent intent versus actual frames

The SILENT STORYBOARD check was written in story.md before the first ImageGen. State changes across cuts replace continuous character/object motion.

| Shot | Seconds | Function | Intended silent observation | Actual dense-frame / source observation |
| --- | --- | --- | --- | --- |
| shot-01 | 0–5 | establish | Maker blacks out a wooden message. | Same auburn maker inks raised wooden letters using brayer; block, face, cardigan and apron read clearly. |
| shot-02 | 5–10 | clue | Envelope and unique nick suggest a one-off invitation. | Envelope and partial letters visible, but right corner nick and end letters are clipped by cover crop. |
| shot-03 | 10–15 | clue | Backwards raised letters are fair evidence of a print matrix. | Raking macro shows raised M/O and ink on top; the reversed E and full word are outside crop, weakening the backwards-letter clue. |
| shot-04 | 15–21 | reaction | She calmly protects blank paper while ink darkens block. | Blank cream sheet remains clean; same maker holds it above half-inked block. |
| shot-05 | 21–27 | clue | Fully black surface appears ruined, paper remains blank. | Blackened block and blank sheet are visible. Raised lettering remains visibly legible by sheen; it has not literally vanished as narration says. |
| shot-06 | 27–30 | reveal | Paper contacts the relief. | Paper is pressed against block using wooden baren; action state is readable without words. |
| shot-07 | 30–33 | reveal | Peeling reveals a correct-direction printed word. | Corrected sheet puts peel in cell 0; whole HOME proof is readable in portrait crop, with fully black block below. |
| shot-08 | 33–39 | reveal | Finished invitation differs from apparent destroyed block. | Corrected cell 1 shows whole HOME and maker holding proof; black block below maintains inked state. Green-ribbon envelope mostly outside portrait crop. |

## Continuity and story-logic findings

Impact classes describe observed limitations; none is a gate decision. Hairstyles/clothes/identities generally match their canonical sheet. Minor pose, size and facial perspective changes between photographs are expected; failures of evidence/state are recorded explicitly.

| Timestamp(s), seconds | Impact class | Finding |
| --- | --- | --- |
| 5.0–15.0 | confusing | Central cover crop loses the distinctive nick and reversed E; central M/O alone do not establish backwards writing. |
| 0.0–27.0 | confusing | Brayer and raised type may expose printing explanation early; lettering remains visible at 21–27 despite narration saying it vanished. No reader evidence measures predictability. |
| 30.0–39.0 | cosmetic | Paper dimensions and block nick depiction vary slightly between stills; readable proof and fully black block state are retained after one correction. |

## Calls, timing and corrections

- ImageGen invocations: 4; completed images: 4; correction pass count: 1. Every accepted/rejected image has a ledger receipt; failed input validation has its own no-image entry.
- Local libx264 encode count: 8; final stream-copy/AAC mux recorded separately. One final master per story, preserved without replacement.
- Render invocation wall time: 49.063 s. Image dollar cost UNKNOWN (tool did not expose charges). Local Kokoro uses existing verified model bytes; no hosted TTS call. No dollar total invented.
- Elapsed input-creation to completed QA: 1193.9 s, from 2026-11-24T15:38:38.219806+00:00 to 2026-11-24T15:58:32.080568+00:00. This includes waiting while earlier stories were produced and is not active labor/provider latency. Late record writing is excluded. Pipeline wall time above is separately measured.
- Foley: deterministic local 24 kHz mono PCM tick/noise, mixed softly as snip or contact, with bilingual accessibility cue. It is synthetic foley; source room ambience and every original P01 needle/purse sound were not recreated.

One shots-b correction fixed ignored cell assignments, portrait proof legibility and black block state. Original rejected output preserved. Separately, initial audio scheduling failed before any encode because narration exceeded 36 s; final timeline extended to 39 s using copies of all seven already-trimmed PCM cues, without resynthesis.

Reference sheet was produced first. Shot sheets were conditioned on extracted canonical cells when at most five were required; P01/P04 used the whole six-cell reference sheet because the image tool accepts only five image paths. P02 correction additionally attached its already-inspected setup sheet. Prompt hashes and output hashes are in images.jsonl. No second correction loop was run.

## Measured narration / caption schedule

| Cue | Start s | End s | Trimmed PCM samples at 24 kHz | Reveal |
| --- | --- | --- | --- | --- |
| line-01 | 0.000 | 3.503 | 84076 | False |
| line-02 | 5.000 | 7.966 | 71175 | False |
| line-03 | 10.000 | 12.338 | 56109 | False |
| line-04 | 15.000 | 17.872 | 68917 | False |
| line-05 | 21.000 | 22.989 | 47746 | False |
| line-06 | 27.000 | 30.258 | 78199 | True |
| line-07 | 32.000 | 36.265 | 102368 | True |

The first reveal shot starts at 27 s. Audio and captions marked reveal are guarded against an earlier start. Foley has its own timed bilingual caption.

## Reproduction commands and unverified scope

From repository root, with existing local tool/model paths supplied by S2V environment variables (see ../README.md):

```powershell
& $env:S2V_RENDER_PYTHON -B experiments/cluepause/static-ten-20261124/puzzle/run.py validate experiments/cluepause/static-ten-20261124/puzzle/P02
& $env:S2V_RENDER_PYTHON -B experiments/cluepause/static-ten-20261124/puzzle/run.py run experiments/cluepause/static-ten-20261124/puzzle/P02
```

The run command was executed successfully for this master. It deliberately rejects replacing an existing MP4; reproduction requires a new revision id in an isolated copy. Detailed successful subprocess commands, exits, times and diagnostics: `artifacts/static-ten-20261124/puzzle/puzzle-p02-static-v1/commands.jsonl`. Technical probe, report, cost, source/tool hashes, source storyboard, image ledger and caption provenance all remain under this output folder.

Not verified: full spoken-audio listening in both caption modes, ASR, actual phone readability, blind story/visual comprehension, external originality/rights review, audience retention, market demand. No public/private upload, YouTube access, commit, push or memory modification. Core src/video/governance unchanged; full engine uv pytest/npm checks were not rerun for isolated content. Shared pipeline offline suite: 33 passed; pytest caches/temp confined to puzzle artifacts.
