# P03 — The Crack That Crossed the Table — v2 production record

Status: **FIX-CANDIDATE pending independent review, not uploaded** (2026-11-25 Asia/Taipei).

The v1 reveal removed the wire shadow from directly lit ceramic outside the hand shadow. v2 replaces shot-06 with an entirely shaded vase and a thin wire shadow still visible on lit tabletop beyond the broad hand-shadow edge. Shot-08 now shows the lifted vase and the thin shadow crossing the empty tabletop inside 9:16. This is the primary agent's visual finding, not independent approval.

Original fictional puzzle. Rights: pending_verification. Story Quality Gate PENDING. Storyboard Quality Gate PENDING. Viewer Gate HUMAN_TEST_PENDING. Market acceptance NOT_TESTED.

## Current files and engineering acceptance

- Master: `artifacts/static-ten-20261124/puzzle/puzzle-p03-static-v2/puzzle-p03-static-v2.mp4`
- SHA-256: `b30a0b8f62b29fabe83333152211f11e9b164d1902dd99815bbe0155d7a01f80`
- Duration: 39.000 s; 1170 frames; 1080×1920; 30 fps; H.264 High/yuv420p; AAC stereo 48 kHz; faststart.
- Sidecars: same output folder, `puzzle-p03-static-v2.en.srt` and `puzzle-p03-static-v2.zh-Hant.srt`.
- Current inputs: [revisions/v2/shots.json](revisions/v2/shots.json), [story.md](revisions/v2/story.md), [references.json](revisions/v2/references.json). Root P03 input files remain the frozen v1 inputs; reproduce v2 from the revision directory.
- Base Git SHA: `79e9afc0e05f1143a4aeaaab56c116eaaff8dd3b`, branch `codex/cluepause-static-ten-20261124`. Work is uncommitted; input, image and master hashes identify the exact revision.
- Final audit observed HEAD `7a65c6cb9ac74a022acda159ce569885fcf20e45` (H04 v3 commit), which appeared externally while this task ran. This task issued no commit or push; the render manifest retains its actual starting SHA. Exact shared-pipeline and content hashes bind the candidate independently of that unrelated HEAD movement.
- Job schema/cross-reference validate: VALID. Full pipeline QA: PASS, all 10 checks true (video, frames, duration, audio, no embedded subtitles, faststart, full decode, EN captions, zh-Hant captions, caption bounds).
- Pipeline pytest: **33 passed in 0.54 s**. Root engine/npm/governance checks not run: those code/contracts were unchanged.
- Render: 39.484 s wall time, 8 libx264 cut encodes and one final stream-copy/AAC mux. No new TTS; all seven narration WAVs copied byte-for-byte from v1. PCM mix, both sidecars and decoded AAC audio are identical to v1. Unchanged shots 01/02/04/05 have byte-identical encoded cuts.
- All eight timestamped decoded strips personally inspected: 178 samples every 7 frames at 4.286 fps plus each final shot frame. Shot-06: 14 samples, 27.000–29.967 s. Shot-08: 27 samples, 33.000–38.967 s. Also inspected both generated sheets, revised full-size plates 03/06/07/08 and ordered source `silent-storyboard.jpg`. These are AI observations, not human/independent tests.
- Detailed portable evidence: output `qa/report.json`, `qa/probe.json`, `qa/shot-*-strip.jpg`, `silent-storyboard.jpg/.json`, `revision-checks.json`, `timeline.json`, `assets.json`, `manifest.json`, `commands.jsonl`, `images.jsonl`, `call-prompts/`, `cost.json`, `delivery.sha256`, `delivery-audit.json`.

## Per-shot changes and mechanism state check

The single direct light source remains the upper-left window. The wire stays suspended on the circular mobile with the small brass disk. The vase always remains structurally intact, with its cobalt dot. Different framing changes screen coordinates; this is a qualitative projection/occlusion inspection, not calibrated optical reconstruction. Off-camera states below are explicitly identified as inferred.

| Shot / seconds | Change | Light source | Wire | Hand | Wire-shadow | Vase / transition consistency |
| --- | --- | --- | --- | --- | --- | --- |
| 01 / 0–5 | Reused | Upper-left daylight, direct on vase | Ring, hanging straight wire and disk visible | Buyer points; not blocking beam | Diagonal line crosses lit vase and continues onto table | On table, blue dot; initial apparently cracked state. Coherent. |
| 02 / 5–10 | Reused | Same direct daylight | Same mobile above vase | Open gesture outside vase beam | Line persists on vase and table | Same table position/marking; gesture does not erase line. Coherent. |
| 03 / 10–16 | Crop shifted right | Same direction visible in ceramic lighting | Off-camera, unchanged inferred | Off-camera; no blocker shown | Line passes right of dot and reaches tabletop; continuation remains near right edge and is subtle under vase's own shadow | Vase stationary. Crop only; no mechanism change. Coherent, clue readability limited. |
| 04 / 16–21 | Reused | Window direction remains upper left | Mobile, wire and brass disk clearly above vase | Absent from frame | Vase line and tabletop continuation remain visible | On table under wire projection. Establishes source relationship without a repair. Coherent. |
| 05 / 21–27 | Reused | Beam still reaches vase | Same hanging mobile/disk | Approaching from left, no ceramic contact; hand shadow falls on table left of vase | Thin line remains on directly lit vase | Same vase on table; approaching hand has not yet occluded vase beam. Coherent. |
| 06 / 27–30 | Regenerated; static hold | Window still bright; entire vase deprived of direct beam | Same ring/wire/disk remains above; no removal | Raised nearer window, upstream of wire in light path, no vase contact; broad soft shadow surrounds vase | No thin line on shaded ceramic; thin diagonal line visibly continues on bright table beyond broad shadow's lower-right edge | Whole rim/neck/shoulders/right edge/foot shaded, dot retained; no still-lit ceramic loses its line. Coherent occlusion transition from 05. |
| 07 / 30–33 | Crop shifted right | Vase now in ambient/diffuse fill outside narrow wire projection | Off-camera, unchanged inferred | Now supports vase at base/side; blocking pose released | No line on lifted vase; table outside frame, not claimed observed | Complete smooth vase outline and dot visible. Lifting/moving it aside between cuts accounts for no line without a repair. Coherent; relocation inferred across cut. |
| 08 / 33–39 | Regenerated; static hold | Window beam again reaches empty table | Ring/wire/brass disk visible, unchanged | Both hands hold lifted vase aside, clear of tabletop beam | Uninterrupted thin diagonal shadow crosses central empty tabletop, visible for full hold | Whole vase lifted away to upper-left, air gap above table and no line on ceramic. Continued table shadow confirms source stayed in place. Coherent transition from 07. |

## ImageGen calls and budget

Built-in `image_gen.imagegen`, **2 new calls / 2 images**, one two-cell `repair` sheet and its **one correction**. Historical v1 used 3 calls / 3 images; cumulative P03 total is 5 calls / 5 images. No new canonical sheet. Dollar charges UNKNOWN; the tool did not expose costs.

1. `assets/repair-attempt1.png`: rejected conservatively. Shot-08 proof was visible, but bright left rim/shoulder in shot-06 made complete hand shade ambiguous. Exact prompt: output `call-prompts/01-repair.json`. Canonical reference sheet attached.
2. `assets/repair.png`: selected for this candidate after inspection. Targeted correction removes the ambiguous bright ceramic rim/edge, leaving the entire vase in deep broad shade and preserving lit-table continuation; shot-08 staging retained. Exact prompt: output `call-prompts/02-repair.json`. Canonical sheet plus inspected first attempt attached. No further correction allowed or used.

Every call has a pipeline `log-image` receipt in output `images.jsonl`, with prompt/output SHA-256, accepted/rejected status, reference-attachment paths/hashes and archived actual prompts. The canonical sheet was reused, not logged as a new generation. Service-managed outputs were copied into project assets. Acceptance means selected for rendering; it grants no story/storyboard approval.

## Disclosure and residual findings

- Opening question is unchanged: “Why buy the cracked vase?” / 「為什麼買有裂痕的花瓶？」, only at 1.0–3.5 s. It does not name shadow or an unbroken vase.
- Opening narration and both sidecars preserve the apparent-crack setup. Line 03 (10 s) gives the table continuation; line 04 (16 s) identifies the wire mobile in window light. They are clues and may strongly telegraph the solution. The first explicit answer (“Her hand blocked the light. The crack disappeared.”) starts at 27.000 s, with line 07 at 32.000 s. Neither sidecar starts these answers early. Existing reveal timing, including line 07 spanning the cut to shot-08, is preserved.
- The wire and shadow-like softness are visible early; suspense/predictability remains a confusing-level risk, not measured with blind viewers. No claim of zero inferable answer disclosure.
- Shot-03 tabletop continuation is still near the right edge and competes with the vase's broad natural shadow. The corrected shots 06/08 carry the decisive evidence centrally. Shot-07's face is more tightly cropped to retain the whole vase.
- Shot-06 uses a broad, soft, rounded hand/palm shadow rather than a crisp finger silhouette. Exact 3D ray geometry and photometric fidelity are not proven by these stills; the observed all-shaded ceramic and line continuing outside the shadow satisfy the requested qualitative mechanism check. Independent optical/story review is pending.
- Cuts imply hand movement and vase relocation; no continuous action is shown. Local synthetic contact foley is unchanged, despite no ceramic contact in shot-06. It is not a source recording.
- Not verified: independent review, full audio listening, ASR, physical phone readability, blind comprehension, rights/originality clearance, retention, demand or other market outcomes. Gates stay PENDING / HUMAN_TEST_PENDING. No upload authorization or publication acceptance is claimed.

## Reproduction and verification commands

From repository root, supply trusted existing tool paths as environment variables as described in [pipeline README](../../pipeline/README.md). Tool paths never belong in story files. The renderer reuses prerecorded WAVs; no Kokoro model or hosted provider is needed.

```powershell
python -B experiments/cluepause/static-ten-20261124/puzzle/run.py validate experiments/cluepause/static-ten-20261124/puzzle/P03/revisions/v2
python -B experiments/cluepause/static-ten-20261124/puzzle/run.py run experiments/cluepause/static-ten-20261124/puzzle/P03/revisions/v2
python -B artifacts/static-ten-20261124/puzzle/puzzle-p03-static-v2/verify_revision.py
python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/puzzle/puzzle-p03-static-v2/pytest-cache --basetemp artifacts/static-ten-20261124/puzzle/puzzle-p03-static-v2/pytest-temp
git diff --check
python -B artifacts/static-ten-20261124/puzzle/puzzle-p03-static-v2/audit_delivery.py
```

Validate, render/full QA, revision checks and pytest all exited 0. Final whitespace/path audit results are in `delivery-audit.json`. The run command refuses to overwrite an existing master; reproduction must choose another isolated revision id. Avoid rerunning `prompts` over the archived repair payload: it includes the exact canonical-sheet/correction instructions used by the tool.

All 252 frozen v1 inputs/output files covered by the pre-edit SHA snapshot remain byte-identical, excluding this explicitly authorized current record. The v1 master remains `artifacts/static-ten-20261124/puzzle/puzzle-p03-static-v1/puzzle-p03-static-v1.mp4`, SHA-256 `f5b62dbca0b8f5a0490b1fbd96cd7a808dd64cb44732e0e925b07d5441ec9ff9`, 39 s, status HOLD for its retained defect. Its full prior record is preserved at [revisions/v1-record.md](revisions/v1-record.md).

No commit, push, upload, YouTube access or memory edit. The other checkout was read only for existing trusted executables; no files there were modified. Existing unrelated worktree changes were preserved. Shared pipeline, core source, video and governance files were not modified.
