# P03 — The Crack That Crossed the Table — production record

Original fictional puzzle. Rights: pending_verification. No claim of a real event, person, business or external originality clearance.

A buyer chooses a vase with an apparent black crack. The line continues across the table, and blocking light reveals it is a suspended wire’s shadow.

Story Quality Gate PENDING (no blind readers in this round).
Storyboard Quality Gate PENDING (primary-agent observations below are not independent approval).
Viewer Gate HUMAN_TEST_PENDING. Market acceptance NOT_TESTED.

Status: **HOLD (not uploaded)**. Independent review on 2026-11-25 identified a blocking optical story-logic failure in the retained master; engineering PASS does not clear it.

## Delivered files and engineering acceptance

- MP4: `artifacts/static-ten-20261124/puzzle/puzzle-p03-static-v1/puzzle-p03-static-v1.mp4`
- Duration: 39 s; 1080×1920; 30 fps; H.264 High/yuv420p; AAC stereo 48 kHz; faststart.
- SHA-256: `f5b62dbca0b8f5a0490b1fbd96cd7a808dd64cb44732e0e925b07d5441ec9ff9`
- EN sidecar: `artifacts/static-ten-20261124/puzzle/puzzle-p03-static-v1/puzzle-p03-static-v1.en.srt`
- zh-Hant sidecar: `artifacts/static-ten-20261124/puzzle/puzzle-p03-static-v1/puzzle-p03-static-v1.zh-Hant.srt`
- Source Git SHA: `aef24410f8b45c8651fd922343aeb52db11bfc75` (uncommitted genre additions; SHA identifies unchanged worktree base).
- Shared schema validator: VALID. Pipeline engineering result: PASS. Checks: video=True; frames=True; duration=True; audio=True; no_embedded_subtitles=True; faststart=True; full_decode=True; captions_en=True; captions_zh-Hant=True; caption_bounds=True.
- 178 dense decoded frames sampled every 7 video frames plus each shot’s last frame; all 8 timestamped strips personally inspected by the primary agent. Also inspected the ordered source `silent-storyboard.jpg` export. This is AI visual inspection, not human testing.
- Opening question only at 1.0–3.5 s; captions remain separate; photographed evidence text only P02 HOME.
- Alignment is measured trimmed PCM timing plus exact SRT-content/bounds comparison, not ASR, independent listening or human comprehension.

## Shot table: silent intent versus actual frames

The SILENT STORYBOARD check was written in story.md before the first ImageGen. State changes across cuts replace continuous character/object motion.

| Shot | Seconds | Function | Intended silent observation | Actual dense-frame / source observation |
| --- | --- | --- | --- | --- |
| shot-01 | 0–5 | establish | Buyer selects apparently cracked vase. | Both people, ivory vase and diagonal line are visible. The thin line already looks like a shadow; alternative cracked-vase inference may be weak. |
| shot-02 | 5–10 | reaction | Buyer confidently insists without repair. | Buyer insists with open hand; potter looks puzzled. Same navy clothing, rust apron, hair and faces. |
| shot-03 | 10–16 | clue | Line continues seamlessly off vase onto tabletop. | Blue dot and line passing to its right are clear. Continuation onto tabletop is less obvious after portrait crop. |
| shot-04 | 16–21 | clue | Wire mobile sits between window and vase. | Same wire ring, brass disk, window direction and vase visible; tabletop continuation can be seen at bottom. |
| shot-05 | 21–27 | reaction | Hand approaches light beam without touching ceramic. | Hand approaches without contact; line still visible, blue dot and vase geometry stable. |
| shot-06 | 27–30 | reveal | Blocking light removes the thin line. | The wire shadow disappears on still-lit neck/right-side areas outside the new hand shadow, while the vase, blue dot and mobile remain in place. This contradicts the optical explanation. |
| shot-07 | 30–33 | reveal | Smooth vase shows no repair or break. | Buyer holds apparently smooth vase away from wire. Right contour is clipped in portrait crop, limiting whole-surface inspection. |
| shot-08 | 33–39 | reveal | Shadow remains on empty tabletop while vase leaves. | Buyer holds vase and potter smiles. Wire remains above. Most empty tabletop/shadow is lost below portrait crop; closing proof relies on prior hand-shadow shot. |

## Continuity and story-logic findings

Impact classes describe observed limitations; none is a gate decision. Hairstyles/clothes/identities generally match their canonical sheet. Minor pose, size and facial perspective changes between photographs are expected; failures of evidence/state are recorded explicitly.

| Timestamp(s), seconds | Impact class | Finding |
| --- | --- | --- |
| 0.0–21.0 | confusing | Line has a visibly shadow-like softness and mobile is shown early, so the apparent-crack alternative may not hold. No blinded evidence collected. |
| 10.0–16.0; 33.0–39.0 | confusing | Portrait cover reduces tabletop continuation in close-up and removes most final empty-table shadow proof. |
| 27.0–30.0 | breaks story logic | BLOCKING independent-review finding: the wire shadow disappears on still-lit neck/right-side areas outside the new hand shadow. Changing the hand cannot remove a shadow from regions that remain illuminated; the key experiment contradicts the claimed optical explanation. The cropped final tabletop proof provides no later visual repair. |
| 30.0–33.0 | cosmetic | Right vase contour clipped; blue dot, clothing and hairstyle remain consistent. No confirmed prop-state contradiction observed. |

## Calls, timing and corrections

- ImageGen invocations: 3; completed images: 3; correction pass count: 0. Every accepted/rejected image has a ledger receipt; failed input validation has its own no-image entry.
- Local libx264 encode count: 8; final stream-copy/AAC mux recorded separately. One final master per story, preserved without replacement.
- Render invocation wall time: 63.265 s. Image dollar cost UNKNOWN (tool did not expose charges). Local Kokoro uses existing verified model bytes; no hosted TTS call. No dollar total invented.
- Elapsed input-creation to completed QA: 1300.4 s, from 2026-11-24T15:38:38.222806+00:00 to 2026-11-24T16:00:18.625189+00:00. This includes waiting while earlier stories were produced and is not active labor/provider latency. Late record writing is excluded. Pipeline wall time above is separately measured.
- Foley: deterministic local 24 kHz mono PCM tick/noise, mixed softly as snip or contact, with bilingual accessibility cue. It is synthetic foley; source room ambience and every original P01 needle/purse sound were not recreated.

No visual correction used (3 generated sheets total). Reference mobile’s small brass disk was registered before shot generation. No confirmed hair/clothing/face or vase-state break; the optical story-logic failure and crop limitations remain in the master. Any future revision needs consistent wire/light/hand/shadow states and a visible tabletop proof; no revision was made in this records-only update.

Reference sheet was produced first. Shot sheets were conditioned on extracted canonical cells when at most five were required; P01/P04 used the whole six-cell reference sheet because the image tool accepts only five image paths. P02 correction additionally attached its already-inspected setup sheet. Prompt hashes and output hashes are in images.jsonl. No second correction loop was run.

## Measured narration / caption schedule

| Cue | Start s | End s | Trimmed PCM samples at 24 kHz | Reveal |
| --- | --- | --- | --- | --- |
| line-01 | 0.000 | 3.161 | 75856 | False |
| line-02 | 5.000 | 7.732 | 65561 | False |
| line-03 | 10.000 | 13.129 | 75090 | False |
| line-04 | 16.000 | 18.766 | 66392 | False |
| line-05 | 21.000 | 23.960 | 71048 | False |
| line-06 | 27.000 | 29.418 | 58020 | True |
| line-07 | 32.000 | 35.041 | 72995 | True |

The first reveal shot starts at 27 s. Audio and captions marked reveal are guarded against an earlier start. Foley has its own timed bilingual caption.

## Reproduction commands and unverified scope

From repository root, with existing local tool/model paths supplied by S2V environment variables (see ../README.md):

```powershell
& $env:S2V_RENDER_PYTHON -B experiments/cluepause/static-ten-20261124/puzzle/run.py validate experiments/cluepause/static-ten-20261124/puzzle/P03
& $env:S2V_RENDER_PYTHON -B experiments/cluepause/static-ten-20261124/puzzle/run.py run experiments/cluepause/static-ten-20261124/puzzle/P03
```

The run command was executed successfully for this master. It deliberately rejects replacing an existing MP4; reproduction requires a new revision id in an isolated copy. Detailed successful subprocess commands, exits, times and diagnostics: `artifacts/static-ten-20261124/puzzle/puzzle-p03-static-v1/commands.jsonl`. Technical probe, report, cost, source/tool hashes, source storyboard, image ledger and caption provenance all remain under this output folder.

Not verified: full spoken-audio listening in both caption modes, ASR, actual phone readability, blind story/visual comprehension, external originality/rights review, audience retention, market demand. No public/private upload, YouTube access, commit, push or memory modification. Core src/video/governance unchanged; full engine uv pytest/npm checks were not rerun for isolated content. Shared pipeline offline suite: 33 passed; pytest caches/temp confined to puzzle artifacts.
