# Static photographic storyboards

Shared, offline pipeline for the next 4 puzzle, 3 uncanny_mystery and 3
urban_horror jobs. This task builds the pipeline, not those ten stories. Character
animation is paused. The existing motion module is not imported or required.
No ImageGen client, upload client or YouTube integration is present.

The implementation generalizes the A path of
`experiments/cluepause/genre-pilot-20261124/h01_v21_ab.py` and the adjacent
`production-spec-v2.md`. It preserves photographic cover crops, the measured
Kokoro PCM approach and exact FFmpeg binary bindings without importing motion.
This isolated experiment does not change Episode v1 or the production CLI.

## Environment

Use a local Python with `jsonschema` and Pillow installed. Pytest is needed for
tests. The repo's locked environment supplies jsonschema/pytest; the renderer
also needs Pillow (not added to the core engine's dependencies). Local TTS
additionally needs the existing `kokoro_onnx` environment and its dependencies.
There are no downloads in this program. Run Python with `-B` to prevent bytecode
writes in shared/read-only environments.

Supply these environment variables from your local installation, without
putting absolute paths in story files, prompts, logs or tracked configuration:

| Variable | Value |
| --- | --- |
| `S2V_FFMPEG` | Existing verified FFmpeg executable |
| `S2V_FFPROBE` | Existing verified ffprobe executable |
| `S2V_QUESTION_FONT` | Local font supporting both English and Traditional Chinese |
| `S2V_KOKORO_MODELS` | Local model directory; unnecessary for prerecorded WAVs/smoke |
| `S2V_GIT_SHA` | `git rev-parse HEAD` result for provenance; otherwise explicitly UNRECORDED |

`tools.lock.json` pins the exact A-pilot executable sizes and SHA-256 values.
Executables are verified before use; subprocesses use full resolved paths and
argument arrays, no shell and no PATH search. The font and installed provider
packages are environment prerequisites, not bundled assets. Use a licensed font
with Traditional Chinese glyphs and visually inspect the question.

## Run one story

From the repository root, copy `pipeline/template/` to your genre job's story
folder, for example `experiments/cluepause/static-ten-20261124/puzzle-01/`.
Give it a unique revision-aware `story_id`, such as `puzzle-01-v1`, before running
anything. All three jobs use this same pipeline file. Each job owns its own
story folder and output id; never edit another job's files.

```powershell
$pipe = 'experiments/cluepause/static-ten-20261124/pipeline'
$story = 'experiments/cluepause/static-ten-20261124/puzzle-01'
python -B "$pipe/static_storyboard.py" validate $story
python -B "$pipe/static_storyboard.py" prompts $story
```

1. Replace `story.md`, `shots.json` and `references.json` together. The Markdown
   starts with `# FICTION`, declares the matching `Genre: ...`, and includes
   `## Script` and `## Shot list`. JSON carries the exact rendered timeline,
   bilingual lines and visual instructions; keep the human script consistent.
2. Generate **one canonical character/prop/set reference sheet first** in a
   separately authorized image workflow. This pipeline only writes prompt
   payloads. Save the sheet at the story-relative path from `sheets.reference`.
   Log every completed call immediately, including rejected outputs:

   ```powershell
   python -B "$pipe/static_storyboard.py" log-image $story --sheet reference --result assets/reference.png --status accepted
   python -B "$pipe/static_storyboard.py" prompts $story --supports-images
   ```

   The second command extracts canonical cells into the story's output
   `prompts/references/` and includes their names in each applicable payload's
   `reference_images`. Attach **all** listed images when the image tool supports
   image input. Canonical invariant descriptions are always injected, including
   when image input is unavailable. Do not request image-conditioned payloads
   until the canonical sheet exists.
3. Generate shot sheets from their payloads. Each `CELL` instruction carries its
   narrative function and required reference ids. A 2×3 sheet contains six
   independent photographic shots, never a video layout. Assign each used cell
   explicitly, trim seams and check portrait crops. Preserve rejected versions
   under distinct result filenames and log accepted/rejected receipts with
   `log-image --sheet shots --result assets/shots.png --status accepted`.
4. Keep the budget around **3–5 total calls**, including reference creation and
   corrections. Two calls can suffice for a short story. Use one reference sheet
   plus 1–3 shot sheets; reserve a correction slot rather than spending all five
   on originals. Inspect `images.jsonl` **before** every external call. Logging
   rejects a sixth total call or third call for one sheet. No automated client
   can enforce usage outside this workflow; never make an unlogged call. A
   payload records the actual prompt hash; do not alter the prompt after export
   without re-exporting it. Regenerate payloads if invariants or shots change.
5. Use local Kokoro or per-line prerecorded WAVs. Default voice is explicit in
   each line, with the existing natural speed of 1.08. Model bytes must match
   the hashes embedded in the implementation. Each line is synthesized once,
   trimmed to active PCM with 5 ms margins, and placed using its actual sample
   length, `gap_before` and `not_before`. Prerecorded `file` takes precedence and
   must be 24 kHz mono PCM16, already trimmed to speech boundaries. No TTS is
   needed for prerecorded audio. SFX use that same WAV format, have bilingual
   accessibility cues, and must fit their declared shot; clipping and truncation
   fail instead of silently changing audio.
6. Adjust cuts around that audio, then render:

   ```powershell
   python -B "$pipe/static_storyboard.py" run $story
   ```

   Explicit seconds or measured cue bindings are accepted for each shot endpoint:

   ```json
   {"cue": "setup", "edge": "end", "offset": 0.2}
   ```

   Endpoints resolve to the nearest 30 fps frame. Shots must cover a contiguous
   timeline from zero, at least through 3.5 seconds; speech/SFX cannot extend past
   the picture. Lines with `reveal: true` cannot start before the first reveal
   shot. Every narration/dialogue line and meaningful audio clue belongs in the
   cues; the pipeline does not transcribe or detect omitted speech.

## Input contract and references

`shots.schema.json` and `references.schema.json` are JSON Schema 2020-12.
`validate` applies both and cross-file rules. A source is
`{"sheet":"shots","cell":0,"crop":[0,0,1,1]}`. Cells are zero-based, row-major.
Crop coordinates are normalized `[x,y,width,height]` **inside the seam-trimmed
cell**. Extraction then performs a centered 9:16 cover crop to 1080×1920.
Choose a crop that keeps the clue visible; recompose the source if cover loses
essential evidence. No contain mode, padding or sheet display exists.

`camera.zoom` gives starting/ending zoom, restricted to 1–1.25.
`camera.from`/`to` give normalized viewport positions in the remaining pan space.
Equal values make a static hold, changing zoom gives a slow zoom, changing
positions gives a pan. Cuts occur between shots. There is no character motion.

Every reference declares `kind` (character/prop/set), invariant features,
canonical sheet/cell/crop and `appears_in` shot ids. Each shot lists exactly those
`required_references`. The reciprocal registry rejects omissions or unknown ids.
Declare **all** recurring items: the validator cannot discover an unregistered
person/prop in a photograph. It rejects missing narrative functions, no reveal,
and no clue close-up before the first reveal. These structural checks cannot
prove that a clue is fair or that a generated person actually matches a reference.

`conveys` is the silent frame's expected observation, not narration or an
explanation card. `prompt` is photographic staging. Do not let setup images,
in-world text, spoken audio or captions disclose the answer prematurely. Fiction
framing belongs in script/manifest/review context, outside the video image.

## Outputs, isolation and review

All generated files stay under
`artifacts/static-ten-20261124/<story-id>/` (already gitignored):

| File/directory | Purpose |
| --- | --- |
| `<story-id>.mp4` | Clean master, full-bleed 1080×1920 30 fps, H.264 High/yuv420p CRF18, faststart, AAC48k stereo |
| `<story-id>.en.srt`, `<story-id>.zh-Hant.srt` | Separate switchable sidecars; never muxed/burned |
| `timeline.json`, `assets.json`, `manifest.json` | Measured cues, source/plate hashes, fiction and input/toolchain bindings |
| `commands.jsonl` | Arguments, exit status, wall time, diagnostics; portable path tokens |
| `images.jsonl`, `prompts/` | Manual image-call receipts and canonical-conditioned prompt payloads |
| `qa/report.json`, `qa/probe.json` | Format/frame/duration/audio/faststart/sidecar results |
| `qa/<shot-id>/`, `qa/<shot-id>-strip.jpg` | Decoded master frames every 7 frames (4.286 fps), final frame, timestamped contact strips |
| `silent-storyboard.jpg`, `silent-storyboard.json` | Ordered isolated key plates without question/captions/narration, plus separate intended meanings |
| `cost.json` | Image call count, encode count, render wall time, failure/pass result |
| `cache/`, `tmp/` | This story's voice, plates, encoded cuts and temporary/provider caches |

The opening question is the only editorial image text and appears at 1.0–3.5 s,
including across cuts. No narration captions or fiction labels are burned in.
Scripted photographed in-world evidence is allowed. The silent storyboard uses
the extracted source plates before question compositing; it is a source-staging
review, while dense strips show decoded output including camera and question.

Per-story exclusive locks reject simultaneous use of the same id; separate ids
share no mutable caches. No existing master is overwritten. After a failed render
with a master present, use a new revision id and preserve the failed evidence.
Only remove a stale `.running` after verifying its owning process has stopped.
QA/cost logs remain available on render failure; an error before rendering or
toolchain initialization may have no completed QA/cost record.

QA fully decodes the master and probes duration, counted frames, resolution,
frame rate, H.264 profile, pixel format, AAC layout/duration, no subtitle stream
and faststart atom order. It runs audio loudness/peak measurement (diagnostics
in commands.jsonl), checks PCM-derived caption bounds and compares SRT content
exactly to generated cues. This is timing provenance, **not ASR or listening**.
Human continuity, phone readability and comprehension remain PENDING; market
acceptance is NOT_TESTED. Image costs are UNKNOWN when manual calls exist;
wall time measures this render invocation, not external generation or editorial
time. Encode count counts each libx264 cut; the final stream-copy/AAC mux is
separately recorded in command history.

## Storyboard Quality checklist

- Situation is clear from the first shot and first concrete observation.
- Each cut adds a new observation: establish, clue, reaction, reveal or purposeful transition.
- Clue close-up is visible and readable once on a portrait phone, at all camera positions.
- Reaction is readable as a response to the immediately preceding observation.
- Reveal re-explains earlier shots through matching visible evidence.
- Character face/wardrobe, prop geometry and set layout match canonical references.
- Silent storyboard conveys the core event without narration or question text.
- No crop, seam, frame edge or camera move hides evidence; all shots fill the canvas.
- Sidecars cover actual speech and meaningful sounds, end with their PCM, and reveal nothing early.
- Listen with EN sidecar, zh-Hant sidecar, captions OFF/sound ON, then sound OFF/captions OFF.
- Record actual human findings separately from technical QA and later market evidence.

## Offline verification

From the repository root, using a Python with the prerequisites above:

```powershell
python -B -m pytest experiments/cluepause/static-ten-20261124/pipeline/tests -q -o cache_dir=artifacts/static-ten-20261124/pytest-cache --basetemp artifacts/static-ten-20261124/pytest-temp
python -B experiments/cluepause/static-ten-20261124/pipeline/smoke.py --id synthetic-smoke
git diff --check
```

The smoke creates solid-color multi-cell sheets, tone WAVs and an SFX, then runs
the same prompt/reference extraction, cell extraction, renderer, sidecars and QA
at full delivery resolution. It performs no ImageGen or TTS calls. Use a fresh
`--id` on subsequent runs so earlier evidence is preserved. Synthetic tones
prove audio/timing plumbing, not speech intelligibility or story quality.

Root `uv run --locked pytest` remains the core-engine regression command. No
`src/story2video/`, `video/`, governance, memory or Episode schema is modified.
