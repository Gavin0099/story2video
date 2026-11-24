# P04 — The Rope He Refused to Pull — production record

Original fictional puzzle. Rights: pending_verification. No claim of a real event, person, business or external originality clearance.

A sailmaker cuts the rope holding a pennant low. A hidden sandbag falls along the opposite side of a simple pulley and raises the pennant; the cut removes a restraint.

Story Quality Gate PENDING (no blind readers in this round).
Storyboard Quality Gate PENDING (primary-agent observations below are not independent approval).
Viewer Gate HUMAN_TEST_PENDING. Market acceptance NOT_TESTED.

## Delivered files and engineering acceptance

- MP4: `artifacts/static-ten-20261124/puzzle/puzzle-p04-static-v1/puzzle-p04-static-v1.mp4`
- Duration: 39 s; 1080×1920; 30 fps; H.264 High/yuv420p; AAC stereo 48 kHz; faststart.
- SHA-256: `dae5314dea81cbb8c002c1e6fa247e34fd7de0768dc1d26d5d03da6100325bb4`
- EN sidecar: `artifacts/static-ten-20261124/puzzle/puzzle-p04-static-v1/puzzle-p04-static-v1.en.srt`
- zh-Hant sidecar: `artifacts/static-ten-20261124/puzzle/puzzle-p04-static-v1/puzzle-p04-static-v1.zh-Hant.srt`
- Source Git SHA: `aef24410f8b45c8651fd922343aeb52db11bfc75` (uncommitted genre additions; SHA identifies unchanged worktree base).
- Shared schema validator: VALID. Pipeline engineering result: PASS. Checks: video=True; frames=True; duration=True; audio=True; no_embedded_subtitles=True; faststart=True; full_decode=True; captions_en=True; captions_zh-Hant=True; caption_bounds=True.
- 178 dense decoded frames sampled every 7 video frames plus each shot’s last frame; all 8 timestamped strips personally inspected by the primary agent. Also inspected the ordered source `silent-storyboard.jpg` export. This is AI visual inspection, not human testing.
- Opening question only at 1.0–3.5 s; captions remain separate; photographed evidence text only P02 HOME.
- Alignment is measured trimmed PCM timing plus exact SRT-content/bounds comparison, not ASR, independent listening or human comprehension.

## Shot table: silent intent versus actual frames

The SILENT STORYBOARD check was written in story.md before the first ImageGen. State changes across cuts replace continuous character/object motion.

| Shot | Seconds | Function | Intended silent observation | Actual dense-frame / source observation |
| --- | --- | --- | --- | --- |
| shot-01 | 0–5 | establish | Maker holds scissors beside a low flag. | Maker, orange scissors and low flag visible. Flag tip near right crop edge, circle and both eyelets retained. |
| shot-02 | 5–10 | clue | Taut rope and low pennant suggest jam. | Taut cream line, blue restraint and low flag show clearly. Flag edge is partly clipped but identity marker remains. |
| shot-03 | 10–16 | reaction | Maker studies rig rather than pulling. | Maker studies rig, does not pull. Teal shirt, beige trousers and wavy dark hair match reference. |
| shot-04 | 16–22 | clue | Two rope legs run over pulley, blue restraint differs. | Two rope legs and brass pulley visible; right rope disappears behind bench apron, with bag concealed. |
| shot-05 | 22–27 | clue | Only blue restraint is cut; cream running rope stays intact. | Scissors, severed blue tip and intact cream line visible. Cut is a frozen after-state; lower flag eyelet remains above. |
| shot-06 | 27–30 | reveal | Opposite end is weighted by falling bag. | Corrected tight reveal shows tan X-stitched bag on floor and right cream rope; contradictory low flag removed. |
| shot-07 | 30–33 | reveal | Flag has risen as counterweight has fallen. | Flag is now high, but left cream tail still appears to reach bench cleat; bag itself is below portrait crop. Intended complete rig is incomplete in output. |
| shot-08 | 33–39 | reaction | Maker shows empty hands below raised pennant. | Maker open hands, scissors on bench and high flag visible. Left cream tail still at cleat, bag cropped below frame. Flag-to-floor-bag causality is inferred across cuts. |

## Continuity and story-logic findings

Impact classes describe observed limitations; none is a gate decision. Hairstyles/clothes/identities generally match their canonical sheet. Minor pose, size and facial perspective changes between photographs are expected; failures of evidence/state are recorded explicitly.

| Timestamp(s), seconds | Impact class | Finding |
| --- | --- | --- |
| 0.0–10.0 | cosmetic | Flag tip cropped at right edge; circle and two eyelets still readable. |
| 22.0–27.0 | confusing | Blue snip is readable but relation of loose cream tail to the blue knot is not fully resolved in the still. |
| 30.0–39.0 | breaks story logic | After flag rises, left running-rope tail still reaches/appears anchored at original bench cleat. A fixed flag on that same rope should carry its free lower tail upward too. The added/remaining rope length makes the demonstrated counterweight state inconsistent. |
| 30.0–39.0 | confusing | Floor bag is outside portrait crop; no final decoded frame shows high pennant and floor bag together. Separate close-up and high-flag cuts carry only part of the intended causal proof. |

## Calls, timing and corrections

- ImageGen invocations: 4; completed images: 4; correction pass count: 1. Every accepted/rejected image has a ledger receipt; failed input validation has its own no-image entry.
- Local libx264 encode count: 8; final stream-copy/AAC mux recorded separately. One final master per story, preserved without replacement.
- Render invocation wall time: 65.421 s. Image dollar cost UNKNOWN (tool did not expose charges). Local Kokoro uses existing verified model bytes; no hosted TTS call. No dollar total invented.
- Elapsed input-creation to completed QA: 1695.9 s, from 2026-11-24T15:38:38.226817+00:00 to 2026-11-24T16:06:54.169320+00:00. This includes waiting while earlier stories were produced and is not active labor/provider latency. Late record writing is excluded. Pipeline wall time above is separately measured.
- Foley: deterministic local 24 kHz mono PCM tick/noise, mixed softly as snip or contact, with bilingual accessibility cue. It is synthetic foley; source room ambience and every original P01 needle/purse sound were not recreated.

One shots-a correction replaced the floor-bag plus still-low-flag contradiction with a tight bag-only shot. Original rejected sheet retained. Remaining left-tail/final-crop defect was not corrected again.

Reference sheet was produced first. Shot sheets were conditioned on extracted canonical cells when at most five were required; P01/P04 used the whole six-cell reference sheet because the image tool accepts only five image paths. P02 correction additionally attached its already-inspected setup sheet. Prompt hashes and output hashes are in images.jsonl. No second correction loop was run.

## Measured narration / caption schedule

| Cue | Start s | End s | Trimmed PCM samples at 24 kHz | Reveal |
| --- | --- | --- | --- | --- |
| line-01 | 0.000 | 2.530 | 60728 | False |
| line-02 | 5.000 | 7.944 | 70660 | False |
| line-03 | 10.000 | 12.766 | 66381 | False |
| line-04 | 16.000 | 19.914 | 93940 | False |
| line-05 | 22.000 | 23.311 | 31459 | False |
| line-06 | 27.000 | 30.170 | 76076 | True |
| line-07 | 32.000 | 34.663 | 63912 | True |

The first reveal shot starts at 27 s. Audio and captions marked reveal are guarded against an earlier start. Foley has its own timed bilingual caption.

## Reproduction commands and unverified scope

From repository root, with existing local tool/model paths supplied by S2V environment variables (see ../README.md):

```powershell
& $env:S2V_RENDER_PYTHON -B experiments/cluepause/static-ten-20261124/puzzle/run.py validate experiments/cluepause/static-ten-20261124/puzzle/P04
& $env:S2V_RENDER_PYTHON -B experiments/cluepause/static-ten-20261124/puzzle/run.py run experiments/cluepause/static-ten-20261124/puzzle/P04
```

The run command was executed successfully for this master. It deliberately rejects replacing an existing MP4; reproduction requires a new revision id in an isolated copy. Detailed successful subprocess commands, exits, times and diagnostics: `artifacts/static-ten-20261124/puzzle/puzzle-p04-static-v1/commands.jsonl`. Technical probe, report, cost, source/tool hashes, source storyboard, image ledger and caption provenance all remain under this output folder.

Not verified: full spoken-audio listening in both caption modes, ASR, actual phone readability, blind story/visual comprehension, external originality/rights review, audience retention, market demand. No public/private upload, YouTube access, commit, push or memory modification. Core src/video/governance unchanged; full engine uv pytest/npm checks were not rerun for isolated content. Shared pipeline offline suite: 33 passed; pytest caches/temp confined to puzzle artifacts.
