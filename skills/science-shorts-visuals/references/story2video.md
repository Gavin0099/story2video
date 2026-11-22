# story2video pilot reference

Read when working in story2video. Paths below are repository-relative, not relative to this skill. Read current PLAN.md, AGENTS.md, AGENTS.base.md and contract.yaml; a later pilot authorization does not authorize release.

## Content and examples

- `experiments/science-shorts/batch-20261121/scripts-final.json` / `.md`: reviewed bilingual scripts for ice, sky and radio in space. Its `source-cards.json`, `gate-policy.json`, `editorial-gate.json` and `reviews/` contain original evidence. The original policy uses an 85-point comprehension candidate threshold plus separate fact/visual requirements. These are pilot criteria, not universal standards or human validation.
- `artifacts/science-shorts/batch-20261121/{ice,sky,space}/timeline.json` and `narration.wav`: actual Kokoro speech and timing. Hash-bind and compare public en/zh text when reusing them.
- `experiments/science-shorts/ice-visual-v2/`: generated glass/ice layers, magnification, equal-count comparison and fresh preview/encoded-output reviews. Do not modify its frozen renderer when using it as a dependency.
- `experiments/science-shorts/sky-space-visual-v2/`: matching day/sunset scenes and astronaut layer, with separate reviews per topic. Shared typography/caption helpers are hash-bound to the ice renderer; its approval is not copied.
- `experiments/science-shorts/visual-direction-review.md`: initial fixed-layout diagnosis and rationale for layered scenes plus mechanism animation.

These pilots use Pillow/numpy and FFmpeg. `video/` is a Remotion scaffold, not a finished science composition. Do not claim production Remotion integration, a new Episode contract or complete SC-00/01 productization.

These paths are historical evidence and runnable local pilot examples, not the mandatory renderer for every new handoff. A plan-only request can use original scripts/timing without reading a completed visual revision or invoking its commands. When reusing a specific renderer, inspect its actual prerequisites first.

## WhyNest Lab art direction

The owner selected the right-hand, full-bleed version of the paper towel opening. The optional visual reference is `artifacts/science-shorts/visual-direction-20261122/comparison.jpg` in the project workspace. This choice sets the look for WhyNest Lab and was made on a still comparison.

- **Start with the physical change.** Frame the subject for the full 9:16 image and use a close view when the change is small. For a tabletop effect such as condensation, wicking or a suction cup releasing, prefer actual footage when it can be captured or sourced within scope. If an illustration suits the shot, generate a wordless portrait composition with the subject and action already positioned for mobile.
- **Keep the scene recognizable as the shot gets closer.** Carry a visible anchor into the detail shot, such as the same glass rim, towel edge or liquid surface. Match camera side, orientation, color and lighting across assets. Use a close-up, inset or cutaway when it reveals something new, and retain a visual link to the original object.
- **Place labels at the moment and location they help.** Add short English labels and leaders in editable layers. Give the subject the full frame and use the available space around it for the title or annotation. Provide selectable English and Traditional Chinese subtitles in the delivery workflow. Preview on a phone-sized frame with captions visible to check that the labels and key motion are clear.
- **Use the existing compositor for the shot.** Layer footage or stills with masks, camera moves and tracked callouts. Reserve a 3D cutaway for a mechanism that genuinely needs depth to make sense. Keep the mechanism and its comparisons under animation control and identify schematic or time-compressed views where that affects interpretation.

For paper towel wicking, establish the strip in the glass and follow the wet edge upward in a matched close-up. Keep the wet region connected to the reservoir and the reservoir surface recognizable as the reference level. If the explanation moves inside the paper, anchor the magnified fiber diagram to the same wet edge. Inspect the frames on both sides of that transition during the existing visual review.

## A minimal planning handoff

For example, a sky setup cue can be recorded as follows. This is a planning record, not an executable render manifest or an approval:

```json
{
  "cue_index_zero_based": 2,
  "fps": 30,
  "start_frame_inclusive": 216,
  "speech_end_frame": 332,
  "end_frame_exclusive": 341,
  "public_text": "Reuse the approved cue without rewriting",
  "purpose": "Follow incoming mixed light into the atmosphere",
  "layers": ["scene", "atmospheric shell", "editable light paths"],
  "motion": "Camera changes scale; incoming color components stay bundled",
  "invariants": ["No prism-like separation by air", "Label geometry schematic"],
  "source_claim_ids": ["c2"],
  "production_verification": "Not run in this planning example"
}
```

A production bundle records paths, byte sizes and measured digests for required inputs and dependencies, the reviewer identity/scope/result, and the covered renderer/input-manifest digests. Label metadata-only hashes as declared until verified. A handoff can propose the bundle without claiming a production pass.

Original vector-only art constraints belonged to the initial programmatic pilots. The Owner later explicitly requested and accepted generated illustration layers; that authorizes those visual revisions while keeping scientific diagrams editable and source figures uncopied. A new unrelated task must use its own actual authorization rather than infer a standing waiver.

## Reuse and evidence

Use a new source/output directory for revisions. Keep original videos and reviews. Freeze inputs including executable helpers outside the renderer directory. The v2 review convention includes `status`, `critical_defects`, `renderer_sha256`, `inputs_sha256`; PASS covers only those bytes and the stated review scope. Original reader scores are not new video scores. Main-agent observations are not independent results.

Local dependencies currently include `artifacts/render-venv/` and verified tools under `artifacts/render-tools/verified/`. Read the renderer and Episode02 manifest for canonical paths, sizes and digests. Do not fetch different binaries for convenience or claim fresh-clone reproduction without required assets/models.

Example commands from repo root, using the existing local environment:

```powershell
& 'artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/sky-space-visual-v2/render.py --episode sky --mode preview
& 'artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/sky-space-visual-v2/render.py --episode sky --mode render
& 'artifacts/render-venv/Scripts/python.exe' -I experiments/science-shorts/sky-space-visual-v2/render.py --episode sky --mode qa
```

Use `--episode space` for its files/review. Final render/QA require the matching new review. `prepare.py` freezes once; it is not an approval-refresh command. Changed code needs a new review, not edited reviewer evidence. In another workspace resolve/verify intended tools according to project rules; the relative launcher above is a usage example, not an outer-shell trust claim.

## Scientific traps

- Ice: most floating ice stays submerged. Art-asset bubbles do not explain ordinary ice buoyancy. Compare same-size, equal-count water symbols; a grid is not a crystal model.
- Sky: side-scattered light reaches an observer not looking at the direct Sun. Use the same observer/atmospheric shell for sunset path comparison. Redirect blue outward; let red/orange continue forward. Check pulse pairs for travel direction.
- Space: do not add matter to a vacuum to show sound. In an independent AIR inset particles oscillate locally; an advancing compression marker is not a traveling particle. Receiver speaker/air/ear belong inside a labeled helmet cutaway. Distant stars are not a local medium.

## Validation

Run README.md checks and record Git SHA, commands, results and limits: `uv sync --locked`, `uv run --locked pytest`, then `npm ci` and `npm run typecheck` in video/. Windows may use `npm.cmd`. Record installed Node differing from the pinned range.

Pilot QA additionally needs full decode and real MP4 samples, glyph-based caption bounds, audio loudness/true peak, black/silence checks. Sky has an intentional final pause around 2.1 seconds; record that hold rather than changing narration to satisfy a generic silence rule.

Record actual assets/prompts and reported cost. Subscription, human review and compute are not automatically zero cost. Technical/scientific checks do not supply mobile human viewing, aesthetic approval, retention or channel-market evidence. Leave these pending until observed.
