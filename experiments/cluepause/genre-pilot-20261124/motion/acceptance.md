# Motion layer acceptance — 2026-11-24 (Asia/Taipei)

The requested isolated local renderer is implemented, with three ImageGen-layer H01 motion studies and a still/motion/still technical montage. Rotation, translation along a polyline, fade/glow and shake are calculated in FFmpeg; each moving prop uses one immutable bitmap. The latch uses an unchanged foreground housing to hide the retracting shaft. Existing still-shot clips can be replaced without shifting narration or caption timecodes; mismatched replacement lengths are rejected.

Repository: `D:/s2v-motion`, branch `codex/cluepause-motion-layer-20261124`. The initial delivery was committed as **`5253512d18ad15e7a4e3c7f8e84615b0012b077d`**, based on **`a4890685fdba78889f616b558dce930dfc049b7b`**. The sections below headed "Historical initial delivery" preserve the pre-commit acceptance record; their commands/results describe that original attempt. The review corrections described separately were recorded as a pre-commit snapshot and subsequently committed as **`6270889a9de8cfb056c7009b69ffa01f7e02e474`**. The no-commit statements below describe actions during that earlier correction task. No upload, commit, push or reference-tree modification was performed in this correction task. Existing script/story Markdown, production records/specification, `src/story2video/`, `video/` source, Episode schema, SQLite and governance contracts were not edited. The Owner's instruction authorizes this local pilot despite the older document-only restriction in the v2 production specification; it does not qualify a story or authorize release. Formal milestone scope remains unchanged.

## Review corrections — historical pre-commit snapshot (committed at 6270889a)

The independent review `rev-motion.md` requested changes against `5253512d18ad15e7a4e3c7f8e84615b0012b077d`. Its pivot defect was real: the staged pivot lay at `(half, half)` on an even-sized canvas, while FFmpeg rotates around `(half-0.5, half-0.5)`. Staging now uses `(2*half+1)` square pixels, so both centers agree. The final overlay still subtracts `half`. A production-rendered marker stays at `(64,64)` at 0/90/180/270/360 degrees; restoring the even canvas makes this test fail.

The suite now has **40 passing tests**, including **9 new rendered cases**. They call the actual parser, Pillow staging, production filtergraph, H.264 encoder, ffprobe/full decode and PNG decoder; only the synthetic output canvas is reduced to 256×256 for speed. Expected positions/opacity are explicit independent measurements, not values from the helper math. Checks include translation and rotation for every easing at 25%/75%, a 24px/72px polyline with a repeated point at three intermediate times, nonzero two-axis shake plus boundary holds, and fade/glow before/during/after the interval with base opacity multiplication and a visible glow halo. Position tolerances account for raster/overlay rounding (up to 1.01px for shake); opacity allows 4 luminance levels for encoding. The pivot quarter-turn tolerance is 0.15px, small enough to detect the reported 1px drift.

All six deliberate source mutations were **killed by assertion failures**, then the original source bytes were restored in `finally`. Results, exact mutation replacements, pytest commands and logs: `artifacts/genre-pilot-20261124/motion/mutation-review/results.json` and sibling `.log` files. Restored `hybrid_motion.py` SHA-256: `d4eaa8d24b12800833c63ba035aa1346625f046264c04b0912d912ab688ae4c7`.

| Deliberate regression | Result from rendered tests |
| --- | --- |
| Restore even canvas | Pivot assertion fails; 1 failed |
| Replace production easing with linear | All 3 nonlinear cases fail; linear control passes |
| Replace production shake amplitude with zero | Intermediate position assertion fails; 1 failed |
| Give every path segment equal traversal time | Intermediate path position assertion fails; 1 failed |
| Start fade at zero instead of 0.2s | Fade opacity assertion fails; glow control passes |
| Start glow at zero instead of 0.2s | Glow opacity assertion fails; fade control passes |

`verify_demo.py` now accepts `--tools`, `--demo-root`, `--skip-demos` and optional `--reference-media`. Default verification uses a generated local legacy fixture (90 frames, grouped/repeated shot IDs, first cue at frame 1), with no external production dependency. A separate configured-reference run passed against a newly generated **60-frame local fixture**; expected duration comes from its timeline. The original external 1151-frame reference was not rerun. Verification directories are unique on every run; receipt selection matches the actual clip SHA-256. `imagegen-requests.json` retains the original filenames/session identifier and repo-relative raw-asset provenance, with no personal absolute source path. The original delivery and historical pre-commit correction snapshot are distinguished throughout this record.

### Rerendered media and frame check

New output root: **`artifacts/genre-pilot-20261124/motion/review-fix-20261124/`**. All three studies were rerendered (90 frames / 3 seconds each), together with a new still hold and 330-frame / 11-second `hybrid-demo.mp4`. All passed 1080×1920, 30 FPS, SAR 1:1, H.264/yuv420p probing and complete decode. The new master has AAC 48kHz stereo. Original source image assets/spec geometry/timings are unchanged; no new ImageGen requests.

| Output | SHA-256 |
| --- | --- |
| `handle.mp4` | `b6d052d91b175ca0e1875bbe2382c21df5dc2c3d9eea81a4b0fc07818b83ac6a` |
| `intercom.mp4` | `b57e6d27fce0f74391d34cbf29bb0977808923ecced2aeed093e590f10dad7f9` |
| `latch.mp4` | `5ad9b024d1805e614f8c6020180a28d320c5b7aa3ff8bdf9645752742b02aa10` |
| `hybrid-demo.mp4` | `e4e9d51ad7af560df42bf90fc0534f0af1a6fa3217d4affece2c35ceaa1afcee` |

The primary agent inspected fresh start/action-middle/clip-middle/end frames (handle 0/20/45/89, intercom 0/24/45/89, latch 0/57/45/89), the full-scene contact sheet and native-pixel hardware crops. Hub/spindle registration, screen/LED placement, shaft retraction/foreground occlusion, unchanged object identity and clear hand separation passed sampled inspection. No letterbox, fit box, burned words/captions or watermark was observed. Machine outer-edge checks also passed. Evidence: `frame-check-action.jpg`, `*-hardware-check.jpg`, `visual-review.json` and the per-shot receipt directories listed in `rerender.json` under the new root.

The montage was decoded at frames **0,29,30,50,60,119,120,144,165,209,210,255,267,299,300,329**. Its four cut boundaries and sampled action frames match the expected source clips within mean absolute RGB error <4 after reencoding; `hybrid-frame-check.json` records each measurement. `hybrid-frame-check.jpg` was visually inspected for correct still/handle/intercom/latch/still order. Fresh audio measurements remain **2.300020833s** for the latch cue and **9.300020833s** for the montage cue, peak **−24.6656 dBFS**, both within one frame. No human listening or continuous playback claim.

Correction ledger: conservatively count the original FFmpeg compatibility fix as handle correction 1 and this pivot fix as correction 2 (limit reached). Intercom/latch were each regenerated once for the shared staging change, with no new visual alignment or image corrections. The first rerender wrapper stopped **after a successful handle render** when reading the old MP4 for comparison was denied. It resumed using that same new handle, without rendering it again. Old MP4 and old receipt reads were denied by current permissions; no permission bypass was attempted. All studies, the hold and the synthetic click/mix were regenerated locally using the original formulas and timings. New-vs-old media byte identity/output difference is therefore **NOT_VERIFIED**; the pivot regression is proven independently by the rendered mutation test. Existing media/evidence were preserved.

### Current commands and results

From `D:/s2v-motion`, using the read-only render Python and workspace pytest (no install/write to `D:/story2video`):

```powershell
$py = 'D:/story2video/artifacts/render-venv/Scripts/python.exe'
$uv = 'D:/story2video/artifacts/tooling/bin/uv.exe'
$code = 'experiments/cluepause/genre-pilot-20261124/motion'
$out = 'artifacts/genre-pilot-20261124/motion'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:UV_CACHE_DIR='D:/s2v-motion/artifacts/uv-cache'
$env:UV_PYTHON='D:/story2video/artifacts/tooling/retention-python/cpython-3.13.18-windows-x86_64-none/python.exe'
$env:UV_PYTHON_DOWNLOADS='never'
& $uv run --locked pytest --basetemp="$out/pytest-baseline-review" -o cache_dir="$out/pytest-baseline-cache" -q
# PASS: 61 core tests in 4.44s (supported Python 3.13).
$env:PYTHONPATH='D:/s2v-motion/.venv/Lib/site-packages'
& $py -B -m pytest "$code/test_hybrid_motion.py" -q --basetemp="$out/pytest-final-review" -o cache_dir="$out/pytest-review-cache" --tb=short
# PASS after mutation restoration: 40 motion tests in 19.24s; pytest-final-review.log.
& $py -B "$out/run_review_mutations.py"
# Six mutants killed; exact source bytes restored; mutation-review/results.json.
& $py -B "$out/rerender_review.py"
& $py -B "$code/verify_demo.py" --demo-root "$out/review-fix-20261124"
& $py -B "$out/inspect_review_frames.py"
& $py -B "$out/finish_review_evidence.py"
& $py -B "$code/verify_demo.py" --skip-demos --demo-root "$out/portable-review"
& $py -B "$code/verify_demo.py" --skip-demos --tools "$code/tools.lock.json" --demo-root "$out/configured-reference-review" --reference-media "$out/reference-option-fixture"
& $py -B "$code/audit_delivery.py" --demo-root "$out/review-fix-20261124"
git diff --check
```

The commands above are the invocation ledger, not a rerunnable batch: mutation/fixture creation scripts deliberately retain create-once evidence, and the final 40-test pass occurred after mutation restoration. All final checks PASS. Portable fixture runs also verify deterministic encoded bytes, hostile PATH, combined primitives, original audio/SRT splice and fail-closed replacement length. `audit_delivery.py` accepts versioned roots and binds current source/evidence to the current base SHA. `video/`, dependencies and governance contracts were untouched; npm/Node and governance suites were not repeated for these scoped fixes.

Earlier diagnostic failures are retained: the first new-test run was 39 passed / 1 failed because tiny negative floating-point sine values floor to a 1px overlay offset; the shake assertion now permits raster rounding while still rejecting zero shake. An attempted combined core/motion run using render Python 3.12 produced 3 collection errors (the project package is installed in the Python 3.13 environment); core and motion were then run separately as above. No product assertion was bypassed. The later complete motion run passed with the restored source. The workspace's default pytest cache path is permission-restricted, so the final commands explicitly place caches/temp files below the allowed artifact root.

**Engineering acceptance:** PASS for the reviewed local-motion fixes, rendered regression checks, mutation sensitivity, fresh media/frame/audio checks and portable verifier. **Market acceptance:** NOT_TESTED. Final H01 narrative/voice/caption timing, rights/story qualification, human playback/comprehension and cross-platform byte identity remain unverified. No new external review was commissioned; this is the primary agent's correction/validation record. No commit, push, upload, publication or formal session closeout was performed.

## Historical initial delivery: deliverables and visual inspection

All paths below are relative to `D:/s2v-motion`. Binary outputs are gitignored.

| File | Measured result |
| --- | --- |
| `artifacts/genre-pilot-20261124/motion/handle.mp4` | 3.000 s / 90 frames; lever rotates 0→18° clockwise at 0.35–1.0 s, hand remains clear |
| `artifacts/genre-pilot-20261124/motion/intercom.mp4` | 3.000 s / 90 frames; blank physical glass and listening LED turn on at 0.4–1.2 s |
| `artifacts/genre-pilot-20261124/motion/latch.mp4` | 3.000 s / 90 frames; same shaft translates −405 px at 1.5–2.3 s and disappears behind housing |
| `artifacts/genre-pilot-20261124/motion/hybrid-demo.mp4` | 11.000 s / 330 frames; 1 s original still clip, three motion clips, same 1 s still clip; AAC 48 kHz stereo |
| `artifacts/genre-pilot-20261124/motion/frame-check-action.jpg` | Start / action-middle / end contact sheet, three shots; no editorial labels burned in |

Every output is 1080×1920, H.264/yuv420p, 30 FPS, SAR 1:1. Each clip and the montage passed full FFmpeg decode and ffprobe frame/format validation. ImageGen plates actually arrived at 941×1672; these are cover-cropped/upscaled to delivery resolution. Original alpha elements have different aspect ratios, intentionally resized to their registered prop geometry. [README](README.md) documents all transforms and limits.

| Shot | Decoded frames inspected | Alignment/object result | Borders/text | Corrections |
| --- | --- | --- | --- | --- |
| Handle | 0, 20 (0.667 s), 45, 89 | Hub stays on spindle, one unchanged rigid lever; hand remains below and separate | No box, letterbox, captions, text or watermark observed | 1 shared engine compatibility correction; 0 visual corrections |
| Intercom | 0, 24 (0.800 s), 45, 89 | Insert stays within screen recess; LED centered on physical lens; no object mutation | No box, letterbox, captions, text or watermark observed; screen intentionally blank | 0 |
| Latch | 0, 45, 57 (1.900 s), 89 | Shaft enters keeper initially, slides left on its axis, is occluded by fixed left housing | No box, letterbox, captions, text or watermark observed | 0 |

Inspection was performed by the primary Codex agent on decoded images, including both clip-middle and action-middle samples. It is not an independent review or a human continuous-playback/viewer pass. There is no automatic OCR claim. Every start/end outer edge row and column also passed a nonblack-content check. Same-object continuity follows from the fixed asset hashes and deterministic transforms, alongside the sampled observations; moving lighting/reflection physics are not simulated.

The optional synthetic latch click's first decoded sample above 50 PCM16 units occurs at **2.300020833 s**, matching its 2.3 s cue within one frame. In the montage it occurs at **9.300020833 s**, matching 9.3 s; decoded peak **−24.6656 dBFS**. It was measured, not listened to by a human. The other two studies are silent. There is no dialogue to subtitle in this diagnostic montage, so no invented/empty H01 SRT is supplied. Real caption-sidecar delivery is exercised with the local splice fixture below.

## Historical initial delivery: commands and results

Commands were run from `D:/s2v-motion` except the two npm commands, which ran from `D:/s2v-motion/video`. Python calls used `-B`, preventing bytecode writes into reference dependencies. uv's interpreter and executable were read only. No reference production/build entry point was executed.

Environment used for uv:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:UV_CACHE_DIR='D:/s2v-motion/artifacts/uv-cache'
$env:UV_PYTHON='D:/story2video/artifacts/tooling/retention-python/cpython-3.13.18-windows-x86_64-none/python.exe'
$env:UV_PYTHON_DOWNLOADS='never'
& D:/story2video/artifacts/tooling/bin/uv.exe sync --locked
```

PASS; Python 3.13.18, pytest 9.2.0, workspace `.venv`. Exact local motion/runtime versions and interpreter digest are in `artifacts/genre-pilot-20261124/motion/runtime.json` (render Python 3.12.10, Pillow 12.0.0). `tools.lock.json` records exact FFmpeg/ffprobe executable paths, byte counts and SHA-256, calculated from the Owner-specified verified tool directory before their first invocation.

```powershell
& D:/story2video/artifacts/render-venv/Scripts/python.exe -B experiments/cluepause/genre-pilot-20261124/motion/prepare_demo.py "<Codex generated-images folder>/01a20d06-1fdb-7d63-aed0-760717643d5a"

& D:/story2video/artifacts/tooling/bin/uv.exe run --locked pytest experiments/cluepause/genre-pilot-20261124/motion/test_hybrid_motion.py -q --basetemp=artifacts/genre-pilot-20261124/motion/pytest-tmp

& D:/story2video/artifacts/render-venv/Scripts/python.exe -B experiments/cluepause/genre-pilot-20261124/motion/hybrid_motion.py render artifacts/genre-pilot-20261124/motion/handle.json artifacts/genre-pilot-20261124/motion/handle.mp4
& D:/story2video/artifacts/render-venv/Scripts/python.exe -B experiments/cluepause/genre-pilot-20261124/motion/hybrid_motion.py render artifacts/genre-pilot-20261124/motion/intercom.json artifacts/genre-pilot-20261124/motion/intercom.mp4
& D:/story2video/artifacts/render-venv/Scripts/python.exe -B experiments/cluepause/genre-pilot-20261124/motion/hybrid_motion.py render artifacts/genre-pilot-20261124/motion/latch.json artifacts/genre-pilot-20261124/motion/latch.mp4

& D:/story2video/artifacts/render-venv/Scripts/python.exe -B experiments/cluepause/genre-pilot-20261124/motion/verify_demo.py
& D:/story2video/artifacts/render-venv/Scripts/python.exe -B experiments/cluepause/genre-pilot-20261124/motion/build_preview.py
& D:/story2video/artifacts/render-venv/Scripts/python.exe -B experiments/cluepause/genre-pilot-20261124/motion/audit_delivery.py
```

Staging PASS, initial motion tests **31 passed**. The handle render command was executed twice: the first invocation failed before encoding because FFmpeg 9.1 removed `-filter_complex_script`; changing the module to pass the recorded filter graph directly via `-filter_complex` fixed it. Failed attempt logs remain in `handle-4oc6bdkb/commands.jsonl`; final evidence is `handle-s2k14anj`. No image/spec alignment adjustment or further key-shot retries were needed. Intercom and latch passed on their initial invocation. The correction limit was not exhausted for any shot.

`verify_demo.py` PASS:

- Identical local fixture rendered twice produces identical encoded MP4 SHA-256.
- A real combined rotate/arc-length-path/fade/shake filter is encoded/decoded; hidden-start and rotated/translated endpoint pixels checked. Glow also rendered in the intercom demonstration.
- The real renderer succeeds with an empty/hostile PATH; children use pinned absolute FFmpeg/ffprobe binaries and an allowlisted environment. A unit test exercises the CLI entry point with incorrect executable bytes/digest and verifies no launch and no output-root creation.
- A two-shot local fixture is spliced to 60 frames with its original 2-second mix, AAC output and byte-identical English/Traditional Chinese SRT sidecars. These SRTs are labelled local fixtures, not H01 subtitles.
- A declared 31-frame replacement for a 30-frame clip fails closed, with no final master.
- The actual read-only reference `36-v1/media/timeline.json` and existing cuts adapt to **1151 frames**, including its first cue starting at frame 1. Only a plan is created locally; no reference render or story gate is bypassed.

The README baseline check was also executed exactly:

```powershell
& D:/story2video/artifacts/tooling/bin/uv.exe run --locked pytest
```

Initial result: **40 passed, 21 setup errors**, caused by permission errors in the default pytest temporary-directory setup. No assertion failure is claimed from that run. The retry specifies a writable workspace temporary root and includes both baseline and new tests:

```powershell
& D:/story2video/artifacts/tooling/bin/uv.exe run --locked pytest tests experiments/cluepause/genre-pilot-20261124/motion/test_hybrid_motion.py -q --basetemp=artifacts/genre-pilot-20261124/motion/pytest-all-tmp --tb=short
```

PASS: **92 tests in 4.16 s** (61 existing + 31 new). Saved output: `artifacts/genre-pilot-20261124/motion/pytest-all.log`.

```powershell
$env:npm_config_cache='D:/s2v-motion/artifacts/npm-cache'
& 'C:/Program Files/nodejs/npm.cmd' ci
& 'C:/Program Files/nodejs/npm.cmd' run typecheck
```

Both PASS, seven packages installed, audit reports zero vulnerabilities. npm warns that the available **Node 24.13.0** exceeds the declared Node `>=22.16.0 <23`; validation on supported Node 22 and CI operating systems was not performed. No `video/` source or dependency/lockfile was edited. Governance contracts/framework were untouched, so governance-update verification was not triggered.

```powershell
git branch --show-current
git rev-parse HEAD
git status --short
git diff --check
git diff --exit-code HEAD -- experiments/cluepause/genre-pilot-20261124/urban_horror-v2.md experiments/cluepause/genre-pilot-20261124/production-spec-v2.md experiments/cluepause/genre-pilot-20261124/production.md
```

Branch/SHA match the values above; original inspected story/spec/production Markdown are unchanged. Because new files are untracked, they also receive the following checks. Git emits a warning reading the user's global ignore file; local ignore rules still apply to generated outputs.

```powershell
Get-ChildItem experiments/cluepause/genre-pilot-20261124/motion -File | ForEach-Object {
  $diagnostics = @(git diff --no-index --check -- NUL $_.FullName 2>&1)
  if ($LASTEXITCODE -gt 1 -or $diagnostics.Count) { throw "Whitespace check failed: $($_.Name): $diagnostics" }
}
git check-ignore artifacts/genre-pilot-20261124/motion/hybrid-demo.mp4 artifacts/genre-pilot-20261124/motion/raw/handle-plate.png
```

PASS: tracked diff and every new motion file's whitespace check; both example generated files match the artifact ignore rule.

The first wrapper incorrectly treated no-index exit 1 (new-file differences with no diagnostic) as a whitespace failure. The corrected wrapper above accepts that expected status only when no diagnostic exists; all files pass it.

## Historical initial delivery: persistent evidence and acceptance boundaries

Built-in ImageGen was used **7 times**, with **0 ImageGen correction requests**: three background plates, the lever, screen, listening LED and bolt. The exact tool arguments/prompts/order and original filenames are in [imagegen-requests.json](imagegen-requests.json). No CLI/API fallback was used. Originals are copied into `artifacts/genre-pilot-20261124/motion/raw/`; `assets.json` binds original/staged hashes, crops, alpha checks and the inspected H01 source hash.

Successful clip evidence directories are `handle-s2k14anj`, `intercom-if8n_g3h`, `latch-81l7luks`; the montage receipt/log is in `hybrid-demo-splice-j_njnzfn`. Each contains exact FFmpeg/ffprobe argv, exit result/stdout/stderr, probe/full-decode evidence and source bindings. Each shot contains full-resolution start/middle/end PNGs and `action-middle.png`. `visual-review.json` records per-shot frame inspection and correction attempts; `verification.json` records executable media tests. `delivery-manifest.json` binds final code and evidence/media bytes, including generated assets. These records preserve the distinction between machine checks, agent visual inspection and human evaluation.

Executable inventory under the `external-executable-trust-audit` skill: FFmpeg/ffprobe are active, exact-path/size/digest bound before each launch; argv are generated from validated numeric specs, child environment contains only OS roots and workspace TEMP/TMP. Python/uv/npm are explicit local launch paths recorded above. The outer interpreter/dependency/DLL chain has not received a comprehensive adversarial audit, so a process-tree-wide executable-trust claim is **evidence insufficient**. No authorization, credentials or hosted publishing boundary exists in this isolated module.

**Engineering acceptance:** PASS for this local reusable 2D motion layer, per-shot decoded samples, tested deterministic primitives and timeline adapter/splice. The H01 latch is a visible sliding-bolt staging study; final cross-shot prop/mechanical continuity is pending. The blank screen is a power-on study; H01's required photographed rule/input/saved-word readouts are not produced. Full 39-second H01 timing, exact recorded voice/cough matching, invitation-before-latch ordering, phone text readability, physical reflection/contact realism and human playback remain unverified. The montage is a diagnostic sequence, not a narrative pacing pass. Cross-platform byte identity and supported Node 22 execution are not verified.

**Market acceptance:** NOT_TESTED. No human attraction/comprehension score, story/genre/rights approval, release authority, retention data or public result is claimed. The original local delivery is committed at `5253512d18ad15e7a4e3c7f8e84615b0012b077d`; the review fixes were subsequently committed at `6270889a9de8cfb056c7009b69ffa01f7e02e474`. No formal session closeout was requested; task completion is not a session-end event under `AGENTS.base.md`.
