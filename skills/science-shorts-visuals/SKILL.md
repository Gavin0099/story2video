---
name: science-shorts-visuals
description: Produce science Shorts with filmed or illustrated scenes, layered motion and accurate explanatory animation. Use for new science videos or visual upgrades of approved narration, including story2video pilots.
---

# Science Shorts Visuals

Build a watchable explanation: a concrete scene introduces the question, controlled animation shows the cause, and the ending returns to the original scene. Treat the scene illustration and scientific diagram as different production responsibilities.

For story2video, read [references/story2video.md](references/story2video.md) for contracts, pilot commands and evidence locations. Locate the repository from the active workspace instead of assuming a drive or copying old output paths. For planning, start with raw content; completed renderers are historical examples unless the task is to reuse or inspect them.

## Establish the content

- For a visual-only revision, retain approved narration, translation, voice and timing unless the user also requests editorial changes. Preserve the original video for comparison. Old script scores describe that script, not the new visual quality.
- Read existing visual/rights constraints before choosing raster or vector. A later user request can supersede an earlier art-direction constraint; record that change and retain scientific and rights invariants. Do not ask again for an override already authorized in the conversation.
- For a new topic, research the mechanism before drafting. Keep traceable primary sources for factual claims and record simplifications. Apply the project's editorial criteria and independent fact/comprehension review before final production; do not invent reviewer scores or substitute source quantity for correctness.
- Deliver local previews and videos within user scope. This skill does not authorize uploads, public release, channel creation, a new paid provider or unrelated engine work.

Match the requested stage: a planning task delivers a handoff and proposed checks; an art-prototype task delivers labeled samples; production performs the applicable review and render; an encoded-video audit inspects existing files. Later-stage instructions below are future handoff requirements when those stages were not requested.

## Design shots before assets

For opening hooks, pacing, payoffs and mobile first-watch tests, use [shorts-viewer-gate](../shorts-viewer-gate/SKILL.md). Plan for the next visible causal step after the opening, and use the science workflow below to check how that step is portrayed.

Give each shot a purpose: the question, a change of scale, a causal step, a comparison, or the return to the answer. Record narration/timing, subject/action, framing, layers, camera movement, overlays and scientific invariants. Preserve speech end separately from cue end/intentional hold, and state whether frame ends are exclusive; see the handoff example in the project reference.

For WhyNest Lab, use the approved [full-bleed art direction](references/story2video.md#whynest-lab-art-direction). Lead with the phenomenon in a 9:16 scene, follow the same object into a closer view, and add editable annotations where the explanation needs them.

Use scene changes when understanding benefits from them. Avoid a permanent title/diagram/subtitle-card layout for the whole video. Enlarge the subject, reveal labels when needed and reserve readable mobile subtitles. Arbitrary cuts, constant zooming and decorative particles do not replace explanation.

Useful patterns include familiar object → magnification → controlled comparison → original object, or character's problem → mechanism inset → resolved action. These are options, not a fixed shot count or timing.

## Create coherent layers

Choose consistent palette, lighting, materials and characters. For raster scenes or cutouts, use the available image-generation tool and imagegen workflow. Use references for alternate views, edits or time-of-day changes. Request genuine transparency for foregrounds and inspect the alpha.

Save selected assets into the workspace. Persist prompts, reference roles, paths, generation mode and reported cost. An unreported price is not evidence of zero cost.

Keep diagram labels, counts, arrows, comparisons and timing in editable code/vector layers. Do not accept an attractive generated molecular structure, ray diagram or formula as verified science. Prefer native vectors for simple diagrams rather than generating an arrow or dot.

Use restrained parallax, object motion, material highlights and changes of scale. An illustrated still with a zoom can support a shot; it should not carry every causal step.

## Make the mechanism auditable

- Preserve comparison invariants. Equal amount/mass requires equal molecule symbols; do not imply molecular swelling by enlarging comparison symbols. Magnification is a different viewing scale and should be presented as such.
- Distinguish schematic geometry and exaggerated spacing from measured results or actual crystal structure. Explain meaningful simplifications.
- Keep incoming/outgoing light arrows and pulses consistent. Do not show scattered blue light changing into red to explain sunset.
- For sound, distinguish local particle oscillation from propagation of a disturbance. Keep AIR examples separate from vacuum; distinguish radio across a gap from local sound at speaker and ear.
- Check the topic's actual invariant rather than copying these examples mechanically.

## Review and inspect the encoded file

Produce representative full-resolution frames and motion pairs before full rendering. Inspect the question, mechanisms, comparison and answer, including transitions that might introduce ambiguity.

When independent reviewers are available and delegation is authorized, obtain a fresh scientific visual review. Give the actual plan, renderer, assets, sources and representative frames; request findings and limitations rather than a preselected verdict. Apply the project's review requirement. If a required reviewer is unavailable, label the result as a draft and report the missing check instead of fabricating a pass.

Bind a required production review to the exact renderer, executable helpers and inputs: script, audio, timing, sources and assets. Record relevant fonts/tools when reproducibility depends on them. Distinguish a hash declared in metadata from a digest actually measured from a file. Planning may list unverified bindings, but required production bindings must be checked. Changed narration or scientific visuals need appropriate new review. A stale or absent required pass must reject final encoding; do not refresh approval hashes yourself to make a gate pass. Distinguish art prototypes from reviewed production.

Use the existing renderer when practical; isolate experiments when integration is outside scope. Do not install another animation stack merely because it exists. Describe the engine actually used. Reuse verified media-tool bindings where present; do not silently change executable or provider.

Validate MP4 dimensions, frame rate, codec, duration, full decode, caption bounds, audio level/peaks, black frames and unexpected silence. Record the actual commands, thresholds and intentional-hold exceptions; use project criteria rather than universal guessed values. Extract frames and motion pairs from the encoded MP4 and check against the scientific plan; pre-render PNGs do not prove encoded output.

Report playable links, important changes, actual checks and limits. Separate machine QA, sampled scientific review, human comprehension, aesthetic acceptance and market evidence. A short art preview is not a complete explanation or retention evidence.

Stop after the requested batch and deliver it for viewing. Further polish, topics or publishing follow user scope. Complete required repository validation and milestone/review records without unrelated configuration changes.
