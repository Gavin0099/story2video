# P01 — The Thread Under the Scale — production record

Original fictional puzzle. Rights: pending_verification. No claim of a real event, person, business or external originality clearance.

A buyer cuts the thread loading a dishonest spring scale. A brass calibration weight seems responsible, but merely hides the seller’s toe loop.

Story Quality Gate PENDING (no blind readers in this round).
Storyboard Quality Gate PENDING (primary-agent observations below are not independent approval).
Viewer Gate HUMAN_TEST_PENDING. Market acceptance NOT_TESTED.

## Delivered files and engineering acceptance

- MP4: `artifacts/static-ten-20261124/puzzle/puzzle-p01-static-v1/puzzle-p01-static-v1.mp4`
- Duration: 36 s; 1080×1920; 30 fps; H.264 High/yuv420p; AAC stereo 48 kHz; faststart.
- SHA-256: `f806ed777997b2fc6e37d4e7a345b605cba2980ff55ad23491d6ebea82469a8e`
- EN sidecar: `artifacts/static-ten-20261124/puzzle/puzzle-p01-static-v1/puzzle-p01-static-v1.en.srt`
- zh-Hant sidecar: `artifacts/static-ten-20261124/puzzle/puzzle-p01-static-v1/puzzle-p01-static-v1.zh-Hant.srt`
- Source Git SHA: `aef24410f8b45c8651fd922343aeb52db11bfc75` (uncommitted genre additions; SHA identifies unchanged worktree base).
- Shared schema validator: VALID. Pipeline engineering result: PASS. Checks: video=True; frames=True; duration=True; audio=True; no_embedded_subtitles=True; faststart=True; full_decode=True; captions_en=True; captions_zh-Hant=True; caption_bounds=True.
- 167 dense decoded frames sampled every 7 video frames plus each shot’s last frame; all 12 timestamped strips personally inspected by the primary agent. Also inspected the ordered source `silent-storyboard.jpg` export. This is AI visual inspection, not human testing.
- Opening question only at 1.0–3.5 s; captions remain separate; photographed evidence text only P02 HOME.
- Alignment is measured trimmed PCM timing plus exact SRT-content/bounds comparison, not ASR, independent listening or human comprehension.

## Shot table: silent intent versus actual frames

The SILENT STORYBOARD check was written in story.md before the first ImageGen. State changes across cuts replace continuous character/object motion.

| Shot | Seconds | Function | Intended silent observation | Actual dense-frame / source observation |
| --- | --- | --- | --- | --- |
| shot-01 | 0–0.5 | clue | Scissors and separated thread ends show a snip. | Separated thread ends and scissors are clear. This is a frozen post-snip state, not visible severing motion. |
| shot-02 | 0.5–3.5 | establish | Needle is lower, all three gold pieces remain. | Lower-left needle, rim dent and three gold pieces are visible. No high-to-low needle motion occurs within the opening second. |
| shot-03 | 3.5–7 | establish | Both hands are visible above a high-reading scale. | High needle and pointing hand visible. Second seller hand is pushed to the right crop edge, weakening the two-hands evidence. |
| shot-04 | 7–11 | clue | Purse has fallen; thread is tied to moving pan. | Purse is on floor after correction; knot under pan and counter hole are visible in the upper portion. |
| shot-05 | 11–15 | clue | Thread appears to lead behind a brass weight. | Empty brass ring and thread to its right are separate after correction. Bottom support is hidden as intended. |
| shot-06 | 15–19 | reaction | Seller offers receipt while high reading persists. | High needle and receipt-sliding hand visible. Other seller hand is outside crop; buyer face partially clipped. |
| shot-07 | 19–23 | clue | Scissors are ready; seller heel is raised. | Buyer retrieves scissors from purse. Seller raised heel and brass cylinder are lost from the portrait crop. |
| shot-08 | 23–27 | reaction | Unchanged gold contradicts the lower reading. | Lower reading and same distinctive gold set visible, with leftmost round/oval piece partly clipped by crop. |
| shot-09 | 27–29 | reveal | Brass weight is supported and its ring is empty. | Cylinder clearly stands on shelf and ring is empty. Thread crosses horizontally behind cylinder, unlike vertical route shown earlier. |
| shot-10 | 29–32 | reveal | Toe loop is the hidden source of tension. | Black shoe toe loop and taut diagonal line are visible. Upper line appears to terminate at front wooden counter edge, not visibly continue to pan hole. |
| shot-11 | 32–34 | reveal | Post-cut lower reading and same gold resolve the opening. | Lower reading and three pieces return. Pan thread stump is visible. Gold oval is more circular than the written invariant throughout. |
| shot-12 | 34–36 | reaction | Buyer confronts seller with the evidence. | Buyer with scissors and seller face each cropped near frame edges; both retain original clothes and hair. Cylinder now appears at counter height in background. |

## Continuity and story-logic findings

Impact classes describe observed limitations; none is a gate decision. Hairstyles/clothes/identities generally match their canonical sheet. Minor pose, size and facial perspective changes between photographs are expected; failures of evidence/state are recorded explicitly.

| Timestamp(s), seconds | Impact class | Finding |
| --- | --- | --- |
| 0.0–3.5 | confusing | No visible needle movement or earlier high baseline in first second; opening anomaly depends on narration until the 3.5 s flashback. |
| 3.5–7.0; 15.0–19.0 | confusing | Portrait crop prevents a clear simultaneous view of both seller hands, weakening the alternative ballast explanation. |
| 19.0–23.0 | confusing | Raised heel clue is outside the crop; silent viewers lose the pre-reveal foot hint. |
| 23.0–27.0 | cosmetic | Oval/round gold partly clipped at left; all three pieces can still be counted. Oval is visually round across the sequence. |
| 27.0–32.0 | breaks story logic | Thread routing changes: vertical pan-to-hole setup becomes horizontal cylinder pass and a diagonal line apparently attached to the front counter edge at toe reveal. No single continuous force path to the moving pan is demonstrated; a fixed counter attachment would not load the pan. |
| 34.0–36.0 | confusing | Cylinder appears at counter height in final background rather than clearly on the under-counter shelf. Confrontation faces cropped. |

## Calls, timing and corrections

- ImageGen invocations: 5; completed images: 4; correction pass count: 1. Every accepted/rejected image has a ledger receipt; failed input validation has its own no-image entry.
- Local libx264 encode count: 12; final stream-copy/AAC mux recorded separately. One final master per story, preserved without replacement.
- Render invocation wall time: 107.719 s. Image dollar cost UNKNOWN (tool did not expose charges). Local Kokoro uses existing verified model bytes; no hosted TTS call. No dollar total invented.
- Elapsed input-creation to completed QA: 651.4 s, from 2026-11-24T15:38:38.215805+00:00 to 2026-11-24T15:49:29.648486+00:00. This includes waiting while earlier stories were produced and is not active labor/provider latency. Late record writing is excluded. Pipeline wall time above is separately measured.
- Foley: deterministic local 24 kHz mono PCM tick/noise, mixed softly as snip or contact, with bilingual accessibility cue. It is synthetic foley; source room ambience and every original P01 needle/purse sound were not recreated.

One shots-a correction separated thread from brass ring and placed purse on floor. The original rejected sheet is preserved. One earlier tool invocation rejected six reference paths without producing an image; a complete reference sheet replaced the six separate attachments.

Reference sheet was produced first. Shot sheets were conditioned on extracted canonical cells when at most five were required; P01/P04 used the whole six-cell reference sheet because the image tool accepts only five image paths. P02 correction additionally attached its already-inspected setup sheet. Prompt hashes and output hashes are in images.jsonl. No second correction loop was run.

## Measured narration / caption schedule

| Cue | Start s | End s | Trimmed PCM samples at 24 kHz | Reveal |
| --- | --- | --- | --- | --- |
| line-01 | 0.000 | 2.138 | 51317 | False |
| line-02 | 3.500 | 6.667 | 76006 | False |
| line-03 | 7.000 | 8.743 | 41831 | False |
| line-04 | 11.000 | 13.647 | 63527 | False |
| line-05 | 15.000 | 17.176 | 52220 | False |
| line-06 | 23.000 | 24.565 | 37569 | False |
| line-07 | 27.000 | 29.902 | 69653 | True |
| line-08 | 32.000 | 33.946 | 46692 | True |

The first reveal shot starts at 27 s. Audio and captions marked reveal are guarded against an earlier start. Foley has its own timed bilingual caption.

## Reproduction commands and unverified scope

From repository root, with existing local tool/model paths supplied by S2V environment variables (see ../README.md):

```powershell
& $env:S2V_RENDER_PYTHON -B experiments/cluepause/static-ten-20261124/puzzle/run.py validate experiments/cluepause/static-ten-20261124/puzzle/P01
& $env:S2V_RENDER_PYTHON -B experiments/cluepause/static-ten-20261124/puzzle/run.py run experiments/cluepause/static-ten-20261124/puzzle/P01
```

The run command was executed successfully for this master. It deliberately rejects replacing an existing MP4; reproduction requires a new revision id in an isolated copy. Detailed successful subprocess commands, exits, times and diagnostics: `artifacts/static-ten-20261124/puzzle/puzzle-p01-static-v1/commands.jsonl`. Technical probe, report, cost, source/tool hashes, source storyboard, image ledger and caption provenance all remain under this output folder.

Not verified: full spoken-audio listening in both caption modes, ASR, actual phone readability, blind story/visual comprehension, external originality/rights review, audience retention, market demand. No public/private upload, YouTube access, commit, push or memory modification. Core src/video/governance unchanged; full engine uv pytest/npm checks were not rerun for isolated content. Shared pipeline offline suite: 33 passed; pytest caches/temp confined to puzzle artifacts.
