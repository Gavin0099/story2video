# P04 v4 ? fixed-assembly candidate, 2026-11-25

The v3 review found a real mechanical contradiction: the rope between the fixed flag and its blue endpoint knot grew roughly threefold. v4 reuses the shot-04 setup assembly, removes alternate setup assemblies from the maker portraits, and edits only the cut/final sheet against one canonical assembly close-up. Decoded measurements now stay between 0.4853 and 0.5354 eyelet spacings, an across-shot range of 0.0502 within the declared 0.06 visual tolerance. This supports a visually fixed assembly; it is not pixel identity, calibrated length measurement or independent approval.

Status: **REVIEWED: UPLOAD-OK private review copy, not uploaded yet**. Story Quality Gate PENDING; Storyboard Quality Gate PENDING; Viewer Gate HUMAN_TEST_PENDING. Engineering media acceptance PASS; market acceptance NOT_TESTED. FICTION; rights pending_verification.

## Independent v4 review disposition — 2026-11-25

[Independent review](../../../../../artifacts/independent-review-p04-v4-20261125/REVIEW.md): **UPLOAD-OK private review copy; BLOCKING: none**. Independent sampled measurements support approximate fixed flag-to-knot geometry (ratios 0.4933–0.5391, range 0.0458), not exact dimensional identity or calibrated physical proof. The previous attachment/geometry contradictions are resolved for this private-copy review. The original records verdict was **REQUEST_CHANGES**; this integration corrects the story table and both README rows without claiming a fresh independent records approval.

- Records SHOULD-FIX applied: current v4 story rows 01/03 describe the maker-only crops, and shot 08 now describes the unoccupied rig hold continuing shot 07, with no closing maker reaction. Both summaries identify the reviewed v4 path/SHA instead of rejected v3. v3 remains historical **HOLD** below.
- Remaining **SHOULD-FIX**: narration and both SRTs explain the blue restraint at 16 s (16.000–19.914) and cutting only that tie at 22 s (22.000–23.311), allowing an early release sub-answer before the full counterweight reveal at 27 s. It is nonblocking for private review; suspense remains untested.
- Remaining **NIT**: both sidecars' snip caption at 22.000–22.200 overlaps narration at 22.000–23.311. Player stacking/replacement and real-time listening remain untested. No speech/caption edits or media regeneration were performed in this integration.

The records-only story correction intentionally changes `revisions/v4/story.md` after rendering. The frozen output manifest's original story SHA-256 is `1785600882c72832d8857e9ffc8a91219ff260e526bc5269202dced7a243d0b8`; original manifest/provenance/QA input assertions describe those render-time bytes and were not rewritten or rerun against the corrected prose. The master remains `ff01d6c8c0c02e5a50bd768c1a323360df9333e9db7cc111b12aefa220c0ef4a`.

Private-copy suitability is not upload/publication authorization, human comprehension or a gate pass. Story/Storyboard Gates remain **PENDING**, Viewer Gate **HUMAN_TEST_PENDING**, rights **pending_verification**, market acceptance **NOT_TESTED**. No upload occurred.

## v4 deliverables and engineering acceptance

- Master: `artifacts/static-ten-20261124/puzzle/puzzle-p04-static-v4/puzzle-p04-static-v4.mp4`
- SHA-256: `ff01d6c8c0c02e5a50bd768c1a323360df9333e9db7cc111b12aefa220c0ef4a`
- 39.000 s, 1170 decoded frames, 1080?1920, 30 fps, H.264 High/yuv420p, AAC stereo 48 kHz, faststart, no embedded subtitles. All 10 automated QA checks PASS, including full audio/video decode and exact sidecar/bounds checks.
- EN/zh-Hant sidecars: `artifacts/static-ten-20261124/puzzle/puzzle-p04-static-v4/puzzle-p04-static-v4.en.srt` and `.zh-Hant.srt`.
- Silent storyboard: `artifacts/static-ten-20261124/puzzle/puzzle-p04-static-v4/silent-storyboard.jpg`, companion JSON and all 8 timestamped `qa/shot-XX-strip.jpg` files. Primary agent personally inspected all 178 decoded samples (every 7 frames = 4.286 fps, plus each shot's final frame), the storyboard, 10 exact full-resolution decoded frames and their coordinate crops. This is sampled AI visual inspection, not a human or independent gate.
- Base Git SHA at render: `b7801291cf7af830272070e416130125ed0df7b5`; branch `codex/cluepause-static-ten-20261124`. SHA identifies the base, not uncommitted content. `manifest.json` binds story/config/reference inputs and shared pipeline; `revision-provenance.json` additionally binds the v4-only renderer, verifier, adapter, call ledger and landmarks.
- Seven narration WAVs and their measured narration schedule remain byte-identical to v3/v1. No TTS calls. Mix changes are confined to the old/new snip windows. Snip and bilingual SFX cues now start with the cut image at **22.000?22.200 s**, replacing 27.100?27.300 s. Both full sidecars were read.
- 8 local libx264 shot encodes plus final stream-copy/AAC mux; render/full-QA wall time 44.204 s. First adapter launch failed before any encode because its relative adapter path was one level too high; corrected once and reran successfully. No failed render/master was overwritten.
- Generated cells are slightly narrower than 9:16. `revisions/v4/render_revision.py` contains the complete cells with narrow neutral side mattes, preserving pulley and floor contact. It changes no image content, speech, timeline or shared pipeline. Reproduce using this renderer, not the shared cover-crop `run` mode.

## v4 per-shot changes and mechanism states

One open running rope goes from the left free cream endpoint, through the two fixed flag eyelets, over the fixed brass pulley, and down the right side to the sandbag. A distinct blue restraint connects the left endpoint knot to the bench cleat before cutting. Only the blue restraint is cut. A short blue remnant travels with the cream endpoint while another remains at the cleat. Offscreen states are inference, not evidence from that individual shot.

| Shot / seconds | Change from v3 | Assembly / rope route | Cleat / flag / free endpoint | Counterweight | Hands |
| --- | --- | --- | --- | --- | --- |
| 01 / 0?5 | Recrop original cell to maker/scissors only | Assembly and pulley outside frame | Low/intact state inferred from following setup, not measured here | Hidden | Maker holds orange scissors; other hand at bench edge; no rope pull |
| 02 / 5?10 | Recrop the exact shot-04 source cell | Canonical two eyelets, fixed short cream tail and blue endpoint knot visible; upper route outside crop | Low flag; intact blue link reaches cleat | Outside frame | None |
| 03 / 10?16 | Recrop original maker reaction, excluding alternate assembly | Assembly outside frame | Intact low state inferred from adjacent views | Hidden | Maker looks toward rig, scissors down; no visible pull |
| 04 / 16?22 | Source/camera unchanged | Canonical assembly; both cream legs over brass pulley; right descends behind bench | Low flag; short tail and blue restraint down to cleat | Initial suspension concealed by apron; not independently established | None |
| 05 / 22?27 | New conditioned sheet cell 0; snip moved here | Same short flag-to-knot segment; cream line uncut; blue ends separated | Released after-state, cream tip and blue stub in air above blue-only cleat; gap implies some rise may already have happened | Outside crop; coupled descent inferred | Scissors hand beside severed gap, no cream-rope support |
| 06 / 27?30 | Source/camera unchanged; late snip removed | Right cream leg terminates at bag; other route outside crop | Flag/cleat outside crop; raised/free state inferred | Tan black-X bag rests on floor | None |
| 07 / 30?33 | New conditioned sheet cell 1 | Complete route: short free tail ? both eyelets ? pulley ? floor bag | Raised flag, short airborne cream tip and blue stub; clear air gap; only blue remnant at old cleat | Floor contact visible together with raised flag | No person; scissors on bench |
| 08 / 33?39 | Same cell 1 as 07; continuous zoom range across cut | Exactly same source assembly and route as 07 | Same settled state | Same floor bag | No maker reaction or hands; story shot table corrected |

The change across release is whole-assembly elevation and blue-restraint separation. The cut shot freezes a sampled released state rather than five seconds of equilibrium. Coupled motion and equal travel are inferred across cuts. The shared final plate locks shots 07?08 only; setup-to-release continuity is separately supported by the normalized measurements below. No additional cream attachment to the cleat was observed.

## v4 decoded eyelet?knot measurements

Ratio = Euclidean distance(lower eyelet center, blue knot center) / distance(upper eyelet center, lower eyelet center). Exact MP4 frame indices, manual pixel centers and computed distances: `artifacts/static-ten-20261124/puzzle/p04-v4-fix/landmarks.json`. Decode schedule and tolerance were saved before landmark entry. Declared visual tolerance: maximum range 0.06 eyelet spacings, with manual-center uncertainty approximately ?3 pixels in the wide view. Ratios are not centimetres or a claim of exact mechanical identity.

| Shot | Exact decoded times s | Ratios at start / final frame |
| --- | --- | --- |
| 01 | 0?5 interval inspected | N/A ? assembly excluded by crop |
| 02 | 5.000 / 9.9667 | 0.4910 / 0.4924 |
| 03 | 10?16 interval inspected | N/A ? assembly excluded by crop |
| 04 | 16.000 / 21.9667 | 0.4891 / 0.4853 |
| 05 | 22.000 / 26.9667 | 0.5118 / 0.5087 |
| 06 | 27?30 interval inspected | N/A ? bag-only view |
| 07 | 30.000 / 32.9667 | 0.5354 / 0.5354 |
| 08 | 33.000 / 38.9667 | 0.5354 / 0.5313 |

All 10 samples: 0.4853?0.5354; range 0.0502 < 0.06. No sliding motion is visible within the dense strips; each is a still plus camera zoom. The residual approximately 0.05 spacing difference is retained explicitly, not described as perfect equality. Primary-agent judgment: visually compatible within this tolerance, pending independent review. Comparison figure: `artifacts/static-ten-20261124/puzzle/p04-v4-fix/tail-comparison-v4.jpg`.

## v4 ImageGen ledger and budget

Exactly **2 new built-in ImageGen calls, 2 completed sheets, 1 correction of the same sheet**; no new reference generation. P04 cumulative unique calls = 8 (4 original + 2 v2, reused by v3 + 2 v4). Dollar charges UNKNOWN. Call prompts, actual attachment hashes, output hashes and rejection reason are archived in `revisions/v4/call-prompts/` and `images.jsonl`, copied to the v4 output ledger.

1. Initial `precise-object-edit` call: canonical shot-04 assembly close-up plus existing cut/final edit targets. Rejected: cut ratio approximately 0.50 but final approximately 1.00 rather than 0.49. Rejected sheet retained as `assets/shots-b-v4-attempt1.png`.
2. Sole correction: same sheet plus canonical close-up. Requested only moving the right-panel blue knot up to half an eyelet spacing. Accepted as a fix candidate after decoded inspection/measurement. No third call or extra correction. Prompt set: preserve all eyelets/flag markings and rope topology; shorten lower cream segment to canonical proportion; maintain separate severed blue ends, complete pulley route and floor bag.

## v4 residuals and acceptance boundaries

- Static edits imply fall/rise; concealed initial bag height, counterweight mass, friction and exact equal rope travel remain unmeasured. These limits cannot explain away the failed v3 geometry, which is explicitly recorded below.
- Cut-panel pennant tip reaches/clips the source-cell right edge; both eyelets, white circle, short cream tail and knot remain visible. Full flag, free endpoint, pulley route and bag are visible in the final wide hold. That proof is relatively small; actual phone readability is pending. Maker-only opening establishes scissors first, with the flag introduced at 5 s.
- Generated cut/final photos retain about 0.05 eyelet-spacing maximum measured variation versus canonical setup, within the declared visual tolerance; this is not pixel-identical compositing. Subsequent independent private-copy acceptance and measurement limits are recorded above.
- Early restraint sub-answer remains spoken/captioned at 16 s and cut-only-blue at 22 s. No speech edits/new TTS were authorized or needed for this geometry revision. First full counterweight explanation/reveal stays at 27 s.
- The 22 s snip cue overlaps the narration cue in both SRTs. Timing/content and PCM scheduling are verified; switchable-caption player behavior, real-time listening/ASR, human comprehension/suspense, external originality/rights clearance and market acceptance are unverified.
- Original v4 render delivery scope (historical): no YouTube access, upload, commit, push or memory edits; no other story folder, v1?v3 revision or master, puzzle README, or batch README was edited. README integration was deferred then and is completed in the records-only update above. Market acceptance NOT_TESTED.

## v4 verification commands and results

From repo root, using existing hash-pinned media tools through `S2V_FFMPEG`, `S2V_FFPROBE`, an existing CJK font through `S2V_QUESTION_FONT`, and `S2V_GIT_SHA` set to the base above:

```powershell
python -B experiments/cluepause/static-ten-20261124/puzzle/run.py validate experiments/cluepause/static-ten-20261124/puzzle/P04/revisions/v4
python -B experiments/cluepause/static-ten-20261124/puzzle/P04/revisions/v4/render_revision.py
python -B artifacts/static-ten-20261124/puzzle/p04-v4-fix/inspect_decoded.py
python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/puzzle/p04-v4-fix/pytest-cache --basetemp artifacts/static-ten-20261124/puzzle/p04-v4-fix/pytest-temp
python -B experiments/cluepause/static-ten-20261124/puzzle/P04/revisions/v4/verify_revision.py
git diff --check
```

Validate, render/full QA, exact detail decode, and deliverable audit: exit 0. Pipeline pytest: **33 passed in 0.49 s**, P04 v4-specific cache/basetemp, bytecode disabled. Final integrity audit verifies 777 pre-task file hashes (only the intentionally updated P04 record differs), unchanged v1?v3 inputs/outputs and both README files, 7 unchanged WAVs, narration schedule, mix-difference windows, both ImageGen receipts/attachments, 178 dense samples and all decoded landmarks. Personal-path regex scan and authored-text whitespace scan: zero hits. `git diff --check` and cached check: exit 0. Detailed render commands/exits/times: v4 `commands.jsonl`; integrity/provenance: v4 `revision-provenance.json` and revision `verification.json`.

The root README's exact `uv` invocation could not run because `uv` is absent from PATH. No dependencies were installed. Core engine pytest, npm install/typecheck and governance checks were not rerun: `src/`, `video/`, shared pipeline, Episode/SQLite/governance contracts are unchanged. This is an isolated content/render-adapter revision, with full offline pipeline tests and concrete render QA above. Engineering file acceptance does not confer story, independent-review, human-viewer or market acceptance.

---

The corrected historical v3/v1 records follow. v3 is HOLD; the authoritative v4 story table contains no closing maker reaction. Frozen revision directories v1?v3 were not modified to fix their historical prose.

# P04 — current local fix candidate, 2026-11-25

The raised flag now carries its free cream tail upward. The final portrait frames show that tail ending in open air above the cleat, only a severed blue stub on the cleat, and the other rope end attached to the floor sandbag. Shots 07 and 08 use the exact same source plate so the settled mechanism cannot change rope length across their cut.

Status after independent review: **HOLD, not uploaded**. The v3 free-tail/cleat separation fix succeeded, but the fixed flag-to-knot geometry failed. The following v3 observations are historical and superseded by the v4 record above. Story Quality Gate PENDING; Storyboard Quality Gate PENDING; Viewer Gate HUMAN_TEST_PENDING; market acceptance NOT_TESTED. These are primary-agent observations, not independent approval.

## Current deliverables and engineering acceptance

- Final master: `artifacts/static-ten-20261124/puzzle/puzzle-p04-static-v3/puzzle-p04-static-v3.mp4`
- SHA-256: `ff4e5de88c62c09b9c01886bde01eeaacc62bc421f145154a326e1c48c7cfd78`
- Duration 39.000 s; 1170 frames; 1080×1920; 30 fps; H.264 High/yuv420p; AAC 48 kHz stereo; faststart; no embedded subtitle stream.
- EN: `artifacts/static-ten-20261124/puzzle/puzzle-p04-static-v3/puzzle-p04-static-v3.en.srt`
- zh-Hant: `artifacts/static-ten-20261124/puzzle/puzzle-p04-static-v3/puzzle-p04-static-v3.zh-Hant.srt`
- Silent storyboard: `artifacts/static-ten-20261124/puzzle/puzzle-p04-static-v3/silent-storyboard.jpg` and companion JSON.
- Authoritative final inputs: `P04/revisions/v3/`. v2 was the next free id, rendered and inspected before v3; its master and inputs remain as attempt evidence. v1 story/shots/references/assets/output bytes were preserved; this record is intentionally updated.
- Source Git SHA at BOTH new renders: `435f4ab3dfec21526358bd3bed3b175ab1a914af` (read from each completed manifest; initial inspection HEAD was `adaa21081a9cbd79365117bb4ac152b86569f2c8`). The SHA identifies the worktree base, not the uncommitted P04 content; input, tool and source hashes bind the actual render in each manifest. Branch `codex/cluepause-static-ten-20261124`.
- Shared validator: VALID for v2 and v3. Full automated media QA: PASS for both, all 10 checks true (video, counted frames, duration, audio format/duration, clean subtitle streams, faststart, full decode, exact EN/zh-Hant sidecars, caption bounds).
- Personally inspected all 8 timestamped decoded strips for EACH render and each silent storyboard. Final v3: 178 decoded samples, every 7 frames at 30 fps = 4.286 fps, plus each shot's last frame. No missing free tip, cleat gap, pulley or floor bag in the final two strips.
- Seven original trimmed narration WAVs, mixed PCM and both SRT sidecars are byte-identical to v1. No TTS call. First four source plates and shot-06 plate are byte-identical to v1. Shot-07 and shot-08 source plate hashes are identical to each other.
- v2: 8 libx264 cuts + one final mux, render/QA wall time 46.843 s. v3: 8 cuts + one mux, 49.297 s. `cost.json` distinguishes these local encodes from ImageGen. No new shared pipeline, core engine, video, SQLite or governance code.

## Per-shot changes and mechanism state table

The rig is ONE continuous **open-ended** running rope bent over a fixed pulley, not an endless closed loop. The left endpoint is the cream tail below the fixed flag; the right endpoint is the sandbag handle. A separate blue restraint connects the left endpoint to the cleat before release. Only that blue restraint is cut. R below means left tail → two flag attachments → brass pulley → right leg → bag. Offscreen/hidden states below are inferred from adjacent views, not directly proven by that individual frame. Photographs are static sampled states, not real-time simulation.

| Shot / seconds | Change from v1 | Rope route | Cleat state | Flag height | Tail end position | Counterweight | Hands |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 / 0–5 | Image/camera unchanged | R; left leg and pulley visible, right near upright | Intact blue restraint | Low, two eyelets | At bench-cleat level; blue holds it | Hidden by bench, initially suspended in story; not directly visible | Scissors held; other hand on bench, neither pulls rope |
| 02 / 5–10 | Unchanged closeup | Left cream leg and two eyelets; rest outside crop | Intact blue link visible | Low | Near cleat, cream and blue distinguishable | Outside frame | No hands |
| 03 / 10–16 | Unchanged | Same R visible above/at flag, bag hidden | Intact blue | Low | Near original cleat | Hidden | Scissors down at side; no pull |
| 04 / 16–22 | Unchanged mechanism view | Both cream legs across pulley; right descends behind bench | Intact blue | Low | Down at cleat | Hidden by apron | No hands |
| 05 / 22–27 | New corrected sheet cell 0; small zoom | Intact left leg through both eyelets to visible free tip; pulley/right outside closeup | Two separated blue ends; only blue attached to cleat | Low / just released | Free cream tip with blue stub above cleat; no cream attachment remains | Outside frame, release underway inferred | One scissors hand beside blue gap; does not hold cream rope |
| 06 / 27–30 | Image/camera unchanged | Right cream leg tied to bag; other leg outside closeup | Offscreen, already cut | Offscreen, rising/raised inferred | Offscreen, rising/raised inferred | X-stitched tan bag on floor, attached to right rope | No hands |
| 07 / 30–33 | New corrected sheet cell 1, portrait complete-rig view | Entire R visible, no branch or second weight | Only cut blue stub remains | Raised with both fixed eyelets | Short tail ends high in air, clearly above bench; tiny blue stub travels with tip | Floor bag and full right leg visible together with high flag | No person or hands; scissors rest on bench |
| 08 / 33–39 | Same cell 1 as 07, replacing maker reaction | Exactly same R/source plate as 07 | Same cut-blue-only cleat | Same raised flag | Same elevated free endpoint and empty gap | Same floor bag | No person or hands; scissors remain on bench |

| Transition | Primary-agent check and evidence boundary |
| --- | --- |
| 01 → 02 | Same low flag, two eyelets, cream tail and intact blue-to-cleat restraint; closeup hides pulley/bag. |
| 02 → 03 | Returns to low rig with no pull; restraint remains intact. |
| 03 → 04 | Both legs are shown over the same fixed pulley; right endpoint remains concealed. |
| 04 → 05 | Only blue link separates; cream line and both flag attachments stay intact. This is a frozen release instant, not five seconds of unsupported equilibrium. |
| 05 → 06 | Cut restraint is followed by floor-bag after-state. Coupled motion happens across the cut; simultaneous moving endpoints are not shown. |
| 06 → 07 | Wider after-state confirms the floor bag, full right leg, pulley, raised flag and raised free tail together; no cream rope reaches old cleat. |
| 07 → 08 | Same source bytes lock flag-to-tip distance and both endpoints; camera restarts its slight 1.2% zoom, but mechanism state is unchanged. |

Independent review disproved the compatible-states conclusion for v3: the lower-eyelet-to-blue-knot distance grows about 0.49 ? 1.10 ? 1.48 eyelet spacings at 16, 22 and 30 seconds. That is a material fixed-assembly contradiction, not a zoom explanation or merely unknown bag travel. Only the free-tail/cleat separation and the unchanged state between shots 07?08 were successfully fixed. v3 remains HOLD. Exact equal rope travel and the concealed initial bag position were not measured.

## ImageGen receipts and iteration budget

Exactly **2 new built-in ImageGen calls / 2 completed sheets**, one initial call and **one correction for the same shots-b sheet**; no new reference generation. Original P04 history was 4 calls, so P04 cumulative unique calls = 6. v3 adds zero calls and reuses v2's two unique receipts; duplicated ledger copies are not additional invocations. Charges UNKNOWN.

1. Initial replacement two-panel sheet: rejected. Tail left the cleat correctly and bag was on floor, but the tail was too long versus setup and included an extra knot.
2. Single correction: three-panel sheet. Cell 0 clarifies the snip and two separated blue ends; cell 1 shows complete settled rig. Cell 2 includes maker reaction but has different tail proportions, so it is **excluded from final v3**. v2 used it and is retained as an unsuccessful continuity attempt. Final v3 holds cell 1 twice; no further image call.

Canonical reference sheet was attached to BOTH calls; first call also attached old shots-b, second attached the inspected first result and original shot-04 plate. Canonical identity/prop/set appearances were retained; mechanically incorrect old reference states were explicitly overridden in the prompts.

Every call, rejected output, actual attachment hash, exact prompt and output hash is retained in `P04/revisions/v2/images.jsonl`, `P04/revisions/v2/call-prompts/` and the corresponding output ledger/archive. v3 carries the same receipt history and assets for reproducibility. Prompt set: precise-object-edit; full pulley route, fixed eyelets, moving free tail, cut-blue-only cleat, floor bag, portrait crop safety. Original/unused images remain preserved; no further correction budget remains for this sheet.

## Question, narration and sidecar disclosure check

- Opening EN/zh question, shown only at 1.0–3.5 s, asks why cutting raises the flag; it does not name a counterweight or explain the release.
- Lines 01–03 (0–12.766 s) set up scissors, taut rope and possible jam. No sandbag or counterweight answer is spoken or captioned.
- **Partial early disclosure remains**: line-04 at 16.000–19.914 s explicitly says the blue tie held the left side down; line-05 at 22.000–23.311 s says he cut only blue. EN and zh-Hant sidecars disclose the same restraint sub-answer before the nominal reveal. This is a predictability risk, not a clean spoiler-free pass.
- Full counterweight explanation first starts at 27.000 s in line-06, exactly the first reveal shot; line-07 explains the restraint/weight at 32.000 s. No marked reveal narration or sidecar starts before 27 s. The hidden bag is not shown in pre-reveal shots. Sidecars exactly match measured PCM scheduling; no ASR claim.
- Text, WAVs and sidecars were preserved because fixing rope routing did not require a narration change. Both language sidecars were read for content and timing. Meaningful audio and source PCM were checked structurally; full real-time spoken-audio listening remains pending.

## Residuals and unverified scope

- Static cuts imply the fall/rise; shot-05 freezes a release instant. This is not a continuous physics demonstration. Hidden initial bag suspension and precise rope-length conservation remain unmeasured. More seriously, normalized eyelet-to-knot distance changes from 0.49 to 1.10 to 1.48: a fixed flag/rope assembly cannot do this without unshown sliding or reattachment. This breaks story logic and is not mild photographic drift.
- Original shot-01–03 portrait crop clips the pennant tip; white circle and two eyelets remain. Final rig proof is small in wide framing; actual phone viewing is pending.
- Ending now holds the mechanism instead of showing the maker's reaction. A slight zoom reset occurs at 33 s.
- Existing synthetic snip cue/caption remains at 27.1–27.3 s although the cut image starts at 22 s. This inherited sound/image timing mismatch was retained with the unchanged mix/sidecars; it is a residual for review.
- Early restraint sub-answer is disclosed at 16 s. Independent story/storyboard review, full listening, switchable-caption playback, phone readability, human comprehension and external originality/rights clearance remain pending. Market acceptance NOT_TESTED.
- Concurrent external changes were observed during this task: HEAD advanced after rendering, P03 record/upload draft and U03 record changed versus the initial read-only snapshot. This task did not write those paths or run commit/push/upload. The final audit reports those differences separately; it asserts preservation only for owned P04 v1 inputs/assets/output. Other pre-existing batch edits were retained.
- No YouTube access, commit, push, upload, memory edit, personal absolute path in authored files, or write to the read-only source checkout was performed by this task.

## Verification commands and results

From repo root with trusted existing tools supplied through `S2V_FFMPEG`, `S2V_FFPROBE`, `S2V_QUESTION_FONT` and `S2V_GIT_SHA`:

```powershell
python -B experiments/cluepause/static-ten-20261124/puzzle/run.py validate experiments/cluepause/static-ten-20261124/puzzle/P04/revisions/v2
python -B experiments/cluepause/static-ten-20261124/puzzle/run.py run experiments/cluepause/static-ten-20261124/puzzle/P04/revisions/v2
python -B experiments/cluepause/static-ten-20261124/puzzle/run.py validate experiments/cluepause/static-ten-20261124/puzzle/P04/revisions/v3
python -B experiments/cluepause/static-ten-20261124/puzzle/run.py run experiments/cluepause/static-ten-20261124/puzzle/P04/revisions/v3
python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/puzzle/p04-fix/pytest-cache --basetemp artifacts/static-ten-20261124/puzzle/p04-fix/pytest-temp
python -B experiments/cluepause/static-ten-20261124/puzzle/P04/revisions/v3/verify_revision.py
git diff --check
```

Render/validate results above: exit 0. Pipeline pytest: 33 passed in 0.60 s, with P04-specific cache/basetemp and bytecode disabled. Integrity audit: PASS (master/input/prompt/attachment hashes; 7 unchanged WAVs; unchanged mix/sidecars; identical final rig plates; 178 samples >=4 fps; P04 v1 preservation). Personal-path regex grep covers new revision/output text and both changed README rows; zero matches. `git diff --check`: exit 0. New untracked text also checked for trailing whitespace. Detailed per-render subprocess arguments, status and times live in each output `commands.jsonl`; final integrity/check results in `artifacts/static-ten-20261124/puzzle/p04-fix/verification.json` and v3 `verification.json`.

The initial integrity attempt encountered an externally removed P03 draft. The audit was narrowed to assert P04 preservation and report external P03/U03 differences, without restoring or editing those forbidden paths. Core engine `uv run --locked pytest`, video npm checks and governance verify were not run: their code/contracts were unchanged. No independent/human or market pass is claimed.

---

The original v1 production record follows for historical evidence; its limitations below describe v1, not the current v3 candidate.

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
