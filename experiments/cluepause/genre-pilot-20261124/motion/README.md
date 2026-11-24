# CluePause hybrid motion

Local experiment authorized on 2026-11-24. A photographic plate stays fixed while separately generated RGBA props move through deterministic FFmpeg filters. Pillow only stages cover crops, transparent margins, pivot padding and fixed glow halos. No generative video, production CLI/schema change, story revision or publishing integration.

The current demonstrations are three 3-second H01 motion studies plus an 11-second still/motion/still montage. They are not a finished 39-second H01, a story qualification, or release evidence. [Acceptance and exact commands](acceptance.md); [ImageGen requests](imagegen-requests.json).

## Run

From `D:/s2v-motion`, PowerShell:

```powershell
$py = 'D:/story2video/artifacts/render-venv/Scripts/python.exe'
$code = 'experiments/cluepause/genre-pilot-20261124/motion'
$out = 'artifacts/genre-pilot-20261124/motion'
& $py -B "$code/hybrid_motion.py" render "$out/handle.json" "$out/handle-new.mp4"
& $py -B "$code/hybrid_motion.py" splice "$out/hybrid-timeline.json" "$out/hybrid-new.mp4"
```

Python needs Pillow (tested 12.0.0); math/parser tests need pytest. The existing render venv is read only: do not install into it. CLI help and parser/math tests use the standard library. FFmpeg/ffprobe are pinned by canonical absolute path, byte count and SHA-256 in `tools.lock.json`, verified before output roots and before every launch. On another machine, independently verify the binaries and update that local binding explicitly. Child processes have an allowlisted OS environment and no PATH lookup. All generated writes are restricted to this checkout's `artifacts/genre-pilot-20261124/motion/`; input assets can be read elsewhere. No shell or network calls exist in the module.

`prepare_demo.py <original-generated-directory>` copies the seven original ImageGen PNGs into `raw/`, preserves their alpha, creates matching `layers/`, three shot JSON specs and a synthetic click. It refuses to overwrite a staged demonstration. The original filenames are in that script and `imagegen-requests.json`. Generate new imagery explicitly if the original PNGs are unavailable; do not pretend the prompts reproduce identical pixels. `build_preview.py` creates the still holds, local mix and montage after the three clips exist. `verify_demo.py` runs real-media checks and creates additional decoded action samples. It uses create-once output names; use a new version directory in code when deliberately repeating the entire experiment.

## Shot contract

Example for a transparent 440×119 element. Paths are relative to the JSON file; absolute local paths also work.

```json
{
  "version": 1,
  "frames": 90,
  "background": "layers/handle-plate.png",
  "layers": [{
    "id": "lever",
    "image": "layers/handle-element.png",
    "size": [440, 119],
    "pivot": [57, 60],
    "anchor": [368, 921],
    "motions": [{
      "type": "rotate", "from": 0, "to": 18,
      "start_s": 0.35, "end_s": 1.0, "easing": "smoothstep"
    }]
  }],
  "sound_cues": [{"file": "click.wav", "time_s": 1.0, "gain": 0.6}]
}
```

Output is always opaque full-bleed 1080×1920, square pixels, 30 FPS H.264/yuv420p. `frames` is authoritative. Frame `n` samples time `n/30`; animations must end by `(frames-1)/30` to show their final state. The plate is scaled to cover and center-cropped, never fitted, boxed or stretched. Crop/reframe source assets first when a centered cover crop would cut off evidence. Elements require real alpha; flat backgrounds must be removed and inspected before rendering. Unknown fields, nonfinite values and invalid intervals fail closed.

Coordinates are pixels, x right and y down. `size` is the resized element's dimensions; `pivot` is inside that resized element; `anchor` is the pivot's position on the final canvas. Layers composite in list order, last on top. The pivot is padded to the rotation canvas center without integer rounding. Static foreground layers can occlude moving parts; the latch example copies its original plate's housing pixels into a foreground alpha layer.

| Primitive | Motion fields | Meaning |
| --- | --- | --- |
| `rotate` | `from`, `to` | Degrees clockwise about pivot; supports a needle/handle |
| `translate` | `path: [[x,y], ...]` | Offset from anchor, polyline traversed by arc length; 2–32 points; supports drops/latches |
| `fade` | `from`, `to` | Opacity in [0,1] |
| `glow` | `from`, `to` | Opacity of an emissive asset and its optional static halo; add layer `glow_radius` in pixels |
| `shake` | `amplitude: [x,y]`, `cycles` | Fixed-phase sine displacement, sine envelope, zero outside interval; max 30 px per axis |

Each motion has `start_s`, `end_s`, optional `easing`: `linear` (default), `smoothstep`, `ease_in`, `ease_out`. Shake uses its own envelope and accepts only linear easing. One of each motion type per layer; fade and glow share a single opacity channel. Distinct primitives compose as rotation, translated anchor plus shake, and opacity. Optional layer `opacity` multiplies motion opacity. Motion endpoints hold before/after their interval; shake returns to zero. `sound_cues` place local audio files on the shot clock at 48 kHz with optional gain. No synthetic cue is added unless specified. Review clipping/loudness when supplying real sound.

## Replace shots in an existing still timeline

Keep the existing still renderer's `media/cuts/shot-NNN.mp4` clips and actual spoken `media/timeline.json`. Group indices are contiguous shot **occurrences**, not the `shot` ids in narration cues. Repeated adjacent cues with the same id form one group. The first group's start is zero, matching the reference renderer even when its first spoken cue starts at frame 1.

Create `replacements.json` mapping group indices to newly rendered clips, then:

```powershell
& $py -B "$code/hybrid_motion.py" legacy-plan `
  'D:/story2video/artifacts/cluepause-retention-ten/36-v1/media/timeline.json' `
  'D:/story2video/artifacts/cluepause-retention-ten/36-v1/media/cuts' `
  "$out/replacements.json" "$out/replacement-plan.json"
```

The adapter only reads that reference. For actual production, use a workspace copy of the intended timeline. Before rendering, replace the selected group's spec `frames` with its exact group length, preserving the original timeline. The plan has this shape:

```json
{
  "version": 1,
  "shots": [{"clip": "existing-still-shot.mp4", "frames": 90},
            {"clip": "new-motion-shot.mp4", "frames": 60}],
  "audio": "original-timeline-mix.wav",
  "sidecars": {"en": "original.en.srt", "zh-Hant": "original.zh-Hant.srt"}
}
```

Add the original `audio` and `sidecars` entries to the generated plan, using paths relative to the plan or absolute paths. `splice` decodes/validates every clip, rejects mismatched dimensions, frame counts, frame rates or pixel aspect, concatenates frames, and reencodes H.264. It retains the supplied timeline mix, reencoding audio to 48 kHz stereo AAC. Input mix duration must match total video within one frame. Individual shot audio is discarded: place the new cues in the timeline mix at `group_start/30 + local_cue_time` first. Omitting `audio` deliberately creates a silent master. SRTs copy byte-for-byte beside the master; the tool never burns or muxes subtitles, questions or watermark text. Its SRT copy check does not assess linguistic correctness or source timecodes.

For the H01 reveal, latch motion and its click must follow the final played “in.” This module has no semantic story gate: bind the final spoken/playback timeline and check that order before production. The blank intercom demo does not implement H01's necessary in-world status text, voice/cough matching or live/saved readouts.

## ImageGen layer requests and correction limit

Request one full-bleed 9:16 photographic **plate with the moving element absent**, retaining the fixed mounting/housing, and a separate **single rigid element on true transparent alpha**. Reuse the plate as a reference. Specify identical camera angle, focal perspective, material, light direction/color, scale and intended pivot/contact point. Avoid residual element shadows in the plate. For a flat-background fallback request a uniform removable color absent from the element, then inspect the resulting matte; this demo used genuine alpha. Never request multiple animation states from ImageGen: those can change the object and break fair clues. Stage to 1080×1920 with cover cropping, inspect alignment and record the transforms. Keep originals and hashes.

For **each key shot**, allow the initial attempt plus **at most two correction attempts**, including positioning, masking, timing or replacement imagery. After each attempt inspect decoded start, action-middle, clip-middle and end frames plus any causal transition. If it still fails after correction 2, **stop that shot** and report its id, observed defect, both attempted fixes and evidence paths. Do not silently regenerate, keep retrying, replace the shot with an unreviewed asset or count a failed shot as passed. The CLI has no automatic correction loop; maintain this ledger manually in the acceptance record. A global engine compatibility fix must also be recorded and conservatively charged to the shot that exposed it.

## Evidence and limits

Each render retains the staged plate/elements, filter graph, exact FFmpeg/ffprobe argv and results in `commands.jsonl`, full decode/probe, source SHA-256 bindings, receipt, and decoded start/middle/end PNGs in its uniquely named evidence directory. `verify_demo.py` adds action-middle PNGs and `frame-check-action.jpg`. Successful masters appear only after format and full-decode checks. Failures leave staging and logs, with no final output. Existing outputs are never overwritten. Sidecar copying can leave partial sidecars on filesystem failure; choose a new output name for recovery.

After the preview and manual decoded-frame inspection, `audit_delivery.py` measures cue timing, checks the final montage and hashes final code, media and evidence into `delivery-manifest.json`. Re-running it refreshes that manifest and its diagnostic WAVs/logs; it does not replace the reviewed clips. `visual-review.json` is the separately recorded agent inspection, not an automatically inferred visual pass.

Determinism is demonstrated with identical encoded bytes on this pinned local toolchain; cross-platform/encoder-version byte identity is not claimed. No 3D perspective, relighting, moving reflections, deformation, hand/prop interaction, automatic matte/registration or full-film editorial validation. Shadows/glow are baked/static in prop space. Transparent margins can clip a large glow; inspect the halo before finalizing. The element remains the same bitmap; rotation interpolation/compression change sampled pixels. The source plates are 941×1672, upscaled to delivery resolution. The visible sliding-bolt study illustrates retraction and needs final prop/lock continuity review in H01.

Run local tests explicitly because the repo's default pytest discovery targets only `tests/`:

```powershell
uv run --locked pytest tests experiments/cluepause/genre-pilot-20261124/motion/test_hybrid_motion.py `
  --basetemp=artifacts/genre-pilot-20261124/motion/pytest-all-tmp
& $py -B "$code/verify_demo.py"
```

Engineering checks and visual sample inspection do not establish human appeal, silent-viewer comprehension, rights clearance, the H01 story/genre gates, or market acceptance. No upload, commit, public action or modification to `D:/story2video` is part of this work.
